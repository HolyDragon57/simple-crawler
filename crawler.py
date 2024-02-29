# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import sys
from dateutil import parser
from datetime import datetime

def is_valid_date(date):
    try:
        _ = parser.parse(date)
        return True
    except ValueError:
        return False

if len(sys.argv) < 3:
    print("Usage: python crawler.py [valid_date_like_20121231] [current_like_USD]")
    sys.exit()

# 检查输入日期合法性
date = sys.argv[1]
if is_valid_date(sys.argv[1]):
    date = datetime.strptime(date, "%Y%m%d").date()
    if date > datetime.now().date():
        print("Please do not travel to the future!")
        sys.exit()
    date = date.strftime("%Y-%m-%d")
else:
    print("Please input valid date!")
    sys.exit()

url = "https://www.boc.cn/sourcedb/whpj"
browser = webdriver.Chrome()
browser.get(url)
# 等待一段时间防止网页加载太慢
browser.implicitly_wait(1000)

'''
邮件中参考货币代号网站中存在诸多问题，比如（中国银行写法 => 参考网站写法）德国马克 => 马克；法国法郎 => 法郎；无沙特里亚尔，土耳其里拉等等
由于中国银行支持外币类型有限且为静态，因此选择打表。先爬取中国银行中可选的货币value

nodes = browser.find_elements('xpath', "//select[@id='pjname']//option[position()>1]")
currency_list = []
for node in nodes:
    currency_list.append(node.text)
print(currency_list)

然后使用ChatGPT进行提示工程获取形如{'USD': '美元'}的字典结构，提示词如下：
现有一个Python List: ['英镑', '港币', '美元', '瑞士法郎', '新加坡元', '瑞典克朗', '丹麦克朗', '挪威克朗', '日元', '加拿大元', '澳大利亚元', 
'欧元', '澳门元', '菲律宾比索', '泰国铢', '新西兰元', '韩元', '卢布', '林吉特', '新台币', '西班牙比塞塔', '意大利里拉', '荷兰盾', '比利时法郎',
'芬兰马克', '印尼卢比', '巴西里亚尔', '阿联酋迪拉姆', '印度卢比', '南非兰特', '沙特里亚尔', '土耳其里拉']
寻找出对应的三位英文代码货币代号，比如USD：美元。并把它转化成Python字典，如{'USD': '美元', ...}，注意使用英文分号和冒号，忽略过程仅输出结果，
用markdown代码格式输出，不要全部写在同一行中。

提示工程得到以下内容
'''
currency_list = {
  'GBP': '英镑',
  'HKD': '港币',
  'USD': '美元',
  'CHF': '瑞士法郎',
  'SGD': '新加坡元',
  'SEK': '瑞典克朗',
  'DKK': '丹麦克朗',
  'NOK': '挪威克朗',
  'JPY': '日元',
  'CAD': '加拿大元',
  'AUD': '澳大利亚元',
  'EUR': '欧元',
  'MOP': '澳门元',
  'PHP': '菲律宾比索',
  'THB': '泰国铢',
  'NZD': '新西兰元',
  'KRW': '韩元',
  'RUB': '卢布',
  'MYR': '林吉特',
  'TWD': '新台币',
  'ESP': '西班牙比塞塔',
  'ITL': '意大利里拉',
  'NLG': '荷兰盾',
  'BEF': '比利时法郎',
  'FIM': '芬兰马克',
  'IDR': '印尼卢比',
  'BRL': '巴西里亚尔',
  'AED': '阿联酋迪拉姆',
  'INR': '印度卢比',
  'ZAR': '南非兰特',
  'SAR': '沙特里亚尔',
  'TRY': '土耳其里拉'
}
if sys.argv[2] not in currency_list: 
    print("Currency", sys.argv[2], "not supported yet!")
    sys.exit()
currency = currency_list[sys.argv[2]]

start_date = browser.find_element('xpath', "//input[@id='erectDate']")
start_date.clear()
start_date.click()
start_date.send_keys(date)

end_date = browser.find_element('xpath', "//input[@id='nothing']")
end_date.clear()
end_date.click()
end_date.send_keys(date)

# 中国银行网站bug，点开结束时间input框后，牌价选择select框会消失，需要额外点击一下日历的关闭按钮
browser.find_element('xpath', "//input[@id='calendarClose']").click()

drop_down = browser.find_element('xpath', '//select')
drop_down.click()
select = Select(drop_down)
select.select_by_value(currency)

browser.find_element('xpath', "(//input[@class='search_btn'])[2]").click()

# 由于只需要输出某一个日期下某种货币的一个现汇卖出价价位，因此不必爬取无关数据
node = browser.find_element('xpath', "((//div[@class='BOC_main publish']//tr)[2]//td)[4]")
price = node.text
info = date + currency + "的现汇卖出价为" + price
print(info)

with open('result.txt', 'a') as file:
    file.write(info + "\n")
print("Data has been written to result.txt.")

browser.close()

# 本机跑有一些Warning，是由于最新的Chrome版本对应的chromeDriver还没有发布，存在版本不匹配导致。