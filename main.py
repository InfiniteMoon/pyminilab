# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import time
import requests
import urllib
# 导入必要的模块
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QAction, QToolBar, QLabel
import pypinyin
import pykakasi


lfasr_host = 'https://raasr.xfyun.cn/v2/api'
# 请求的接口名
api_upload = '/upload'
api_get_result = '/getResult'

#定义一个获取文件名的函数
def getfilepath():
    # 获取列表框中选中的文件名
    item = listbox.currentItem()
    # 如果没有选中任何文件，弹出提示框并返回
    if item is None:
        QtWidgets.QMessageBox.warning(window, "警告", "请先选择一个文件")
        return
    # 否则，获取文件名
    filename = item.text()
    # 拼接完整的文件路径
    filepath = os.path.join(folder, filename)
    return filepath

# 定义一个播放音频的函数
def play_audio():
    filepath = getfilepath()
    # 尝试加载和播放音频文件
    try:
        # 设置音频源为本地文件的url
        sound.setSource(QtCore.QUrl.fromLocalFile(filepath))
        # 播放音频
        sound.play()
    # 如果出现异常，弹出错误提示框
    except:
        QtWidgets.QMessageBox.critical(window, "错误", "无法播放该文件")

# 定义一个显示文本的函数
def show_text():
    # 保存之前编辑过的内容
    save_text()
    # 获取列表框中选中的文件名
    item = listbox.currentItem()
    # 如果没有选中任何文件，清空文本框并返回
    if item is None:
        textbox.clear()
        return
    # 否则，获取文件名
    filename = item.text()
    # 替换扩展名为.lab
    filename = filename.replace(".wav", ".lab")
    # 拼接完整的文件路径
    filepath = os.path.join(folder, filename)
    # 尝试打开和读取文本文件
    try:
        with open(filepath, "r") as f:
            text = f.read()
            # 如果文本为空，显示提示信息
            if not text:
                text = ""
            # 设置文本框的内容为文本
            textbox.setText(text)
            # 设置当前编辑过的文件路径为filepath
            global current_file
            current_file = filepath
            # 记录当前光标位置
            global cursor_pos
            cursor_pos = textbox.textCursor().position()
    # 如果出现异常，尝试新建一个同名的空白文件，并清空文本框，并设置当前编辑过的文件路径为filepath，并记录当前光标位置
    except:
        with open(filepath, "w") as f:
            textbox.clear()
            current_file = filepath
            cursor_pos = 0

# 定义一个保存文本的函数
def save_text():
    # 获取当前编辑过的文件路径
    global current_file
    if current_file:
        # 获取文本框中的内容
        text = textbox.toPlainText()
        # 尝试打开和写入文本文件
        try:
            with open(current_file, "w") as f:
                f.write(text)
        # 如果出现异常，弹出错误提示框
        except:
            QtWidgets.QMessageBox.critical(window, "错误", "无法保存该文件")

# 定义一个选择文件夹的函数
def select_folder():
    # 弹出一个对话框，让用户选择一个文件夹
    global folder
    folder = QtWidgets.QFileDialog.getExistingDirectory()
    # 如果用户没有选择任何文件夹，直接返回
    if not folder:
        return
    # 清空列表框中的内容
    listbox.clear()
    # 遍历文件夹中的所有文件
    for file in os.listdir(folder):
        # 如果文件是wav格式，将其添加到列表框中
        if file.endswith(".wav"):
            listbox.addItem(file)

# 定义一个处理上下键事件的函数
def handle_key(event):
    # 获取当前按下的键
    key = event.key()
    # 如果是上键，且列表框有选中的项目，且不是第一个项目，就向上移动一项，并显示文本，并保持光标位置不变
    if key == QtCore.Qt.Key_Up and listbox.currentItem() and listbox.currentRow() > 0:
        listbox.setCurrentRow(listbox.currentRow() - 1)
        show_text()
        cursor = textbox.textCursor()
        cursor.setPosition(cursor_pos)
        textbox.setTextCursor(cursor)
    # 如果是下键，且列表框有选中的项目，且不是最后一个项目，就向下移动一项，并显示文本，并保持光标位置不变
    elif key == QtCore.Qt.Key_Down and listbox.currentItem() and listbox.currentRow() < listbox.count() - 1:
        listbox.setCurrentRow(listbox.currentRow() + 1)
        show_text()
        cursor = textbox.textCursor()
        cursor.setPosition(cursor_pos)
        textbox.setTextCursor(cursor)
    # 否则，调用原来的事件处理函数
    else:
        QtWidgets.QTextEdit.keyPressEvent(textbox, event)

