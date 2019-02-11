import requests as rq
import argparse
from pprint import pprint
from openpyxl import Workbook
from multiprocessing import Pool, cpu_count
import time


class DDBC_LOCATION():
    """BBBC_LOCATION class used to access location data via ID or location name

    Buddhist Studies Place Authority Databases '<http://authority.dila.edu.tw/place/>'

    Args:
        URL (str): DDBC url string.

    Methods:

    """

    URL = 'http://authority.dila.edu.tw/webwidget/getAuthorityData.php?type=place&id={}&jsoncallback='''

    def __init__(self):
        pass

    def parser_data(self, query_id):
        try:
            res = rq.get(self.URL.format(query_id))

            data = res.json()['data1']

            if data is None:
                print(query_id)
                return None

            if res.status_code != 200:
                print('not 200 status code', query_id)
            else:
                return data

        except:
            print('error occurs:', query_id)

    def id_generator(self, n):
        START_ID = 'PL000000000000'

        for _ in range(1, n + 1):
            yield START_ID[:-len(str(_))] + str(_)


    def get_basic_info(self, data):
        """Parse data to list of basic info

        """

        # filter dictionary according BASIC_INFO_kEY
        BASIC_INFO_KEY = ['name', 'authorityID', 'long', 'lat', 'dynasty', 'districtHistorical']

        filtered_dict = {k:v for k,v in data.items() if k in BASIC_INFO_KEY}

        if 'districtHistorical' not in filtered_dict:
            authority_id = filtered_dict['authorityID']
            print(f'{authority_id} no districtHistorical')
            #print(filtered_dict)
            filtered_dict['districtHistorical'] = ''
        elif filtered_dict['districtHistorical']== None:
            filtered_dict['districtHistorical'] = ''
        return_dict = {}
        for k,v in filtered_dict.items():
            if v == None:
                return_dict[k] = ''
            else:
                return_dict[k] = v
        return return_dict

    def query_id_list(self, path):
        return [i.replace(' ', '') for i in open(path, 'r', encoding='utf-8').read().split('\n')]

    def fetch_data_by_ID(self, id):
        c = self.parser_data(id)

        if c is None:
            return None

        filtered_dict = DDBC_LOCATION().get_basic_info(c)

        # 過濾不需要資料
        if len(filtered_dict) != 6:
            return None
            # print(filtered_dict)
        else:
            # 處理資料成為我們想要的格式
            basic_info_list = [filtered_dict['name'], filtered_dict['authorityID'],
                               filtered_dict['long'], filtered_dict['lat'],
                               filtered_dict['dynasty'], filtered_dict['districtHistorical']]

        return basic_info_list

    @staticmethod
    def store_excel(lst, file_name):
        wb = Workbook()
        worksheet1 = wb.active
        worksheet1.title = "worksheet1"
        worksheet1.append(['name', 'authorityID', 'long', 'lat', 'dynasty', 'districtHistorical'])

        for basic_info_list in lst:
            if isinstance(basic_info_list, list):
                worksheet1.append(basic_info_list)
            else:
                pass

        if 'xlsx' not in file_name:
            file_name = file_name + '.xlsx'
        else:
            pass

        wb.save(file_name)

def main():
    parser = argparse.ArgumentParser(
        description="""
                An DDBC API, which allows users access location data easily
                """
    )
    parser.add_argument('-r', type=str)
    parser.add_argument('-w', type=str, default='data/output.xlsx')
    args = parser.parse_args()

    # 讀取不重複權威碼
    if args.r:
        PATH = args.r

    #PATH = 'C:/Users/Linus/PycharmProjects/GaosengZhuan/DDBC_location/高僧傳地名詞組/八部高僧傳地名規範碼_不重複.txt'
    #PATH = 'C:/Users/Linus/PycharmProjects/GaosengZhuan/DDBC_location/高僧傳地名詞組/八部高僧傳地名規範碼_不重複_1000.txt'

    lst = DDBC_LOCATION().query_id_list(PATH)

    print(f'available cpu {cpu_count()}')

    how_many = cpu_count()
    p = Pool(processes=how_many)
    data = p.map(DDBC_LOCATION().fetch_data_by_ID, lst)

    # save excel
    if args.w:
        DDBC_LOCATION().store_excel(data, 'data/'+args.w)


if __name__ == '__main__':
    s = time.time()
    main()
    # 紀錄時間
    print(time.time() - s)


