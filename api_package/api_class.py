import requests
from configs.config import AVIASALES_API_KEY


class ApiMethods:
    """Класс методов работы с АПИ"""

    @staticmethod
    def get_cheapest_tickets(from_city: str, to_city: str, date: str, period: str, one_way: str) -> list:
        """Метод возвращает все билеты за указаный период с сортировкой по цене от дешевых"""
        results = list()
        querystring = {"origin": from_city,
                       "destination": to_city,
                       "beginning_of_period": date,
                       "period_type": period,
                       "one_way": one_way,
                       "sorting": "price",
                       "trip_class": "0",
                       "locale": "ru",
                       "currency": "eur",
                       "market": "eu",
                       "limit": 200,
                       "page": 1}
        headers = {'x-access-token': AVIASALES_API_KEY}

        for i_class in range(3):
            querystring["trip_class"] = i_class
            tickets = requests.request("GET", "https://api.travelpayouts.com/aviasales/v3/get_latest_prices",
                                       headers=headers, params=querystring)
            if tickets.json()["data"]:
                for i_ticket in tickets.json()["data"]:
                    results.append(i_ticket)

        results.sort(key=lambda ii_ticket: ii_ticket["value"])
        return results

    @staticmethod
    def get_expensive_tickets(from_city: str, to_city: str, date: str, period: str, one_way: str) -> list:
        """Метод возвращает все билеты за указаный период с сортировкой по цене от дорогих"""
        results = ApiMethods.get_cheapest_tickets(from_city=from_city, to_city=to_city,
                                                  date=date, period=period, one_way=one_way)

        results.sort(key=lambda i_ticket: -i_ticket["value"])

        return results

    @staticmethod
    def get_diapason_tickets(from_city: str, to_city: str, date: str, period: str,
                             one_way: str, min_price: int, max_price: int) -> list:
        """Метод возвращает все билеты за указаный период в выбранном ценовом диапазоне"""
        results = list()
        pre_results = ApiMethods.get_cheapest_tickets(from_city=from_city, to_city=to_city,
                                                      date=date, period=period, one_way=one_way)
        for i_ticket in pre_results:
            if min_price-1 < i_ticket["value"] < max_price+1:
                results.append(i_ticket)

        results.sort(key=lambda ii_ticket: ii_ticket["value"])

        return results
