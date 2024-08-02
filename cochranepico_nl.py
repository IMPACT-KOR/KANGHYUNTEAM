from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

# ChromeDriver 경로 설정
service = Service('/Users/myo/Desktop/Kangs/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# CSV 파일에 저장할 데이터를 보관할 리스트
pico_data_list = []

try:
    driver.get('https://www.cochranelibrary.com/')
    search_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'searchText'))
    )
    search_box.send_keys('Immunosuppressive therapy for IgA nephropathy in children')
    search_box.submit()

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="10.1002/14651858.CD015060.pub2/full"]'))
    ).click()

    # PICO 섹션을 확장
    pico_section = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.fa-caret-up.section-collapse-icon'))
    )
    pico_section.click()  # JavaScript 없이 클릭 가능

    # PICO 데이터 추출
    populations = driver.find_elements(By.CSS_SELECTOR, 'div.pico-column.Population a')
    interventions = driver.find_elements(By.CSS_SELECTOR, 'div.pico-column.Intervention a')
    comparisons = driver.find_elements(By.CSS_SELECTOR, 'div.pico-column.Comparison a')
    outcomes = driver.find_elements(By.CSS_SELECTOR, 'div.pico-column.Outcome a')

    pico_data = {
        'Population': [pop.text for pop in populations],
        'Intervention': [intv.text for intv in interventions],
        'Comparison': [comp.text for comp in comparisons],
        'Outcome': [outc.text for outc in outcomes]
    }

    pico_data_list.append(pico_data)

finally:
    driver.quit()

# 데이터 프레임 생성 및 CSV 파일로 저장
df = pd.DataFrame(pico_data_list)
df.to_csv('/Users/myo/Desktop/Kangs/pico_data.csv', index=False)
print("CSV 파일 저장 완료")

