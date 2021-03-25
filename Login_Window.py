from sys import argv as SYS_argv
from sys import exit as SYS_exit
from re import match as RE_match
from re import search as RE_search
from threading import Thread as THREAD_Thread
from selenium import webdriver as Selenium_Webdriver
from selenium.webdriver.chrome.options import Options as Chrome_Options


from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

from Login_Window_UI import Ui_Login_Window_UI
from Message_Window import Message_Window



class Login_Window(QMainWindow, Ui_Login_Window_UI):
    '''登录窗口，检验用户输入的学号和密码是否正确并把登录成功的学号密码和bro对象返回回去，只与data_struct_module通信'''
    show_message_single = pyqtSignal(str)
    message_window_close_single = pyqtSignal()

    def __init__(self,data_struct_module):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Set_style()

        self.data_struct_module = data_struct_module

        self.Login_Button.released.connect(self.On_login_button_clicked)
        self.Close_Button.released.connect(self.On_close_button_clicked)

        self.mousePressEvent = self.On_mouse_press_event
        self.mouseMoveEvent = self.On_mouse_move_event
        self.mouseReleaseEvent = self.On_mouse_release_event
        self.closeEvent = self.On_close_event

        self.show_message_single.connect(self.On_show_message_single)

        self.message_window = None
        self.login_thread = None

        self.darging = False
        self.drag_first_point = None
        self.drag_second_point = None

        self.setWindowOpacity(self.data_struct_module.window_opacity)

        if self.data_struct_module.message_window_bg_custom:
            self.Central_Widget.setStyleSheet('''#Central_Widget{
                                                    border-radius: 50px;

                                                    border-image: url(./local_cache/Custom_Login_Window_Bg.png);
                                                }''')
        else:
            self.Central_Widget.setStyleSheet('''#Central_Widget{
                                                border-radius: 50px;

                                                border-image: url(:/all_images/res/Login_Window_Bg.png);
                                            }''')

    def Set_style(self):
        self.setWindowFlag(Qt.FramelessWindowHint)      #隐藏边框
        self.setAttribute(Qt.WA_TranslucentBackground)  #窗口背景透明，做圆角窗口用的
        self.setWindowOpacity(0.85)                     #窗口透明度

        self.Central_Widget_Layout.setContentsMargins(10,10,10,10)
        self.Central_Widget_Layout.setSpacing(0)

        self.Main_Panel.setStyleSheet('''#Main_Panel{
                                            border-radius: 40px;

                                            background: rgba(0,0,0,0.2);
                                        }''')
        self.Main_Panel_Layout.setContentsMargins(0,0,0,0)
        self.Main_Panel_Layout.setSpacing(0)

        self.Close_Button.setStyleSheet('''#Close_Button{
                                                border: 0px;
                                                padding: 0px;

                                                margin-right: 10px;
                                                margin-top: 10px;

                                                background: rgba(0,0,0,0);

                                                width: 30px;
                                                height: 30px;
                                            }''')
        self.Close_Button_Layout.setContentsMargins(0,0,0,0)
        self.Close_Button_Layout.setSpacing(0)

        #TODO:lineedit光标样式
        self.Login_Panel.setStyleSheet('''#Login_Panel QLabel{
                                            color: rgb(255,255,255);

                                            font-family: 'Microsoft Yahei light';
                                            font-size: 20px;
                                        }
                                        #Login_Panel QLineEdit{
                                            padding-left: 10px;
                                            padding-right: 10px;
                                            border-radius: 20px;

                                            width: 160px;
                                            height: 40px;

                                            color: rgb(255,255,255);
                                            background: rgba(0,0,0,0.2);

                                            font-family: 'Microsoft Yahei light';
                                            font-size: 20px;
                                        }''')
        self.Login_Panel_Layout.setContentsMargins(0,0,0,0)
        self.Login_Panel_Layout.setSpacing(0)
        self.Login_Panel_Layout.setStretch(0,2)
        self.Login_Panel_Layout.setStretch(1,3)
        self.Login_Panel_Layout.setStretch(2,2)

        self.Login_Layout.setContentsMargins(0,0,0,0)
        self.Login_Layout.setSpacing(15)

        self.Name_Layout.setContentsMargins(0,0,0,0)
        self.Name_Layout.setSpacing(10)

        self.Password_Layout.setContentsMargins(0,0,0,0)
        self.Password_Layout.setSpacing(10)

        self.Login_Button.setStyleSheet('''#Login_Button{
                                                border: 0px;
                                                border-radius: 20px;

                                                width: 40px;
                                                height: 40px;

                                                color: rgb(255,255,255);
                                                background: rgba(0,0,0,0.2);

                                                font-family: 'Microsoft Yahei light';
                                                font-size: 20px;

                                                outline: 0px;
                                            }
                                            #Login_Button:hover{
                                                background: rgba(0,0,0,0.3);
                                            }
                                            #Login_Button:pressed{
                                                background: rgba(0,0,0,0.4);
                                            }''')

    def On_show_message_single(self,message):
        '''Login_Window的消息窗口只可能由出错产生，显示一条消息并做一些清理工作'''
        if self.message_window != None:
            self.message_window.close()
            self.message_window = None

        self.message_window = Message_Window(message,self)
        self.message_window.show()

        self.login_thread = None
        self.Login_Button.setStyleSheet('''#Login_Button{
                                                border: 0px;
                                                border-radius: 20px;

                                                width: 40px;
                                                height: 40px;

                                                color: rgb(255,255,255);
                                                background: rgba(0,0,0,0.2);

                                                font-family: 'Microsoft Yahei light';
                                                font-size: 20px;

                                                outline: none
                                            }
                                            #Login_Button:hover{
                                                background: rgba(0,0,0,0.3);
                                            }
                                            #Login_Button:pressed{
                                                background: rgba(0,0,0,0.4);
                                            }''')

    def On_message_window_close_single(self):
        self.message_window = None

    def On_login_button_clicked(self):
        '''检验学号密码长度对不对，再尝试登录教务处'''
        #已经有个登录线程开起来了，那就不能响应点击登录了
        if self.login_thread != None:
            return

        #登录这玩意很耗时，为了防止登录时窗口卡着不响应用户，开个多线程
        def Login_logic(self):
            name = self.Name_LineEdit.text()
            password = self.Password_LineEdit.text()

            if len(name) == 0:
                self.show_message_single.emit('在？不填学号的吗???')
                return
            if len(password) == 0:
                self.show_message_single.emit('在？不填密码的吗???')
                return
            if not RE_match(r'^.{13}$',name):
                self.show_message_single.emit('噔   噔   咚\n学号长度不对劲???')
                return
            if not RE_match(r'^\d{13}$',name):
                self.show_message_single.emit('噔   噔   咚\n学号是只有数字的，对吧')
                return
            #密码长度4位以上
            if not RE_match(r'^.{4}.*$',password):
                self.show_message_single.emit('噔   噔   咚\n密码长度不对劲???')
                return

            try:
                url = 'http://sso.jwc.whut.edu.cn/Certification/toIndex.do'
                chrome_options = Chrome_Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                bro = Selenium_Webdriver.Chrome('./chromedriver', options=chrome_options)
                bro.get(url)
                bro.find_element_by_id('username').send_keys(name)
                bro.find_element_by_id('password').send_keys(password)
                bro.find_element_by_id('submit_id').click()

                #如果学号密码错误，点击登录按钮并不会报错，还要试一下获取网页内容，看能不能获取登录后的教务处网页，不能就是学号密码错了
                bro.find_element_by_xpath('//*[@class="main-logo"]')

            except BaseException as e:
                try:
                    #selenium扔出来的Exception是有msg属性的，但非selenium扔出来的Exception就没有，这种就说不准是咋整的报错了
                    massage = e.msg
                    if RE_search(r'您的密码安全级别过低，请进入教务系统按要求修改密码',massage) or RE_search(r'unexpected alert open',massage):
                        self.show_message_single.emit('噔   噔   咚\n学号或者密码错了???')
                        return
                    elif RE_search(r'no such element: Unable to locate element: {"method":"xpath","selector":"//*[@class="main-logo"]"}',massage):
                        self.show_message_single.emit('噔   噔   咚\n学号或者密码错了???')
                        return
                    elif RE_search(r'unknown error: net::ERR_INTERNET_DISCONNECTED',massage) or RE_search(r'unexpected alert open',massage):
                        self.show_message_single.emit('噔   噔   咚\n网不好嘛，打不开教务处网站???')
                        return
                    else:
                        self.show_message_single.emit('噔   噔   咚\n发生了咱也搞不懂的错误，咱也不知道是咋整的，建议拜拜图灵老爷子，肯定灵（大概）???')
                        return
                #非selenium扔出来Exception
                except BaseException as e:
                    self.show_message_single.emit('噔   噔   咚\n发生了咱也搞不懂的错误，咱也不知道是咋整的，建议拜拜图灵老爷子，肯定灵（大概）???')
                    return

                finally:
                    bro.quit()
                    self.login_thread = None
                    self.Login_Button.setStyleSheet('''#Login_Button{
                                                        border: 0px;
                                                        border-radius: 20px;

                                                        width: 40px;
                                                        height: 40px;

                                                        color: rgb(255,255,255);
                                                        background: rgba(0,0,0,0.2);

                                                        font-family: 'Microsoft Yahei light';
                                                        font-size: 20px;

                                                        outline: none
                                                    }
                                                    #Login_Button:hover{
                                                        background: rgba(0,0,0,0.3);
                                                    }
                                                    #Login_Button:pressed{
                                                        background: rgba(0,0,0,0.4);
                                                    }''')

            else:
                #没报错就是登录成功了
                self.data_struct_module.login_successful_signal.emit(name, password, [bro])
                self.message_window = None  #如果有没有关闭的消息窗口，就会被垃圾回收强行清理掉

        self.login_thread = THREAD_Thread(target = Login_logic,args = (self,))
        self.login_thread.start()
        self.Login_Button.setStyleSheet('''#Login_Button{
                                                border: 0px;
                                                border-radius: 20px;

                                                width: 40px;
                                                height: 40px;

                                                color: rgb(255,255,255);
                                                background: rgba(0,0,0,0.4);

                                                font-family: 'Microsoft Yahei light';
                                                font-size: 20px;

                                                outline: none
                                            }
                                            #Login_Button:hover{
                                                background: rgba(0,0,0,0.4);
                                            }
                                            #Login_Button:pressed{
                                                background: rgba(0,0,0,0.4);
                                            }''')

    def On_close_button_clicked(self):
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
        if self.message_window != None:
            self.message_window.close()
            self.message_window = None
        self.data_struct_module.login_fail_signal.emit()