from pprint import pprint

from bs4 import BeautifulSoup
import requests
import sys
sys.path.append('../')
import logging
import logs.bot_log



def request_just_bel(regnum):

    logger = logging.getLogger('botlog')
    logger.debug(f'request to just_bel')

    response_list = []
    session = requests.Session()


    page = session.get(f'https://justbel.info/claim/search?reg={regnum}&name=&publishFrom=&publishTo=&liqFrom=&liqTo=&status=all&page=1')
    response_code = page.status_code
    logger.debug(f'status code {response_code}')
    if response_code == 200:

        soup = BeautifulSoup(page.text, "html.parser")
        ss = soup.find('div', class_='result')
        if ss is not None:

            for i in ss:
                response_list.append(i)
            result_str = f'-Дата и номер решения о ликвидации (прекращении деятельности): {response_list[2]}' \
                         f'\n-ФИО ликвидатора (председателя ликвидационной комиссии, наименование юрлица, ' \
                         f'назначенного ликвидатором): {response_list[3]}' \
                         f'\n-Адрес ликвидатора (председателя ликвидационной комиссии): {response_list[4]}' \
                         f'\n-Телефон ликвидатора (председателя ликвидационной комиссии): {response_list[5]}' \
                         f'\n-Дата опубликования сведений о ликвидации (прекращения деятельности): {response_list[8]}'
            result_str = result_str.replace("<p>", "")
            result_str = result_str.replace("</p>", "")
            result_str = result_str.replace("<span>", "")
            result_str = result_str.replace("</span>", "")
            return result_str
        else:
            return 'объявления о ликвидации не найдены'


    else:
        return 'данные не полученыот сервера'


if __name__ == '__main__':
    print(request_just_bel(291474043))

