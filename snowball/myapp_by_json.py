import requests
from bs4 import BeautifulSoup
import time
import json

headers = {
			'cookie':'s=em11tif7qs; \
			 _gid=GA1.2.173619717.1528098380;\
			 xq_a_token=019174f18bf425d22c8e965e48243d9fcfbd2cc0;\
			 xq_a_token.sig=_pB0kKy3fV9fvtvkOzxduQTrp7E;\
			 xq_r_token=2d465aa5d312fbe8d88b4e7de81e1e915de7989a;\
			 xq_r_token.sig=lOCElS5ycgbih9P-Ny3cohQ-FSA;\
			 u=831528287480558;\
			 Hm_lvt_1db88642e346389874251b5a1eded6e3=1528163423,1528183023,1528251078,1528287481;\
			 Hm_lpvt_1db88642e346389874251b5a1eded6e3=1528287488',
        	'User-Agent': 'aliyungf_tc=AQAAACZheBs1KQQArATEc4iISe6n8GjL; \
        	xq_a_token=7023b46a2c20d7b0530b4e9725f7f869c8d16e7d; \
        	xq_a_token.sig=ENETvzFNvxxbtpbc1TfjQpBjoaE; \
        	xq_r_token=19bf36bc92fc764fb5cc550744d7fe922069fd14; \
        	xq_r_token.sig=dRocG0wcTXQQLq8b3AmLY9RYqyk'
        }

encoding='utf-8'

def get_info(url):
	r = requests.get(url,headers = headers)
	soup = BeautifulSoup(r.text,'lxml')

	stock_name = soup.find_all('div','stock-name')
	stock_current = soup.find_all('div','stock-current')
	stock_change = soup.find_all('div','stock-change')
	stock_name = stock_name[0].text.split('(')[0]
	stock_current = stock_current[0].strong.text[1:]
	stock_change = stock_change[0].text.split(' ')[2]

	stock_info = [stock_name,stock_current,stock_change]
	print(stock_name,stock_current,stock_change)


def get_json(url):
	comments = []
	r = requests.get(url,headers = headers)
	stock_info = json.loads(r.text)
	comment = {}
	comment['name'] = stock_info['data']["quote"]['name']
	comment['current'] = stock_info['data']["quote"]['current']
	comment['percent'] = str(stock_info['data']["quote"]['percent'])+'%'
	comments.append(comment)
	print(comments[0]) 
	return comments
	# print(stock_info['data']["quote"]['name'],stock_info['data']["quote"]['current'],stock_info['data']["quote"]['percent'])



# 股票ID，基础链接
base_url = 'https://xueqiu.com/S/'
json_url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol=%s&extend=detail'
stock_id = ['SH600340','SH601318','SZ000651','SZ002415']

def main():
	# 法一、获取完整网页信息后抓取
	print("\n方法一，获取完整网页信息后抓取...")
	t0 = time.time()			#计时器
	for id in stock_id:
		url = base_url + id
		# 获取到爬取链接，开始爬取...
		get_info(url)
	print('运行时间(s)：','%.3f'%(time.time() - t0))
	
	# 法二、分析调用接口直接抓取json
	print("\n方法二，分析调用接口直接抓取json...")
	t1 = time.time()			#计时器
	for j in stock_id:
		url = json_url%(j)
		# 获取到爬取链接，开始爬取...
		get_json(url)
	print('运行时间(s)：','%.3f'%(time.time() - t1))


if __name__ == '__main__':
	main()

