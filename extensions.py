import requests
import json
from config import keys



class ConvertionException(Exception):
    pass

class PriceConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Нельзя перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обрадотать количество {amount}')


        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=d0b8875944669fd25d731ac121173b04')
        total_base1 = json.loads(r.content)["data"][f'{quote_ticker}{base_ticker}']
        total_base = float(total_base1) * amount
        return total_base
