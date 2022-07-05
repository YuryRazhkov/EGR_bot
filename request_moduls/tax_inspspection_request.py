import os

import requests
import sys

import logging
import logs.bot_log



logger = logging.getLogger('botlog')



def request_to_tax_inspection(regnum):

    logger.debug('send request to_tax_inspection')
    response = requests.get(f'http://www.portal.nalog.gov.by/grp/getData?unp={regnum}&charset=UTF-8&type=json')
    logger.debug(f'status code {response.status_code}')
    if response.status_code == 200:
        response_for_pars = response.json().get('ROW')
        tax_inspection_answer = f"- УНП: {response_for_pars.get('VUNP')}\n" \
                                f"- наименование: {response_for_pars.get('VNAIMP')}\n" \
                                f"- статус: {response_for_pars.get('VKODS')}\n" \
                                f"- адрес: {response_for_pars.get('VPADRES')}\n" \
                                f"- дата регистрации ИМНС: {response_for_pars.get('DREG')}\n" \
                                f"- ИМНС: {response_for_pars.get('VMNS')}\n"

        return tax_inspection_answer

    else:
        tax_inspection_answer = 'Данные не получены'
        return tax_inspection_answer


if __name__ == '__main__':
    request_to_tax_inspection(290290290)
