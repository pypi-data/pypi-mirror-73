import re


class Car:

    def __init__(self, car):
        self.account_id = car['data-accountid']
        self.body_style = car['data-bodystyle']
        self.city = car['data-city']
        self.classification = car['data-classification']
        self.doors = car['data-doors']
        self.drive_train = car['data-drivetrain']
        self.engine = car['data-engine']
        self.make = car['data-make']
        self.model = car['data-model']
        self.state = car['data-state']
        self.transmission = car['data-transmission']
        self.trim = car['data-trim']
        self.uuid = car['data-uuid']
        self.vin = car['data-vin']
        self.year = car['data-year']
        self.zip_code = car['data-zipcode']
        self.drive_line = car['data-driveline']
        self.city_fuel_economy = car['data-cityfueleconomy']
        self.ext_color = car['data-exteriorcolor']
        self.int_color = car['data-interiorcolor']
        self.car_url = 'https://www.hertzcarsales.com' + car.find('a', {'class': re.compile('url')})['href']
        self.odometer = car.find('span', {'data-name': re.compile('odometer')}).span.text.split()[0].replace(',', '')
        self.prices = car.findAll('span', {'class': re.compile('value')})
        if len(self.prices) == 3:
            self.kbb_price = int(self.prices[0].text.strip().replace(',', '').replace('$', ''))
            self.diff = int(self.prices[1].text.strip().replace(',', '').replace('$', ''))
            self.actual_price = int(self.prices[2].text.strip().replace(',', '').replace('$', ''))
            self.saving = self.diff / self.kbb_price * 100
        else:
            try:
                self.actual_price = int(self.prices[0].text.strip().replace(',', '').replace('$', ''))
                self.kbb_price = self.actual_price
            except Exception as e:
                print("Failed to convert Integer: ", e)
            self.diff = 0
        self.saving = round(self.saving, 2)

    def __repr__(self):

        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}" \
            .format(self.saving, self.actual_price, self.diff, self.make, self.odometer, self.year, self.model,
                    self.body_style, self.kbb_price, self.state, self.city, self.ext_color, self.int_color,
                    self.car_url, self.drive_line, self.transmission, self.city_fuel_economy, self.engine, self.doors,
                    self.vin, self.zip_code, self.drive_train, self.classification, self.trim, self.uuid,
                    self.account_id)
