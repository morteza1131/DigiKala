import requests
from bs4 import BeautifulSoup
from lxml import html
login_url = 'https://www.digikala.com/users/login/?_back=https%3A//www.digikala.com/'
url = 'https://www.digikala.com/profile/orders/' 
print("DigiKala's Costs for me\n")
user_pass = [input("UserName/Phone: "),input("Password: ")] 
values = {'login[email_phone]': user_pass[0],
          'login[password]': user_pass[1]}


def login_func (login_url,values,url):
    session_requests = requests.session()
    result = session_requests.get(login_url)
    result = session_requests.post(login_url,data = values,headers = dict(referer=login_url))
    soup = BeautifulSoup(result.content,"html.parser")
    for div in soup.findAll('div', {'class': 'c-message-light c-message-light--error has-oneline'}):
        if div.text == "اطلاعات کاربری نادرست است":
            print("Username/Password is incorrect!")
            break
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

def all_costs():
    pages_list = []
    total_pages = 0
    content = login_func(login_url,values,url).content
    soup = BeautifulSoup(content,"html.parser")
    cost = ''
    int_cost = 0
    all_costs = 0     
    for a in soup.findAll('a', {'class': 'c-pager__item'}):
        for page_num in a.text:
            page_num = change_number(page_num)
            total_pages = int(page_num)
            #print(total_pages)
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
        content = login_func(login_url,values,page).content
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

    return all_costs

print("\n *** Total Costs: ",all_costs() , " Tooman ***")


