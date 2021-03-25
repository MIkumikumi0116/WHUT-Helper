from os import path as OS_path
from re import match as RE_match
from os import mkdir as OS_mkdir
from sys import argv as SYS_argv
from sys import exit as SYS_exit
from copy import copy as COPY_copy
from PIL import Image as PIL_image
from re import findall as RE_findall
from lxml import etree as LXML_etree
from time import sleep as TIME_sleep
from json import loads as JSON_loads
from json import dumps as JSON_dumps
from datetime import date as DATE_date
from threading import Thread as THREAD_Thread
from shutil import copyfile as SHUTIL_copyfile
from datetime import datetime as DATE_Datetime
from datetime import timedelta as DATE_timedelta
from selenium import webdriver as Selenium_webdriver
from selenium.webdriver.chrome.options import Options as Chrome_options



from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QBitmap, QPainter, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QHeaderView, QListView, QFileDialog

from Main_Window_UI import Ui_Main_Window_UI
from Login_Window import Login_Window
from Message_Window import Message_Window

FIRST_WEEK_DATE = DATE_date(2021,3,1)


#TODO:通知队列和读取文件出错通知，所有try都要有
class Main_Window(QMainWindow, Ui_Main_Window_UI):
    '''管理窗口控件、所有模块公用的逻辑、主业务逻辑'''
    show_info_single = pyqtSignal(str,bool)     #在Info_Label显示提示信息3秒(bool = False)或持续显示(bool = True)
    show_message_single = pyqtSignal(str)       #用message_window显示一条消息
    message_window_close_single = pyqtSignal()

    def __init__(self):
        QMainWindow.__init__(self)
        #设置窗口样式、设置激励与响应等构造方法中不包含业务逻辑的部分
        self.Main_window_init()
        self.Custom_setting_init()

        self.message_window = None  #为避免垃圾回收把窗口搞没了，留一个指向窗口的指针

        self.info_thread = None

        self.darging = False
        self.drag_first_point = None
        self.drag_second_point = None

        self.schedule_tab.Set_schedule()
        self.data_struct_module.Check_data_same_to_web()

    def Main_window_init(self):
        '''构造方法中不包含业务逻辑的部分，如设置窗口样式、设置激励与响应等'''
        self.setupUi(self)

        self.main_window = self #各个模块访问窗口里的控件或与窗口有关的方法（设置鼠标样式之类的）和全局变量
                                #都统一通过模块各自的main_window指针访问
                                #各模块的main_window指针在构造函数里都指到主窗口去

        self.view_manage = Main_Window_View(self.main_window)
        self.view_manage.Set_main_window_style()

        self.data_struct_module = Data_Struct_Module(self.main_window)

        self.schedule_tab = Schedule_Tab(self.main_window)
        self.judge_tab = Judge_Tab(self.main_window)
        self.score_tab = Score_Tab(self.main_window)
        self.setting_tab = Setting_Tab(self.main_window)

        self.main_window.Schedule_Button.released.connect(self.On_schedule_button_clicked)
        self.main_window.Judge_Button.released.connect(self.On_judge_button_clicked)
        self.main_window.Score_Button.released.connect(self.On_score_button_clicked)
        self.main_window.Setting_Button.released.connect(self.On_setting_button_clicked)
        self.main_window.Close_Button.released.connect(self.On_close_button_clicked)

        self.main_window.mousePressEvent = self.On_mouse_press_event
        self.main_window.mouseMoveEvent = self.On_mouse_move_event
        self.main_window.mouseReleaseEvent = self.On_mouse_release_event
        self.main_window.closeEvent = self.On_close_event

        self.show_info_single.connect(self.On_show_info_single)
        self.show_message_single.connect(self.On_show_message_single)
        self.message_window_close_single.connect(self.On_message_window_close_single)

    def Custom_setting_init(self):
        '''构造函数中设置背景，透明度等等个性化设置'''
        self.main_window.Set_Opacity_Slider.blockSignals(True)
        self.main_window.Set_Opacity_Slider.setValue(int(self.data_struct_module.window_opacity * 100))
        self.main_window.Set_Opacity_Slider.blockSignals(False)
        self.main_window.Set_Opacity_LineEdit.setText(str(self.data_struct_module.window_opacity))
        self.Set_opacity(self.data_struct_module.window_opacity)

        if self.data_struct_module.save_account:
            self.main_window.Save_Account_CheckBox.blockSignals(True)
            self.main_window.Save_Account_CheckBox.setCheckState(2)
            self.main_window.Save_Account_CheckBox.blockSignals(False)
        else:
            self.main_window.Save_Account_CheckBox.blockSignals(True)
            self.main_window.Save_Account_CheckBox.setCheckState(0)
            self.main_window.Save_Account_CheckBox.blockSignals(False)

        if self.data_struct_module.main_window_bg_custom:
            try:
                bg = PIL_image.open('./local_cache/Custom_Main_Window_Bg.png').convert('RGB')  #尝试打开图片看看有没有问题
            except BaseException:
                self.data_struct_module.main_window_bg_custom = False
            else:
                self.main_window.Main_Window_Bg_Img_Label.setPixmap(QPixmap("./local_cache/Custom_Main_Window_Bg.png"))
                self.main_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                    border-radius: 50px;

                                                                    border-image: url(./local_cache/Custom_Main_Window_Bg.png);
                                                                }''')

        if self.data_struct_module.login_window_bg_custom:
            try:
                bg = PIL_image.open('./local_cache/Custom_Login_Window_Bg.png').convert('RGB')
            except BaseException:
                self.data_struct_module.login_window_bg_custom = False
            else:
                self.main_window.Login_Window_Bg_Img_Label.setPixmap(QPixmap("./local_cache/Custom_Login_Window_Bg.png"))
                #登录窗口可能还没有打开，所以不设置登录窗口的样式，消息窗口也是一样

        if self.data_struct_module.message_window_bg_custom:
            try:
                bg = PIL_image.open('./local_cache/Custom_Message_Window_Bg.png').convert('RGB')
            except BaseException:
                self.data_struct_module.message_window_bg_custom = False
            else:
                self.main_window.Message_Window_Bg_Img_Label.setPixmap(QPixmap("./local_cache/Custom_Message_Window_Bg.png"))

    def Set_opacity(self,window_opacity):
        self.data_struct_module.window_opacity = window_opacity
        self.main_window.setWindowOpacity(self.data_struct_module.window_opacity)

        if self.data_struct_module.login_window != None:
            self.data_struct_module.login_window.setWindowOpacity(self.data_struct_module.window_opacity)
            if self.data_struct_module.login_window.message_window != None:
                self.data_struct_module.login_window.message_window.setWindowOpacity(self.data_struct_module.window_opacity)

        #Set_opacity第一次调用是在Custom_setting_init里，message_window还未声明，所以先看看有没有message_window
        if hasattr(self,'message_window') and self.message_window != None:
            self.message_window.setWindowOpacity(self.data_struct_module.window_opacity)

    def On_show_info_single(self, info, whether_last):
        '''在Info_Label显示3秒信息'''
        if whether_last == True:
            self.main_window.Info_label.setText(info)
        else:
            def Set_info(info_label,info):
                info_label.setText(info)
                TIME_sleep(3)
                info_label.setText('')

            self.info_thread = THREAD_Thread(target = Set_info,args = (self.main_window.Info_label,info,))
            self.info_thread.start()

    def On_show_message_single(self,message):
        '''在消息窗口显示一条消息'''
        self.message_window = Message_Window(message,self)
        self.message_window.show()

    def On_message_window_close_single(self):
        self.message_window = None

    def On_schedule_button_clicked(self):
        self.main_window.Main_Tab_Widget.setCurrentIndex(0)
        self.view_manage.Set_tab_button_style_on_click(self.main_window.Schedule_Button)

    def On_judge_button_clicked(self):
        self.main_window.Main_Tab_Widget.setCurrentIndex(1)
        self.view_manage.Set_tab_button_style_on_click(self.main_window.Judge_Button)

    def On_score_button_clicked(self):
        self.main_window.Main_Tab_Widget.setCurrentIndex(2)
        self.view_manage.Set_tab_button_style_on_click(self.main_window.Score_Button)

    def On_setting_button_clicked(self):
        self.main_window.Main_Tab_Widget.setCurrentIndex(3)
        self.view_manage.Set_tab_button_style_on_click(self.main_window.Setting_Button)

    def On_close_button_clicked(self):
        self.close()

    def On_mouse_press_event(self,event):
        '''用来实现窗口拖动'''
        if event.pos().y() <= self.main_window.Main_Tab_Widget.geometry().y():
            self.drag_first_point = event.pos()
            self.main_window.setCursor(Qt.ClosedHandCursor)
            self.darging = True

    def On_mouse_move_event(self,event):
        '''用来实现窗口拖动'''
        if self.darging:
            self.drag_second_point = event.pos()
            self.main_window.move(self.main_window.pos() + (self.drag_second_point - self.drag_first_point))

    def On_mouse_release_event(self, event):
        '''用来实现窗口拖动'''
        self.main_window.setCursor(Qt.ArrowCursor)
        self.darging = False

    def On_close_event(self, event):
        self.data_struct_module.Save_data_struct_to_disk()

        if self.data_struct_module.login_window != None:
            if self.data_struct_module.login_window.message_window != None:
                self.data_struct_module.login_window.message_window.close()
            self.data_struct_module.login_window.close()

        if self.message_window != None:
            self.message_window.close()

        self.main_window.close()

class Main_Window_View:
    '''管理主窗口样式，对控件样式，按深度优先便利控件树的顺序设置各控件样式，下同'''
    def __init__(self,main_window):
        self.main_window = main_window

    def Set_main_window_style(self):
        self.main_window.setWindowFlag(Qt.FramelessWindowHint)      #隐藏边框
        self.main_window.setAttribute(Qt.WA_TranslucentBackground)  #窗口背景透明，做圆角窗口用的

        self.main_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                            border-radius: 50px;

                                                            border-image: url(:/all_images/res/Main_Window_Bg.png);
                                                        }''')
        self.main_window.Central_Widget_Layout.setContentsMargins(10,20,10,10)
        self.main_window.Central_Widget_Layout.setSpacing(0)

        self.main_window.Tab_Select_Widget.setStyleSheet('''#Tab_Select_Widget QPushButton{
                                                                padding: 5px;
                                                                border-top-left-radius: 20px;
                                                                border-top-right-radius: 20px;

                                                                width: 80px;
                                                                height: 20px;

                                                                background: rgba(0,0,0,0.06);
                                                                color: rgb(255,255,255);

                                                                font-family: 'Microsoft Yahei light';
                                                                font-size: 18px;
                                                            }
                                                            #Tab_Select_Widget QPushButton:hover{
                                                                background: rgba(0,0,0,0.08);
                                                            }
                                                            #Tab_Select_Widget QPushButton:pressed{
                                                                background: rgba(0,0,0,0.1);
                                                            }''')
        self.main_window.Tab_Select_Widget_Layout.setContentsMargins(0,0,0,0)
        self.main_window.Tab_Select_Widget_Layout.setSpacing(0)

        #初始时Schedule_Tab被选中，因此设置Schedule_Button的选中样式
        self.main_window.Schedule_Button.setStyleSheet('''#Schedule_Button {
                                                            background: rgba(0,0,0,0.1);
                                                        }''')

        self.main_window.Info_label.setStyleSheet('''#Info_label {
                                                        margin-right:40px;

                                                        color: rgb(255,255,255);

                                                        font-family: 'Microsoft Yahei light';
                                                        font-size: 20px;
                                                    }''')

        self.main_window.Close_Button.setStyleSheet('''#Close_Button{
                                                            padding: 0px;

                                                            border-top-left-radius: 15px;
                                                            border-top-right-radius: 15px;

                                                            background: rgba(0,0,0,0.1);

                                                            width: 30px;
                                                            height: 30px;
                                                        }''')

        self.main_window.Main_Tab_Widget.setStyleSheet('''#Main_Tab_Widget:pane{
                                                            border: 0px;
                                                        }''')#TODO:这样子把间距写死成多少像素很不优雅，高分屏用户会哭的

    def Set_tab_button_style_on_click(self,clicked_button):
        '''Tab栏按钮按下时，设置被按下按钮和其他按钮的样式'''
        stander_style = '''{
                            background: rgba(0,0,0,0.06);
                        }'''
        stander_style_hover = ''':hover{
                                    background: rgba(0,0,0,0.8);
                                }'''
        stander_style_pressed = ''':pressed{
                                        background: rgba(0,0,0,0.1);
                                    }'''

        button_name_list = [(self.main_window.Schedule_Button,'Schedule_Button'),
                            (self.main_window.Judge_Button,'Judge_Button'),
                            (self.main_window.Score_Button,'Score_Button'),
                            (self.main_window.Setting_Button,'Setting_Button')]

        for button,name in button_name_list:
            button.setStyleSheet('''#{name}{stander_style}
                                    #{name}{stander_style_hover}
                                    #{name}{stander_style_pressed}''')

        clicked_button.setStyleSheet(f'#{[i for i in button_name_list if i[0] == clicked_button][0][1]}' + '''{
                                            background: rgba(0,0,0,0.1);
                                        }''')