# 创建一个PyQt应用对象
app = QtWidgets.QApplication(sys.argv)

# 创建一个QSoundEffect对象，用于播放音频
sound = QtMultimedia.QSoundEffect()

# 创建一个PyQt窗口对象
window = QtWidgets.QWidget()
window.setWindowTitle("pyminilab")
window.resize(400, 300)

# 创建一个创建一个按钮对象
menubar = QtWidgets.QMenuBar(window)
# 创建一个菜单项对象，用于选择文件夹
menu = menubar.addMenu("文件")
action = menu.addAction("选择文件夹")
action.triggered.connect(select_folder)

# 创建一个创建一个按钮对象，用于选择文件夹
button_open = QtWidgets.QPushButton("打开", window)
button_open.move(300, 110)
button_open.clicked.connect(select_folder)

# 创建一个列表框对象，用于显示wav文件
listbox = QtWidgets.QListWidget(window)
listbox.move(0, 10)
# 绑定列表框的点击事件和显示文本函数
listbox.itemClicked.connect(show_text)
# 绑定列表框的上下键事件和显示文本函数
listbox.currentItemChanged.connect(show_text)

# 创建一个按钮对象，用于播放音频
button = QtWidgets.QPushButton("播放", window)
button.move(300, 170)
button.clicked.connect(play_audio)

# 创建一个快捷方式对象，用于绑定空格键和播放音频函数
shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), window)
shortcut.activated.connect(play_audio)

# 创建一个文本框对象，用于显示和编辑文本文件
textbox = QtWidgets.QTextEdit(window)
textbox.move(0, 250)
textbox.resize(400, 100)
textbox.setObjectName('textbox')
# 重写文本框的键盘事件处理函数，用于处理上下键事件
textbox.keyPressEvent = handle_key

# 创建一个文本框对象，用于显示和编辑文本文件(日文或者中文)
textbox2 = QtWidgets.QTextEdit(window)
textbox2.move(0, 205)
textbox2.resize(400, 20)

# 创建一个文本框对象，appid
textboxapp = QtWidgets.QTextEdit(window)
textboxapp.move(270, 40)
textboxapp.resize(400, 20)

# 创建一个文本框对象，key
textboxkey = QtWidgets.QTextEdit(window)
textboxkey.move(270, 80)
textboxkey.resize(400, 20)

# 创建一个标签对象，用于提示appid
app_label = QtWidgets.QLabel(window)
app_label.move(270, 20)
app_label.setText("appid:")

# 创建一个标签对象，用于提示appid
app_label = QtWidgets.QLabel(window)
app_label.move(270, 60)
app_label.setText("secret_key:")


# 重写文本框的键盘事件处理函数，用于处理上下键事件
#textbox2.keyPressEvent = handle_key
# 创建一个按钮对象，用于保存文本文件
save_button = QtWidgets.QPushButton("保存", window)
save_button.move(300, 140)
save_button.clicked.connect(save_text)

# 初始化当前编辑过的文件路径为空字符串
current_file = ""

# 选择语言
combo = QtWidgets.QComboBox(window)
combo.addItem('cn')
combo.addItem('ja')
combo.move(10, 222)


def on_change():
    # 获取当前选择的文本
    text = combo.currentText()
    # 在控制台打印出结果
    print('你选择了' + text)
    language = text
    print(language)

combo.currentIndexChanged.connect(on_change)

# 获取用户选择的项目的索引
index = combo.currentIndex()
    # 根据索引执行不同的操作


#def planguage():
#   if index == 0:
#       language = 'zh'
#      print(language)
# else:
#    language = 'jp'
#   print(language)

#save_label = QtWidgets.QLabel(window)
#save_label.move(328, 180)
#save_label.setText(combo.currentText())
# 创建一个按钮对象，用于转换标记

def convert_to_pinyin():
    print(textbox2)
    # 从文本框中获取中文字符串
    chinese = textbox2.toPlainText()
    # 去除掉符号，只保留汉字和空格
    chinese = ''.join([c for c in chinese if c.isalnum() or c.isspace()])
    # 使用pypinyin库将中文转换为拼音列表，不带声调，用空格分隔
    pinyin = ' '.join([p[0] for p in pypinyin.pinyin(chinese, style=pypinyin.NORMAL)])
    # 将拼音字符串填入到textbox中
    textbox.setText(pinyin)

