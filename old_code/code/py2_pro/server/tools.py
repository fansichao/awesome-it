# -*- coding=utf-8 -*-
u"""后台工具箱

"""
import os
import sys
import datetime
import logging
import traceback

from optparse import OptionParser, OptionGroup

from fdm.base.utils import to_md5 
from fdm.database.sqlal import Base, simple_session
from fdm.model import *
from fdm.tools.datetime_tools import str2date, date2str, get_last_date_of_month, calc_date

reload(sys)
sys.setdefaultencoding("utf8")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

def mining_model(run_dt, model_no):
    u"""
    """
    run_dt = date2str(str2date(run_dt), "%Y%m%d")

    session = simple_session()
    rst = session.execute("select model_no from mining_model").fetchall()
    all_models = [r.model_no for r in rst]

    model_list = []
    if model_no != 'ALL':
        model_list = [m.upper() for m in model_no.split(",")]
        if set(model_list) - set(all_models):
            logging.error("存在未知的模型名称:%s, 请确认后在执行命令" % (list(set(model_list) - set(all_models))))
            return 

    if not bool(model_list) or model_list=="ALL":
        model_list = all_models

    from fdm.mining.model_logic_v3 import mining
    #from fdm.mining.model_logic import mining # TODO:测试开发用
    mining(run_dt, model_list=model_list)

def make_mining_entity(from_dt, end_dt):
    u"""加工基础指标"""
    from fdm.mining.model_entity import main_processer

    from_dt = str2date(from_dt)
    end_dt = str2date(end_dt)

    run_entity = ["cust_base" , "wd_cash", "tsfr", "dpst_cash", "ir",
                  "tran",  "atm_tran", "cb_atm_wd", "xjat_spa", "xjat_spn",
                  "xjat_euro", "spat_tran", "spat_spn", "spat_euro", "cash_tran",
                  'credit_tran', 'debit_tran', 'credit_tsfr_tran', 'debit_tsfr_tran',
                  "evade_cash", "evade_tsfr", "ebank_d_tran", "peer_tran_log",
                  "nl_cash", "nlct_cd_tran", "nlct_cd_tsfr_tran",
                ]

    run_dt = from_dt
    while run_dt <= end_dt:
        print "开始执行[%s]日基础数据加工" % run_dt
        main_processer(date2str(run_dt, '%Y%m%d'), run_entity)
        run_dt = calc_date(run_dt, 1)


def rpt_aftertreatment(run_dt):
    u""" 报告后处理，加工报告上需要的各类字段信息

    :param run_dt:
    """
    from fdm.mining.mining_tools import report_aftertreatment
    report_aftertreatment(run_dt)


def init_db():
    u"""重置数据库"""

    os.system("cd ./fdm/tests; source ~/.bash_profile; nosetests -sv test_dbinit.py")
    return 
    from fdm.tests.init_namemapping import init_np
    logging.info(u">> 执行重置数据库命令...")
    session = simple_session()

    Base.metadata.drop_all(session.bind, checkfirst=True)
    Base.metadata.create_all(session.bind, checkfirst=True)

    logging.info(u">> 已重置所有表，开始导入初始化数据...")
    
    time = datetime.datetime.utcnow()
    user=User(code='1001',password=to_md5('qwe123'),status=u'正常',name=u'张三')
    session.add(user)
    data=FTBatch(data_dt=datetime.date(2017,1,1),batch_type=u'手工导入',batch_status=u'已导入',\
                 present_dt=time,import_dt=time,operator=u'张三')
    session.add(data)
    batch=PreTreatedBatch(data_dt=datetime.datetime.now(),batch_status=u'异常终止',begin_dt=time,\
                 end_dt=time)
    session.add(batch)
    session.flush()
    log1=PreTreatedBatchLog(batch_id=batch.id,process_code='9327',log_dt=time,\
                            log_type='info',log_info=u'系统开始执行数据预处理任务')

    log2=PreTreatedBatchLog(batch_id=batch.id,process_code='9327',log_dt=time,\
                            log_type='info',log_info=u'提取客户数据...')

    log3=PreTreatedBatchLog(batch_id=batch.id,process_code='9327',log_dt=time,\
                            log_type='info',log_info=u'客户数据提取完成')


    log4=PreTreatedBatchLog(batch_id=batch.id,process_code='9327',log_dt=time,\
                            log_type='error',log_info=u'提取交易数据错误')
    session.add_all([log1,log2,log3,log4])

    init_np(session)
    
    logging.info(u"数据库重置完成")
    session.commit()


