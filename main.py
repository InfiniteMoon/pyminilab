# 导入必要的模块
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

# 定义一个播放音频的函数
def play_audio():
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
    # 如果出现异常，尝试新建一个同名的空白文件，并清空文本框
    except:
        with open(filepath, "w") as f:
            textbox.clear()

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

# 创建一个PyQt应用对象
app = QtWidgets.QApplication(sys.argv)

# 创建一个QSoundEffect对象，用于播放音频
sound = QtMultimedia.QSoundEffect()

# 创建一个PyQt窗口对象
window = QtWidgets.QWidget()
window.setWindowTitle("PyQt WAV Player")
window.resize(400, 300)

# 创建一个菜单栏对象
menubar = QtWidgets.QMenuBar(window)
# 创建一个菜单项对象，用于选择文件夹
menu = menubar.addMenu("文件")
action = menu.addAction("选择文件夹")
action.triggered.connect(select_folder)

# 创建一个列表框对象，用于显示wav文件
listbox = QtWidgets.QListWidget(window)
listbox.move(0, menubar.height())
# 绑定列表框的点击事件和显示文本函数
listbox.itemClicked.connect(show_text)
# 绑定列表框的上下键事件和显示文本函数
listbox.currentItemChanged.connect(show_text)

# 创建一个按钮对象，用于播放音频
button = QtWidgets.QPushButton("播放", window)
button.move(300, 150)
button.clicked.connect(play_audio)

# 创建一个快捷方式对象，用于绑定空格键和播放音频函数
shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), window)
shortcut.activated.connect(play_audio)

# 创建一个文本框对象，用于显示文本文件
textbox = QtWidgets.QTextEdit(window)
textbox.move(0, 200)
textbox.resize(400, 100)
# 设置文本框为只读模式
textbox.setReadOnly(True)

# 显示窗口
window.show()

select_folder()

# 进入主循环
sys.exit(app.exec_())
