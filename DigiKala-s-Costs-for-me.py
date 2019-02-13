import requests
from bs4 import BeautifulSoup
from lxml import html
import time
seperator = ".............................................................................."
login_url = 'https://www.digikala.com/users/login/?_back=https%3A//www.digikala.com/'
url = 'https://www.digikala.com/profile/orders/' 
print ("\n*******************************************************\n\
                DigiKala Costs for me\n\
*******************************************************") 


user_pass = [input("Email: "),input("Password: ")]
values = {'login[email_phone]': user_pass[0],
          'login[password]': user_pass[1]}
session_requests = requests.session()

def login_func (login_url,values):
    result = session_requests.get(login_url)
    result = session_requests.post(login_url,data = values,headers = dict(referer=login_url))
    soup = BeautifulSoup(result.content,"html.parser")
    at_counter = 0
    for char in user_pass[0]:
        if char == '@':
            at_counter += 1
    if at_counter != 1:
        print("  Email syntax is incorrect!\n",seperator)
        return 1
    if len(user_pass[1]) < 6:
        print("  Password must be grater than 6 character!\n",seperator)
        return 1
    for div in soup.findAll('div', {'class': 'c-message-light c-message-light--error has-oneline'}):
        if div.text == "اطلاعات کاربری نادرست است":
            print("  Login informations are Invalid!\n",seperator)
            return 1

def get_page_content(url):
    result = session_requests.get(
        url,
        headers = dict(referer = url)
    )

    return result


def change_number(persian_char):
    num_dic = {'۰':'0','۱':'1','۲':'2',\
        '۳':'3','۴':'4','۵':'5','۶':'6',\
        '۷':'7','۸':'8','۹':'9'}
    str_num = str(num_dic[persian_char])
    return (str_num)

def total_costs():
    pages_list = []
    total_pages = 0
    print("\n  Im Trying to login to your account...\n",seperator)
    login_return = login_func(login_url,values)
    if login_return == 1:
        return "Err"

    content = get_page_content(url).content
    print("  Login was successful, Now Im trying to get total number of order pages in your account...")    
    soup = BeautifulSoup(content,"html.parser")
    cost = ''
    int_cost = 0
    all_costs = 0
    counter = 0     
    for a in soup.findAll('a', {'class': 'c-pager__item'}):
        for page_num in a.text:
            page_num = change_number(page_num)
            total_pages = int(page_num)
    print("  Number of total order pages in your account is: ",total_pages,"\n",seperator)
    for i in range (0,total_pages):
        if i == 0:
            next_page = url
            pages_list.append(next_page)
        elif i !=0:
            i += 1
            page_num = '?page=%s' %i
            next_page = url + ('%s' %page_num)
            pages_list.append(next_page)
    for page in pages_list:
        counter += 1
        print ("\n  Calculation on Order Page ",counter," starts. Please wait...")
        content = get_page_content(page).content
        soup = BeautifulSoup(content,"html.parser") 
        for div in soup.findAll('div', {'class': 'c-table-orders__cell c-table-orders__cell--price'}):
            #print(div.text)
            if div.text[0] == '۰':
                continue
            for char in div.text:
                if char == '۰'\
                    or char == '۱'\
                    or char == '۲'\
                    or char == '۳'\
                    or char == '۴'\
                    or char == '۵'\
                    or char == '۶'\
                    or char == '۷'\
                    or char == '۸'\
                    or char == '۹' :
                    char = change_number(char)
                    cost +=char
            if cost != '':
                int_cost = int(cost)
                all_costs += int_cost
            cost = ''
        print ("  Calculation on Page ",counter," is finished! page address is: ",page)
    print(seperator)
    return all_costs

final_result = total_costs()
if final_result != "Err":
    print ("*** Total Costs: ",final_result, " Tooman ***")
else:
    print ("\nPlease try again!")

time.sleep(7)

