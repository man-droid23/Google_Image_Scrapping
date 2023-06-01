from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
import time
import requests

class Image_Scrapping():
    def teardown_method(self, method):
        self.driver.quit()

    def scroll_down_to_bottom(self):
        last_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(2)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

    def check_show_more_button(self):
        try:
            show_more_button = self.driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
            show_more_button.click()
        except:
            pass

    def define_constants(self, keyword):
        self.keyword = keyword
        self.google_images = 'https://www.google.com/imghp?hl=en'
        self.scroll_pause_time = 3
        self.images_folder = os.path.join('images', self.keyword)

    def create_images_folder(self):
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

    def create_chrome_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)

    def scrapping_image(self):
        self.driver.get(self.google_images)
        search_box = self.driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        search_box.send_keys(self.keyword)
        search_box.send_keys(Keys.ENTER)
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        self.check_show_more_button()
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        self.scroll_down_to_bottom()
        images = self.driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')
        image_urls = set()
        for image in images:
            try:
                image_url = image.get_attribute('src')
                if image_url and image_url.startswith('http'):
                    image_urls.add(image_url)
            except:
                continue
        return image_urls
    
    def download_image(self, image_url, image_path):
        try:
            image_content = requests.get(image_url).content
        except Exception as e:
            print(f'ERROR - Could not download {image_url} - {e}')
        try:
            f = open(image_path, 'wb')
            f.write(image_content)
            f.close()
            print(f'SUCCESS - saved {image_url} - as {image_path}')
        except Exception as e:
            print(f'ERROR - Could not save {image_url} - {e}')

    def download_images(self, image_urls):
        for i, image_url in enumerate(image_urls):
            self.download_image(image_url, f'{self.images_folder}/{self.keyword}_{i+1}.jpg')

    def main(self, keyword):
        self.define_constants(keyword)
        self.create_images_folder()
        self.create_chrome_driver()
        image_urls = self.scrapping_image()
        self.download_images(image_urls)

if __name__ == '__main__':
    image_scrapping = Image_Scrapping()
    image_scrapping.main('ayam goreng')
    image_scrapping.main('brokoli')
    image_scrapping.main('kentang')
    image_scrapping.main('nasi goreng')
    image_scrapping.main('sate')
    image_scrapping.main('soto')
    image_scrapping.main('kangkung')
    image_scrapping.main('mie goreng')
    image_scrapping.main('mie rebus')
    image_scrapping.main('rendang')
    image_scrapping.main('sambal')
    image_scrapping.main('nasi putih')
    image_scrapping.teardown_method('')