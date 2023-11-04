from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up Chrome options
chrome_options = Options()
# driver_path = "D:\\env\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe" # 修改为你的 ChromeDriver 路径
# driver = webdriver.Chrome(driver_path)

# Specify the path to chromedriver you downloaded
service = Service(executable_path='D:\\env\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')  # Update this to your actual chromedriver path

# Initialize the driver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
# 打开网页
url = "https://cmrdb.fysik.dtu.dk/c2db"
driver.get(url)

# 手动调rows
input()


# Wait for the dropdown to be present in the page
wait = WebDriverWait(driver, 30)  # Wait for a maximum of 10 seconds

search_table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'search')))
dynamically_stable = search_table.find_element(By.NAME, 'dynamically_stable')
# click and choose 'all' option
# 实例化Select对象
select = Select(dynamically_stable)

# 根据option的value属性选择"All"
select.select_by_value('all')



# input()
time.sleep(1)

# 点击搜索按钮
form = wait.until(EC.presence_of_element_located((By.ID, 'mainFormID')))
search = form.find_element(By.CLASS_NAME, 'btn-default')
search.click()



dropdown_menu = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu')))

# Find all the <a> tags within the dropdown menu
links = dropdown_menu.find_elements(By.TAG_NAME, 'a')

# Extract the JavaScript commands from the href attributes
js_commands = [link.get_attribute('href') for link in links]

# Replace the "javascript:" part to get only the JavaScript function call
js_commands = [cmd.replace('javascript:', '') for cmd in js_commands]

# Now js_commands list contains all the JavaScript function calls from the hrefs
# print(js_commands)

# Close the driver
fin_num=0
for js_command in js_commands:
    fin_num=fin_num+1
    print("now num",fin_num,'/',len(js_commands))
    driver.execute_script(js_command)
    # wait for the page to load
    
    # Wait for the dropdown to be present in the page
    wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
    dropdown_menu = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu')))
    # time.sleep(2)
# num=0
# while 1:
#     if num>4:
#         print('too more')
#         break
#     drop_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pull-right')))
#     drop_button = drop_div.find_element(By.CLASS_NAME, 'dropdown-toggle')
#     drop_button.click()
#     time.sleep(1)
#     # Wait for the dropdown to be present in the page
#     dropdown_menu = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'dropdown-menu')))
#     # 查看dropdown-menu下是否有li
#     lis = dropdown_menu.find_elements(By.TAG_NAME, 'li')
#     num=num+1
#     if len(lis) > 0:
#         lis[0].click()
#         time.sleep(1)
#     else:
#         print('no li')
#         break


table_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-default')))
table = table_div.find_element(By.CLASS_NAME, 'table-striped')
tbody = table.find_element(By.TAG_NAME, 'tbody')

rows = tbody.find_elements(By.TAG_NAME, 'tr')
# 第一行是表头
header_row = rows[0]
# 提取表头的文本
header_cols = header_row.find_elements(By.TAG_NAME, 'th')
header_data = [col.text for col in header_cols]
# 打印表头数据
print('header_data: ',header_data)
head_num = len(header_data)
# 遍历每一行，提取每个单元格的文本
table_data = []
for row in rows[1:]:
    cols = row.find_elements(By.TAG_NAME, 'td')
    row_data = [col.text for col in cols]
    table_data.append(row_data)
# input()

# # 打印获取到的数据
# for row in table_data:
#     print(row)
# 将数据转换为pandas的DataFrame对象写入output.xlsx文件

# 依次请求js，javascript:update_table(5797, 'page', 1)，javascript:update_table(5797, 'page', 2)...javascript:update_table(5797, 'page', 187)

uls = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pagination-sm')))
lis = uls.find_elements(By.TAG_NAME, 'li')
# 获取li的href
js_command = lis[2].find_element(By.TAG_NAME, 'a').get_attribute('href') 
print(js_command)
js_format = js_command[:-2]+'{})'
print('js_format',js_format)

for i in range(1, 24):
    print('i: ',i)

    # Scroll to the bottom of the page
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # # Wait for page to load (if necessary)
    # import time
    # time.sleep(3)  # waits 3 seconds

    js_command = js_format.format(i)
    driver.execute_script(js_command)
    # wait for the page to load
    
    # Wait for the dropdown to be present in the page
    wait = WebDriverWait(driver, 10)  # Wait for a maximum of 10 seconds
    table_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-default')))
    table = table_div.find_element(By.CLASS_NAME, 'table-striped')
    tbody = table.find_element(By.TAG_NAME, 'tbody')

    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    # 第一行是表头
    header_row = rows[0]
    # 提取表头的文本
    header_cols = header_row.find_elements(By.TAG_NAME, 'th')
    header_data = [col.text for col in header_cols]
    head_num2 = len(header_data)
    if head_num != head_num2:
        print('head_num != head_num2')
        input()
        # break
    # 打印表头数据
    print('header_data{}: '.format(i),header_data)
    # 遍历每一行，提取每个单元格的文本
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, 'td')
        row_data = [col.text for col in cols]
        table_data.append(row_data)
    # input()
    

    # # 打印获取到的数据
    # for row in table_data:
    #     print(row)
    # print(table_data)
    # 将数据转换为pandas的DataFrame对象写入output.xlsx文件
    # 在原先文件的基础上继续写入

df = pd.DataFrame(table_data, columns=header_data)
df.to_excel('output.xlsx', index=False)


# print(table_data)

# # 执行自定义 JavaScript
# # 如果 update_table 是一个全局可调用的函数，你可以这样直接执行它
# js_command = '''
# javascript:update_table(5731,
#                                                    'toggle',
#                                                    'plasmafrequency_y')
# '''
# driver.execute_script(js_command)

# 等待页面更新（可能需要具体的等待条件）
# ...

# 获取更新后的页面源码或者是页面上的特定数据
updated_content = driver.page_source  # 或其他操作

input()
# 关闭浏览器
driver.quit()

# 在这里可以使用 updated_content 进行解析或其他操作