def rebuild_orm(tbname):
    u"""重建ORM模型表

    :param tbname: 表名称
    """
    flag = tbname in Base.metadata.tables
    if flag is not True:
        print "未知的表名称[%s]，请确认后再执行" % tbname
        return 

    session = simple_session()
    print "Table[%s]: existed" % tbname if flag else "Table[%s]: not existed" % tbname
    if flag:
        print "Droping Existed Table[%s].." % tbname
        Base.metadata.tables.get(tbname).drop(session.bind, checkfirst=True)

    print "Creating Table[%s].." % tbname
    Base.metadata.tables.get(tbname).create(session.bind, checkfirst=True)


def load_odsdata(run_month, bankno, tabs):
    u"""手工加载ODS数据

    :param run_month: 导入月份
    :param bankno: 银行编号
    :param tabs:导入表
    """
    from fdm.tests.init_namemapping import init_np
    from fdm.tools import pretreatment_tools

    try:
        if len(run_month) > 6:
            logging.error(u"日期长度不正确！")
            raise ValueError("日期长度不正确")

        run_month = str2date(run_month, "%Y%m")
    except:
        logging.error(u"输入日期格式问题，请确认后再执行！")
        return 

    if tabs != 'ALL':
        tabs = tabs.split(",")
        for t in tabs:
            if t not in [u'TRANJRNL', u'CUSTACCT']:
                logging.error(u"指定表必须是 TRAJRNL 与 CUSTACCT 中的一个！")
                return 

    if not bool(tabs) or tabs=="ALL":
        tabs = [u'TRANJRNL', u'CUSTACCT']

    pretreatment_tools.start(run_month, bankno, tabs=tabs, reset_index=True)


def load_custdata(bankno, run_month):
    u"""从CUSTACCT中加工客户数据

    :param bankno: 运行银行
    :param run_month: 运行月份
    """
    from fdm.tools.pretreatment_tools import make_cust_info

    bankno = bankno if bankno != 'ALL' else None

    if run_month != 'ALL':
        try:
            run_month = str2date(run_month, "%Y%m")
            run_month = get_last_date_of_month(run_month.year, run_month.month, str_flag=True)
        except:
            traceback.print_exc()
            logging.error(u"输入日期格式问题，请确认后再执行！")
            return 
    else:
        run_month = None
    
    make_cust_info(run_month, bankno)


def check_odsdata(check_month, bankno, tabs):
    u""" 检测数据是否到达
        
    :param check_month: 数据月份
    :param bankno: 银行编号
    :param tabs: 表
    """
    from fdm.tools.dataset_tools import check_data

    try:
        str2date(check_month, "%Y%m")
    except:
        logging.error(u"输入日期格式问题，请确认后再执行！")
        return 

    if tabs != 'ALL':
        tabs = tabs.split(",")
        for t in tabs:
            if t not in [u'TRANJRNL', u'CUSTACCT']:
                logging.error(u"指定表必须是 TRAJRNL 与 CUSTACCT 中的一个！")
                return 

    if not bool(tabs) or tabs=="ALL":
        tabs = [u'TRANJRNL', u'CUSTACCT']

    flag, msg =  check_data(check_month, bankno, tabs)
    
    print msg


def fake_test_data(data_dt, bankno, length, tabs):
    u"""造假数据

    :param data_dt: 数据日期
    :param bankno: 银行编号
    :param length: 数据量
    """
    #from fdm.tools.data_faker_tools import fake_data
    from fdm.tools.data_faker_pandas_tools import fake_data

    if tabs != 'ALL':
        tabs = tabs.split(",")
        for t in tabs:
            if t not in [u'TRANJRNL', u'CUSTACCT']:
                logging.error(u"指定表必须是 TRAJRNL 与 CUSTACCT 中的一个！")
                return 

    if not bool(tabs) or tabs=="ALL":
        tabs = [u'TRANJRNL', u'CUSTACCT']

    fake_data(data_dt, bankno, int(length), sheet_names=tabs)


def fake_neo4j_data(data_dt, bankno, length):
    u"""造假数据

    :param data_dt: 数据日期
    :param bankno: 银行编号
    """
    from fdm.tools.data_faker_neo4j_tools import data_faker_neo4j 
    data_dt = '-'.join([data_dt[0:4],data_dt[4:6],data_dt[6:8]])
    data_faker_neo4j(data_dt, bankno, length)

