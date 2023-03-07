from selenium.webdriver.common.by import By
import csv
import time

class Auction():
    def __init__(self, navigator, config):
        self.navigator = navigator
        self.config = config
        pass

    def click(self, path, type='xpath'):
        if type == 'xpath':
            self.navigator.find_element(By.XPATH, self.config['XPaths'][path]).click()
        if type == 'name':
            self.navigator.find_element(By.NAME, self.config['XPaths'][path]).click()
    
    def translate_title(self, title):
        english_titles = {'Ano': 'YEAR', 'Km': 'KM', 'Combustível': 'FUEL', 'Cor': 'COLOR',
                          'Estimativa de mercado': 'FIPE', 'Pátio': 'YARD', 'Retomada': 'RESUME-TYPE',
                          'Tipo': 'TYPE', 'Possui Chave': 'HAS-KEY'}
        return english_titles[title]
    
    def get_element_text(self, path):
        value = self.navigator.find_element(By.XPATH, self.config['XPaths'][path]).text
        return value

    def get_vehicle_data(self):
        data = {}
        for i in range(1,10):
            try:     
                result = self.navigator.find_element(By.XPATH,f"/html/body/div[2]/div/div[1]/main/div[2]/div[2]/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div[{i}]/div/div").text.split('\n')
                data[self.translate_title(result[0])] = result[1]
                # title.append(result[0])                
                # value.append(result[1])
            except:
                pass

        # data = {self.translate_title(title[i]): value[i] for i in range(len(title))}
        return data

    def write_csv(self, name, cars):
        with open(f'{name}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = cars[0].keys())
            writer.writeheader()
            writer.writerows(cars)
    
    def get_full_information(self):
        car_info = self.get_vehicle_data()
        full_car_info = {'BATCH': self.get_element_text('BATCH'),
                        'VEHICLE': self.get_element_text('VEHICLE'),
                        'BANK':self.get_element_text('BANK'),
                        'KM':'',
                        'YEAR': '',
                        'FUEL': '',
                        'COLOR': '',
                        'FIPE': '',
                        'YARD': '',
                        'RESUME-TYPE': '',
                        'TYPE':'',
                        'HAS-KEY': ''
            }
        full_car_info.update(car_info)
        return full_car_info

    def get_all_vehicles(self, total_results, delay = 8):
        vehicles = []

        for _ in range(1, total_results+1):
            try:
                data = self.get_full_information()
                vehicles.append(data)
                time.sleep(delay)
                self.click('NEXT_VEHICLE') 
            except:
                print('error')
                self.click('NEXT_VEHICLE') 
        
        return vehicles

    def click_first_car(self):
        for i in range(1,6):
            try:
                self.click(f'FIRST-CAR-{i}')
                time.sleep(5)
                return
            except:
                # click_first_car()
                time.sleep(5)