# -*-coding=utf-8 -*-
import traceback
import datetime
import time
from decimal import Decimal
from ..database.sqlal import *
from ..model.ftpacct import *
from ..model.adjustments import *
from ..services.policyadjust import *
import decimal
import sys
from .tools import DataFlowTool, BatchSys, Proxy, save2db_orm\
                    , coroutine, json2str, ftp_log, eq_log, checkholiday
from .interest_rate_info import get_rate
from mylogger import logger

reload(sys)
sys.setdefaultencoding('utf-8')




session = simple_session()
session1 = simple_session(encoding='utf-8')
session2 = simple_session()
xcdw_session = dwdb_session()
xcdw_session2 = dwdb_session()
xcdw_session3 = dwdb_session()

def _now(info=''):
    print info,datetime.datetime.now()
    return datetime.datetime.now()

#缓存区
##利率缓存
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
            max.append(item[2])
        max.sort()
        max.reverse()
        for i in range(len(max)):
            if ftp_date >= max[i]:
                aim = max[i]
                for item in _d_s_rate[key]:
                    if item[2] == aim:
                        
                        #if unitagreementflag = u'是':
                        #   p 

                        return {'jzll':item[0], 'zxll':item[1]}     
                

##协定利率缓存
from collections import defaultdict, OrderedDict
data_all = defaultdict(OrderedDict)
def multi_rate_all():
    u"""
        缓存数据多档次利率
    """
    data_rate = data_all#defaultdict(OrderedDict)
    mrate = xcdw_session2.execute(u"""
        select 
            distinct trim(M2__AC20) acctno, M2__DATE "date", M2__IRTS irts, M2__AMNT amt,
            M2__RATE rate, M2__RTIO rtio 
        from ods.core_BIFMAIRT  
        order by acctno,"date",M2__IRTS 
    """)

    for m in mrate:
        data_rate[m.acctno].setdefault(m.date,[]).append((m.date, m.irts, m.amt, m.rate, m.rtio))

    return data_rate

def multi_rate(acctno, ftp_date):
    u""" 
        获取不同档次利率
    """
    global data_all
    data = []
    acct_data = data_all.get(acctno)

    if not bool(acct_data):
        return data
    last_day = None
    dates = acct_data.keys()
    dates.sort(reverse=True)
    for d in dates:
        if ftp_date >= d:
            return acct_data.get(d)
        else:
            continue
            
    


def interest_2001():
    u"""
        计算利息总入口
    """
    strdt = BatchSys.date()
    enddt = BatchSys.date()


    print "***"*10
    start = _now()

    #缓存利率
    pre_d_s_rate()
    #缓存协定利率
    multi_rate_all()
    itemnos = ['2001']
    if not(enddt):
        enddt = strdt
    for itemno in itemnos:
        #for o in orgno:
        print "start"
        interest_count(itemno,strdt,enddt)
        print "%s 计算OK"%(itemno)



    print _now() - start
    print "***"*10

    


