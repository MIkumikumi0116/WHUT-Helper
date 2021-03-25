from sys import argv as SYS_argv
from sys import exit as SYS_exit


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from Message_Window_UI import Ui_Message_Window_UI



class Message_Window(QMainWindow, Ui_Message_Window_UI):
    '''显示一条消息'''
    def __init__(self,massage,parent_window):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Set_style()

        self.parent_window = parent_window

        self.Close_Button.released.connect(self.On_close_button_clicked)
        self.Confirm_Button.released.connect(self.On_confirm_button_clicked)

        self.mousePressEvent = self.On_mouse_press_event
        self.mouseMoveEvent = self.On_mouse_move_event
        self.mouseReleaseEvent = self.On_mouse_release_event
        self.closeEvent = self.On_close_event

        self.parent_window.message_window_close_single.connect(self.parent_window.On_message_window_close_single)

        self.darging = False
        self.drag_first_point = None
        self.drag_second_point = None

        self.setWindowOpacity(self.parent_window.data_struct_module.window_opacity)

        if self.parent_window.data_struct_module.message_window_bg_custom:
            self.Central_Widget.setStyleSheet('''#Central_Widget{
                                                    border-radius: 50px;

                                                    border-image: url(./local_cache/Custom_Message_Window_Bg.png);
                                                }''')
        else:
            self.Central_Widget.setStyleSheet('''#Central_Widget{
                                                border-radius: 50px;

                                                border-image: url(:/all_images/res/Message_Window_Bg.png);
                                            }''')

        self.Massage_Label.setText(massage)

    def Set_style(self):
        self.setWindowFlag(Qt.FramelessWindowHint)      #隐藏边框
        self.setAttribute(Qt.WA_TranslucentBackground)  #窗口背景透明，做圆角窗口用的
        self.setWindowOpacity(0.85)                     #窗口透明度

        self.Central_Widget_Layout.setContentsMargins(10,10,10,10)
        self.Central_Widget_Layout.setSpacing(0)

        self.Massage_Panel.setStyleSheet('''#Massage_Panel{
                                            border-radius: 40px;

                                            background: rgba(0,0,0,0.25);
                                        }''')
        self.Massage_Panel_Layout.setContentsMargins(0,0,0,0)
        self.Massage_Panel_Layout.setSpacing(0)
        self.Massage_Panel_Layout.setStretch(0,0)
        self.Massage_Panel_Layout.setStretch(1,1)
        self.Massage_Panel_Layout.setStretch(2,0)

        self.Close_Button.setStyleSheet('''#Close_Button{
                                                padding: 0px;

                                                margin-right: 20px;
                                                margin-top: 20px;

                                                background: rgba(0,0,0,0);

                                                width: 30px;
                                                height: 30px;
                                            }''')

        self.Massage_Label.setStyleSheet('''#Massage_Label{
                                                color: rgb(255,255,255);

                                                font-family: 'Microsoft Yahei light';
                                                font-size: 20px;
                                            }''')
        self.Massage_Label.setWordWrap(True)    #自动换行

        self.Confirm_Button.setStyleSheet('''#Confirm_Button{
                                                border-radius: 20px;
                                                margin-bottom: 10px;

                                                width: 160px;
                                                height: 40px;

                                                color: rgb(255,255,255);
                                                background: rgba(0,0,0,0.2);

                                                font-family: 'Microsoft Yahei light';
                                                font-size: 18px;
                                            }
                                            #Confirm_Button:hover{
                                                background: rgba(0,0,0,0.3);
                                            }
                                            #Confirm_Button:pressed{
                                                background: rgba(0,0,0,0.4);
                                            }''')

    def On_close_button_clicked(self):
        self.close()

    def On_confirm_button_clicked(self):
        self.close()

    def On_mouse_press_event(self,event):
        '''用来实现窗口拖动'''
        if event.pos().y() <= 30:
            self.drag_first_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            self.darging = True

    def On_mouse_move_event(self,event):
        '''用来实现窗口拖动'''
        if self.darging:
            self.drag_second_point = event.pos()
            self.move(self.pos() + (self.drag_second_point - self.drag_first_point))

    def On_mouse_release_event(self, event):
        '''用来实现窗口拖动'''
        self.setCursor(Qt.ArrowCursor)
        self.darging = False

    def On_close_event(self, event):
        self.parent_window.message_window_close_single.emit()