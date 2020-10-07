from enum import Enum
from typing import List
import requests
import json


class Currency(Enum):
    ETH = 'eth'
    USD = 'usd'
    BTC = 'btc'


class PriceFetcher:
    parameters = []
    function_count = 1

    function_detail_total = {}

    def scrape_price(self, *, currency: Currency, denomination_currency: Currency):
        # TODO: implement
        # id_url = 'https://api.coingecko.com/api/v3/coins/list'
        # headers = {}

        # response = requests.request("GET", id_url, headers=headers)
        # response = json.loads(response.text)
        # for each in response:
        #     if each["symbol"] == currency.value:
        #         currency_id = each["id"]
        #     elif each["symbol"] == denomination_currency.value:
        #         denomination_currency_id = each["id"]
        #     else:
        #         continue
        # print(currency_id, denomination_currency_id)
        # self.parameters = [currency.value,denomination_currency.value]

        function_parameters = [currency.value, denomination_currency.value]
        function_parameters_string = "/".join(function_parameters)
        exchages_url = "https://api.coingecko.com/api/v3/exchange_rates"
        headers = {}
        try:
            response = requests.request("GET", exchages_url, headers=headers)
        except Exception:
            print("Error occured during accessing api")
        response = json.loads(response.text)
        rates = response["rates"]
        try:
            currency_rate = rates[currency.value]
            denomination_currency_rate = rates[denomination_currency.value]
        except Exception:
            print("Currency Name not found or invalid")
        exchanged_price = denomination_currency_rate['value'] / \
            currency_rate['value']
        reverse_exchanged_price = currency_rate['value'] / \
            denomination_currency_rate['value']
        result = {
            "currency_name": currency.value,
            "domination_currency_name": denomination_currency.value,
            'currency_value': currency_rate['value'],
            'domination_value': denomination_currency_rate['value'],
            "exchange_rate": exchanged_price,
            "reverse_exchanged_price": reverse_exchanged_price
        }

        if len(self.parameters) == 0:
            self.parameters = function_parameters.copy()

            self.function_detail_total = {
                function_parameters_string: {
                    'parameters': function_parameters,
                    'function_count': 1,
                    'exchange_rates': [result['exchange_rate']],
                    'detail': result
                }
            }

        else:
            if self.parameters == function_parameters:
                self.function_count = self.function_count + 1

                self.function_detail_total[function_parameters_string]["function_count"] += 1
                self.function_detail_total[function_parameters_string]["exchange_rates"].append(
                    result['exchange_rate'])

            else:
                self.function_count = 1
                self.parameters = function_parameters.copy()
                self.function_detail_total[function_parameters_string] = {
                    'parameters': function_parameters,
                    'function_count': 1,
                    'exchange_rates': [result['exchange_rate']],
                    'detail': result
                }

    def get_historical_prices(self, *, currency: Currency, denomination_currency: Currency) -> List[float]:
        # TODO: implement
        function_parameters = [currency.value, denomination_currency.value]
        function_parameters_string = "/".join(function_parameters)
        function_parameters_reverse = function_parameters[::-1]
        function_parameters_string_reverse = "/".join(
            function_parameters_reverse)

        try:

            return self.function_detail_total[function_parameters_string]["exchange_rates"]
        except Exception:
            exchange_rate = []
            if self.function_detail_total[function_parameters_string_reverse]["parameters"] == function_parameters[::-1]:
                for i in range(int(self.function_detail_total[function_parameters_string_reverse]["function_count"])):
                    exchange_rate.append(
                        self.function_detail_total[function_parameters_string_reverse]["detail"]["reverse_exchanged_price"])
                return exchange_rate
            else:

                print("Currency Not found or Invalid.")


price_fetcher = PriceFetcher()