def interest_count(itemno,strdt,enddt):
    """
    活期利息计算:单位活期,个人活期 科目号2001 ,2003 ,2005 ,2006 
    涉及参数:
        acctno 账号
        balance 余额
        interestdt 起息日
        unitagreementflag 协定标志
    """
    count = 0  #调试信息
    count_interest = 0
    colums = {'itemno':'itemno','orgno':"orgno",'currcd':"currcd",'ftp_date':'ftp_date','id':'acctno','balance':'balance','curinterest':'curinterest',"rate":"rate","level1_itemno":"level1_itemno",'dayaccum':'dayaccum'}
    insert_sql = InterestCount.__table__.insert(colums)


    list_test = []
    #sql = u"select * from ma_ftp_acct where  left(itemno,4) = '%s'  and itemno not in ('20030103','20050202','20050204')   and ftp_date>='%s' and ftp_date<='%s' and interestway !='不计息' and ( LEVEL1_ITEMNO!='内部帐' or LEVEL1_ITEMNO is null ) "%(itemno,strdt,enddt) #获取需要计算的账户数据
    #print "one begin"
    #result = session1.execute(sql);
    sql = """select c.acctno as id,c.acctno,c.acctname,c.custno,c.accttypecd,org.orgno,org.orgname,dc.currcd as currcd,c.autotranflag,c.prodname,nvl(c.interestdt,d.date) interestdt,nvl(c.expiredt,'1899-12-31') as expiredt,c.unitagreementflag,
       c.interestway,c.storperd as storperd,c.prodno ,c.prodtypecd ,fc.balance,fc.yearaccum,
       fc.yearaccum/d.yearday as dayaccum, it.itemno,it.itemname , cu.industry,cu.industryclass,cu.risklevel ,d.date as ftp_date , fc.source_date ,c.status, it.itemtype,'调整' as rateadjustyype,c.defaulttimes as IsDefaulting ,c.enddt,  
        c.begindt as begindt , c.endamt as endamt , c.endint as endint ,c.endinttax as endinttax, '否'  update_rate
           from xcdw.f_c_custacctbal  fc      
           inner join xcdw.d_o_org org on org.ID = fc.orgid
           left join xcdw.d_c_custacct c on fc.acctid = c.id 
           left join xcdw.d_p_product p on fc.prodid = p.id 
           left join xcdw.d_o_item it on fc.itemid = it.id 
           left join xcdw.d_c_cust cu on fc.custid = cu.id 
           left join xcdw.d_s_date d on fc.dateid = d.id 
           left join xcdw.d_s_currency dc on dc.ID = fc.CURRID
           where d.date ='{0}' and left(it.itemno,4) = '{1}'   and it.itemno not in ('20030103','20050202','20050204') and c.interestway !='不计息' and dc.currcd='CNY' """.format(strdt,itemno)
    logger.debug(sql)
    result = xcdw_session.execute(sql)

    _now()
    count_interst = 0
    balance_all = 0 

    insert_data = []
    for r in result:

        if count>0 and count%1000==0:
            print insert_data[0]
            session2.flush()
            session2.execute(insert_sql, insert_data)
            session2.commit()
            insert_data = []
            sys.stdout.flush()
            print "Processing %s ..." % count

        count += 1
        balance_all += r.balance

        update_rate = r.update_rate #利率调整方式

        if update_rate == u'是':
            d, ci = is_adjust_true(r)
            count_interst += ci
        else:
            d, ci = is_adjust_false(r)
            count_interst += ci

        insert_data.append(d)

    print "----------end--------------"
    print itemno,enddt,count_interst,balance_all
    if insert_data:
        session2.execute(insert_sql, insert_data)
    session2.commit()


count = 0
def is_adjust_true(r):
    global count
    u""" 是否调整  - 是 
    当利率发生调整时,调用此方法进行利息计算
    涉及参数:
        prodtypecd 产品类别代码
        prodno 产品代码
        currcd 币种
        storperd 存期
        interestway 计息方式 用于利率调整
        update_rate 利率调整方式
        yearaccum 积数
        begindt 积数
        interestdt 起息日
        unitagreementflag 协定标志
    """
    acctno = r.acctno#账号
    unitagreementflag = r.unitagreementflag#协定标志
    balance =r.balance#余额
    interestdt = r.interestdt#存款计息日
    ftp_date = r.ftp_date#

    if interestdt == None:
        count += 1
        interestdt = ftp_date
    if count>=100 and count%100==0:
        print "DEBUG:  起息日为空，设置起息日为ftp_date --- 数据条数为:  ",count 

    days = days_(interestdt,ftp_date)

    itemno = r.itemno
    prodtypecd = r.prodtypecd#产品类别代码
    prodno = r.prodno#产品代码
    currcd = r.currcd#币种
    storperd = r.storperd#存期
    interestway = r.interestway #计息方式 用于利率调整
    update_rate = r.update_rate #利率调整方式
    yearaccum = r.yearaccum #记数
    begindt = r.begindt #记数

    count_interst = 0


    if interestway == u'利随本清':
        rate = get_regularrate('101','11',0,currcd,ftp_date)['zxll']
        curinterest = round((balance * rate / Decimal('36000')),8)
        regularrate = rate
        count_interst += curinterest

    # if interestway == u'按季':
    # u'按季' + u'NON'
    else:
        if unitagreementflag == u'是' :
            multiData = multi_rate(acctno,ftp_date)
            amnt =  multiData[0][2]#档次金额上限 
            rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)['jzll']#基准利率，例如 0.35  
            balance = adjust_balance(acctno,interestdt,ftp_date,u'协定',amnt)
            rate_old = get_regularrate(prodno,prodtypecd,storperd,currcd,(ftp_date - datetime.timedelta(1)))['jzll']  

            curinterest = round(balance * (rate - rate_old) * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000'),8)

            if balance > amnt:

                balance_rest = balance - amnt
                balance = amnt
                curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000')  +  balance_rest * multiData[1][3]/Decimal('36000'),8)
                regularrate = round(multiData[1][3],8)
                count_interst += curinterest 
                

            else:

                
                curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000'),8)
                regularrate = round(rate*(Decimal('1') + multiData[0][4]/Decimal('100')),8)
                count_interst += curinterest 



        else:
           
               
            rate_old = get_regularrate(prodno,prodtypecd,storperd,currcd,(ftp_date - datetime.timedelta(1)))['zxll']  
   
            rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)
            if rate:
                rate = rate['zxll']

            curinterest = round((balance * rate / Decimal('36000')),8)

            balance = yearaccum - adjust_balance(acctno,begindt,ftp_date,interestway)
            curinterest = curinterest + round((balance * (rate - rate_old) / Decimal('36000')),8)
            regularrate = rate
            count_interst += curinterest 

        if days == 0:
            dayaccum = balance
        else:
            dayaccum = balance / Decimal(days)
        


    
    level1_itemno = u"存款|2001"


   #if r.acctno in get_rate().keys():
   #    regularrate = get_rate()[r.acctno]
   #curinterest = balance * regularrate / 36000
            

    return {'itemno':r.itemno,'orgno':r.orgno,'currcd':r.currcd,'ftp_date':ftp_date,'id':acctno,'rate':regularrate,'balance':r.balance,'curinterest':curinterest,'level1_itemno':level1_itemno,'dayaccum':r.dayaccum}, count_interst
    
    
        
