# -*-coding=utf-8-*-
import datetime
import time
from decimal import Decimal
from ..database.sqlal import *
from ..model.ftpacct import *
from ..model.adjustments import *
from ..services.policyadjust import *
import decimal
#from .price_method_para_process import get_para
from ..model.data import *
from .tools import DataFlowTool, BatchSys, Proxy, save2db_orm\
                    , coroutine, json2str, ftp_log, eq_log, checkholiday
import sys
from mylogger import logger
u"""
2014 科目计算OK,只有895010有偏差
time:2016-12-18 13:00


"""



session = simple_session() #ftp 连接
session1 = simple_session()
session2 = simple_session()
xcdw_session = dwdb_session() #数据仓库 连接
xcdw_session2 = dwdb_session()
xcdw_session3 = dwdb_session()

def _now():
    print datetime.datetime.now()


_yesterday_data = {}
def pre_data(item,etl_dt):
    u"""
        缓存昨日账户数据
    """
    _yesterday_data.clear()
    print datetime.datetime.now()
    #result = session1.execute(u"select acctno, balance from ma_ftp_acct where ftp_date='%s' and left(itemno,4) = '%s'  " %(etl_dt,item)).fetchall();
    sql = """select c.acctno ,fc.balance
           from xcdw.f_c_custacctbal  fc      
           left join xcdw.d_c_custacct c on fc.acctid = c.id 
           left join xcdw.d_s_date d on fc.dateid = d.id 
           left join xcdw.d_o_item it on fc.itemid = it.id 
           where d.date ='{0}' and left(it.itemno,4) = '2014'  and c.interestdt !='1899-12-31' and it.itemno not in ('20030103','20050202','20050204') and interestway !='不计息' """.format(etl_dt)
    logger.debug(sql)
    result = xcdw_session.execute(sql)
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
        item = [Decimal('0.35'),Deicmal('0.35')]
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
                        return {'jzll':item[0], 'zxll':item[1]}     
            
def multi_rate(acctno,ftp_date):
    u"""  缓存多档次的利率  """
    mrate = xcdw_session2.execute(u"""select  
                                    M2__DATE,M2__IRTS,M2__AMNT,M2__RATE,M2__RTIO
                                    from ods.core_BIFMAIRT where M2__AC20 = '%s' and M2__DATE =
                                    (select max(M2__DATE) from ods.core_BIFMAIRT where M2__DATE<'%s'  and M2__AC20 = '%s' ) order by M2__AMNT"""%(acctno,ftp_date,acctno))
    list = []
    for m in mrate:
        list.append(m)
    return list

def interest_2014():
    u"""
        2014科目利息计算主入口
    """
    strdt = BatchSys.date()
    enddt = BatchSys.date()

    item='2014'
    if not enddt:
        enddt=strdt
    pre_data(item,(strdt - datetime.timedelta(1)))
    interest(item,strdt,enddt)


        