class Data_Struct_Module(QMainWindow):
    '''管理所有会写入硬盘的数据和登录教务处需要的数据和登录窗口，继承QMainWindow只是为了使用pyqtSignal
       很烦的一点就是因为登录耗时很长，所以要单独开个线程免得主窗口卡着不响应用户，
       而用本地缓存的学号密码登录失败就要开Login_Window重新登录，
       但是天杀的qt在多线程里开窗口会出问题，就不能在新开的线程里开Login_Window，
       所以就改用信号槽来曲线救国，
       然后看着就多余的On_try_login_fail_singal()和On_no_account_in_cache_single()就这么有了,
       很烦'''
    no_account_in_cache_single = pyqtSignal()            #由自己发出，本地缓存中没有学号密码时发出
    try_login_fail_singal = pyqtSignal()                #由自己发出，以本地缓存的学号密码登录失败时发出
    login_successful_signal = pyqtSignal(str,str,list)  #由Login_Window发出，告知main_window用户输入了正确的用户名和密码，并返回登录成功的浏览器指针，放在list里
    login_fail_signal = pyqtSignal()                    #没有登录成功就关闭了Login_Window

    class Course:
        def __init__(self,name,teacher,classroom,day,big_class,start_week,end_week,start_class,end_class,type = '非自定义'):
            self.name = name
            self.teacher = 'None' if teacher == '' else teacher
            self.classroom = classroom
            self.day = day
            self.big_class = big_class
            self.start_week = start_week
            self.end_week = end_week
            self.start_class = start_class
            self.end_class = end_class
            self.type = type

        def __eq__(self,other):
            if JSON_dumps(self.To_dict()) == JSON_dumps(other.To_dict()):
                return True
            else:
                return False

        def To_dict(self):
            return {'name':self.name,'teacher':self.teacher,'classroom':self.classroom,'day':self.day,'big_class':self.big_class,
                    'start_week':self.start_week,'end_week':self.end_week,'start_class':self.start_class,'end_class':self.end_class,'type':self.type}

    def __init__(self,main_window):
        QMainWindow.__init__(self)
        self.main_window = main_window

        self.no_account_in_cache_single.connect(self.On_no_account_in_cache_single)
        self.try_login_fail_singal.connect(self.On_try_login_fail_singal)
        self.login_successful_signal.connect(self.On_login_successful_signal)
        self.login_fail_signal.connect(self.On_login_fail_signal)

        self.login_window = None
        self.background_thread = None   #登录教务处或者显示提示信息几秒后清楚信息用的

        self.bro = None                 #登录用的浏览器
        self.course_list_temp = []      #用于比对主课程列表与教务处是否一致

        #以下是会写到硬盘的数据
        self.name = ''
        self.password =''
        self.window_opacity = 0.85
        self.course_list = []           #主课程列表
        self.save_account = False
        self.main_window_bg_custom = False
        self.login_window_bg_custom = False
        self.message_window_bg_custom = False

        self.Get_data_struct_from_disk()

    def On_no_account_in_cache_single(self):
        self.main_window.show_info_single.emit('请登录账号',True)
        self.login_window = Login_Window(self)
        self.login_window.show()

    def On_try_login_fail_singal(self):
        self.name = ''
        self.password = ''
        self.main_window.show_info_single.emit('本地缓存的账号密码登录失败，请重新登录',True)
        self.login_window = Login_Window(self)
        self.login_window.show()

    def On_login_successful_signal(self,name,password,bro):
        self.name = name
        self.password = password

        self.bro = bro[0]
        self.Get_course_list_from_web()
        self.course_list = COPY_copy(self.course_list_temp)
        self.main_window.schedule_tab.Set_schedule()
        self.Save_data_struct_to_disk()

        self.login_window.close()
        self.login_window = None
        self.main_window.show_info_single.emit('课表已更新至最新',False)

    def On_login_fail_signal(self):
        self.login_window = None
        self.main_window.show_info_single.emit('登录失败，当前的课表可能不是最新的',False)

    def Try_login(self):
        '''尝试登录教务处，成功返回True并保存bro对象供后续get课表、get成绩、get评教等方法使用，失败返回False'''
        try:
            from selenium.webdriver.chrome.options import Options as Chrome_options #搞不懂为啥最前面的import没有生效
            url = 'http://sso.jwc.whut.edu.cn/Certification/toIndex.do'
            Chrome_options = Chrome_options()
            Chrome_options.add_argument('--headless')
            Chrome_options.add_argument('--disable-gpu')
            bro = Selenium_webdriver.Chrome('./chromedriver', options=Chrome_options)
            bro.get(url)
            bro.find_element_by_id('username').send_keys(self.name)
            bro.find_element_by_id('password').send_keys(self.password)
            bro.find_element_by_id('submit_id').click()

            #如果学号密码错误，点击登录按钮并不会报错，还要试一下获取网页内容，看能不能获取登录后的教务处网页，不能就是学号密码错了
            bro.find_element_by_xpath('//*[@class="main-logo"]')
        #这里不用管为什么登不上去，只要登不上返回了False就会开Login_Window让用户重新登录，在那里处理咋登不上去
        except BaseException as e:
            return False
        else:
            self.bro = bro
            return True

    def Get_course_list_from_web(self):
        '''从教务处网站获取课程列表'''
        row_to_columns_dict = {1:3, 2:2, 3:3, 4:1, 5:3}     #表格里每一列的课程起始行数不一样
        #能走到这里来那之前就已经登录了，现在浏览器里的页面里就有课程表了
        tree = LXML_etree.HTML(self.bro.execute_script("return document.documentElement.outerHTML"))
        self.bro.quit()
        self.bro = None

        def Get_a_course_from_a_row(row):
            '''获取一行的课'''
            for col_count in range(row_to_columns_dict[row],row_to_columns_dict[row] + 7 if row != 4 else row_to_columns_dict[row] + 8):
                td = tree.xpath(f'/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody[2]/tr[{row}]/td[{str(col_count)}]')[0]
                anchors = td.xpath('./div/a')

                for a in anchors:
                    course_info = a.xpath('./text()') + a.xpath('./p/text()')
                    course_info = list(map(lambda str:str.replace('\n', '').replace('\t', ''),course_info))

                    while '' in course_info:
                        course_info.remove('')

                    if len(course_info) != 0:
                        Generate_course_object(course_info,col_count - (row_to_columns_dict[row] - 1) if row != 4 else col_count - row_to_columns_dict[row],row)
                        #不知道为啥第四行不一样 #TODO:测试第五行

        def Generate_course_object(course_info,day,big_class):
            '''根据由教务处网页获取的信息生成一个course对象，放入target_course_list'''
            name = course_info[0]
            teacher = '' #TODO:爬老师下来
            classroom = course_info[1].replace('@', '')
            day = day               #course_info是务处课程表中课程的文本，不包含大节和星期几
            big_class = big_class   #这两项信息由课程在课程表中的横纵位置指定，并作为参数传进来

            start_week = RE_findall(r'第0?(\d+)-', course_info[2])[0]
            start_week = eval(start_week)

            end_week = RE_findall(r'-0?(\d+)周', course_info[2])[0]
            end_week = eval(end_week)

            start_class = RE_findall(r'\((\d+)-', course_info[2])[0]
            start_class = eval(start_class)

            end_class = RE_findall(r'-(\d+)节', course_info[2])[0]
            end_class = eval(end_class)

            self.course_list_temp.append(Data_Struct_Module.Course(name,teacher,classroom,day,big_class,start_week,end_week,start_class,end_class))

        for row in range(1,6):
            Get_a_course_from_a_row(row)

    def Get_data_struct_from_disk(self):
        '''从磁盘获取课程列表，成功返回True，失败返回错误类型'''
        if OS_path.isdir('local_cache') and OS_path.isfile('local_cache\local_cache.json'):
            with open('local_cache\local_cache.json', 'r',encoding='utf-8') as file:
                data_struct_json = file.read()
            if len(data_struct_json) == 0:
                return 'File empty'

            try:
                data_struct_dict = JSON_loads(data_struct_json)
                #验证这些字段是否存在和字段有没有问题
                data_struct_dict['name']
                if not data_struct_dict['name'] == '' and not RE_match(r'^\d{13}$',data_struct_dict['name']):
                    raise BaseException

                data_struct_dict['password']
                if not data_struct_dict['password'] == '' and not RE_match(r'^.{4}.*$',data_struct_dict['password']):
                    raise BaseException

                data_struct_dict['save_account']
                if not (data_struct_dict['save_account'] == True or data_struct_dict['save_account'] == False):
                    raise BaseException

                data_struct_dict['main_window_bg_custom']
                if not (data_struct_dict['main_window_bg_custom'] == True or data_struct_dict['main_window_bg_custom'] == False):
                    raise BaseException

                data_struct_dict['login_window_bg_custom']
                if not (data_struct_dict['login_window_bg_custom'] == True or data_struct_dict['login_window_bg_custom'] == False):
                    raise BaseException

                data_struct_dict['message_window_bg_custom']
                if not (data_struct_dict['message_window_bg_custom'] == True or data_struct_dict['message_window_bg_custom'] == False):
                    raise BaseException

                data_struct_dict['course_list']
                course_list = []
                for course_json in data_struct_dict['course_list']:
                    course_dict = JSON_loads(course_json)
                    course_list.append(Data_Struct_Module.Course(course_dict['name'],course_dict['teacher'],course_dict['classroom'],course_dict['day'],course_dict['big_class'],
                                                                 course_dict['start_week'],course_dict['end_week'],course_dict['start_class'],course_dict['end_class']))

            except  BaseException as e:
                #文件有问题，清空文件
                with open('local_cache\local_cache.json', 'w') as file:
                    file.write('')
                return 'Wrong in file'

            else:
                self.name = data_struct_dict['name']
                self.password = data_struct_dict['password']
                self.window_opacity = data_struct_dict['window_opacity']
                self.save_account = data_struct_dict['save_account']
                self.main_window_bg_custom = data_struct_dict['main_window_bg_custom']
                self.login_window_bg_custom = data_struct_dict['login_window_bg_custom']
                self.message_window_bg_custom = data_struct_dict['message_window_bg_custom']
                self.course_list = course_list

                if len(self.course_list) > 0:
                    return True
                else:
                    return 'Empty course list'

        #没找到文件
        else:
            return 'File not found'

    def Save_data_struct_to_disk(self):
        '''保存课程列表到本地'''
        if not OS_path.isdir('local_cache'):
            OS_mkdir('local_cache')

        with open('local_cache\local_cache.json', 'w',encoding='utf-8') as file:
            course_list_json = []
            for course in self.course_list:
                course_info = JSON_dumps(course.To_dict(),ensure_ascii=False)
                course_list_json.append(course_info)

            data_struct_dict = {'name':self.name if self.save_account else '',
                                'password':self.password if self.save_account else '',
                                'window_opacity':self.window_opacity,
                                'save_account':self.save_account,
                                'main_window_bg_custom':self.main_window_bg_custom,
                                'login_window_bg_custom':self.login_window_bg_custom,
                                'message_window_bg_custom':self.message_window_bg_custom,
                                'course_list':course_list_json}
            data_struct_json = JSON_dumps(data_struct_dict,ensure_ascii=False)

            file.write(data_struct_json)

    def Check_data_same_to_web(self):
        '''检查本地数据与教务处是否一致'''
        #开多线程全是因为有个Try_login，反正涉及到登录就很耗时，就开个多线程防止主窗口半天不响应用户
        def Check_data_logic(self):
            self.main_window.show_info_single.emit('正在从教务处获取最新课表',True)

            #本地没有保存账号密码，要重新登录
            if self.name == '' or self.password == '':
                self.no_account_in_cache_single.emit()
                return

            #保存了账号密码但是登录失败，要重新登录
            if not self.Try_login():
                self.try_login_fail_singal.emit()
                return

            #登录成功的浏览器对象已经保存在self.bro里了，可以直接Get_course_list_from_web()
            self.Get_course_list_from_web()

            course_data_same_flag = True
            if len(self.course_list) == len(self.course_list_temp):
                for i in range(len(self.course_list)):
                    if self.course_list[i] != self.course_list_temp[i]:
                        course_data_same_flag = False
                        break
            else:
                course_data_same_flag = False

            if course_data_same_flag == True:
                self.main_window.show_info_single.emit('当前课表是最新的',False)
            else:
                self.course_list = COPY_copy(self.course_list_temp)
                self.main_window.schedule_tab.Set_schedule()
                self.Save_data_struct_to_disk()
                self.main_window.show_info_single.emit('课表已更新至最新',False)

        self.background_thread = THREAD_Thread(target = Check_data_logic,args = (self,))
        self.background_thread.start()