# 定义一个函数，接受一个文本框对象作为参数
def convert_to_romaji():
    # 从文本框中获取日语字符串
    japanese = textbox2.toPlainText()
    # 去除掉符号，只保留汉字、假名和空格
    japanese = ''.join([c for c in japanese if c.isalnum() or c.isspace()])
    # 使用pykakasi库将日语转换为罗马音列表，用空格分隔
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a") 
    kakasi.setMode("K", "a")
    kakasi.setMode('J', 'a')
    kakasi.setMode("s", True) # 添加空格
    converter = kakasi.getConverter()
    romaji = converter.do(japanese)
    # 将罗马音字符串填入到textbox1中
    textbox.setText(romaji)



def trance():
    if combo.currentText() == 'cn':
        convert_to_pinyin()
    else:
        convert_to_romaji()


# 创建一个用于转换文本到拼音罗马字的按钮
trance_button = QtWidgets.QPushButton("转换", window)
trance_button.move(80, 222)
trance_button.clicked.connect(trance)





class RequestApi(object):
    def __init__(self, appid, secret_key, upload_file_path, language):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()
        self.language = language

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa


    def upload(self):
        print("上传部分：")
        upload_file_path = self.upload_file_path
        language = self.language
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        param_dict["language"] = str(language)
        print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url =lfasr_host + api_upload+"?"+urllib.parse.urlencode(param_dict),
                                headers = {"Content-type":"application/json"},data=data)
        print("upload_url:",response.request.url)
        result = json.loads(response.text)
        print("upload resp:", result)
        return result


    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        print("")
        print("查询部分：")
        print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(url=lfasr_host + api_get_result + "?" + urllib.parse.urlencode(param_dict),
                                     headers={"Content-type": "application/json"})
            print("get_result_url:",response.request.url)
            result = json.loads(response.text)
            # global txt
            # txt = result
            print(result)
            status = result['content']['orderInfo']['status']
            print("status=",status)
            if status == 4:
                break
            time.sleep(5)
        print("get_result resp:",result)
        print("test:",result['content']['orderResult'])
        # 将json字符串转换为Python字典
        json_dict = json.loads(result['content']['orderResult'])

        # 从字典中获取lattice列表
        lattice_list = json_dict["lattice"]

        # 从列表中获取第一个元素，也是一个字典
        lattice_dict = lattice_list[0]

        # 从字典中获取json_1best的值，也是一个json字符串
        json_1best_str = lattice_dict["json_1best"]

        # 将json_1best字符串转换为Python字典
        json_1best_dict = json.loads(json_1best_str)

        # 从字典中获取st的值，也是一个字典
        st_dict = json_1best_dict["st"]

        # 从字典中获取rt的值，也是一个列表
        rt_list = st_dict["rt"]

        # 从列表中获取第一个元素，也是一个字典
        rt_dict = rt_list[0]

        # 从字典中获取ws的值，也是一个列表
        ws_list = rt_dict["ws"]

        # 定义一个空字符串，用于存放汉字内容
        text = ""

        # 遍历ws列表中的每个元素，也是一个字典
        for ws_dict in ws_list:
            # 从字典中获取cw的值，也是一个列表
            cw_list = ws_dict["cw"]
            # 从列表中获取第一个元素，也是一个字典
            cw_dict = cw_list[0]
            # 从字典中获取w的值，也是一个字符串
            w_str = cw_dict["w"]
            # 将w的值拼接到text字符串中
            text += w_str

        # 打印text字符串，即json_1best里面的汉字内容
        print(text)
        # print("get_result need:",result['orderResult'])
        return text

# 定义一个函数，进行语音识别
def analyse():
    # 输入讯飞开放平台的appid，secret_key和待转写的文件路径
    api = RequestApi(appid=textboxapp.toPlainText(),
                     secret_key=textboxkey.toPlainText(),
                     upload_file_path=getfilepath(),
                     language=combo.currentText())

    textbox2.setText(api.get_result())

# 创建一个用于语音识别的按钮
trance_button = QtWidgets.QPushButton("识别", window)
trance_button.move(160, 222)
trance_button.clicked.connect(analyse)

# 显示窗口
window.show()

# 首次选择文件夹
select_folder()

#初始化语言
on_change()

# 进入主循环
sys.exit(app.exec_())
