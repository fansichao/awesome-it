# -*- coding: utf-8 -*-
"""
    印象笔记 - 功能脚本

功能:
    复制 指定笔记本中指定笔记模板 到指定笔记本中
用途:
    每日日记模板自动复制
参考文档:
    https://www.jianshu.com/p/e5d17efaff53

sudo crontab -e
1 0 * * * bash -c 'cd /home/scfan/MyData/Scripts && python create_evernote_dairy_from_template.py >> /home/scfan/MyData/Scripts/logs/create_dairy.log 2>&1'
    

"""
import logging
import datetime
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore

logging.basicConfig(level=logging.INFO)

"""
配置区域，请自行修改
- auth_token: 访问 https://app.yinxiang.com/api/DeveloperToken.action 生成
- diary_template_name：日记模板名称，请保证有且仅有一个标题为这个的笔记
- diary_notebook_name：复制生成的笔记要放入哪个笔记本，填写笔记本名称
"""
import os
auth_token = os.environ['evernote_auth_token']
diary_template_name = '晨间日记模板'
diary_notebook_name = 'diary'

# 日记标题。个人习惯用形如 『20170325（周六）』这样的标题，可以根据自己的需求修改。
weekday_chinese_map = {
    0: '周一',
    1: '周二',
    2: '周三',
    3: '周四',
    4: '周五',
    5: '周六',
    6: '周日',
}
now = datetime.datetime.now()
diary_title = '%s（%s）' % (now.strftime('%Y%m%d'),
                          weekday_chinese_map[now.weekday()])
logging.info('diary_title: %s', diary_title)

client = EvernoteClient(token=auth_token, service_host='app.yinxiang.com')

user_store = client.get_user_store()

note_store = client.get_note_store()

# 定位日记所在笔记本 guid
notebooks = note_store.listNotebooks()
logging.debug('Found %s notebooks', len(notebooks))
for notebook in notebooks:
    logging.debug('guid: [%s], notebook [%s]', notebook.guid, notebook.name)
    if notebook.name == diary_notebook_name:
        logging.info('found diary notebook! guid: [%s], notebook [%s]',
                     notebook.guid, notebook.name)
        diary_notebook_guid = notebook.guid
        break
else:
    logging.critical('diary [%s] not found', diary_notebook_name)
    exit(1)

# 定位日记模板 guid
noteFilter = NoteStore.NoteFilter(words=diary_template_name)
spec = NoteStore.NotesMetadataResultSpec()

nmdList = note_store.findNotesMetadata(noteFilter, 0, 250, spec)
logging.debug('nmdList: %s', nmdList)
for n in nmdList.notes:
    note = note_store.getNote(n.guid, True, True, False, False)
    logging.debug('guid: [%s], title: [%s]', note.guid, note.title)
    if note.title == diary_template_name:
        logging.info('found diary template note! guid: [%s], title: [%s]',
                     note.guid, note.title)
        diary_template_guid = note.guid
        break
else:
    logging.critical('diary_template [%s] not found', diary_template_name)
    exit(1)

# 复制模板，生成笔记，修改标题
res_note = note_store.copyNote(diary_template_guid, diary_notebook_guid)
res_note.title = diary_title
res_note = note_store.updateNote(res_note)
logging.info('create diary for %s done!', now)