def is_adjust_false(r):
    u""" 是否调整  - 否
    当利率未发生调整时,调用此方法进行利息计算
    涉及参数:
        prodtypecd 产品类别代码
        prodno 产品代码
        currcd 币种
        storperd 存期
        interestway 计息方式 用于利率调整
        update_rate 利率调整方式
        yearaccum 积数
        begindt 积数
        interestdt 起息日
        unitagreementflag 协定标志
    """
    acctno = r.acctno#账号
    unitagreementflag = r.unitagreementflag#协定标志
    balance =r.balance#余额
    interestdt = r.interestdt#存款计息日
    ftp_date = r.ftp_date#

    if interestdt == None:
        print "起息日为空，设置起息日为ftp_date --- ftp_date:  ",ftp_date,r 
        interestdt = ftp_date

    days = days_(interestdt,ftp_date)

    itemno = r.itemno
    prodtypecd = r.prodtypecd#产品类别代码
    prodno = r.prodno#产品代码
    currcd = r.currcd#币种
    storperd = r.storperd#存期
    interestway = r.interestway #计息方式 用于利率调整
    update_rate = r.update_rate #利率调整方式
    yearaccum = r.yearaccum #记数
    begindt = r.begindt #记数
    count_interst = 0
    if unitagreementflag == u'是' :
        multiData = multi_rate(acctno,ftp_date)
        amnt =  multiData[0][2]#档次金额上限 
        rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)['jzll']#基准利率，例如 0.35  
       
        if balance > amnt:

            balance_rest = balance - amnt
            balance = amnt
            curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000')+ balance_rest * multiData[1][3]/Decimal('36000'),8)
            regularrate = round(multiData[1][3],8)
            count_interst += curinterest 

        else:
            
            curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000'),8)
            regularrate = round(rate*(Decimal('1') + multiData[0][4]/Decimal('100')),8)
            count_interst += curinterest 



    else:
        rate = get_regularrate('101','11','0',currcd,ftp_date)['zxll']
        #rate = get_regularrate(prodno,prodtypecd,storperd,currcd,interestdt)['zxll']
        curinterest = round((balance * rate / Decimal('36000')),8)
        regularrate = rate
        count_interst += curinterest 

        #print rate

    level1_itemno = u"存款|2001"
    return {'itemno':r.itemno,'orgno':r.orgno,'currcd':r.currcd,'ftp_date':ftp_date,'id':acctno,'rate':regularrate,'balance':r.balance,'curinterest':curinterest,'level1_itemno':level1_itemno,'dayaccum':r.dayaccum}, count_interst
   


