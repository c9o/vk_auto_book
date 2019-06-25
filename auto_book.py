#!/usr/bin/env python
# coding: utf-8

# In[60]:


import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# In[61]:


def login():
    dir_path = os.getcwd()
    if 'Darwin' in platform.platform():
        chromedriver = os.path.join(dir_path, "chromedriver_mac64")
    elif 'Linux' in platform.platform():
        chromedriver = os.path.join(dir_path, "chromedriver_linux64")
    else:
        chromedriver = os.path.join(dir_path, "chromedriver.exe")

    browser = webdriver.Chrome(chromedriver)
    browser.get('https://www.vipkid.com.cn/login')
    browser.maximize_window()

    browser.switch_to.frame(0)
    pw_mode = browser.find_element_by_xpath("//span[@class='title right']")
    time.sleep(0.5)
    pw_mode.click()

    mobile = browser.find_element_by_xpath("//input[@type='text' and @class='username']")
    mobile.send_keys('xxxxxxxxxxx')
    time.sleep(0.5)
    password = browser.find_element_by_xpath("//input[@type='password' and @class='password']")
    password.send_keys('xxxxxx')

    button = browser.find_element_by_class_name("login-btn-panel")
    time.sleep(0.5)
    button.click()

    for i in (0,10):
        try:
            temp = browser.find_element_by_class_name("login-btn-panel")
            time.sleep(1)
            break
        except:
            pass

    time.sleep(1)
    try:
        close = browser.find_element_by_class_name("close")
        time.sleep(0.5)
        close.click()

        confirm = browser.find_element_by_class_name("confirm-btn")
        time.sleep(0.5)
        confirm.click()
    except:
        pass

    print("Login Done")
    
    return browser


def goto_booking(browser):
    order_link = browser.find_element_by_class_name("icon-clock")
    if order_link:
        time.sleep(0.5)
        order_link.click()
    else:
        print("Failed")
        exit(0)
        

def goto_teacher(browser, teacher):
    ordered_arry = []
    teacher_search = browser.find_element_by_class_name("teacher-input").find_element_by_xpath("input[@type='text']")
    print(teacher)
    teacher_search.send_keys(teacher)
    time.sleep(0.5)
    teacher_search.send_keys(Keys.ENTER)
    
    
def update_time(time_dic_array, ordered_array):
    # one for weekday and one for weekend
    if not ordered_array: return time_dict_array
    weekday, weekend = False, False
    for item in ordered_array:
        if item['date'] in [1,2,3,4,5]: weekday = True
        else: weekend = True
    ans = []
    for item in time_dic_array:
        if item['date'] in [1,2,3,4,5] and not weekday:
            ans.append(item)
        if item['date'] in [6, 7] and not weekend:
            ans.append(item)
    time_dic_array = ans 
    return time_dic_array


def book_class(ordered=0, ORDER_TIMES=2, time_dic_array=[], ordered_array=[]):
    weekday, weekend = False, False
    for time_dic in time_dic_array:
        #print(time_dic)
        time.sleep(0.5)
        while True:
            try:
                trlist = browser.find_element_by_class_name("schedule-table-body").find_elements_by_xpath("tbody/tr")
                break
            except:
                time.sleep(1)

        #nowhandle = browser.current_window_handle
        if ordered >= ORDER_TIMES:  # 预约次数
            break
        for tr in trlist:
            if ordered >= ORDER_TIMES: #预约次数
                break
            c_time = tr.find_element_by_xpath("th").text
            if c_time == time_dic["time"]:  # 打算预约的时间段
                tdlist = tr.find_elements_by_xpath("td")
                date = 0
                for td in tdlist:
                    if ordered >= ORDER_TIMES:
                        break
                    date = date + 1 #星期几
                    if date in [1,2,3,4,5] and weekday: continue
                    if date in [6,7] and weekend: continue
                    if date == time_dic["date"]:
                        print(u"星期"+str(date) + " " + c_time + ":" + "=="+td.text.strip()+"==")
                        if td.text.strip() == u"可预约":
                            #print(u"星期" + str(date) + " " + c_time + ":" + "==" + td.text.strip() + "==")
                            if date in [1,2,3,4,5]: weekday = True
                            if date in [6,7]: weekend = True
                            book_btn = td.find_element_by_xpath("div")
                            time.sleep(1)
                            book_btn.click()

                            ####CANCEL#####
                            btn_lst = browser.find_elements_by_class_name("cancel-btn")
                            for btn in btn_lst:
                                print(btn.text.strip())
                                if btn.text == u"再想想": ##debug
                                    time.sleep(0.5)
                                    btn.click()
                                    time.sleep(0.5)
                                    ordered = ordered + 1
                                    ordered_array.append(time_dic)
                            '''
                            ####CONFIRM#####
                            btn_lst = browser.find_elements_by_class_name("confirm-btn")
                            for btn in btn_lst:
                                print(btn.text.strip())
                                if btn.text == u"确定预约": ##release
                                    time.sleep(0.5)
                                    btn.click()
                                    time.sleep(0.5)

                            #time.sleep(1)
                            btn_confirm = browser.find_elements_by_class_name("confirm-btn")
                            for btn in btn_confirm:
                                print(btn.text.strip())
                                if btn.text == u"确定": ##release
                                    print("Get it!!!")
                                    time.sleep(0.5)
                                    btn.click()
                                    time.sleep(0.5)
                                    ordered = ordered + 1
                                    ordered_array.append(time_dic)
                                    time_dic_array = update_time(time_dic_array, ordered_array)
                            '''
    return ordered, ordered_array


# In[62]:


## login
browser = login()
goto_booking(browser)


# In[64]:


teacher_array = ["Melissa VUP", "Darren R", "Liz B"]
time_dic_array = [
        {"date": 1, "time": "20:00"},
        {"date": 2, "time": "20:00"},
        {"date": 3, "time": "20:00"},
        {"date": 4, "time": "20:00"},
        {"date": 5, "time": "20:00"},
        {"date": 6, "time": "20:00"},
        {"date": 7, "time": "20:00"},
        #{"date": 1, "time": "20:30"},
        #{"date": 2, "time": "20:30"},
        #{"date": 3, "time": "20:30"},
        #{"date": 4, "time": "20:30"},
        #{"date": 5, "time": "20:30"},
        #{"date": 6, "time": "20:30"},
        #{"date": 7, "time": "20:30"},
        ]
ordered_array = []
ordered = 0

for teacher in teacher_array:
    browser.refresh()
    goto_teacher(browser, teacher)
    time.sleep(2)
    ordered, ordered_array = book_class(ordered=ordered,
                                                        ORDER_TIMES=2,
                                                        time_dic_array=time_dic_array,
                                                        ordered_array=ordered_array)
    print(teacher, ordered, ordered_array)
    time_dic_array = update_time(time_dic_array, ordered_array)


# In[65]:


browser.close()


# In[ ]:


print(ordered_array)

