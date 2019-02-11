import requests as rq
import argparse
from pprint import pprint


class DDBC_location(object):
	DDBC_API = 'http://authority.dila.edu.tw/webwidget/getAuthorityData.php?type=place&id={}&jsoncallback='''.format('長安')
	'''docstring for DDBC location'''
	def __init__(self, loc_arg):
		pass


parser = argparse.ArgumentParser(description='請輸入地名: ')
parser.add_argument('-r', '--location', type=str, help='中文地名')
location_args = parser.parse_args().location



exit_status = False
data_looking = False

while exit_status is False:
	user_cmd = input('輸入您要搜尋的地名: ')
	DDBC_API = 'http://authority.dila.edu.tw/webwidget/getAuthorityData.php?type=place&id={}&jsoncallback='''.format(user_cmd)

	if user_cmd == '-q':
		exit_status = True

	res = rq.get(DDBC_API)
	print('狀態碼: ', res.status_code)

	if not res.json():
		print('don\' not receieve response')
	else:
		data = res.json()
		data_looking = True

	if len(data) > 1 and data_looking == True:

		show_msg = '\n共有{}筆資料，請輸入一筆: '.format(len(data))
		user_kw = input(show_msg)
		if user_cmd == '-s':
			break

		print('第 {} 筆資料:'.format(user_kw))
		pprint(data['data' + str(user_kw.strip())])
		print('\n')


		while show_msg != '-s':
			user_kw = input(show_msg)
			if user_kw == '-s':
				data_looking = False
				print()
				break

			print('第 {} 筆資料:'.format(user_kw))
			pprint(data['data' + str(user_kw.strip())])
			print('\n\n')

			show_msg = '共有{}筆資料，請輸入一筆: '.format(len(data), end='\n\n')



# python argparse_demo.py
# if __name__ == '__main__':
# 	print(location_args)
#   main()