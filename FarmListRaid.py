import webbrowser

import pyautogui
import clipboard

import CaptchaSolver
import RaidSingleFarm
import time

farmNumber = [0]

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


def edit_farms():
    for i in range(285, 296):
        webbrowser.open(f"https://s1.ss-travi.com/farmlist.php?edit={i}", new=2)
        time.sleep(1)
        pyautogui.moveTo(627 * 1.25, 442 * 1.25)
        pyautogui.click()
        pyautogui.write("1300")
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 'w')


def open_farm(number):
    pyautogui.moveTo(712 * 1.25, 193 * 1.25)
    pyautogui.moveRel(0, 8 * (number[0] % 20), _pause=False)
    pyautogui.middleClick()
    number[0] += 1


def create_horses():
    pyautogui.hotkey('ctrl', 'w')
    webbrowser.open("https://s1.ss-travi.com/build.php?id=20", new=2)
    time.sleep(1)
    pyautogui.moveTo(810 * 1.25, 160 * 1.25)
    pyautogui.click()
    pyautogui.moveTo(669 * 1.25, 196 * 1.25)
    pyautogui.click()


def navigate_to_village():
    pyautogui.hotkey('ctrl', 'w')
    webbrowser.open('https://s1.ss-travi.com/village2.php', new=2)
    time.sleep(1)


def open_farm_list():
    pyautogui.hotkey('ctrl', 'w')
    webbrowser.open('https://s1.ss-travi.com/farmlist.php', new=2)
    time.sleep(1)


def download_captcha():
    pyautogui.moveTo(736 * 1.25, 576 * 1.25)
    pyautogui.rightClick()
    pyautogui.moveTo(778 * 1.25, 608 * 1.25)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.press('enter')
    time.sleep(1)
    return "C:\\Users\\sanmo\\PycharmProjects\\traviBot\\captchas\\" + clipboard.paste()


startTime = time.time()
open_farm_list()
while True:
    pyautogui.PAUSE = 0.7
    if time.time() - startTime > 180 / 6:
        startTime = time.time()
        pyautogui.scroll(60)
        pyautogui.moveTo(682 * 1.25, 167 * 1.25)
        pyautogui.click()
        pyautogui.scroll(-300)
        captcha_solution = CaptchaSolver.process_image(download_captcha())
        pyautogui.moveTo(740 * 1.25, 591 * 1.25)
        pyautogui.click(clicks=2)
        pyautogui.write(captcha_solution)
        pyautogui.press('enter')
        time.sleep(1)
        open_farm_list()
    elif farmNumber[0] % 30 == 0:
        pyautogui.scroll(100)
        create_horses()
        navigate_to_village()
        open_farm_list()
        farmNumber[0] += 1
    else:
        time.sleep(7)
        open_farm(farmNumber)
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(1)
        RaidSingleFarm.raid()
        pyautogui.hotkey('ctrl', 'w')
