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
from TravianContract import TroopsFarmListContract, TroopsType, TroopsCustomFarmListContract, \
    FarmRaidLink, FarmType


class TravianActions:
    last_oasis_raid_index = 0
    last_farm_raid_index = 0
    base_url = "https://s2.ss-travi.com/"
    driver = webdriver.Chrome(executable_path="C:\Program Files\ChromeDriver\chromedriver.exe")
    web_driver_wait = WebDriverWait(driver, 2)
    farms_links = None

    def __init__(self):
        self.troops_farm_list_contract = TroopsFarmListContract()
        self.oasises = FileUtils.read_all_oasis_from_file()

    def login(self, username_text, password_text):
        self.driver.get(self.base_url)
        username = self.web_driver_wait.until(EC.visibility_of_element_located((By.NAME, "namee")))
        password = self.web_driver_wait.until(EC.visibility_of_element_located((By.NAME, "pass")))
        username.send_keys(username_text)
        password.send_keys(password_text)
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        self.web_driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, r'//*[@id="side_navi"]/p[1]/a[3]')))
        self.driver.get(self.base_url + "farmlist.php")
        self.driver.implicitly_wait(2)
        farms = self.driver.find_elements_by_partial_link_text("Farm")
        self.farms_links = tuple(map(lambda farm: farm.get_attribute("href"), farms))
        self.driver.get(self.base_url + "profile.php")
        return self.web_driver_wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, r'//*[@id="profile"]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td'))).text

    def _raid_farm_by_link(self, farm_link, number_of_troops, troops_raid_type, tribe, farm_type):
        self.driver.get(farm_link)

        farm_raid_text_link = None
        if farm_type == FarmType.NORMAL_FARM:
            farm_raid_text_link = FarmRaidLink.NORMAL_FARM
        else:
            farm_raid_text_link = FarmRaidLink.OASIS

        self.web_driver_wait.until(EC.visibility_of_element_located((By.LINK_TEXT, farm_raid_text_link.value))).click()
        troop = self.web_driver_wait.until(EC.visibility_of_element_located(
            (By.ID, tribe.get_troops_for_custom_farm_list(troops_name=troops_raid_type))))
        troop.send_keys(number_of_troops)
        self.driver.find_element_by_xpath("//input[@type='radio'][@value = '4']").click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
        self.web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='submit']"))).click()

    def raid_farms_from_farm_list(self, number_of_troops, troops_type, tribe):
        relevant_farms = self.farms_links[self.last_oasis_raid_index % len(self.farms_links):]
        for farm in relevant_farms:
            time.sleep(7)
            self.last_farm_raid_index += 1
            self._raid_farm_by_link(farm, number_of_troops, troops_type, tribe, FarmType.NORMAL_FARM)

    def raid_next_farm_from_farm_list(self, number_of_troops, troops_type, tribe):
        farm = self.farms_links[self.last_farm_raid_index % len(self.farms_links)]
        time.sleep(7)
        self.last_farm_raid_index += 1
        self._raid_farm_by_link(farm, number_of_troops, troops_type, tribe, FarmType.NORMAL_FARM)

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

    def raid_custom_farm_list(self, number_of_troops, troops_raid_type, tribe):
        relevant_oasises = self.oasises[self.last_oasis_raid_index % len(self.oasises):]
        for oasis in relevant_oasises:
            time.sleep(7)
            self.last_oasis_raid_index += 1
            self._raid_farm_by_link(oasis, number_of_troops, troops_raid_type, tribe, FarmType.OASIS)

    def raid_next_farm_in_custom_farm_list(self, number_of_troops, troops_raid_type, tribe):
        oasis = FileUtils.read_oasis_from_file(self.last_farm_raid_index % len(self.oasises))
        time.sleep(7)
        self.last_oasis_raid_index += 1
        self._raid_farm_by_link(oasis, number_of_troops, troops_raid_type, tribe, FarmType.OASIS)

    def train_soldiers_in_barracks(self, troops_type, tribe):
        self.driver.get(self.base_url + "village2.php")
        self.driver.get(self.web_driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, "//area[contains(@alt,'Barracks')]"))).get_attribute("href")
                        )
        # self.driver.find_element_by_xpath("//*[@id='build']/form/table/tbody").find_element_by_xpath(
        #     "//a[contains(@onclick, '_tf12')]")
        troops_id = tribe.get_training_id_by_name(troops_name=troops_type)
        self.web_driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='build']/form/table/tbody"))).find_element_by_xpath(
            f'//a[contains(@onclick, "{troops_id}")]').click()
        self.driver.find_element_by_id("btn_train").click()

    def train_soldiers_in_stable(self, troops_type, tribe):
        self.driver.get(self.base_url + "village2.php")
        self.driver.get(self.web_driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, "//area[contains(@alt,'Stable')]"))).get_attribute("href"))

        troops_id = tribe.get_training_id_by_name(troops_name=troops_type)
        self.web_driver_wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='build']/form/table/tbody"))).find_element_by_xpath(
            f'//a[contains(@onclick, "{troops_id}")]').click()
        self.driver.find_element_by_id("btn_train").click()

    def add_farm_account_to_farm_list(self, tribe, troops_raid_type, number_of_soldiers):
        self.driver.get(self.base_url + "profile.php?uid=9")
        self.driver.implicitly_wait(2)
        elements = list(map(lambda element: element.find_element_by_xpath(".//a").get_attribute("href"),
                            tuple(self.web_driver_wait.until(
                                EC.visibility_of_all_elements_located((By.CLASS_NAME, "nam"))))))
        for farm in elements:
            self.driver.get(farm)
            self.web_driver_wait.until(
                EC.visibility_of_element_located((By.XPATH, r'//*[@id="options"]/tbody/tr[4]/td/a'))).click()
            self.web_driver_wait.until(EC.visibility_of_element_located(
                (By.ID, self.troops_farm_list_contract.get_troops_select_by_type(troops_raid_type)))).click()
            self.web_driver_wait.until(EC.visibility_of_element_located(
                (By.NAME, self.troops_farm_list_contract.get_troops_by_tribe(tribe, troops_raid_type)))).send_keys(
                number_of_soldiers)
            self.driver.find_element_by_xpath("//input[@type='submit']").click()
