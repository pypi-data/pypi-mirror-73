from bs4 import BeautifulSoup
import re
import requests

from .Car import Car


class HertzCarScraper:

    def __init__(self, url, total_cars):
        self.url = url
        self.total_cars = total_cars
        self.csv_file = None
        self.retries_count = None

    def scrap(self, file="nonname.csv", retries_count=5):
        self.csv_file = open(file, 'w+')
        self.retries_count = retries_count
        self._write_column_name()
        current_car = 0

        while current_car < self.total_cars:

            if current_car == 0:
                page_url = self.url
            else:
                page_url = self.url + '&start=' + str(current_car)

            # Increase the current car
            current_car += 35
            response = None

            for i in range(self.retries_count):
                try:
                    response = self._send_rest_request(page_url)
                    break
                except Exception as e:
                    print("Failed attempt: ", i)

            if not response:
                print("Cannot load HTML page for link: ", page_url)
                continue

            # Parse HTML Content
            soup = BeautifulSoup(response.decode('ascii', 'ignore'), 'html.parser')
            cars = soup.findAll('li', {'class': re.compile('item hproduct clearfix closed certified primary')})

            # for each Car build parse data
            for car in cars:
                car_obj = Car(car)
                self._write_in_csv(car_obj)

        self._close_csv_file()

    def _send_rest_request(self, url):
        return requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                          'Safari/537.36'}).content

    def _close_csv_file(self):
        self.csv_file.close()

    def _write_column_name(self):
        self._write_in_csv(
            "saving,actual_price,diff,make,odometer,year,model,body_style,kbb_price,state,city,ext_color,"
            "int_color,car_url,drive_line,transmission,city_fuel_economy,engine,doors,vin,zipCode,"
            "driveTrain,classification,trim,uuid,account_id\n")

    def _write_in_csv(self, content):
        self.csv_file.write(content)
