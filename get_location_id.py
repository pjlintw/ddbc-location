import os
import re
import bs4 as bs
import time
from multiprocessing import Pool, cpu_count

def access_file():
    PATH = 'C:/Users/Linus/PycharmProjects/GaosengZhuan/13.TEI_to_xml/output/sengZhuan_xml_file/'
    return [PATH + f for f in os.listdir(PATH)]

def open_file(path):
    """Open file via string

    """
    return open(path, 'r',encoding='utf-8').read()

def location_id_filter(lst):
    location_id = []

    for tag in lst:
        try:
            place_id = tag['key']
            if place_id not in location_id:
                location_id.append(place_id)
        except:
            pass
    return location_id


def main():

    repository_list = access_file()

    p = Pool(processes=cpu_count())
    data = p.map(open_file, repository_list)


    corpus = ''.join(data)

    soup = bs.BeautifulSoup(corpus, 'lxml')
    location_id = location_id_filter(soup.find_all('placename'))

    with open('gaosengzhuan.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(location_id))



if __name__ == '__main__':
    s = time.time()
    main()
    print(time.time() - s)
