import requests
from requests import Response
from datetime import datetime

from configs.config import REQ_URL
from configs.config import AVIASALES_API_KEY
from db_methods.db_airports_class import DBMethods
from processing.city_checker import check_city


def get_cheapest_tickets(data: dict) -> tuple:
    if data["from_all_airports"]:
        check_res = check_city(city_name=data["from_city"])
        departure_cities = list(DBMethods.get_airports(city_name=check_res[0], language=check_res[1]))
    else:
        departure_cities = [data["from_airport"], ]

    if data["to_all_airports"]:
        check_res = check_city(city_name=data["to_city"])
        destination_cities = list(DBMethods.get_airports(city_name=check_res[0], language=check_res[1]))
    else:
        destination_cities = [data["to_airport"], ]
    departure_date = f"{data['departure_year']}-{data['departure_month_req']}-{data['departure_date_req']}"
    print(departure_date)
    tickets = cheapest_tickets_req(from_fly=departure_cities,
                                   to_fly=destination_cities,
                                   date_fly=departure_date)

    if data["return"]:
        return_date = f"{data['return_departure_year']}-{data['return_departure_month_req']}-{data['return_departure_date_req']}"
        print(return_date)
        return_tickets = cheapest_tickets_req(from_fly=destination_cities,
                                              to_fly=departure_cities,
                                              date_fly=return_date)
        return tickets, return_tickets

    return (tickets, )


def cheapest_tickets_req(from_fly: list,
                         to_fly: list,
                         date_fly: str) -> list:
# querystring = {"origin":"MOW","destination":"HKT","depart_date":"2019-11","return_date":"2019-12"}
    tickets = list()

    for i_departure in from_fly:
        for i_destination in to_fly:
            querystring = {"origin": i_departure,
                           "destination": i_destination,
                           "depart_date": date_fly,
                           "currency": "EUR"}

            headers = {'x-access-token': AVIASALES_API_KEY}

            response = requests.request("GET", REQ_URL, headers=headers, params=querystring)
            tickets.append(response.json())
    return tickets
