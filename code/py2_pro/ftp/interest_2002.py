# -*-coding=utf-8 -*-
import datetime
import time
from decimal import Decimal
from ..database.sqlal import *
from ..model.ftpacct import *
from .tools import *
from .tools import DataFlowTool, BatchSys, Proxy, save2db_orm\
                    , coroutine, json2str, ftp_log, eq_log, checkholiday
from .interest_rate_info import get_rate

from mylogger import logger

session = simple_session() #ftp 连接
session1 = simple_session()
session2 = simple_session()
xcdw_session = dwdb_session() #数据仓库 连接
xcdw_session2 = dwdb_session()

float_ = lambda x,d: d if x in('NON',None) else x

def _now():
    print datetime.datetime.now()

level1_itemno = u"存款|2002"

_yesterday_data = {}
def pre_data(item,etl_dt):
    u"""
        获取昨日余额缓存,用于利息调整
    """
    _yesterday_data.clear()
    print datetime.datetime.now()
    #result = session1.execute(u"select acctno, balance from ma_ftp_acct where ftp_date='%s' and left(itemno,4) = '%s'  " %(etl_dt,item)).fetchall();
    sql = """select c.acctno ,fc.balance
           from xcdw.f_c_custacctbal  fc      
           left join xcdw.d_c_custacct c on fc.acctid = c.id 
           left join xcdw.d_s_date d on fc.dateid = d.id 
           left join xcdw.d_o_item it on fc.itemid = it.id 
           left join xcdw.D_S_CURRENCY ds on fc.CURRID = ds.id 
           where d.date ='{0}' and left(it.itemno,4) = '{1}'  and c.interestdt !='1899-12-31' and it.itemno not in ('20030103','20050202','20050204') and interestway !='不计息' and ds.currcd='CNY' """.format(etl_dt,item)
    logger.debug(sql)
    result = xcdw_session.execute(sql).fetchall()
    print datetime.datetime.now()
    for r in result :
        _yesterday_data[r.acctno]=r.balance
    print datetime.datetime.now()


_d_s_rate = {}
def pre_d_s_rate():
    u"""
        获取缓存数据仓库利率表
    """
    rates = xcdw_session.execute(u"select prodno,prodtypecd,term,currcd,rate,regularrate,begindt,enddt from xcdw.d_s_rate").fetchall()
    for r in rates:
        key = '|'.join([r.prodno,r.prodtypecd,str(r.term),r.currcd])
        if key in  _d_s_rate:
            _d_s_rate[key].append((r.rate,r.regularrate,r.begindt,r.enddt))
        else:
            _d_s_rate[key] = [(r.rate,r.regularrate,r.begindt,r.enddt)]

def get_regularrate(prodno,prodtypecd,term,currcd,ftp_date):
    u"""
        获取当前时间,当前产品,当前存期,当前币种的具体利率
    """
    key = '|'.join([prodno,prodtypecd,str(term),currcd])
    max = []
    if not _d_s_rate.get(key):
        item = [Decimal('0.35'),Decimal('0.35')]
        return {'jzll':item[0], 'zxll':item[1]}
    else:
        for item in _d_s_rate[key]:
            #print 'item',item
            max.append(item[2])
        max.sort()
        max.reverse()
        for i in range(len(max)):
            if ftp_date >= max[i]:
                aim = max[i]
                for item in _d_s_rate[key]:
                    if item[2] == aim:
                        return {'jzll':item[0], 'zxll':item[1]}     
                