class Schedule_Tab:
    '''管理课表Tab的逻辑'''
    def __init__(self,main_window):
        self.main_window = main_window
        self.data_struct_module = self.main_window.data_struct_module

        self.view_manage = Schedule_Tab_View(self.main_window)
        self.view_manage.Set_schedule_tab_style()

        self.first_week_date = COPY_copy(FIRST_WEEK_DATE)
        self.current_week = (DATE_Datetime.now().date() - self.first_week_date).days // 7 + 1
        self.main_window.Week_Select_ComboBox.setCurrentIndex(self.current_week - 1)

        self.main_window.Week_Select_ComboBox.currentIndexChanged.connect(self.On_week_select_comboBox_changed)

    def Set_schedule(self):
        '''设置课程表'''
        #设置表头，很难用qss精确控制qTableWidget的每一个单元格的样式，所以直接用qLabel画单元格，给qLabel写样式
        weekday_dict = {1:'星期一', 2:'星期二', 3:'星期三', 4:'星期四', 5:'星期五', 6:'星期六', 7:'星期天'}
        for weekday_count in range (1,8):
            date = self.first_week_date + DATE_timedelta(7 * (self.current_week - 1) + (weekday_count - 1))
            weekday_label = QLabel(f'{weekday_dict[weekday_count]}\n{date.year}-{date.month}-{date.day}')
            self.view_manage.Set_weekday_label_style(weekday_label,weekday_count)
            self.main_window.Schedule_Table_Widget.setCellWidget(0,weekday_count - 1,weekday_label)

        #设置表格
        course_count = 0
        blank_count = 0
        #逐个设置表格
        for x in range(1,8):
            for y in range(1,6):
                course_find_flag = False

                for course in self.data_struct_module.course_list:
                    #若这个课时有本周的课
                    if course.day == x and course.big_class == y and (course.start_week <= self.current_week and self.current_week <= course.end_week):
                        course_label = QLabel(f'{course.name}\n{course.start_week}-{course.end_week}周 {course.start_class}-{course.end_class}节\n{course.classroom})')
                        self.view_manage.Set_course_label_style(course_label,course,course_count,self.current_week,x,y)
                        self.main_window.Schedule_Table_Widget.setCellWidget(y,x - 1,course_label)  #因表头占据了表格的第0行，所以y需加1

                        course_count += 1

                        course_find_flag = True
                        break

                #若没有本周的课，但有其他周的课,选上课周离当前周最近的
                if not course_find_flag:
                    course_list_temp = []

                    for course in self.data_struct_module.course_list:
                        if course.day == x and course.big_class == y:
                            course_list_temp.append(course)

                    if len(course_list_temp) > 0:
                        #上课时间与当前周之差
                        course_list_week_difference = list(map(lambda course:course.start_week - self.current_week if course.start_week > self.current_week else self.current_week - course.end_week, course_list_temp))

                        course = course_list_temp[course_list_week_difference.index(min(course_list_week_difference))]
                        course_label = QLabel(f'{course.name}\n{course.start_week}-{course.end_week}周{course.start_class}-{course.end_class}节\n{course.classroom})')
                        self.view_manage.Set_course_label_style(course_label,course,course_count,self.current_week,x,y)
                        self.main_window.Schedule_Table_Widget.setCellWidget(y,x - 1,course_label)  #因表头占据了表格的第0行，所以y需加1

                        course_count += 1

                        course_find_flag = True

                #若这个课时没有课
                if not course_find_flag:
                    blank_label = QLabel('')
                    self.view_manage.Set_blank_label_style(blank_label,blank_count,x,y)
                    self.main_window.Schedule_Table_Widget.setCellWidget(y,x - 1,blank_label)

                    blank_count += 1

    def On_week_select_comboBox_changed(self,index):
        self.current_week = index + 1
        self.Set_schedule()

