from datetime import datetime
import pytest

from check_open_restaurants import Restaurant, parse_restaurant, find_open_restaurants

test_csv_file = "restaurants.csv"
current_datetime = datetime.now()


def test_parse_restaurant():
    restaurant = parse_restaurant(
        ["Filip's restaurant", "Mon-Sun 12:00 am - 11:59 pm"])
    assert isinstance(restaurant, Restaurant)
    current_day = current_datetime.strftime("%A")

    assert current_day in restaurant.opened_range.keys()
    assert current_datetime in restaurant.opened_range[current_day]


def test_find_open_restaurants():
    open_res = find_open_restaurants(test_csv_file, current_datetime)
    assert len(open_res) == 32
