import argparse
import calendar
import csv
import datetime
from dataclasses import dataclass

import dateutil.parser
from datetimerange import DateTimeRange

weekdays = {
    "Mon": 0,
    "Tue": 1,
    "Tues": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}
days_listed = list(calendar.day_name)

class WeekTimeRange(DateTimeRange):
    """Exists only to override the contains method of the DateTimeRange class"""

    def __contains__(self, x) -> bool:
        """
        Checks if time X is in self's time range.
        Parameters:
        x: Bool
        """
        if isinstance(x, DateTimeRange):
            return x.start_datetime.time() >= self.start_datetime.time() and x.end_datetime.time() <= self.end_datetime.time()

        try:
            value = dateutil.parser.parse(x)
        except (TypeError, AttributeError):
            value = x

        return self.start_datetime.time() <= value.time() <= self.end_datetime.time()

@dataclass
class Restaurant:
    """Class for keeping track of restaurants."""
    name: str
    opened_range: str

def open_csv(name="restaurants.csv") -> []:
    """
    Reads restaurant data from the CSV and returns parsed data
    Parameters:
    name: String
    """
    restaurants = []
    with open(name, newline='') as csvfile:
        next(csvfile)
        row_list = csv.reader(csvfile)
        for row in row_list:
            restaurants.append(parse_restaurant(row))
    return restaurants

def parse_restaurant(restaurant: []) -> Restaurant:
    """
    Parses a restaurant, returns a Restaurant object & handles worktime parsing
    Parameters:
    restaurant (list): List containing restaurant's name and un-parsed worktime
    """
    worktime = restaurant[1]
    periods = [x.strip() for x in worktime.split("/")]
    date_ranges = []
    base_date = datetime.datetime(2020, 10, 26)
    range_dict = {}
    for period in periods:
        days = []
        extra_day = None
        period = period.split(" ")  # [Mon-Sun, 11:00, am, -, 10pm]
        split_range = 0
        if len(period) > 6:  # Period list will be longer than 6 ONLY if a day and day range are included or there are just simply two days.
            eject_day = period[0]
            if "-" in period[0]:
                eject_day = period[1]
            extra_day = days_listed[weekdays[eject_day.replace(",", "")]]
            period.remove(eject_day)
        days = period[0].replace(",", "").split("-")
        if len(days) > 1:
            days_open = days_listed[weekdays[days[0]]:weekdays[days[1]]+1]
        else:
            days_open = [days_listed[weekdays[days[0]]]]  # Only 1 day is present in the period so turn it into a one-element list
        if extra_day:
            days_open.append(extra_day)  # Appending the extra day which does not fall under the day range
        first_hour = ''.join(period[1:3])
        second_hour = period[4]
        if second_hour.find(":") == -1:
            second_hour = second_hour + ":00"
        if not "am" in period[4] or "pm" in period[4]:
            second_hour = second_hour + period[5]  # This means that AM/PM has been left out by the original split(" ") so it's added back again here
        for day in days_open:
            range_dict[day] = WeekTimeRange(first_hour, second_hour)
    r = Restaurant(restaurant[0], range_dict)
    return r



def find_open_restaurants(csv_filename: "", search_datetime: datetime) -> []:
    """
    Returns all open restaurants during the given datetime.
    Parameters:
    csv_filename (string): Name of the CSV file
    search_datetime (datetime): datetime object to check restaurants worktimes against
    """
    day_to_search = search_datetime.strftime("%A")
    restaurants = open_csv()
    open_restaurants = []
    for r in restaurants:
        if day_to_search in r.opened_range.keys():
            if search_datetime in r.opened_range[day_to_search]:
               open_restaurants.append(r.name)
    return open_restaurants


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-csv", type=str, default="restaurants.csv", action="store", dest="csv")
    parser.add_argument("-datetime", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M'), default=datetime.datetime.now(), action="store", dest="datetime")
    args = parser.parse_args()
    restaurants = open_csv(args.csv)
    res = find_open_restaurants(args.csv, args.datetime)
    print("Open Restaurants:\n")
    for r in res:
        print(r)
    print("There are %d open restaurants for the given datetime." % len(res))