def calcute_(acctno,begindt,endt=None,special_flag=False,amnt=None):
    u"""
        用于计算调整利息对于的积数
    """
    total = 0
    sql = """select fc.yearaccum from xcdw.f_c_custacctbal  fc 
          left join xcdw.d_c_custacct c on fc.acctid = c.id
          left join xcdw.d_s_date d on fc.dateid = d.id
          where acctno= '%s' and d.date ='%s'  
        """
    logger.debug(sql%(acctno,begindt))
    if not endt:
        yearaccum = xcdw_session.execute((sql %(acctno,begindt))).fetchone()
        #yearaccum = session2.execute("select yearaccum from ma_ftp_acct where acctno= '%s' and ftp_date = '%s'  and ( LEVEL1_ITEMNO!='内部帐' or LEVEL1_ITEMNO is null ) " %(acctno,begindt)).fetchone()
        total = yearaccum.yearaccum

    elif endt and not special_flag:
        #yearaccum = session2.execute("select yearaccum from ma_ftp_acct where acctno= '%s' and  ftp_date = '%s' and ( LEVEL1_ITEMNO!='内部帐' or LEVEL1_ITEMNO is null )" %(acctno,begindt)).fetchone()
        yearaccum = xcdw_session.execute((sql %(acctno,begindt))).fetchone()
        total = yearaccum.yearaccum
        #yearaccum = session2.execute("select yearaccum from ma_ftp_acct where acctno= '%s' and  ftp_date = '%s' and ( LEVEL1_ITEMNO!='内部帐' or LEVEL1_ITEMNO is null )" %(acctno,endt)).fetchone()
        yearaccum = xcdw_session.execute((sql %(acctno,endt))).fetchone()
        total = total - yearaccum.yearaccum

    elif endt and special_flag:
        sql = """select fc.yearaccum from xcdw.f_c_custacctbal  fc 
              left join xcdw.d_c_custacct c on fc.acctid = c.id
              left join xcdw.d_s_date d on fc.dateid = d.id
              where acctno= '%s' and d.date >'%s' and d.date <'%s'  
        """%(acctno,begindt,endt)
        logger.debug(sql)
        #balance_result = session2.execute("select balance from ma_ftp_acct where acctno= '%s' and  ftp_date > '%s' and  ftp_date < '%s'  and ( LEVEL1_ITEMNO!='内部帐' or LEVEL1_ITEMNO is null )" %(acctno,begindt,endt)).fetchall()
        balance_result = xcdw_session.execute(sql).fetchone()
        for b in balance_result:
            if (b > amnt):
                total =total + b - amnt
            else:
                total  = total + b
        #total = yearaccum.yearaccum

    return total

def adjust_balance(acctno,begindt,ftp_date,interestway,amnt=None):
    u"""用于利息调整时获取调整起始日期"""
    total = 0
    month_dict={
        1:datetime.date((ftp_date.year - 1),12,20),
        2:datetime.date((ftp_date.year - 1),12,20),
        30:datetime.date((ftp_date.year - 1),12,20),
        31:datetime.date((ftp_date.year),3,20),
        4:datetime.date((ftp_date.year),3,20),
        5:datetime.date((ftp_date.year),3,20),
        60:datetime.date((ftp_date.year),3,20),
        61:datetime.date((ftp_date.year),6,20),
        7:datetime.date((ftp_date.year),6,20),
        8:datetime.date((ftp_date.year),6,20),
        90:datetime.date((ftp_date.year),6,20),
        91:datetime.date((ftp_date.year),9,20),
        10:datetime.date((ftp_date.year),9,20),
        11:datetime.date((ftp_date.year),9,20),
        120:datetime.date((ftp_date.year),9,20),
        121:datetime.date((ftp_date.year),12,20),
    }
    if interestway ==u'按季':
        if ftp_date.month not in (3,6,9,12):

            adjust_date = max(month_dict[ftp_date.month],begindt)
            total = calcute_(acctno, adjust_date)
        elif ftp_date.day <= 20:
            adjust_date = max(month_dict[ftp_date.month*10],begindt)
            total = calcute_(acctno, adjust_date, ftp_date)

        elif ftp_date.day > 20:
            adjust_date = max(month_dict[ftp_date.month*10+1],begindt)
            total = calcute_(acctno, month_dict[ftp_date.month*10+1],ftp_date)

    elif interestway==u'利随本清':
        ed = datetime.date(begindt.year,12,31)
        if ed < ftp_date:
            total += calcute_(acctno,begindt,ed)
        else:
            ed = datetime.date(ed.year+1,12,31)
            while ed < ftp_date:
                total+=calcute_(ed)
                ed = datetime.date(ed.year+1,12,31)
            total +=calcute_(ftp_date)

    elif interestway ==u'协定':
        if ftp_date.month not in (3,6,9,12):
            calcute_(acctno, month_dict[ftp_date.month],ftp_date,True,amnt)
        elif ftp_date.day <= 20:
            total = calcute_(acctno, month_dict[ftp_date.month*10],ftp_date,True,amnt)

        elif ftp_date.day > 20:
            total = calcute_(acctno, month_dict[ftp_date.month*10+1],ftp_date,True,amnt)

    #print acctno,total
    return total


def days_(date1,date2):

    days = int((date2 - date1).days)

    return days

    

