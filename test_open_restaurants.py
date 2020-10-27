from datetime import datetime

from check_open_restaurants import Restaurant, parse_restaurant, find_open_restaurants

test_csv_file = "restaurants.csv"
current_datetime = datetime.now()
test_counter = 0

restaurant = parse_restaurant(
    ["Filip's restaurant", "Mon-Sun 12:00 am - 11:59 pm"])
assert isinstance(restaurant, Restaurant)
test_counter += 1
current_day = current_datetime.strftime("%A")

assert current_day in restaurant.opened_range.keys()
test_counter += 1

assert current_datetime in restaurant.opened_range[current_day]
test_counter += 1

open_res = find_open_restaurants(test_csv_file, current_datetime)
assert len(open_res) == 32
test_counter += 1

print("Passed %d tests, failed %d." % (test_counter, 4-test_counter))
