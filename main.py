import os
import sys
from io import BytesIO
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from ai_module import ali_nls
from core import wsa_server
from gui import flask_server
from gui.window import MainWindow
from utils import config_util
from scheduler.thread_manager import MyThread
from core.content_db import Content_Db
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

def __clear_samples():
    if not os.path.exists("./samples"):
        os.mkdir("./samples")
    for file_name in os.listdir('./samples'):
        if file_name.startswith('sample-') and file_name.endswith('.mp3'):
            os.remove('./samples/' + file_name)


def __clear_songs():
    if not os.path.exists("./songs"):
        os.mkdir("./songs")
    for file_name in os.listdir('./songs'):
        if file_name.endswith('.mp3'):
            os.remove('./songs/' + file_name)


if __name__ == '__main__':
    __clear_samples()
    __clear_songs()
    config_util.load_config()
    dbstatus = os.path.exists("fay.db")  # 打开数据库
    if dbstatus == False:
         contentdb = Content_Db()
         contentdb.init_db()             # 如果没有数据库，那么初始化数据库  
    ws_server = wsa_server.new_instance(port=10002)
    ws_server.start_server()
    web_ws_server = wsa_server.new_web_instance(port=10003)
    web_ws_server.start_server()
    # 增加本地asr后，aliyun调成可选配置
    if config_util.ASR_mode == "ali" and config_util.config['source']['record']['enabled']:
        ali_nls.start()
    flask_server.start() # 打开falsk服务
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    win = MainWindow()
    win.show()
    app.exit(app.exec_())

    
