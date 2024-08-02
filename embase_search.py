from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

# WebDriver 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    # 사이트 열기
    driver.get("https://aml.amc.seoul.kr/")

    # 로그인 페이지로 이동
    login_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="로그인"]')))
    login_link.click()

    # 아이디와 비밀번호 입력 후 로그인
    id_input = wait.until(EC.presence_of_element_located((By.ID, 'id')))
    password_input = driver.find_element(By.ID, 'password')
    id_input.send_keys('20182755')
    password_input.send_keys('19980617')
    submit_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
    submit_button.click()

    # Embase 링크 클릭
    embase_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "https://embase.com")]')))
    embase_link.click()

    # 쿠키 배너 처리
    try:
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        accept_cookies_button.click()
    except:
        pass

    # 페이지가 완전히 로드될 때까지 기다리기
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="search"]')))

    # 검색창에 쿼리 입력
    search_input = driver.find_element(By.XPATH, '//input[@type="search"]')
    search_input.click()
    search_input.send_keys(
        "('IgA nephropathy'/exp OR 'IgA nephropathy') AND "
        "('immunosuppressive therapy'/exp OR 'immunosuppressive therapy' OR 'immunomodulators') AND "
        "('sodium-glucose cotransporter 2 inhibitor'/exp OR 'sodium-glucose cotransporter 2 inhibitor' OR 'placebo'/exp OR 'placebo' OR 'antiplatelet agent'/exp OR 'antiplatelet agent' OR 'supportive care' OR 'anticoagulant therapy') AND "
        "('renal failure'/exp OR 'renal failure' OR 'renal function' OR 'hematuria'/exp OR 'hematuria' OR 'proteinuria'/exp OR 'proteinuria') AND "
        "('child'/exp OR 'child' OR 'preschool'/exp OR 'preschool' OR 'infant'/exp OR 'infant' OR 'adolescent'/exp OR 'adolescent')"
    )

    # 결과 버튼 클릭
    show_results_button = driver.find_element(By.XPATH, '//button[@data-testid="show-results-button"]')
    show_results_button.click()

    # 결과가 로드될 때까지 기다림
    time.sleep(5)

    # 최대 항목 수 선택
    select = wait.until(EC.presence_of_element_located((By.ID, 'selectionAmount')))
    options = select.find_elements(By.TAG_NAME, 'option')
    largest_option = max([opt for opt in options if 'disabled' not in opt.get_attribute('class')], key=lambda x: int(x.text.replace(',', '')))
    largest_option.click()

    # Export 버튼 클릭
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Export"]')))
    export_button.click()

    # CSV 형식 선택
    format_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="embsDropdown opened"]')))
    csv_option = format_dropdown.find_element(By.XPATH, '//span[@data-value="CSV_RECORDS"]')
    csv_option.click()

    # 필요한 필드 선택
    title_checkbox = wait.until(EC.element_to_be_clickable((By.ID, 'exportFieldTitle')))
    author_names_checkbox = driver.find_element(By.ID, 'exportFieldAuthors')
    publication_year_checkbox = driver.find_element(By.ID, 'exportFieldPublicationYear')
    date_of_publication_checkbox = driver.find_element(By.ID, 'exportFieldPublicationDate')

    title_checkbox.click()
    author_names_checkbox.click()
    publication_year_checkbox.click()
    date_of_publication_checkbox.click()

    # Export 버튼 클릭
    export_button = driver.find_element(By.XPATH, '//span[@class="emb-button-text"]')
    export_button.click()

    # 다운로드 버튼 클릭
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="emb-button-text"]')))
    download_button.click()

finally:
    # 브라우저 닫기
    time.sleep(10)  # 다운로드가 완료될 때까지 잠시 기다리기
    driver.quit()