def es_neo4j_data(index_name, node_label, relationship_type):
    u""" es数据 导入到 neo4j

    :param index_name: 数据日期
    :param node_label: 节点标签
    :param relationship_type: 关系类型
    """
    from fdm.tools.data_es_neo4j_tools import data_es_neo4j_tools 
    data_es_neo4j_tools(index_name=index_name, node_label=node_label, relationship_type=relationship_type)



def analysis_test_data(data_dt, bankno, tabs):
    u"""分析数据

    :param data_dt: 数据日期
    :param bankno: 银行编号
    :param tabs:导入表
    """
    from fdm.tools.data_analysis_tools import analysis_main 

    if tabs != 'ALL':
        tabs = tabs.split(",")
        for t in tabs:
            if t not in [u'TRANJRNL', u'CUSTACCT']:
                logging.error(u"指定表必须是 TRAJRNL 与 CUSTACCT 中的一个！")
                return 

    if not bool(tabs) or tabs=="ALL":
        tabs = [u'TRANJRNL', u'CUSTACCT']

    analysis_main(date=data_dt, bankno=bankno, tabs=tabs)

def clear_test_data(data_dt, run_flag):
    u"""重加载数据

    :param data_dt: 数据日期
    :param run_flag:导入表
    """
    from fdm.tools.data_clear import clear_main

    if run_flag.lower() == "true":
        run_flag = True
    else:
        run_flag = False
    
    clear_main(date=data_dt ,run_flag=run_flag)

def tran_name_data(cust_name,tran_name,postfix):
    u"""重加载数据

    :param cust_name: 客户数据名称
    :param tran_name: 交易数据名称
    :param postfix: 新生成后的数据后缀
    """
    from fdm.tools.data_peoplename_tran import data_tran_main
    data_tran_main(cust_name=cust_name,tran_name=tran_name,postfix=postfix)

def start_ftp_monitor():
    u"""开启FTP远程监控程序"""
    from fdm.tools.monitor_tools import FTPRemoteMonitor, check_data_arrive
    from fdm.base.settings import Config
    hostaddr = Config.FTP_HOSTADDR
    username = Config.FTP_USERNAME
    password = Config.FTP_PASSWORD
    port  =  Config.FTP_PORT
    monitor_dir =  Config.FTP_MONITOR_DIR
    save_path = Config.ODS_PATH

    print "开始FTP远程监控程序..."
    f = FTPRemoteMonitor(hostaddr, username, password, port, monitor_dir, 
                            callback=check_data_arrive, save_path=save_path)
    f.start()

def stop_ftp_monitor():
    u"""关闭ftp远程监控程序"""
    print "关闭FTP远程监控程序..."
    os.system("ps -x|grep start_ftp_monitor|awk '{print $1}'|xargs kill -15")
    print "关闭成功."


def start_daily_job_monitor():
    u"""启动每月作业监控"""
    from fdm.tools.monitor_tools import DailyJob
    job = DailyJob()
    job.start()
        

def tools_dispatcher(options, args):
    u"""工作调度器

        后续可支持更多的功能
    """
    # TODO:更好的动态调用
    opts = [p for p in dir(options) if not p.startswith('_')]

    _method_map = {
        'init_db': init_db,
        "orm_tbname": rebuild_orm,

        'load_params':load_odsdata,
        "cust_params":load_custdata,
        "check_params":check_odsdata,

        'faker_params':fake_test_data,
        'faker_neo4j':fake_neo4j_data,
        'es_neo4j':es_neo4j_data,
        'analysis_params':analysis_test_data,
        'clear_params':clear_test_data,
        'tran_name_params':tran_name_data,

        "mining_params":mining_model,
        "entity_date": make_mining_entity,
        "rpt_params":rpt_aftertreatment,

        'start_ftp_monitor':start_ftp_monitor,
        'stop_ftp_monitor':stop_ftp_monitor,
        'start_daily_job_monitor':start_daily_job_monitor,
    }

    for op in opts:
        if getattr(options, op) and op in _method_map:
            opargs = getattr(options, op)
            opargs = opargs if isinstance(opargs, (list, tuple)) else (opargs, )

            funcs = _method_map[op]
            funcs = funcs if isinstance(funcs, (list, tuple)) else [funcs,]

            for func in funcs:
                func() if opargs==(True, ) else func(*opargs)