class Schedule_Tab_View:
    '''管理课表Tab的样式'''
    def __init__(self,main_window):
        self.main_window = main_window
        self.Color_List = [[57,197,187],[255,165,0],[255,226,17],[255,192,203],[216,0,0],[0,0,255],[102,204,255]]   #课程表一周各天的颜色

    def Set_schedule_tab_style(self):
        self.main_window.Schedule_Tab.setStyleSheet('''#Schedule_Tab{
                                                        border: 0px;
                                                        border-radius: 40px;
                                                        border-top-left-radius: 0px;
                                                        border-top-right-radius: 0px;

                                                        background: rgba(0,0,0,0.1);
                                                    }''')
        self.main_window.Schedule_Tab_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Schedule_Tab_Layout.setSpacing(10)

        self.main_window.Week_Select_Layout.setContentsMargins(0,0,0,0)
        self.main_window.Week_Select_Layout.setSpacing(0)

        self.main_window.Week_Select_ComboBox.setStyleSheet('''#Week_Select_ComboBox{
                                                                padding-left: 20px;
                                                                border-radius: 20px;

                                                                width: 72px;
                                                                height: 40px;

                                                                color: rgb(255,255,255);
                                                                background: rgba(0,0,0,0.3);

                                                                font-family: 'Microsoft Yahei light';
                                                            }
                                                            #Week_Select_ComboBox::drop-down{
                                                                border-left-width: 1px;
                                                                border-right-width: 1px;
                                                                margin-right: 10px;

                                                                width: 20px;
                                                            }
                                                            #Week_Select_ComboBox::down-arrow{
                                                                image: url(:/all_images/res/Down_Arrow.png)
                                                            }
                                                            #Week_Select_ComboBox QAbstractItemView {
                                                                margin-top: 1px;
                                                            }''')

        #设置选周下拉框的样式
        QApplication.setEffectEnabled(Qt.UI_AnimateCombo, False)    #禁用弹出动画
        self.main_window.Week_Select_ComboBox.view().parentWidget().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)   #下拉框背景透明
        self.main_window.Week_Select_ComboBox.view().parentWidget().setAttribute(Qt.WA_TranslucentBackground)                                       #下拉框背景透明

        for i in range(self.main_window.Week_Select_ComboBox.count()):
            self.main_window.Week_Select_ComboBox.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)  #下拉文本居中

        comboBox_view = QListView()
        comboBox_view.setObjectName('Week_Select_ComboBox_View')
        comboBox_view.setStyleSheet('''#Week_Select_ComboBox_View{
                                            padding: 5px;
                                            border: 0px;
                                            border-radius: 20px;

                                            background: rgba(0,0,0,0.4);

                                            outline: 0px;
                                        }
                                        #Week_Select_ComboBox_View::item{
                                            border: 0px;
                                            border-radius: 15px;

                                            height: 30px;

                                            color: rgb(200,200,200);

                                            font-family: 'Microsoft Yahei light';
                                        }
                                        #Week_Select_ComboBox_View::item:hover{
                                            background: rgba(135,206,235,0.3);
                                        }
                                        #Week_Select_ComboBox_View::item:selected{
                                            background: rgba(135,206,235,0.3);
                                        }''')
        comboBox_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)     #隐藏滚动条

        self.main_window.Week_Select_ComboBox.setView(comboBox_view)


        self.main_window.Schedule_Table_Containers.setStyleSheet('''#Schedule_Table_Containers{
                                                                        border: 0px;
                                                                        border-radius: 30px;

                                                                        background: rgba(0,0,0,0.15);
                                                                    }''')
        self.main_window.Schedule_Table_Containers_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Schedule_Table_Containers_Layout.setSpacing(0)

        self.main_window.Schedule_Table_Mask.setStyleSheet('''#Schedule_Table_Mask{
                                                                    border: 0px;
                                                                    border-radius: 20px;

                                                                    background: rgba(0,0,0,0);
                                                                }''')
        self.main_window.Schedule_Table_Mask_Layout.setContentsMargins(0,0,0,0)
        self.main_window.Schedule_Table_Mask_Layout.setSpacing(0)

        #设置表格的圆角遮罩
        self.main_window.showNormal()   #强制刷新窗口以应用样式，从而获得受样式调整后的控件尺寸
        mask = QBitmap(self.main_window.Schedule_Table_Mask.width(),self.main_window.Schedule_Table_Mask.height())
        mask.fill()
        #画个和表格一样大的圆角矩形做遮罩
        mask_painter = QPainter(mask)
        mask_painter.setBrush(Qt.black)
        mask_painter.setPen(Qt.NoPen)
        mask_painter.setRenderHint(QPainter.Antialiasing)
        mask_painter.drawRoundedRect(mask.rect(),20,20)
        mask_painter.end()
        self.main_window.Schedule_Table_Mask.setMask(mask)

        self.main_window.Schedule_Table_Widget.setStyleSheet('''#Schedule_Table_Widget{
                                                                    border: 0px;

                                                                    background: rgba(0,0,0,0);
                                                                }''')
        self.main_window.Schedule_Table_Widget.horizontalHeader().setVisible(False)
        self.main_window.Schedule_Table_Widget.verticalHeader().setVisible(False)
        self.main_window.Schedule_Table_Widget.verticalHeader().setDefaultSectionSize(193)
        self.main_window.Schedule_Table_Widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #自动伸展表格各列
        self.main_window.Schedule_Table_Widget.setRowHeight(0,76)   #调整第一行行高 #TODO:不要把高度写死成px
        self.main_window.Schedule_Table_Widget.setShowGrid(False)

    def Set_weekday_label_style(self,weekday_label,x):
        weekday_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  #文字居中
        weekday_label.setObjectName(f'weekday_label_{x}')
        weekday_label.setStyleSheet( f'#weekday_label_{x}' + '''{
                                        border: 0px;
                                        border-radius: 20px;
                                        margin: 5px;
                                        margin-top: 0px;''' +
                                        f'{"margin-left: 0px;" if x == 1 else ""}' +
                                        f'{"margin-right: 0px;" if x == 7 else ""}' + '''

                                        min-height: 60px;

                                        background: rgba(0,0,0,0.3);
                                        color: rgb(255,255,255);

                                        font-family: 'Microsoft Yahei light';
                                    }''')

    def Set_course_label_style(self,course_label,course,count,current_week,x,y):
        course_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  #文字居中
        course_label.setWordWrap(True)  #自动换行
        course_label.setObjectName(f'course_label_{count}')
        color = self.Color_List[course.day - 1] + [0.4] \
            if course.start_week <= current_week and current_week <= course.end_week \
            else [0,0,0,0.2]
        course_label.setStyleSheet( f'#course_label_{count}' + '''{
                                        border: 0px;
                                        border-radius: 20px;
                                        margin: 5px;''' +
                                        f'{"margin-left: 0px;" if x == 1 else ""}' +
                                        f'{"margin-right: 0px;" if x == 7 else ""}' +
                                        f'{"margin-bottom: 0px;" if y == 5 else ""}' +
                                        f'{"margin-bottom: 71px;" if course.end_class - course.start_class == 1 else " "}' +

                                        f'background: rgba({color[0]},{color[1]},{color[2]},{color[3]}); ' + '''
                                        color: rgb(255,255,255);

                                        font-family: 'Microsoft Yahei light';
                                    }''')

    def Set_blank_label_style(self,blank_label,count,x,y):
        blank_label.setObjectName(f'blank_label_{count}')
        blank_label.setStyleSheet(f'#blank_label_{count}' + '''{
                                        border: 0px;
                                        border-radius: 20px;
                                        margin: 5px;''' +
                                        f'{"margin-left: 0px;" if x == 1 else ""}' +
                                        f'{"margin-right: 0px;" if x == 7 else ""}' +
                                        f'{"margin-bottom: 0px;" if y == 5 else ""}' + '''

                                        background: rgba(0,0,0,0.2);
                                    }''')



