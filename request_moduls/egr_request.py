import time
from interruptingcow import timeout
import requests
import sys
sys.path.append('../')
import logging
import logs.bot_log

logger = logging.getLogger('botlog')
response_dict = {}
session = requests.Session()

def request_to_registr(regnum):

    logger.debug('send request EGR')

    try:
        # with timeout(25, exception=RuntimeError):
        #     response = session.get(f'http://egr.gov.by/api/v2/egr/getBaseInfoByRegNum/{regnum}')
        # response_code = response.status_code
        # logger.debug(f'status code {response_code}')

        with timeout(25, exception=RuntimeError):
            response = session.get(f'http://egr.gov.by/api/v2/egr/getBaseInfoByRegNum/{regnum}')
        response_code = response.status_code
        logger.debug(f'status code {response_code}')
        if response_code == 200:
            base_info_by_regnum = response.json()[0]
            # print(base_info_by_regnum)
            response_dict['Тип субъекта'] = base_info_by_regnum.get("nsi00211").get('vnvobp')
            if base_info_by_regnum.get("nsi00211").get('nkvob') == 1:
                # jur_name_by_regnum = requests.get(f'http://egr.gov.by/api/v2/egr/getJurNamesByRegNum/{regnum}').json()[0]
                # response_dict['Наименование'] = jur_name_by_regnum.get('vnaim')
                logger.debug('send request getAllAddressByRegNum')
                address_by_regnum = session.get(f'http://egr.gov.by/api/v2/egr/getAllAddressByRegNum/{regnum}').json()[0]
                country = str(address_by_regnum.get('nindex')) + ', ' + (address_by_regnum.get('nsi00201').get('vnstranp'))
                city = str(address_by_regnum.get('nsi00239').get('vntnpk')) + str(address_by_regnum.get('vnp'))
                street = str(address_by_regnum.get('nsi00226').get('vntulk')) + str(address_by_regnum.get('vulitsa'))
                bilding = str(address_by_regnum.get('vdom')) + ', ' \
                          + str(address_by_regnum.get('nsi00227').get('vntpomk')) \
                          + str(address_by_regnum.get('vpom'))
                full_address = f'{country}, {city}, {street}, {bilding}'
                phone_num = str(address_by_regnum.get('vtels'))
                site = str(address_by_regnum.get('vsite'))
                email = str(address_by_regnum.get('emails'))



            else:
                # base_info_by_regnum.get("nsi00211").get('nkvob') == 2:
                # ip_name_by_regnum = requests.get(f'http://egr.gov.by/api/v2/egr/getIPFIOByRegNum/{regnum}').json()[0]
                # response_dict['Наименование'] = ip_name_by_regnum.get('vfio')
                full_address = 'Информация относится к персональным данным. Доступна по ссылке.'
                phone_num = 'Информация относится к персональным данным. Доступна по ссылке.'
                site = 'Информация относится к персональным данным. Доступна по ссылке.'
                email = 'Информация относится к персональным данным. Доступна по ссылке.'


            response_dict['- Состояние'] = base_info_by_regnum.get("nsi00219").get('vnsostk')
            response_dict['- Регистрационный номер'] = base_info_by_regnum.get("ngrn")
            response_dict['- Регистрирующий орган (на текущую дату)'] = base_info_by_regnum.get("nsi00212CRT").get('vnuzp')
            response_dict['- Регистрирующий орган (при регистрации)'] = base_info_by_regnum.get("nsi00212").get('vnuzp')
            response_dict['- Дата регистрации'] = base_info_by_regnum.get("dfrom")[:10]
            response_dict['- телефон'] = phone_num
            response_dict['- сайт'] = site
            response_dict['- email'] = email

            response_str = response_dict.__str__()
            response_str = response_str[1:-1]
            response_str = response_str.replace("'", "")
            response_str = response_str.replace(", ", "\n")
            response_str = response_str.replace("\n- Состояние:", f'\n- Адрес: {full_address}\n- Состояние:')
            # response_dict['Адрес'] = full_address
            response_str = f'{response_str} \n\nОтчет о субъект можно посмотреть по ссылке:\n' \
                               f'https://egr.gov.by/egrmobile/information?pan={regnum}'

            logger.debug(f'send response {response_str}')
            print(response_str)

            response_str = f"Информация доступна  по ссылке: \n"\
                           "https://egr.gov.by/egrmobile/information?pan="+str(regnum)

            return response_str

        elif response_code == 204:
            response_str = "Данные в ЕГР не найдены"
            return response_str

        elif response_code == 404:
            response_str = "Ошибка 404: сервер не может найти запрашиваемый ресурс"
            return response_str

        elif response_code == 500:
            response_str = "Ошибка 500: Внутренняя ошибка сервера"
            return response_str

        elif response_code == 503:
            response_str = "503 Service Unavailable. \n" \
                           " Похоже ЕГР не готов обработать запрос. Возможно проводятся технические работы" \
                           "\n\nДля доступа к информации попробуйте перейти по ссылке: \n"\
                           "https://egr.gov.by/egrmobile/information?pan="+str(regnum)
            return response_str

        else:
            response_str = str(response_code)
            return f'Ошибка. Код ответа: {response_str}. Проверьте правильность написания УНП'

        # response_str = "Информация доступна по ссылке: \n"\
        #                "https://egr.gov.by/egrmobile/information?pan="+str(regnum)
        # return response_str

    except:

        logger.debug('rise except')
        return f'ЕГР долго не отвечает. \nПопробуйте перейти по ссылке: \n ' \
               f'https://egr.gov.by/egrmobile/information?pan={str(regnum)}'


if __name__ == '__main__':
    start = time.time()
    print(request_to_registr(291474093))
    end = time.time()
    print(end-start)




