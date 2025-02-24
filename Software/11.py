# coding:utf-8

from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QStackedWidget, QApplication, QPushButton, QVBoxLayout, \
    QFileDialog, QMessageBox, QHBoxLayout, QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome
import pyaudio                                  # pyaudio库，使用这个可以进行录音，播放，生成wav文件等
import wave                                     # wave 模块提供了一个处理 WAV 声音格式的便利接口
import threading
import winsound
import sys
from datetime import datetime
import matlab.engine


class MainUi(QtWidgets.QMainWindow):
    def __init__(self, chunk=1024, channels=2, rate=64000):
        super().__init__()
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
        self.recording_counter = 1
        current_filename = None
        self.recordings = []
        self.init_ui()

    def init_ui(self):

        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.left_close = QtWidgets.QPushButton("×")  # 关闭按钮
        self.left_close.clicked.connect(self.close)  # 点击则关闭
        self.left_max = QtWidgets.QPushButton("口")  # 空白按钮
        self.left_max.clicked.connect(self.slot_max_or_recv)
        self.left_mini = QtWidgets.QPushButton("－")  # 最小化按钮
        self.left_mini.clicked.connect(self.showMinimized)

        self.left_label_1 = QtWidgets.QPushButton("场景选择")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("我的音频")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.car', color='white'), "室外")
        self.left_button_1.setObjectName('left_button')
        self.left_button_1.clicked.connect(self.show_page1)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.child', color='white'), "教室")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.show_page2)
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.circle', color='white'), "老年人")
        self.left_button_3.setObjectName('left_button')
        self.left_button_3.clicked.connect(self.show_page3)

        # self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.upload', color='white'), "录制音频")
        # self.left_button_4.setObjectName('left_button')
        # self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "降噪音频")
        # self.left_button_5.setObjectName('left_button')

        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "全部文件")
        self.left_button_6.setObjectName('left_button')

        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "反馈建议")
        self.left_button_7.setObjectName('left_button')
        self.left_button_7.clicked.connect(self.showCommentDialog)

        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')
        self.left_xxx = QtWidgets.QPushButton(" ")
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_max, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)
        # 创建一个堆叠部件（用于管理多个页面）
        self.stacked_widget = QStackedWidget()
        # 创建页面1的内容
        self.page1_widget = QLabel("室外")
        # self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        # self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        # self.right_bar_widget.setLayout(self.right_bar_layout)
        # self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索')
        # self.search_icon.setFont(qtawesome.font('fa', 16))
        # self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        # self.right_bar_widget_search_input.setPlaceholderText("输入场景，回车进行搜索")
        # self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        # self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)

        # 创建页面2的内容
        self.page2_widget = QLabel("教室")

        # 创建页面2的内容
        self.page3_widget = QLabel("老年人")

        # 将页面内容添加到堆叠部件中
        self.stacked_widget.addWidget(self.page1_widget)
        self.stacked_widget.addWidget(self.page2_widget)
        self.stacked_widget.addWidget(self.page3_widget)

        self.right_layout.addWidget(self.stacked_widget, 0, 0, 1, 9)
        self.right_recommend_label = QtWidgets.QLabel("功能选择")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        self.is_switching = False
        self.is_pause = True

        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("录音")  # 设置按钮文本
        self.recommend_button_1.setIcon(QtGui.QIcon('./4.png'))  # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(170, 170))  # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.recommend_button_1.clicked.connect(self.start_recording)

        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("降噪")
        self.recommend_button_2.setIcon(QtGui.QIcon('./3.png'))
        self.recommend_button_2.setIconSize(QtCore.QSize(170, 170))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        # self.recommend_button_2.clicked.connect(self.stop_recording)
        self.recommend_button_2.clicked.connect(self.processMBSS_audio)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("播放原始音频")
        self.recommend_button_3.setIcon(QtGui.QIcon('./1.png'))
        self.recommend_button_3.setIconSize(QtCore.QSize(170, 170))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_3.clicked.connect(self.play_recording)

        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("播放处理音频")
        self.recommend_button_4.setIcon(QtGui.QIcon('./2.png'))
        self.recommend_button_4.setIconSize(QtCore.QSize(170, 170))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.recommend_button_4.clicked.connect(self.play_recordingMBSS)

        # 下面是增加的内容，测试可以把括号内的方法换掉，然后把下面的matlab的这些方法都注释掉
        # 现在还是没办法区分不同的场景
        ######################################################################################################################################################################################
        # self.page3_widget.recommend_button_2.clicked.connect(self.processMBSS_audio)
        # self.page2_widget.recommend_button_2.clicked.connect(self.processPSC_audio)
        # self.page1_widget.recommend_button_2.clicked.connect(self.processNSSP_audio)
        ######################################################################################################################################################################################

        self.right_recommend_layout.addWidget(self.recommend_button_1, 0, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_2, 0, 1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 10, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 10, 1)

        self.right_layout.addWidget(self.right_recommend_label, 1, 0, 1, 9)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)

        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.right_process_bar.setValue(49)
        self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字

        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")
        self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.pause', color='#F76677', font=18), "")
        self.console_button_3.setIconSize(QtCore.QSize(30, 30))

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 0)
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 2)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 1)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示

        self.right_layout.addWidget(self.right_process_bar, 9, 0, 1, 9)
        self.right_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_max.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_max.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget{background-color:rgb(0, 0, 0);}
        ''')

        # self.right_bar_widget_search_input.setStyleSheet(
        #     '''QLineEdit{
        #             border:1px solid gray;
        #             width:300px;
        #             border-radius:10px;
        #             padding:2px 4px;
        #     }''')

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QWidget{background-color:rgb(245, 245, 245);}
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')
        self.right_process_bar.setStyleSheet('''
            QProgressBar::chunk {
                background-color: #F76677;
            }
        ''')

        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    def show_page1(self):
        self.stacked_widget.setCurrentIndex(0)
        self.recommend_button_2.clicked.disconnect()  # 断开当前的连接
        self.recommend_button_2.clicked.connect(self.processMBSS_audio)
        self.recommend_button_4.clicked.connect(self.play_recordingMBSS)

    def show_page2(self):
        self.stacked_widget.setCurrentIndex(1)
        self.recommend_button_2.clicked.disconnect()  # 断开当前的连接
        self.recommend_button_2.clicked.connect(self.processNSSP_audio)
        self.recommend_button_4.clicked.connect(self.play_recordingNSSP)

    def show_page3(self):
        self.stacked_widget.setCurrentIndex(2)
        self.recommend_button_2.clicked.disconnect()  # 断开当前的连接
        self.recommend_button_2.clicked.connect(self.processPSC_audio)
        self.recommend_button_4.clicked.connect(self.play_recordingPSC)

    def slot_max_or_recv(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def start_recording(self):
        if self.is_pause or self.is_switching:
            threading._start_new_thread(self.__recording, ())
            self.is_pause = False
            self.recommend_button_1.setText('结束录音')
        elif not self.is_pause and not self.is_switching:
            self.stop_recording()
            self.is_pause = True
            self.recommend_button_1.setText('录音')

    def __recording(self):
        self._running = True
        self.current_filename = f"recording_{self.recording_counter}.wav"

        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        while (self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

        # def stop(self):
        self._running = False

    def stop_recording(self):
        self._running = False

        self.recordings.append(self.current_filename)

        p = pyaudio.PyAudio()

        wf = wave.open(self.current_filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self._frames))
        wf.close()

        self.recording_counter += 1
        self.current_filename = None

    def showCommentDialog(self):
        dialog = CommentDialog()
        dialog.exec_()

    def play_recording(self):
        # if self.recordings:
        #     filename = self.recordings[-1]
        #     wf = wave.open(filename, 'rb')
        #     stream = self.audio.open(format=self.FORMAT,
        #                             channels=self.CHANNELS,
        #                             rate=self.RATE,
        #                             frames_per_buffer=self.CHUNK,
        #                             output=True)
        #     data = wf.readframes(1024)
        #     while data:
        #         stream.write(data)
        #         data = wf.readframes(1024)
        #     stream.stop_stream()
        #     stream.close()
        #     wf.close()

        filename = self.recordings[-1]
        winsound.PlaySound(filename, winsound.SND_FILENAME)

    def play_recordingNSSP(self):
        winsound.PlaySound('outputNSSP.wav', winsound.SND_FILENAME)

    def play_recordingPSC(self):
        winsound.PlaySound('outputPSC.wav', winsound.SND_FILENAME)

    def play_recordingMBSS(self):
        winsound.PlaySound('outputKamath.wav', winsound.SND_FILENAME)

    # 处理 NSSP 按钮点击事件
    def processNSSP_audio(self):
        filepath = self.recordings[-1]
        # filepath, _ = QFileDialog.getOpenFileName(self, '选择音频文件', '', 'WAV 文件 (*.wav)')
        if filepath:
            try:
                self.NSSP_audio(filepath)
            except Exception as e:
                self.showError(str(e))

    # 处理 PSC 按钮点击事件
    def processPSC_audio(self):
        filepath = self.recordings[-1]
        # filepath, _ = QFileDialog.getOpenFileName(self, '选择音频文件', '', 'WAV 文件 (*.wav)')
        if filepath:
            try:
                self.PSC_audio(filepath)
            except Exception as e:
                self.showError(str(e))

    # 处理 MBSS 按钮点击事件
    def processMBSS_audio(self):
        filepath = self.recordings[-1]
        # filepath, _ = QFileDialog.getOpenFileName(self, '选择音频文件', '', 'WAV 文件 (*.wav)')
        if filepath:
            try:
                self.MBSS_audio(filepath)
            except Exception as e:
                self.showError(str(e))

    # 处理音频文件
    def NSSP_audio(self, filepath):
        # 使用Matlab引擎处理音频
        eng = matlab.engine.start_matlab()
        eng.NSSP_output(filepath)

    def MBSS_audio(self, filepath):
        # 使用Matlab引擎处理音频
        eng = matlab.engine.start_matlab()
        eng.SSMultibandKamath02_output(filepath)

    def PSC_audio(self, filepath):
        # 使用Matlab引擎处理音频
        eng = matlab.engine.start_matlab()
        eng.psc_output(filepath)

    def showError(self, message):
        QMessageBox.critical(self, '错误', message)


class CommentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('添加评论')
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.comment_label = QLabel('请输入您的评论:')
        layout.addWidget(self.comment_label)

        self.comment_textedit = QTextEdit()
        layout.addWidget(self.comment_textedit)

        button_layout = QHBoxLayout()

        self.submit_button = QPushButton('提交')
        self.submit_button.clicked.connect(self.saveComment)
        button_layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton('取消')
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def saveComment(self):
        comment = self.comment_textedit.toPlainText()
        if comment:
            with open('comment.txt', 'a', encoding='utf-8') as f:
                if f.tell() != 0:
                    f.write('\n\n')
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'{current_time}\n{comment}')
            self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()