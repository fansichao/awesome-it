# -*- coding:utf-8 -*- 
u"""
工具类

"""


from ..database import * 
from party import * 
from branch import Branch 
 
 


class pro_tool_name(Base):
    u"""
        工具名称
    """
    id=Column(BigInteger,Sequence('group_id_seq'),primary_key=True) 
    tool_name=Column(String(64),doc=u"工具名称") 
    tool_group_name=Column(String(64),doc=u"工具所属组名") 
    status=Column(String(32),doc=u'状态') 
    oper_name=Column(String(32),doc=u'操作人员') 
    oper_code=Column(String(32),doc=u'操作人员编号') 
    oper_time=Column(DateTime,doc=u'维护时间') 


