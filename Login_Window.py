from sys import argv as SYS_argv
from sys import exit as SYS_exit
from re import match as RE_match
from re import search as RE_search
from threading import Thread as THREAD_Thread
from selenium import webdriver as Selenium_Webdriver
from selenium.webdriver.chrome.options import Options as Chrome_Options


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from Login_Window_UI import Ui_Login_Window_UI
from Message_Window import Message_Window



class Login_Window(QMainWindow, Ui_Login_Window_UI):
    '''登录窗口，负责检验用户输入的学号和密码是否正确，仅此而已，main_window中依赖登录的功能仍需再次登录教务处'''
    def __init__(self,main_window):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Set_style()

        self.main_window = main_window  #主窗口的指针

        self.message_window = None
        self.login_thread = None

        self.darging = False
        self.drag_first_point = None
        self.drag_second_point = None

        self.Login_Button.released.connect(self.On_login_button_clicked)
        self.Close_Button.released.connect(self.On_close_button_clicked)

        self.mousePressEvent = self.Mouse_press_event
        self.mouseMoveEvent = self.Mouse_move_event
        self.mouseReleaseEvent = self.Mouse_release_event

    def Set_style(self):
        self.setWindowFlag(Qt.FramelessWindowHint)      #隐藏边框
        self.setAttribute(Qt.WA_TranslucentBackground)  #窗口背景透明，做圆角窗口用的
        self.setWindowOpacity(0.85)                     #窗口透明度

        self.Central_Widget.setStyleSheet('''#Central_Widget{
                                                border-radius: 50px;

                                                border-image: url(:/all_images/res/Login_Window_Background.png);
                                            }''')
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

        #self.Login_Button.setFocusPolicy(Qt.NoFocus)
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

    def On_login_button_clicked(self):
        '''检验学号密码长度对不对，再尝试登录教务处'''
        #已经有个登录线程开起来了，那就不能响应点击登录了
        if self.login_thread != None:
            return

        name = self.Name_LineEdit.text()
        password = self.Password_LineEdit.text()

        if len(name) == 0:
            self.message_window = Message_Window('在？不填学号的吗???',self)
            self.message_window.show()
            self.hide()
            return
        if len(password) == 0:
            self.message_window = Message_Window('在？不填密码的吗???',self)
            self.message_window.show()
            self.hide()
            return
        if not RE_match(r'^.{13}$',name):
            self.message_window = Message_Window('噔   噔   咚\n学号长度不对劲???',self)
            self.message_window.show()
            self.hide()
            return
        if not RE_match(r'^\d{13}$',name):
            self.message_window = Message_Window('噔   噔   咚\n学号只有数字的，对吧',self)
            self.message_window.show()
            self.hide()
            return
        #密码长度4位以上
        if not RE_match(r'^.{4}.*$',password):
            self.message_window = Message_Window('噔   噔   咚\n密码长度不对劲???',self)
            self.message_window.show()
            self.hide()
            return

        #登录这玩意很耗时，为了防止登录时窗口卡着不响应用户，开个多线程
        def Login_logic(self):
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
                    #selenium的Exception是有msg属性的，但非selenium扔出来的Exception就没有，这种就说不准是咋整的报错了
                    massage = e.msg
                    if RE_search(r'您的密码安全级别过低，请进入教务系统按要求修改密码',massage) or RE_search(r'unexpected alert open',massage):
                        self.message_window = Message_Window('噔   噔   咚\n学号或者密码错了？？？',self)
                        self.message_window.show()
                        self.hide()
                        return
                    if RE_search(r'no such element: Unable to locate element: {"method":"xpath","selector":"//*[@class="main-logo"]"}',massage):
                        self.message_window = Message_Window('噔   噔   咚\n学号或者密码错了？？？',self)
                        self.message_window.show()
                        self.hide()
                        return
                    if RE_search(r'unknown error: net::ERR_INTERNET_DISCONNECTED',massage) or RE_search(r'unexpected alert open',massage):
                        self.message_window = Message_Window('噔   噔   咚\n网不好嘛，打不开教务处网站？？？',self)
                        self.message_window.show()
                        self.hide()
                        return
                    else:
                        self.message_window = Message_Window('噔   噔   咚\n发生了咱也搞不懂的错误，咱也不知道是咋整的，建议拜拜图灵老爷子，肯定灵（大概）',self)
                        self.message_window.show()
                        self.hide()
                        return

                except BaseException as e:
                    self.message_window = Message_Window('噔   噔   咚\n发生了咱也搞不懂的错误，咱也不知道是咋整的，建议拜拜图灵老爷子，肯定灵（大概）',self)
                    self.message_window.show()
                    self.hide()
                    return

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
                self.main_window.login_successful_signal.emit(name,password)
                self.message_window = None  #如果有没有关闭的消息窗口，就会被垃圾回收强行清理掉
                self.main_window.show()
                self.close()

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
        self.main_window.login_fail_signal.emit()
        self.message_window = None  #如果有没有关闭的消息窗口，就会被垃圾回收强行清理掉
        self.main_window.show()
        self.close()

    def Mouse_press_event(self,event):
        '''用来实现窗口拖动'''
        if event.pos().y() <= 30:
            self.drag_first_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            self.darging = True

    def Mouse_move_event(self,event):
        '''用来实现窗口拖动'''
        if self.darging:
            self.drag_second_point = event.pos()
            self.move(self.pos() + (self.drag_second_point - self.drag_first_point))

    def Mouse_release_event(self, event):
        '''用来实现窗口拖动'''
        self.setCursor(Qt.ArrowCursor)
        self.darging = False



if __name__ == '__main__':
    app = QApplication(SYS_argv)
    login_Window = Login_Window()
    login_Window.show()
    SYS_exit(app.exec_())