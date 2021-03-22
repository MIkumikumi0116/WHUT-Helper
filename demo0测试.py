# -- coding: utf-8 --
from selenium import webdriver
from lxml import etree
from time import sleep
from selenium.webdriver.chrome.options import Options
# -- coding: utf-8 --
#登录模块(不可见版本)
def login(input_username,input_password):
    url = 'http://sso.jwc.whut.edu.cn/Certification/toIndex.do'
    name = input_username
    password = input_password

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    bro=webdriver.Chrome('./chromedriver',options=chrome_options)
    # bro = webdriver.Chrome('./chromedriver')
    bro.get(url)
    username_input = bro.find_element_by_id('username')
    password_input = bro.find_element_by_id('password')
    username_input.send_keys(name)
    password_input.send_keys(password)

    button = bro.find_element_by_id('submit_id')
    button.click()

    return bro
#登录模块(可见版本)
def login_for_test(input_username,input_password):
    url = 'http://sso.jwc.whut.edu.cn/Certification/toIndex.do'
    name = input_username
    password = input_password

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    bro=webdriver.Chrome('./chromedriver')
    # bro = webdriver.Chrome('./chromedriver')
    bro.get(url)
    username_input = bro.find_element_by_id('username')
    password_input = bro.find_element_by_id('password')
    username_input.send_keys(name)
    password_input.send_keys(password)

    button = bro.find_element_by_id('submit_id')
    button.click()

    return bro
#点击选课模块
def choose_class_module(bro):
    getin = bro.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/ul/li/ul/li[1]/a/h5')
    getin.click()
    sleep(0.2)
    bro.execute_script("document.getElementById('fade').style.display = 'none';")
    bro.execute_script("document.getElementById('MyDiv').style.display = 'none';")
#点击课表
def click_personal_class(bro):
    get_your_message = bro.find_element_by_xpath('//*[@id="sidebar"]/div[2]/div[3]')
    get_your_class = bro.find_element_by_xpath('//*[@id="sidebar"]/div[2]/div[4]/ul/li[2]/div/a')
    get_your_message.click()
    sleep(0.1)
    get_your_class.click()
    sleep(0.2)
    tree = etree.HTML(bro.execute_script("return document.documentElement.outerHTML"))
    return tree
def get_personal_class(tree):
    # sleep(0.2)
    class_list=[]
    class1=[]
    class2=[]
    class3=[]
    class4=[]
    class5=[]
    for i in range(3,10):
        td=tree.xpath('/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody[2]/tr[1]/td['+str(i)+']')[0]
        a_s=td.xpath('./div/a')
        temp_space=[]
        for a in a_s:
            strs = a.xpath('./text()') + a.xpath('./p/text()')
            temp_s=''
            for s in strs:
                temp_s += s.replace('\n', '').replace('\t', '')
            temp_space.append(temp_s)
        class1.append(temp_space)
    for i in range(2,9):
        td = tree.xpath('/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody[2]/tr[2]/td[' + str(i) + ']')[0]
        a_s = td.xpath('./div/a')
        temp_space = []
        for a in a_s:
            strs = a.xpath('./text()') + a.xpath('./p/text()')
            temp_s = ''
            for s in strs:
                temp_s += s.replace('\n', '').replace('\t', '')
            temp_space.append(temp_s)
        class2.append(temp_space)
    for i in range(3,10):
        td = tree.xpath('/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody[2]/tr[3]/td[' + str(i) + ']')[0]
        a_s = td.xpath('./div/a')
        temp_space = []
        for a in a_s:
            strs = a.xpath('./text()') + a.xpath('./p/text()')
            temp_s = ''
            for s in strs:
                temp_s += s.replace('\n', '').replace('\t', '')
            temp_space.append(temp_s)
        class3.append(temp_space)
    for i in range(1,8):
        td = tree.xpath('/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody[2]/tr[4]/td[' + str(i) + ']')[0]
        a_s = td.xpath('./div/a')
        temp_space = []
        for a in a_s:
            strs = a.xpath('./text()') + a.xpath('./p/text()')
            temp_s = ''
            for s in strs:
                temp_s += s.replace('\n', '').replace('\t', '')
            temp_space.append(temp_s)
        class4.append(temp_space)
    for i in range(3,10):
        td = tree.xpath('/html/body/div/div[1]/div[2]/div/div/div[2]/div[2]/div/table/tbody[2]/tr[5]/td[' + str(i) + ']')[0]
        a_s = td.xpath('./div/a')
        temp_space = []
        for a in a_s:
            strs = a.xpath('./text()') + a.xpath('./p/text()')
            temp_s = ''
            for s in strs:
                temp_s += s.replace('\n', '').replace('\t', '')
            temp_space.append(temp_s)
        class5.append(temp_space)
    class_list.append(class1)
    class_list.append(class2)
    class_list.append(class3)
    class_list.append(class4)
    class_list.append(class5)


    return class_list
    ##############################################################################
def get_personal_class_directly(username,userpassword): #直接使用!!!!
    bro = login(username,userpassword)
    tree = etree.HTML(bro.execute_script("return document.documentElement.outerHTML"))
    list_class=get_personal_class(tree)
    sleep(0.5)
    bro.quit()
    return list_class
    ###############################################################################
def get_personal_score(username,userpassword):################可以直接用 返回成绩列表
    bro = login(username, userpassword)
    score_module=bro.find_element_by_xpath('/html/body/div/div[2]/div/div/div[2]/ul/li/ul/li[4]/a')
    score_module.click()
    sleep(0.1)
    score_query_a=bro.find_element_by_xpath('//*[@id="sidebar"]/div[2]/div[2]/ul/li[1]/ul/li[1]/div/a')
    score_query_a.click()
    sleep(0.5)

    score_page_choose=bro.find_element_by_xpath('//*[@id="navTab"]/div[2]/div[2]/div[2]/div[3]/div[1]/div')
    score_page_choose.click()
    score_page_choose_200=bro.find_element_by_xpath('/html/body/ul/li[4]')
    score_page_choose_200.click()
    tree=etree.HTML(bro.execute_script("return document.documentElement.outerHTML"))
    score_lists=tree.xpath('/html/body/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr')
    score_message=[]
    for score_list in score_lists:
        score_list=score_list.xpath('./td/div/text()')
        score_message.append(score_list)
        # temp=[]
        # for column in score_list:
        #     temp.append(column)



    bro.quit()
    return score_message
if __name__ == '__main__':
    print(get_personal_class_directly('XX','XX'))
    # print(get_personal_score('xxxxxxxxx','xxxxxx'))#这两个函数没有先后关系 随便用