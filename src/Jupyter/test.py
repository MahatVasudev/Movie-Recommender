from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
import time 
import pyautogui

driver = webdriver.Chrome()
# action = ActionChains(driver)#
driver.implicitly_wait(10)
driver.get("https://www.google.com/")
google_search = driver.find_element(By.CLASS_NAME,"gLFyf")
google_search.send_keys("Toy Story 2 Poster")
google_search.submit()
images_link_xpath = "//*[text()='Images']"
image_tab = driver.find_element(By.XPATH, images_link_xpath)
image_tab.click()
image_xpath = 'H8Rx8c'
required_image = driver.find_element(By.CLASS_NAME, image_xpath)
required_image.click()
the_image = driver.find_element(By.XPATH,'//img[@jsname="kn3ccd"]')

print(the_image.get_attribute('src'))

time.sleep(10)