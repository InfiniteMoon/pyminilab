# 导入必要的模块
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

# 定义一个播放音频的函数
def play_audio():
    # 获取列表框中选中的文件名
    filename = listbox.currentItem().text()
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

# 创建一个按钮对象，用于播放音频
button = QtWidgets.QPushButton("播放", window)
button.move(300, 150)
button.clicked.connect(play_audio)

# 创建一个快捷方式对象，用于绑定空格键和播放音频函数
shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), window)
shortcut.activated.connect(play_audio)

# 显示窗口
window.show()

# 进入主循环
sys.exit(app.exec_())
