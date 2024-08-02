from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

try:
    # 웹사이트 접속
    driver.get('https://www.cochranelibrary.com/')
    
    # 검색 입력 박스 찾기
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'searchText'))
    )
    
    # 검색어 입력
    search_term = ('("IgA Nephropathy" OR "IgA nephropathy") AND '
                   '("Immunosuppressive Therapy" OR "Immunomodulators") AND '
                   '("Sodium-glucose Co-transporter 2 Inhibitors" OR "SGLT2 Inhibitors" OR '
                   '"Placebo" OR "Antiplatelet Agents" OR "Supportive Care" OR "Anticoagulant Therapy") AND '
                   '("Renal Failure" OR "Renal Function" OR "Hematuria" OR "Proteinuria") AND '
                   '("Child" OR "Preschool" OR "Infant" OR "Adolescent")')
    
    search_box.send_keys(search_term)
    search_box.submit()  # 검색 수행
    
    # 검색 결과가 로드될 때까지 대기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, '_scolarissearchresultsportlet_WAR_scolarissearchresults_selectAll'))
    )
    
    # 'Select all' 체크박스 선택
    select_all_checkbox = driver.find_element(By.ID, '_scolarissearchresultsportlet_WAR_scolarissearchresults_selectAll')
    if not select_all_checkbox.is_selected():
        select_all_checkbox.click()
    
    # 'Export selected citation(s)' 버튼 클릭
    export_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-link.export-citation-for-selected-btn'))
    )
    export_button.click()
    
    # 'CSV (Excel)' 버튼 클릭
    csv_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="CSV (Excel)"]'))
    )
    csv_button.click()
    
    # 'Download' 버튼 클릭
    download_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Download"]'))
    )
    download_button.click()
    
    # 잠시 대기 (다운로드가 완료될 때까지)
    time.sleep(10)

finally:
    # 브라우저 종료
    driver.quit()