if __name__ == '__main__':
    optParser = OptionParser()

    # 基础工具 -- 基础函数
    base_tools_options = OptionGroup(optParser, "Base Tools Options", "用于处理数据库内表变动.")
    base_tools_options.add_option("--init_db", action="store_true", dest="init_db",
                                    help=u"重置应用数据库")
    base_tools_options.add_option("--rebuild_orm", action="store", dest="orm_tbname",
                         help=u"根据orm模型重建表")
    optParser.add_option_group(base_tools_options)



    # 功能模块 -- 某类功能
    func_tools_options = OptionGroup(optParser, "Base Tools Options", "用于处理数据库内表变动.")
    func_tools_options.add_option("--init_db", action="store_true", dest="init_db",
                                    help=u"重置应用数据库")
    func_tools_options.add_option("--rebuild_orm", action="store", dest="orm_tbname",
                         help=u"根据orm模型重建表")
    optParser.add_option_group(func_tools_options)

    # 其他 -- 其他功能
    else_tools_options = OptionGroup(optParser, "Base Tools Options", "用于处理数据库内表变动.")
    else_tools_options.add_option("--init_db", action="store_true", dest="init_db",
                                    help=u"重置应用数据库")
    else_tools_options.add_option("--rebuild_orm", action="store", dest="orm_tbname",
                         help=u"根据orm模型重建表")
    optParser.add_option_group(else_tools_options)
    























    assist_tools_options = OptionGroup(optParser, "Assist Tools Options", "用于项目工程各类辅助操作.")
    assist_tools_options.add_option("--fake_data", action="store", dest="faker_params", nargs=4,
                                help=u"""用于生成指定时间月份的假数据测试,
                                        --fake_data 数据日期 银行编号 数据量 自定表
                                        --fake_data 20170101 60001 100000 ALL""")
    assist_tools_options.add_option("--fake_neo4jdata", action="store", dest="faker_neo4j", nargs=3,
                                help=u"""用于生成指定时间月份的neo4j假数据测试,
                                        --fake_neo4jdata 数据日期 银行编号 数据量
                                        --fake_neo4jdata 20170101 60001 100000""")
    assist_tools_options.add_option("--es_neo4jdata", action="store", dest="es_neo4j", nargs=3,
                                help=u"""用于将指定索引数据导入到neo4j中
                                        (PS:导入到正在开启的neo4j数据库,custacct-xxxx导入节点,tranjrnl-xxxx导入关系)
                                        --es_neo4jdata 索引名称 节点标签 关系标签
                                        --es_neo4jdata tranjrnl-99999999-2017-01-31 cust tran""")

    assist_tools_options.add_option("--analysis_data", action="store", dest="analysis_params", nargs=3,
                                help=u"""用于生成指定时间月份的数据分析报告,
                                        --analysis_data 数据日期 银行编号 数据类型
                                        --analysis_data 20170131 427,102 TRANJRNL """)
    assist_tools_options.add_option("--clear_data", action="store", dest="clear_params", nargs=2,
                                help=u"""用于自动批量，重新加载数据,删除数据和控制文件
                                        --clear_data 数据日期 是否运行
                                        --clear_data 201701 false
                                        --clear_data 201701 true""")
    assist_tools_options.add_option("--tran_name", action="store", dest="tran_name_params", nargs=3,
                                help=u"""用于将汉人名称转换为维族名称 例如交易数据名称:杰恩斯古丽·地里达尔
                                        --tran_name 客户数据 交易数据 转换后的数据添加的后缀名称
                                                    为none时,会直接替换原有数据,谨慎操作!
                                        --tran_name cust.csv tran.csv _weizu 
                                        --tran_name cust.csv tran.csv none """)

    optParser.add_option_group(assist_tools_options)

    mining_tools_options = OptionGroup(optParser, "Mining Tools Options", "模型运行 TODO：不完整功能.")
    mining_tools_options.add_option("--model_entity", action="store", dest="entity_date", nargs=2,
                                help=u"""用于加工模型基础指标,

                                        --model_entity 20170101 20170131""")
    mining_tools_options.add_option("--mining_model", action="store", dest="mining_params", nargs=2,
                                help=u"""用于测试模型结果,

                                        --mining_model 20160101 K2,K3
                                        --mining_model 20160101 ALL""")
    mining_tools_options.add_option("--report_aftertreatment", action="store", dest="rpt_params",
                                help=u"""用于模型需要字段生成工具

                                        --report_aftertreatment 20170101""")

    optParser.add_option_group(mining_tools_options)


    options, args = optParser.parse_args()
    tools_dispatcher(options, args)
