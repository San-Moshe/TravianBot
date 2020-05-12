import re
import time
from pathlib import Path

from pynput.mouse import Listener, Button
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import CaptchaSolver
import FileUtils


class TravianUtils:
    base_url = "https://s1.ss-travi.com/"
    driver = webdriver.Chrome(executable_path="C:\Program Files\ChromeDriver\chromedriver.exe")
    web_driver_wait = WebDriverWait(driver, 2)

    def login(self, usernameText, passwordText):
        self.driver.get(self.base_url)
        username = self.web_driver_wait.until(EC.visibility_of_element_located((By.NAME, "namee")))
        password = self.web_driver_wait.until(EC.visibility_of_element_located((By.NAME, "pass")))
        username.send_keys(usernameText)
        password.send_keys(passwordText)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

    def raid_farm_by_link(self, farm_link, number_of_troops):
        self.driver.get(farm_link)
        self.web_driver_wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "» Send troops"))).click()
        club = self.web_driver_wait.until(EC.visibility_of_element_located((By.ID, "t1")))
        club.send_keys(number_of_troops)
        self.driver.find_element_by_xpath("//input[@type='radio'][@value = '4']").click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        self.web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='submit']"))).click()

    def raid_farm_from_farm_list(self):
        self.driver.get(self.base_url + "farmlist.php")
        self.driver.implicitly_wait(2)
        farms = self.driver.find_elements_by_partial_link_text("Farm")
        farms_links = tuple(map(lambda farm: farm.get_attribute("href"), farms))
        for farm_link in farms_links:
            self.raid_farm_by_link(farm_link, "1300")

    def raid_batch_farm_list(self):
        captcha_solution = "0"
        Path("captchas").mkdir(parents=True, exist_ok=True)

        while not re.match('[0-9]{4}', captcha_solution):
            self.driver.get(self.base_url + "farmlist.php")
            self.web_driver_wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, "first"))).click()

            captcha_element = self.driver.find_element_by_id("captcha_image")
            captcha_element.screenshot('captchas/captcha.png')
            captcha_solution = CaptchaSolver.process_image("captchas/captcha.png")

        self.driver.find_element_by_id("captcha_code").send_keys(captcha_solution)
        self.driver.find_element_by_name("send").click()

    def add_oasis_to_custom_farm_list(self):
        time.sleep(0.7)
        oasis_tab = self.driver.window_handles[len(self.driver.window_handles) - 1]
        self.driver.switch_to.window(oasis_tab)
        oasis_url = self.driver.current_url
        self.driver.close()
        FileUtils.append_to_file(oasis_url)