rate_all = {}
def multi_rate_all():
    u"""  缓存多档次的利率  """
    mrate = xcdw_session2.execute(u"""select  distinct o.CL01AC15   as acctno   , r.seq, r.days as "days", r.rate from ods.CORE_BFFMDQCL   o inner join 
                                        (select CP01NO12 as code, CP02SN03 as seq, CP04TRCD as days, CP06RATE as rate from ods.core_bffmdqcp   order by CP01NO12,CP02SN03) r
                                      on o.CL02NO12 = r.code
                                        order by acctno, seq
                                    """).fetchall()
    for m in mrate:
        rate_all.setdefault(m.acctno,[]).append((m.seq, m.days, m.rate))
        #if m.acctno in rate_all:
        #    rate_all[m.acctno].append(())
        #else:
        #    rate_all[m.acctno] = [()]
    for k in rate_all:
        rate_all[k].sort(key=lambda x : x[0])
    
    return rate_all

def multi_rate(acctno, days):
    u""" 获取多档次的利率 """
    global rate_all
    data = []
    acct_data = rate_all.get(acctno)

    if not bool(acct_data):
        return 0
    #print acct_data
    for d in acct_data:
        if days <= d[1]:
            return d[2]
        else:
            continue


rates_dict = {}
def pre_daecundang_rate():
    u"""缓存大额存单利率"""
    rates = xcdw_session.execute(u"select  AB25RATE as rate, AB01AC15 as acctno, max(AB30DATE) from ods.CORE_BFFMDQAB where (AB11PRON = '104' and AB10PDTP='23') or AB11PRON not in ('101','201','301','303') and etl_dt !='2014-12-15'  group by AB25RATE,AB01AC15 ").fetchall()
    for r in rates:
        if r.rate < Decimal('0.1'):
            rates_dict[r.acctno] = r.rate*Decimal('100')
        else:
            rates_dict[r.acctno] = r.rate


def interest_2002():

    stdt = BatchSys.date()
    enddt = BatchSys.date()

    pre_daecundang_rate()
    multi_rate_all()
    item='2002'
    pre_data(item,(stdt - datetime.timedelta(1)))

    interest(item,stdt,enddt)



        
