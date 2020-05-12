import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2
farmNumber = 0
while farmNumber < 49:
    pyautogui.moveTo(659 * 1.25, (280 * 1.25) + (farmNumber * 12))
    pyautogui.middleClick()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'tab')
    pyautogui.moveTo(678 * 1.25, 238 * 1.25)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(761 * 1.25, 191 * 1.25)
    pyautogui.click()
    pyautogui.write("1300")
    pyautogui.moveTo(668 * 1.25, 229 * 1.25)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.3)
    farmNumber += 1