class Judge_Tab:
    '''管理评教Tab的逻辑'''
    def __init__(self,main_window):
        self.main_window = main_window
        self.data_struct_module = self.main_window.data_struct_module

        self.view_manage = Judge_Tab_View(self.main_window)
        self.view_manage.Set_judge_tab_style()

class Judge_Tab_View:
    '''管理评教Tab的样式'''
    def __init__(self,main_window):
        self.main_window = main_window

    def Set_judge_tab_style(self):
        self.main_window.Judge_Tab.setStyleSheet('''#Judge_Tab{
                                                        border: 0px;
                                                        border-radius: 40px;
                                                        border-top-left-radius: 0px;
                                                        border-top-right-radius: 0px;

                                                        background: rgba(0,0,0,0.1);
                                                    }''')
        self.main_window.Judge_Tab_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Judge_Tab_Layout.setSpacing(10)

        self.main_window.Judge_Tab_Label.setStyleSheet('''#Judge_Tab_Label{
                                                                color: rgb(255,255,255);

                                                                font-family: 'Microsoft Yahei light';
                                                                font-size: 40px;
                                                            }''')
        self.main_window.Judge_Tab_Label.setAlignment(Qt.AlignCenter)



class Score_Tab:
    '''管理成绩Tab的逻辑'''
    def __init__(self,main_window):
        self.main_window = main_window
        self.data_struct_module = self.main_window.data_struct_module

        self.view_manage = Score_Tab_View(self.main_window)
        self.view_manage.Set_score_tab_style()

