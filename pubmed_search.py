from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
    # PubMed 접속
    driver.get('https://pubmed.ncbi.nlm.nih.gov/')
    
    # 검색어 입력
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'id_term'))
    )
    search_query = (
        '("IgA Nephropathy"[Mesh] OR "IgA Nephropathy"[Title/Abstract]) AND '
        '("Immunosuppressive Agents"[Mesh] OR "Immunosuppressive Therapy"[Title/Abstract] OR "Immunomodulators"[Title/Abstract]) AND '
        '("Renal Failure"[Mesh] OR "Renal Function"[Title/Abstract] OR "Hematuria"[Mesh] OR "Proteinuria"[Mesh] OR "Renal Failure"[Title/Abstract] OR "Renal Function"[Title/Abstract] OR "Hematuria"[Title/Abstract] OR "Proteinuria"[Title/Abstract]) AND '
        '("Child"[Mesh] OR "Infant"[Mesh] OR "Adolescent"[Mesh] OR "Preschool"[Mesh] OR "Child"[Title/Abstract] OR "Infant"[Title/Abstract] OR "Adolescent"[Title/Abstract] OR "Preschool"[Title/Abstract])'
    )  # 원하는 검색 쿼리 입력
    search_box.send_keys(search_query)
    
    # 검색 버튼 클릭
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search-btn'))
    )
    search_button.click()
    
    # 검색 결과 로딩 대기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'save-results-panel-trigger'))
    )
    
    # Save 버튼 클릭
    save_button = driver.find_element(By.ID, 'save-results-panel-trigger')
    save_button.click()
    
    # 드롭다운에서 'All results' 선택
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'save-action-selection'))
    )
    select = Select(select_element)
    select.select_by_value('all-results')
    
    # 결과 형식 선택 (CSV)
    format_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'save-action-format'))
    )
    format_select.send_keys('CSV')
    
    # Create file 버튼 클릭
    create_file_button = driver.find_element(By.CSS_SELECTOR, 'button.action-panel-submit')
    create_file_button.click()
    
    # 파일 다운로드 대기 (다운로드 완료를 위한 대기 시간 설정, 필요시 조정 가능)
    time.sleep(15)  # 15초 대기 (다운로드 완료를 보장하려면 이 시간을 적절히 조정하세요)

finally:
    # 브라우저 종료
    driver.quit()