def interest(item,stdt,enddt):
    u"""
        2014科目利息计算主程序 
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
    count_interst = 0
    count_interst2 = 0 
    balance_all = 0
    pre_d_s_rate() #获取最新利率iand acctno='283000106889164' 
    #result = session1.execute(u"""select * from ma_ftp_acct where itemno like '%s%%'  and ftp_date>='%s' and ftp_date<='%s'  and ( LEVEL1_ITEMNO!='内部帐' or LEVEL1_ITEMNO is null ) """ %(item,stdt,enddt));
    sql = """select c.acctno as id,c.acctno,c.acctname,c.custno,c.accttypecd,org.orgno,org.orgname,dc.currcd as currcd,c.autotranflag,c.prodname,nvl(c.interestdt,'1899-12-31') interestdt,nvl(c.expiredt,'1899-12-31') as expiredt,c.unitagreementflag,
       c.interestway,c.storperd as storperd,c.prodno ,c.prodtypecd ,fc.balance,fc.yearaccum,
       fc.yearaccum/d.yearday as dayaccum, it.itemno,it.itemname , cu.industry,cu.industryclass,cu.risklevel ,d.date as ftp_date , fc.source_date ,c.status, it.itemtype,'不调整' as rateadjustyype,c.defaulttimes as IsDefaulting ,c.enddt,  
        c.begindt as begindt , c.endamt as endamt , c.endint as endint ,c.endinttax as endinttax,(case when  (select distinct 1 from xcdw.d_s_rate where ratename='活期存款' and begindt=d.date and prodno !='non' and prodtypecd!='non') =1 then '调整' else  '不调整' end) update_rate
           from xcdw.f_c_custacctbal  fc      
           inner join xcdw.d_o_org org on org.ID = fc.orgid
           left join xcdw.d_c_custacct c on fc.acctid = c.id 
           left join xcdw.d_p_product p on fc.prodid = p.id 
           left join xcdw.d_o_item it on fc.itemid = it.id 
           left join xcdw.d_c_cust cu on fc.custid = cu.id 
           left join xcdw.d_s_date d on fc.dateid = d.id 
           left join xcdw.d_s_currency dc on dc.ID = fc.CURRID
           where d.date ='{0}' and left(it.itemno,4) = '2014'  and c.interestdt !='1899-12-31' and it.itemno not in ('20030103','20050202','20050204') and interestway !='不计息' and dc.currcd='CNY' """.format(stdt)
    logger.debug(sql)
    result = xcdw_session.execute(sql)
    count = 0  #调试信息
    count2 = 0#调试信息
    count3 = 0
    count4 = 0
    _now()
    curinterest = 0
    colums = {'orgno':'orgno','itemno':'itemno','currcd':'currcd','ftp_date':'ftp_date','id':'acctno','balance':'balance','curinterest':'curinterest','level1_itemno':'level1_itemno','dayaccum':'dayaccum'}
    insert_sql = InterestCount.__table__.insert(colums)
    amnt_list = acctno_list = balance_list = rate_list = insert_data = list_test = []
    for r in result:

        if count>0 and count%1000==0:
            session2.execute(insert_sql, insert_data)
            session2.commit()
            insert_data = []
            sys.stdout.flush()
            print "Processing %s ..." % count
        count += 1

        if r.prodtypecd == '23' and r.prodno == '108':
            count3 += 1

            itemno = r.itemno
            if not itemno:#科目号不存在的情况
                continue
            ftp_date = r.ftp_date
            begindt = r.begindt
            if r.endamt:
                endamt = float(r.endamt)
            else:
                endamt = 0
            if r.endint:
                endint = float(r.endint)
            else:
                endint = 0
            
            
            acctno = r.acctno
            isdefaulting = r.isdefaulting

            fromdate= r.interestdt
            closedate = r.expiredt

            interestway = r.interestway
            if closedate and isdefaulting == u'未违约': 
                if ftp_date>closedate:continue      #过期账户不再计算利息
            if interestway == u'不计息':continue  #去掉不计息账号
            interestdt = r.interestdt
            expiredt =r.expiredt  #到期日期
            storperd = r.storperd #存期
            balance =r.balance
            autotranflag = r.autotranflag

            if expiredt <= ftp_date and ( autotranflag == u'自动转存（自动转存的都有签约信息）' or autotranflag==u'未知'):#TODO ？？？待定
                interestdt,expiredt = update_months(expiredt,storperd,ftp_date,interestdt) #修正自动转存后的起息日期和到期日期

            if balance == Decimal('0') and ftp_date ==expiredt:continue  #去掉余额为零且已经到期的账号,#TODO余额为零没有到期账号利息要扣掉
            regularrate = None
            currcd = r.currcd
            dayaccum = r.dayaccum
            unitagreementflag = r.unitagreementflag
            prodno = r.prodno 
            prodtypecd = r.prodtypecd
            if itemno[:4] == u'2014':
                curinterest = 0

                #保证金定期
                if interestdt !=begindt  and ftp_date ==begindt: #部分提前支取补齐新账号利息
                    rate = get_regularrate(prodno,prodtypecd,storperd,currcd,interestdt)['zxll']
                    balance_count = balance * Decimal((begindt - interestdt + datetime.timedelta(1)).days)
                    curinterest = round((balance_count * rate / Decimal('36000')),8)

                elif expiredt > ftp_date and balance == 0: #提前支取
                    rate = get_regularrate(prodno,prodtypecd,storperd,currcd,interestdt)['zxll']


                    if acctno in _yesterday_data:
                        balance  = _yesterday_data[acctno]
                    else:
                        balance = 0
                    balance = balance * Decimal((ftp_date - interestdt).days)
                    if balance >0:
                        curinterest = endint - round((balance * rate /Decimal('36000')),8)
                    else:continue
                     
                elif expiredt > ftp_date and balance > 0: #正常计息
                    rate = get_regularrate(prodno,prodtypecd,storperd,currcd,interestdt)['zxll']
                    curinterest = round((balance * rate / Decimal('36000')),8)

                elif expiredt < ftp_date and balance > 0: #过期且有余额
                    rate = get_regularrate('101','21','0',currcd,ftp_date)['zxll'] #活期利率
                    curinterest = curinterest  + round((balance * rate / Decimal('36000')),8)

                regularrate = rate
                count_interst += curinterest 
                balance_all += balance
            count2 += 1 
            #continue
                                           

        else:
            #进入单位活期"            
            count4 += 1

            acctno = r.acctno#账号
            unitagreementflag = r.unitagreementflag#协定标志
            balance =r.balance#余额
            interestdt = r.interestdt#存款计息日
            ftp_date = r.ftp_date#
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
            if update_rate == u'是':
                if interestway == u'按季':

                    if unitagreementflag == u'是' :
                        multiData = multi_rate(acctno,ftp_date)
                        multiData = _list_no_chongfu(multiData)
                        amnt =  multiData[0][2]#档次金额上限 
                        amnt_list.append(amnt)
                        rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)['jzll']#基准利率，例如 0.35  
                        balance = adjust_balance(acctno,interestdt,ftp_date,u'协定')
                        rate_old = get_regularrate(prodno,prodtypecd,storperd,currcd,(ftp_date - datetime.timedelta(1)))['jzll']  
                        curinterest = round(balance * (rate - rate_old) * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000'),8)
                        if balance > amnt:

                            balance_rest = balance - amnt
                            balance = amnt
                            curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000')  +  balance_rest * multiData[1][3]/Decimal('36000'),8)
                            regularrate = round(multiData[1][3],8)
                            count_interst += curinterest 
                            

                            balance_all += balance
                        else:

                            
                            curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000'),8)
                            regularrate = round(rate*(Decimal('1') + multiData[0][4]/Decimal('100')),8)
                            count_interst += curinterest 


                            balance_all += balance

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
                        balance_all += balance
                    ftp_price_m = rate * balance / 36000
                    if days == 0:
                        dayaccum = balance
                    else:
                        dayaccum = balance / Decimal(days)
                elif interestway == u'利随本清':
                    rate = get_regularrate('101','11',0,currcd,ftp_date)['zxll']
                    curinterest = round((balance * rate / Decimal('36000')),8)
                    regularrate = rate
                    count_interst += curinterest

                    balance_all += balance
            else:
                if unitagreementflag == u'是' :
                    multiData = multi_rate(acctno,ftp_date)
                    multiData = _list_no_chongfu(multiData) 
                    amnt =  multiData[0][2]#档次金额上限 
                    amnt_list.append(amnt)
                    rate = get_regularrate(prodno,prodtypecd,storperd,currcd,ftp_date)['jzll']#基准利率，例如 0.35  
                    if balance > amnt:

                        balance_rest = balance - amnt
                        balance = amnt
                        curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000')+ balance_rest * multiData[1][3]/Decimal('36000'),8)
                        regularrate = round(multiData[1][3],8)
                        count_interst += curinterest 
                        balance_all += balance
                    else:
                        curinterest = round(balance * rate * (Decimal('1') + multiData[0][4]/Decimal('100')) / Decimal('36000'),8)
                        regularrate = round(rate*(Decimal('1') + multiData[0][4]/Decimal('100')),8)
                        count_interst += curinterest 

                        if regularrate != Decimal('0.38500000'):
                            acctno_list.append(acctno)
                            balance_list.append(balance)
                            rate_list.append(regularrate)

                        balance_all += balance

                else:
                    rate = get_regularrate('101','11','0',currcd,ftp_date)['zxll']
                    curinterest = round((balance * rate / Decimal('36000')),8)
                    regularrate = rate
                    count_interst += curinterest 
                    balance_all += balance

        count_interst2 += curinterest 
        level1_itemno = u"存款|2014"
        insert_data.append({'itemno':r.itemno,'orgno':r.orgno,'currcd':r.currcd,'ftp_date':ftp_date,'id':acctno,'rate':regularrate,'balance':r.balance,'curinterest':curinterest,'level1_itemno':level1_itemno,'dayaccum':r.dayaccum})

    print u"""单位定期，单位活期判断完毕 """
    print "--ok-  -"
    print enddt,count_interst,count_interst2,item,balance_all
    print "--------"*10    
    if insert_data:
        session2.execute(insert_sql, insert_data)
    session2.commit()






def calcute_(acctno,begindt,endt=None,special_flag=False,amnt=None):
    u"""
        用于计算调整利息对于的积数
    """
    total = 0
    if not endt:
        yearaccum = session2.execute("select yearaccum from ma_ftp_acct where acctno= '%s' and ftp_date = '%s' with ur" %(acctno,begindt)).fetchone()
        total = yearaccum.yearaccum

    elif endt and not special_flag:
        yearaccum = session2.execute("select yearaccum from ma_ftp_acct where acctno= '%s' and  ftp_date = '%s' with ur " %(acctno,begindt)).fetchone()
        total = yearaccum.yearaccum
        yearaccum = session2.execute("select yearaccum from ma_ftp_acct where acctno= '%s' and  ftp_date = '%s' with ur " %(acctno,endt)).fetchone()
        total = total - yearaccum.yearaccum

    elif endt and not special_flag:
        balance_result = session2.execute("select balance from ma_ftp_acct where acctno= '%s' and  ftp_date > '%s' and  ftp_date < '%s' with ur " %(acctno,begindt,endt)).fetchall()
        for b in balance_result:
            if (b > amnt):
                total =total + b - amnt
            else:
                total  = total + b
        total = yearaccum.yearaccum

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
    if interestway =='按季':
        if ftp_date.month not in (3,6,9,12):

            adjust_date = max(month_dict[ftp_date.month],begindt)
            total = calcute_(acctno, adjust_date)
        elif ftp_date.day <= 20:
            adjust_date = max(month_dict[ftp_date.month*10],begindt)
            total = calcute_(acctno, adjust_date, ftp_date)

        elif ftp_date.day > 20:
            adjust_date = max(month_dict[ftp_date.month*10+1],begindt)
            total = calcute_(acctno, month_dict[ftp_date.month*10+1],ftp_date)

    elif interestway=='利随本清':
        ed = datetime.date(begindt.year,12,31)
        if ed < ftp_date:
            total += calcute_(acctno,begindt,ed)
        else:
            ed = datetime.date(ed.year+1,12,31)
            while ed < ftp_date:
                total+=calcute_(ed)
                ed = datetime.date(ed.year+1,12,31)
            total +=calcute_(ftp_date)

    elif interestway =='协定':
        if ftp_date.month not in (3,6,9,12):
            calcute_(acctno, month_dict[ftp_date.month],ftp_date,True,amnt)
        elif ftp_date.day <= 20:
            total = calcute_(acctno, month_dict[ftp_date.month*10],ftp_date,True,amnt)

        elif ftp_date.day > 20:
            total = calcute_(acctno, month_dict[ftp_date.month*10+1],ftp_date,True,amnt)

    #print acctno,total
    return total


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



def _list_no_chongfu(list_):
    """
    list = [(1,2),(1,3),(1,2)]  --->  [(1,2),(1,3)]
    list中元组去重
    """   
    list1 = list_
    kk = []

    for i in range(len(list1)) :
       if list1[i] not in kk:
           kk.append(list1[i])

    return kk  


def days_(date1,date2):

    day1 = date2 - date1
    days = str(day1).split(' ')[0]

    if date1 == date2:
        days = 0
    if date1 >= date2:
        days = -days

    return days

    
