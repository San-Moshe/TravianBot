import pyautogui
import time


def raid():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.2
    pyautogui.moveTo(671 * 1.25, 228 * 1.25)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(671 * 1.25, 130 * 1.25)
    pyautogui.click()
    pyautogui.typewrite("1300")
    pyautogui.moveTo(660 * 1.25, 186 * 1.25)
    time.sleep(0.2)
    pyautogui.click(clicks=3)
    pyautogui.moveTo(662 * 1.25, 198 * 1.25)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(662 * 1.25, 186 * 1.25)
    pyautogui.click()
