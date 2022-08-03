from urllib.parse import urlparse
import os
import requests
from dotenv import load_dotenv
import argparse


def shorten_link(long_url, headers):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    payload = {'long_url': long_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(bitlink, headers):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(bitlink, headers):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    headers = {"Authorization": f"Bearer {bitly_token}"}
    parser = argparse.ArgumentParser(description='Данная программа сокращает ссылки и показывает клики по созданным ссылкам')
    parser.add_argument('link', help='Ваша ссылка')
    args = parser.parse_args()
    long_url = args.link
    parsed_url = urlparse(long_url)
    url_without_scheme = parsed_url.netloc + parsed_url.path

    try:
        if is_bitlink(url_without_scheme, headers):
            print('Количество кликов по ссылке:', count_clicks(url_without_scheme, headers))
        else:
            print('Сокращенная ссылка:', shorten_link(long_url, headers))
    except requests.exceptions.HTTPError as error:
        exit("Ошибка:  Неверная ссылка", error)