class Score_Tab_View:
    '''管理成绩Tab的样式'''
    def __init__(self,main_window):
        self.main_window = main_window

    def Set_score_tab_style(self):
        self.main_window.Score_Tab.setStyleSheet('''#Score_Tab{
                                                        border: 0px;
                                                        border-radius: 40px;
                                                        border-top-left-radius: 0px;
                                                        border-top-right-radius: 0px;

                                                        background: rgba(0,0,0,0.1);
                                                    }''')
        self.main_window.Score_Tab_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Score_Tab_Layout.setSpacing(10)

        self.main_window.Score_Tab_Label.setStyleSheet('''#Score_Tab_Label{
                                                                color: rgb(255,255,255);

                                                                font-family: 'Microsoft Yahei light';
                                                                font-size: 40px;
                                                            }''')
        self.main_window.Score_Tab_Label.setAlignment(Qt.AlignCenter)



class Setting_Tab:
    '''管理设置Tab的逻辑'''
    def __init__(self,main_window):
        self.main_window = main_window
        self.data_struct_module = self.main_window.data_struct_module

        self.view_manage = Setting_Tab_View(self.main_window)
        self.view_manage.Set_setting_tab_style()

        self.main_window.Set_Opacity_LineEdit.textChanged.connect(self.On_set_opacity_lineedit_textchanged)
        self.main_window.Set_Opacity_Slider.valueChanged.connect(self.On_set_opacity_slider_value_changed)
        self.main_window.Save_Account_CheckBox.stateChanged.connect(self.On_save_account_checkBox_changed)
        self.main_window.Main_Window_Bg_Custom_Button.released.connect(self.On_main_window_bg_custom_button)
        self.main_window.Main_Window_Bg_Reset_Button.released.connect(self.On_main_window_bg_reset_button)
        self.main_window.Login_Window_Bg_Custom_Button.released.connect(self.On_login_window_bg_custom_button)
        self.main_window.Login_Window_Bg_Reset_Button.released.connect(self.On_login_window_bg_reset_button)
        self.main_window.Message_Window_Bg_Custom_Button.released.connect(self.On_message_window_bg_custom_button)
        self.main_window.Message_Window_Bg_Reset_Button.released.connect(self.On_message_window_bg_reset_button)

    def On_save_account_checkBox_changed(self,event):
        #取消
        if event == 0:
            self.data_struct_module.save_account = False
        #选中
        else:
            self.main_window.show_message_single.emit(r'学号和密码都以明码保存在local_cache\local_cache.json里，请注意数据安全')
            self.data_struct_module.save_account = True

    def On_set_opacity_lineedit_textchanged(self):
        text = self.main_window.Set_Opacity_LineEdit.text()

        if RE_match(r'^[0|1]\.\d{0,2}$',text):
            if eval(text) > 1:
                text = '1.00'
            self.main_window.Set_Opacity_Slider.blockSignals(True)
            self.main_window.Set_Opacity_Slider.setValue(int(eval(text) * 100))
            self.main_window.Set_Opacity_Slider.blockSignals(False)
            self.main_window.Set_Opacity_LineEdit.setText(text)     #应对text>1的情况
            self.main_window.Set_opacity(eval(text))
        else:
            self.main_window.Set_Opacity_LineEdit.setText(str(self.data_struct_module.window_opacity))

    def On_set_opacity_slider_value_changed(self):
        #set了text就会引起On_set_opacity_lineedit_textchanged响应，就不用在slider里Set_opacity了
        self.main_window.Set_Opacity_LineEdit.setText(str(self.main_window.Set_Opacity_Slider.value() / 100))

    def On_main_window_bg_custom_button(self):
        bg_path = QFileDialog.getOpenFileName(self.main_window,'选择一个背景',filter = '图像文件(*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tga *.JPG *.JPEG *.PNG *.WEBP *.BMP *.TIF *.TGA)')
        if bg_path[0] != '':
            try:
                bg = PIL_image.open(bg_path[0])    #转成png格式来统一文件名（文件名都写死在代码里了，所以后缀名也要和代码一致），顺便看看图片有没有问题
                bg.save('local_cache\Custom_Main_Window_Bg.png')
            except:
                self.main_window.show_message_single.emit(r'这个图片有问题嘛，打不开')
            else:
                self.data_struct_module.main_window_bg_custom = True
                self.main_window.Main_Window_Bg_Img_Label.setPixmap(QPixmap("./local_cache/Custom_Main_Window_Bg.png"))
                self.main_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                    border-radius: 50px;

                                                                    border-image: url(./local_cache/Custom_Main_Window_Bg.png);
                                                                }''')

    def On_main_window_bg_reset_button(self):
        self.data_struct_module.main_window_bg_custom = False
        self.main_window.Main_Window_Bg_Img_Label.setPixmap(QPixmap(":/all_images/res/Main_Window_Bg.png"))
        self.main_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                            border-radius: 50px;

                                                            border-image: url(:/all_images/res/Main_Window_Bg.png);
                                                        }''')

    def On_login_window_bg_custom_button(self):
        bg_path = QFileDialog.getOpenFileName(self.main_window,'选择一个背景',filter = '图像文件(*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tga *.JPG *.JPEG *.PNG *.WEBP *.BMP *.TIF *.TGA)')
        if bg_path[0] != '':
            try:
                bg = PIL_image.open(bg_path[0])
                bg.save('local_cache\Custom_Login_Window_Bg.png')
            except:
                self.main_window.show_message_single.emit(r'这个图片有问题嘛，打不开')
            else:
                self.data_struct_module.login_window_bg_custom = True
                self.main_window.Login_Window_Bg_Img_Label.setPixmap(QPixmap("./local_cache/Custom_Login_Window_Bg.png"))
                if self.data_struct_module.login_window != None:
                    self.data_struct_module.login_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                                            border-radius: 50px;

                                                                                            border-image: url(./local_cache/Custom_Login_Window_Bg.png);
                                                                                        }''')

    def On_login_window_bg_reset_button(self):
        self.data_struct_module.login_window_bg_custom = False
        self.main_window.Login_Window_Bg_Img_Label.setPixmap(QPixmap(":/all_images/res/Login_Window_Bg.png"))
        if self.data_struct_module.login_window != None:
            self.data_struct_module.login_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                                    border-radius: 50px;

                                                                                    border-image: url(:/all_images/res/Login_Window_Bg.png);
                                                                                }''')

    def On_message_window_bg_custom_button(self):
        bg_path = QFileDialog.getOpenFileName(self.main_window,'选择一个背景',filter = '图像文件(*.jpg *.jpeg *.png *.webp *.bmp *.tif *.tga *.JPG *.JPEG *.PNG *.WEBP *.BMP *.TIF *.TGA)')
        if bg_path[0] != '':
            try:
                bg = PIL_image.open(bg_path[0])
                bg.save('local_cache\Custom_Message_Window_Bg.png')
            except:
                self.main_window.show_message_single.emit(r'这个图片有问题嘛，打不开')
            else:
                self.data_struct_module.message_window_bg_custom = True
                self.main_window.Message_Window_Bg_Img_Label.setPixmap(QPixmap("local_cache\Custom_Message_Window_Bg.png"))
                if self.main_window.message_window != None:
                    self.main_window.message_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                                    border-radius: 50px;

                                                                                    border-image: url(./local_cache/Custom_Message_Window_Bg.png);
                                                                                }''')
                if self.data_struct_module.login_window != None and self.data_struct_module.login_window.message_window != None:
                    self.data_struct_module.login_window.message_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                                                            border-radius: 50px;

                                                                                                            border-image: url(./local_cache/Custom_Message_Window_Bg.png);
                                                                                                        }''')

    def On_message_window_bg_reset_button(self):
        self.data_struct_module.message_window_bg_custom = False
        self.main_window.Message_Window_Bg_Img_Label.setPixmap(QPixmap(":/all_images/res/Message_Window_Bg.png"))
        if self.main_window.message_window != None:
            self.main_window.message_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                            border-radius: 50px;

                                                                            border-image: url(:/all_images/res/Message_Window_Bg.png);
                                                                        }''')
        if self.data_struct_module.login_window != None and self.data_struct_module.login_window.message_window != None:
            self.data_struct_module.login_window.message_window.Central_Widget.setStyleSheet('''#Central_Widget{
                                                                                                    border-radius: 50px;

                                                                                                    border-image: url(:/all_images/res/Message_Window_Bg.png);
                                                                                                }''')

class Setting_Tab_View:
    '''管理设置Tab的样式'''
    def __init__(self,main_window):
        self.main_window = main_window

    def Set_setting_tab_style(self):
        #设置tab里所有同类型控件应该有统一的样式表，所以都放在Setting_Tab的样式表里，然后子控件继承
        self.main_window.Setting_Tab.setStyleSheet('''#Setting_Tab{
                                                        border: 0px;
                                                        border-radius: 40px;
                                                        border-top-left-radius: 0px;
                                                        border-top-right-radius: 0px;

                                                        background: rgba(0,0,0,0.1);
                                                    }

                                                    #Setting_Tab QLineEdit{
                                                        padding-left: 10px;
                                                        padding-right: 10px;
                                                        border-radius: 15px;

                                                        width: 40px;
                                                        height: 30px;

                                                        color: rgb(255,255,255);
                                                        background: rgba(0,0,0,0.3);

                                                        font-family: 'Microsoft Yahei light';
                                                        font-size: 18px;
                                                    }

                                                    #Setting_Tab QLabel{
                                                        color: rgb(255,255,255);

                                                        font-family: 'Microsoft Yahei light';
                                                        font-size: 18px;
                                                    }

                                                    #Setting_Tab QPushButton{
                                                        border: 0px;
                                                        border-radius: 20px;

                                                        width: 150px;
                                                        height: 40px;

                                                        color: rgb(255,255,255);
                                                        background: rgba(0,0,0,0.3);

                                                        font-family: 'Microsoft Yahei light';
                                                        font-size: 18px;
                                                    }
                                                    #Setting_Tab QPushButton:hover{
                                                        background: rgba(0,0,0,0.4);
                                                    }
                                                    #Setting_Tab QPushButton:pressed{
                                                        background: rgba(0,0,0,0.5);
                                                    }

                                                    #Setting_Tab QSlider::handle:horizontal{
                                                        border: 3px;
                                                        border-style: solid;
                                                        border-radius: 12px;
                                                        border-color: rgb(255,255,255);
                                                        margin: -11px 0px -11px 0px;

                                                        width: 18px;
                                                        height: 20px;

                                                        background: rgb(56, 131, 209);
                                                    }
                                                    #Setting_Tab QSlider::groove:horizontal{
                                                        height: 2px;
                                                        background : rgb(219,219,219);
                                                    }
                                                    #Setting_Tab QSlider::add-page:horizontal{
                                                        background-color: rgb(219,219,219);
                                                    }
                                                    #Setting_Tab QSlider::sub-page:horizontal{
                                                        background-color: rgb(26, 101, 179);
                                                    }

                                                    #Setting_Tab QCheckBox::indicator {
                                                        width: 20px;
                                                        height: 20px;
                                                    }
                                                    #Setting_Tab QCheckBox::indicator:checked {
                                                        image: url(:/all_images/res/CheckBox_Checked.png);
                                                    }
                                                    #Setting_Tab QCheckBox::indicator:unchecked {
                                                        image: url(:/all_images/res/CheckBox_Unchecked.png);
                                                    }''')
        self.main_window.Setting_Tab_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Setting_Tab_Layout.setSpacing(10)

        self.main_window.Setting_Left_Widget.setStyleSheet('''#Setting_Left_Widget{
                                                                border: 0px;
                                                                border-radius: 30px;

                                                                background: rgba(0,0,0,0.1);
                                                            }''')
        self.main_window.Setting_Left_Widget_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Setting_Left_Widget_Layout.setSpacing(10)

        self.main_window.Set_Opacity_Layout.setContentsMargins(0,0,0,0)
        self.main_window.Set_Opacity_Layout.setSpacing(20)
        self.main_window.Set_Opacity_Layout.setStretch(3,1)

        self.main_window.Save_Account_Layout.setContentsMargins(0,0,0,0)
        self.main_window.Save_Account_Layout.setSpacing(20)
        self.main_window.Save_Account_Layout.setStretch(2,1)

        self.main_window.Setting_Right_Widget.setStyleSheet('''#Setting_Right_Widget{
                                                                border: 0px;
                                                                border-radius: 30px;

                                                                background: rgba(0,0,0,0.1);
                                                            }''')
        self.main_window.Setting_Right_Widget_Layout.setContentsMargins(10,10,10,10)
        self.main_window.Setting_Right_Widget_Layout.setSpacing(10)

        self.main_window.Illustrator_ID_Layout.setContentsMargins(0,0,0,10)
        self.main_window.Background_Setting_Layout.setSpacing(20)

        self.main_window.Main_Window_Bg_ID_Label.setText('''<style> a {text-decoration: none; color: white} </style>
                                                            <a href = \"https://www.pixiv.net/artworks/49240323\">
                                                            <div><p>miku千里走单骑</p><p>来自千夜QYS3</p><p>作品id:</p><p>49240323</p>
                                                            </div></a>''')
        self.main_window.Main_Window_Bg_ID_Label.setOpenExternalLinks(True)
        self.main_window.Login_Window_Bg_ID_Label.setText('''<style> a {text-decoration: none; color: white} </style>
                                                            <a href = \"https://www.pixiv.net/artworks/84026087\">
                                                            <div><p>韶华</p><p>来自画师ASK</p><p>作品id:</p><p>84026087</p>
                                                            </div></a>''')
        self.main_window.Login_Window_Bg_ID_Label.setOpenExternalLinks(True)
        self.main_window.Message_Window_Bg_ID_Label.setText('''<style> a {text-decoration: none; color: white} </style>
                                                                <a href = \"https://www.pixiv.net/artworks/79257667\">
                                                                <div><p>ヌードル·ストッパー</p><p>来自画师DangMyo</p><p>作品id:</p><p>79257667</p>
                                                                </div></a>''')
        self.main_window.Message_Window_Bg_ID_Label.setOpenExternalLinks(True)



if __name__ == '__main__':
    app = QApplication(SYS_argv)
    main_window = Main_Window()
    main_window.show()
    SYS_exit(app.exec_())