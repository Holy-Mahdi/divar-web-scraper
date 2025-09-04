from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service("./chromedriver-win64/chromedriver.exe")

driver =  webdriver.Chrome(service=service)

driver.get("https://divar.ir/s/mashhad")

search_box = driver.find_element(By.CLASS_NAME, "kt-accordion")

print(search_box)

driver.quit()