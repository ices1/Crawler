import requests
from bs4 import BeautifulSoup
import yagmail
import time
import random

# 爬取页面信息函数
def get_info(url):
	headers = {
	        	'User-Agent': 'aliyungf_tc=AQAAACZheBs1KQQArATEc4iISe6n8GjL;'
	        }
	encoding='utf-8'
	r = requests.get(url,headers = headers)
	soup = BeautifulSoup(r.text,'lxml')
	# 爬取对应标签信息
	stock_name = soup.find_all('div','stock-name')
	stock_current = soup.find_all('div','stock-current')
	stock_change = soup.find_all('div','stock-change')
		
	stock_name = stock_name[0].text.split('(')[0]
	stock_current = stock_current[0].strong.text[1:]
	stock_change = stock_change[0].text.split(' ')[2]

	stock_info = None
	stock_info = [stock_name,stock_current,stock_change]
	# 条件判断，提取需要的信息
	print( stock_change.split("%")[0]) 
	limit_change =float(stock_change.split("%")[0])
		# 重置容器stock_info,并装入信息
	if limit_change <= -2:
		# 重置容器stock_info,并装入信息
		return stock_info
	else:
		pass

#信息收集筛选函数
def collect_info():
	print('\nStep2，打包收集信息')
	stock_store = []
	for id in stock_id:
		url = base_url + id
		stock_info = get_info(url)
		stock_store.append(stock_info)
		# 列表去除 None
		while None in stock_store:
			stock_store.remove(None)
	return stock_store

#发送邮件
def send_email(stock_store):
	print('\nStep3，将信息以邮件发出')

	# 邮箱正文
	#当为传入数值空时
	if len(stock_store) == 0:
		print('一切ok, 不发邮件~')
		return 0
	#当传入不为空时
	else:
		if len(stock_store) == 1:
			send_status = 100
			title = '你的 ' + stock_store[0][0] +' 跌超过 '+ stock_store[0][2]+'了'
			contents = stock_store[0][0]+" || 价格--> "+stock_store[0][1]+\
						"|| 跌幅--> "+stock_store[0][2]
			print(stock_store[0][0],' ，快加仓')
		else:
			send_status = 100
			title = '你的 ' + stock_store[0][0] + "、" + stock_store[1][0] +\
					'...好几票跌超过 '+ stock_store[0][2]+'了'
			contents = stock_store[0][0]+" || 价格--> "+stock_store[0][1]+\
						"|| 跌幅--> "+stock_store[0][2] +'\n'+ stock_store[1][0]+\
						" || 价格--> "+stock_store[1][1]+"|| 跌幅--> "+\
						stock_store[1][2]+'\n'+'...'
			print(stock_store[0][0], stock_store[1][0], '...超跌'+\
					 stock_store[0][2]+'，快加仓')

		#链接邮箱服务器
		yag = yagmail.SMTP( user="icexxxx@163.com", password="sxxxxx",\
				 host='smtp.163.com')
		# 发送邮件
		try:
			yag.send('1299xxxxxx@qq.com', title, contents)
		except Exception  as e:
			print("Unexpected error:", e)
			print('发送失败了，再试试')
			return 0

		return send_status

# A股市营业时间判断是否运行
def stock_open_time(send_status):
	print('\nStep1，查询对照A股市营业时间')
	now_t = time.strftime("%H", time.localtime())
	now_d = time.strftime("%a", time.localtime())
	# 获取到当前时间，如不为周末，且时间段在9~15点内，则跳出函数语句
	# while 0 :
	while now_d == "Sat" or now_d == "Sun" or int(now_t) <= 9 or int(now_t) >=15 :
	    print("休市中,一小时后刷新...")
	    print ('当前时间为：',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	    time.sleep(3600)
	    print('')
	else:
	    print('开市啦...')
	    sleeping_time(send_status)

# 间歇抓取时间睡眠函数
def sleeping_time(send_status):
	if send_status:
		sleeping_t_num = random.randint(64800,64801)
		print('已经发送过邮件了，休息(s): ',sleeping_t_num)
	else:
		# sleeping_t_num = random.randint(1,3)
		sleeping_t_num = random.randint(300,1200)
		print('间歇时间(s): ',sleeping_t_num)
	time.sleep(sleeping_t_num)




#基础信息（股票代码，URL地址）
base_url = 'https://xueqiu.com/S/'
stock_id = ['SH600340','SH601318','SZ000651','SZ002415']

def main():
	send_status = 0
	while 1>0:
		# 第一步，时间函数，按休市时间，邮件是否已经发送间歇工作
		stock_open_time(send_status)

		# 第二步，获取收集信息
		stock_store = collect_info()

		# 第三步，将信息发送邮件发送
		send_status = send_email(stock_store)
		# print(stock_store)
		print('\n----------------OVER----------------')

if __name__ == '__main__':
	main()
