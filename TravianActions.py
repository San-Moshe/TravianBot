import re
import time
from enum import Enum
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import CaptchaSolver
import FileUtils
from TravianContract import TroopsBarracksContract, TroopsFarmListContract, TroopsType


class TravianActions:
    last_oasis_raid_index = 0
    last_farm_raid_index = 0
    base_url = "https://s1.ss-travi.com/"
    driver = webdriver.Chrome(executable_path="C:\Program Files\ChromeDriver\chromedriver.exe")
    web_driver_wait = WebDriverWait(driver, 2)

    def __init__(self):
        self.troops_farm_list_contract = TroopsFarmListContract()

    def login(self, username_text, password_text):
        self.driver.get(self.base_url)
        username = self.web_driver_wait.until(EC.visibility_of_element_located((By.NAME, "namee")))
        password = self.web_driver_wait.until(EC.visibility_of_element_located((By.NAME, "pass")))
        username.send_keys(username_text)
        password.send_keys(password_text)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        self.driver.get(self.base_url + "profile.php")
        return self.web_driver_wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, r'//*[@id="profile"]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td'))).text

    def _raid_farm_by_link(self, farm_link, number_of_troops):
        self.driver.get(farm_link)
        self.web_driver_wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "» Send troops"))).click()
        club = self.web_driver_wait.until(EC.visibility_of_element_located((By.ID, "t1")))
        club.send_keys(number_of_troops)
        self.driver.find_element_by_xpath("//input[@type='radio'][@value = '4']").click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        self.web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='submit']"))).click()

    def raid_farms_from_farm_list(self, number_of_troops):
        self.driver.get(self.base_url + "farmlist.php")
        self.driver.implicitly_wait(2)
        farms = self.driver.find_elements_by_partial_link_text("Farm")
        farms_links = tuple(map(lambda farm: farm.get_attribute("href"), farms))
        relevant_farms = farms_links[self.last_oasis_raid_index % len(farms_links):]
        for farm in relevant_farms:
            time.sleep(7)
            self.last_farm_raid_index += 1
            self._raid_farm_by_link(farm, number_of_troops)

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

    def raid_custom_farm_list(self, number_of_troops):
        oasises = FileUtils.read_all_oasis_from_file()
        relevant_oasises = oasises[self.last_oasis_raid_index % len(oasises):]
        for oasis in relevant_oasises:
            time.sleep(7)
            self.last_oasis_raid_index += 1
            self._raid_farm_by_link(oasis, number_of_troops)

    def train_soldiers_in_barracks(self, troops_type):
        self.driver.get("//area[contains(@alt,'Barracks')]")
        troops_id = None
        if troops_type == TroopsType.ATTACKER:
            troops_id = TroopsBarracksContract.CLUBSWINGER
        else:
            troops_id = TroopsBarracksContract.SPEARMAN

        self.web_driver_wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, r'//*[@id="build"] and [contains(@onclick, "troops_id)"]'))).click()
        self.driver.find_element_by_id("btn_train").click()

    def train_soldiers_in_stable(self, troops_type):
        self.driver.get("//area[contains(@alt,'Stable')]")

        troops_id = None
        if troops_type == TroopsType.ATTACKER:
            troops_id = TroopsBarracksContract.CLUBSWINGER
        else:
            troops_id = TroopsBarracksContract.SPEARMAN

        self.web_driver_wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, r'//*[@id="build"] and [contains(@onclick, "troops_id)"]'))).click()
        self.driver.find_element_by_id("btn_train").click()

    def add_farm_account_to_farm_list(self, tribe, troops_raid_type, number_of_soldiers):
        self.driver.get(self.base_url + "profile.php?uid=6")
        self.driver.implicitly_wait(2)
        elements = list(map(lambda element: element.find_element_by_xpath(".//a").get_attribute("href"),
                            tuple(self.web_driver_wait.until(
                                EC.visibility_of_all_elements_located((By.CLASS_NAME, "nam"))))))
        for farm in elements:
            self.driver.get(farm)
            self.web_driver_wait.until(
                EC.visibility_of_element_located((By.XPATH, r'//*[@id="options"]/tbody/tr[4]/td/a'))).click()
            self.web_driver_wait.until(EC.visibility_of_element_located(
                (By.NAME, self.troops_farm_list_contract.get_troops_by_tribe(tribe, troops_raid_type)))).send_keys(
                number_of_soldiers)
            self.driver.find_element_by_xpath("//input[@type='submit']").click()