def interest(item,stdt,enddt):
    u"""
        2002利息计算主程序
    涉及参数:
        prodtypecd 产品类别代码
        prodno 产品代码
        currcd 币种
        storperd 存期
        interestway 计息方式 用于利率调整
        yearaccum 积数
        begindt 积数
        interestdt 起息日
        unitagreementflag 协定标志
    """
    count_interst = 0
    pre_d_s_rate() #获取最新利率
    #result = session1.execute(u"select * from ma_ftp_acct where itemno like '%s%%'  and ftp_date>='%s' and ftp_date<='%s' " %(item,stdt,enddt));
    sql = """select c.acctno as id,c.acctno,c.acctname,c.custno,c.accttypecd,org.orgno,org.orgname,dc.currcd as currcd,c.autotranflag,c.prodname,nvl(c.interestdt,'1899-12-31') interestdt,nvl(c.expiredt,'1899-12-31') as expiredt,c.unitagreementflag,
       c.interestway,c.storperd as storperd,c.prodno ,c.prodtypecd ,fc.balance,fc.yearaccum,
       fc.yearaccum/d.yearday as dayaccum, it.itemno,it.itemname , cu.industry,cu.industryclass,cu.risklevel ,d.date as ftp_date , fc.source_date ,c.status, it.itemtype,'不调整' as rateadjustyype,c.defaulttimes as IsDefaulting ,c.enddt,  
        c.begindt as begindt , c.endamt as endamt , c.endint as endint ,c.endinttax as endinttax 
           from xcdw.f_c_custacctbal  fc      
           inner join xcdw.d_o_org org on org.ID = fc.orgid
           left join xcdw.d_c_custacct c on fc.acctid = c.id 
           left join xcdw.d_p_product p on fc.prodid = p.id 
           left join xcdw.d_o_item it on fc.itemid = it.id 
           left join xcdw.d_c_cust cu on fc.custid = cu.id 
           left join xcdw.d_s_date d on fc.dateid = d.id 
           left join xcdw.d_s_currency dc on dc.ID = fc.CURRID
           where d.date ='{0}' and left(it.itemno,4) = '2002'  and c.interestdt !='1899-12-31' 
            and dc.currcd='CNY'

        """.format(stdt)
    logger.debug(sql)
    result = xcdw_session.execute(sql)
    count = 0  #调试信息
    count2 = 0#调试信息
    _now()
    curinterest = 0
    colums = {'orgno':'orgno','itemno':'itemno','currcd':'currcd','ftp_date':'ftp_date','id':'acctno','rate':'rate','balance':'balance','curinterest':'curinterest','level1_itemno':'level1_itemno','dayaccum':'dayaccum'}
    insert_sql = InterestCount.__table__.insert(colums)
    #insert_sql = org_interest.__table__.insert(colums)
    list_test = []
    insert_data = []
    for r in result:
        
        # TODO 203000033003044 2017-01-01 USD 20020101
        if r.status == u'销户':
            data = {'orgno':r.orgno,'itemno':r.itemno,'currcd':r.currcd,'ftp_date':r.ftp_date,'id':r.acctno,'rate':Decimal('0'),'balance':r.balance,'curinterest':Decimal('0.00'),'level1_itemno':level1_itemno,'dayaccum':r.dayaccum}
            insert_data.append(data)
            continue

        
        if count>0 and count%1000==0:
            session2.execute(insert_sql, insert_data)
            session2.commit()
            insert_data = []
            sys.stdout.flush()
            print "Processing %s ..." % count
        count += 1

        itemno = r.itemno
        if not itemno:#科目号不存在的情况
            continue

        ftp_date = r.ftp_date
        
        
        acctno = r.acctno
        isdefaulting = r.isdefaulting
        interestway = r.interestway
        if interestway == u'不计息':continue  #去掉不计息账号
        interestdt = r.interestdt
        expiredt = r.expiredt if r.expiredt else interestdt  #到期日期
        storperd = r.storperd #存期
        balance =r.balance
        autotranflag = r.autotranflag
        if expiredt <= ftp_date and autotranflag == u'自动转存（自动转存的都有签约信息）':
            interestdt,expiredt = update_months(expiredt,storperd,ftp_date,interestdt) #修正自动转存后的起息日期和到期日期
        if balance == Decimal('0') and ftp_date ==expiredt:continue  #去掉余额为零且已经到期的账号,#TODO余额为零没有到期账号利息要扣掉
        regularrate = None
        currcd = r.currcd
        dayaccum = r.dayaccum
        unitagreementflag = r.unitagreementflag
 
        reason = ''
        prodno = r.prodno 
        prodtypecd = r.prodtypecd
        curinterest = 0
        rate = 0
        if (prodtypecd=='17' and prodno=='101') or (prodtypecd=='27' and prodno=='701'):    #通知存款
            if balance == 0 and ((interestdt + datetime.timedelta(storperd) - datetime.timedelta(1)) > ftp_date): #通知提前支取
                rate = Decimal(get_regularrate('101','21','0',currcd,ftp_date)['zxll'] - r.rate) #活期利率
                if acctno in _yesterday_data:
                    balance  = _yesterday_data[acctno]
                else:
                    balance = 0

                balance = balance * Decimal((ftp_date - interestdt).days)
            elif (interestdt + datetime.timedelta(storperd) - datetime.timedelta(1)) == ftp_date and balance > 0: #7天到期补齐利息
                rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)['zxll']
                balance_count = balance * Decimal('6')
                curinterest = round((balance_count * rate / Decimal('36000')),8) - round((balance_count * get_regularrate('101','11',0,currcd,ftp_date)['zxll'] / Decimal('36000')),8)

            elif (interestdt + datetime.timedelta(storperd) - datetime.timedelta(1)) < ftp_date and balance > 0: #超过7天
                rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)['zxll']

            elif (interestdt + datetime.timedelta(storperd) - datetime.timedelta(1)) > ftp_date and balance > 0: #未到7天
                rate = get_regularrate('101','21','0',currcd,ftp_date)['zxll']
            curinterest = curinterest  + round((balance * rate / Decimal('36000')),8)



        elif (prodtypecd=='23' and prodno=='104'):    #大额存单
            if (expiredt -  datetime.timedelta(1)) > ftp_date and balance == 0: #提前支取
                rate = multi_rate(acctno,(ftp_date - interestdt).days)
                if acctno in _yesterday_data:
                    balance  = _yesterday_data[acctno]
                else:
                    balance = 0

                balance = balance * Decimal((ftp_date - interestdt).days)
                curinterest = float_(r.endint, 0 ) - round((balance * rate / Decimal('36500')),8)
            else:
                rate= rates_dict.get(acctno,0)
                curinterest = round((balance * rate / Decimal('36500')),8)


        else:
            if (expiredt -  datetime.timedelta(1)) > ftp_date and balance == 0: #提前支取
                rate = get_regularrate('101','21','0',currcd,ftp_date)['zxll'] - get_regularrate(prodno,prodtypecd,storperd,currcd,interestdt)['zxll']
                if acctno in _yesterday_data:
                    balance  = _yesterday_data[acctno]
                else:
                    balance = 0
                balance = balance * Decimal((ftp_date - interestdt).days)
            else:
                if expiredt < ftp_date and balance > 0: #过期且有余额
                    rate = get_regularrate('101','21','0',currcd,ftp_date)['zxll'] #活期利率
                elif acctno in rates_dict.keys():
                    rate= rates_dict.get(acctno,0)
                else:
                    rate = get_regularrate(prodno,prodtypecd,storperd,currcd,interestdt)['zxll']

            curinterest = curinterest  + round((balance * rate / Decimal('36000')),8)
        regularrate = rate
        count_interst += curinterest 
        count2 += 1 


        ## 手工维护利率
        if acctno in get_rate().keys():
            regularrate = get_rate()[acctno]
        curinterest = r.balance * regularrate / 36000


        insert_data.append({'itemno':r.itemno,'orgno':r.orgno,'currcd':r.currcd,'ftp_date':ftp_date,'id':acctno,'rate':regularrate,'balance':r.balance,'curinterest':curinterest,'level1_itemno':level1_itemno,'dayaccum':r.dayaccum})
        continue
    print "--ok--",enddt,count_interst,count
    if insert_data:
        session2.execute(insert_sql, insert_data)
    session2.commit()



def add_months(dt,months):
    u"""
        获取当前日期对应数月的日期
        如输入 dt=20141215 months=1
        输出 20150115
    """
    targetmonth=months+dt.month
    month_dict={
            1:31,
            2:29,
            3:31,
            4:30,
            5:31,
            6:30,
            7:31,
            8:31,
            9:30,
            10:31,
            11:30,
            12:31,
            0:31,
          }
    try:
        if targetmonth <= 12:
            dt=dt.replace(year=dt.year, month=(targetmonth), day=min(month_dict[targetmonth%12], dt.day))
        elif targetmonth%12 == 0:
            dt=dt.replace(year=dt.year+int(targetmonth/12 - 1),month=(12), day=min(month_dict[targetmonth%12], dt.day))
        else :
            dt=dt.replace(year=dt.year+int(targetmonth/12),month=(targetmonth%12), day=min(month_dict[targetmonth%12], dt.day))
    except:
        if targetmonth <= 12:
            dt=dt.replace(year=dt.year,month=(targetmonth), day=28)
        elif targetmonth%12 == 0:
            dt=dt.replace(year=dt.year+int(targetmonth/12 - 1),month=(12), day=28)
        else :
            dt=dt.replace(year=dt.year+int(targetmonth/12),month=(targetmonth%12), day=28)
    return dt

def update_months(dt1,months,dt2, interestdt):
    u"""
        获取当前日期对应起的息日期
    """
    while dt1 <= dt2:
        dt1 = add_months(dt1,months)
        interestdt = add_months(interestdt,months)
    return interestdt,dt1






