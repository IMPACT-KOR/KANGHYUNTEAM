import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

# 크롬드라이버의 경로를 지정합니다.
service = Service(r"C:\Users\SAMSUNG\Desktop\python tutorial\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# EMBASE 웹사이트로 이동합니다.
driver.get('https://www.embase.com')

# 쿠키 파일 경로
cookie_file_path = 'cookies.pkl'

# 쿠키를 로드하는 함수
def load_cookies():
    try:
        with open(cookie_file_path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                # 'sameSite' 속성을 제거하여 호환성 문제 방지
                if 'sameSite' in cookie:
                    cookie.pop('sameSite')
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("쿠키 파일이 없습니다. 쿠키를 먼저 저장해 주세요.")
        driver.quit()
        exit()

# 로그인 후 쿠키를 저장하는 단계
if not os.path.exists(cookie_file_path):
    print("로그인 후 쿠키를 저장하려면 브라우저에서 수동으로 로그인하세요.")
    print("로그인 완료 후 Enter 키를 눌러 쿠키를 저장합니다.")
    input("Press Enter after logging in...")
    
    # 쿠키를 저장합니다.
    with open(cookie_file_path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    
    print("쿠키가 저장되었습니다.")
    driver.quit()
    exit()

# 쿠키가 저장되어 있다면 쿠키를 로드하여 로그인 상태 유지
load_cookies()

# 쿠키를 로드한 후 페이지를 새로고침하여 로그인된 상태를 유지합니다.
driver.refresh()

# 페이지가 완전히 로드될 때까지 대기합니다.
time.sleep(10)  # 페이지 로딩 시간이 필요할 수 있으므로 대기 시간 조정

# EMBASE 웹사이트에서 검색 수행
# 검색창을 찾습니다 (검색창의 name 또는 id 속성에 따라 수정 필요)
search_text = "('IgA nephropathy'/exp OR 'IgA nephropathy':ti,ab OR 'Berger disease':ti,ab OR 'IgA glomerulonephritis':ti,ab) AND ('child'/exp OR 'adolescent'/exp OR pediatric:ti,ab OR paediatric:ti,ab OR child*:ti,ab OR adolescen*:ti,ab OR teen*:ti,ab OR youth*:ti,ab OR infant*:ti,ab OR newborn*:ti,ab OR neonat*:ti,ab) AND ('immunosuppressive agent'/exp OR 'immunosuppressive treatment'/exp OR 'immunomodulation'/exp OR immunosuppress*:ti,ab OR immunomodulat*:ti,ab OR 'immune therapy':ti,ab)"
search_label = driver.find_element(By.CSS_SELECTOR, 'label[for="fragments[0].value"]')
search_label.click()

# 검색창의 input 요소를 찾고 텍스트를 입력합니다
search_input = driver.find_element(By.ID, 'fragments[0].value')
search_input.send_keys(search_text)

# 검색 버튼 클릭 (버튼이 활성화될 때까지 대기)
search_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="show-results-button"]')

while not search_button.is_enabled():
    time.sleep(1)  # 1초 간격으로 체크

search_button.click()

# 결과 페이지가 완전히 로드될 때까지 대기합니다.
time.sleep(10)  # 페이지 로딩 시간이 필요할 수 있으므로 대기 시간 조정

# `<select>` 요소를 찾고 선택 가능한 가장 큰 숫자를 선택합니다
select_element = driver.find_element(By.ID, 'selectionAmount')
select = Select(select_element)

# 모든 옵션을 가져와서 가장 큰 숫자를 선택합니다
options = select.options
largest_option = None

for option in options:
    value = option.get_attribute('value')
    # `disabled` 속성이 없는 옵션만 고려하고 'none' 값을 제외
    if not option.get_attribute('disabled') and value != 'none':
        try:
            if largest_option is None or int(value) > int(largest_option.get_attribute('value')):
                largest_option = option
        except ValueError:
            # 'value'가 정수가 아닐 경우 무시
            continue

if largest_option:
    select.select_by_value(largest_option.get_attribute('value'))
    print(f"Selected option: {largest_option.text}")

# "Export" 버튼 클릭
export_button = driver.find_element(By.CSS_SELECTOR, 'span.exportSubmit.textButton')
export_button.click()

# 모달 창이 로드될 때까지 대기
time.sleep(5)  # 모달 로딩 시간 대기 조정

# 모달에서 "Export" 버튼 클릭
modal_export_button = driver.find_element(By.ID, 'modalConfirmControl')
modal_export_button.click()

# 작업 완료 후 브라우저 닫기 
input("작업이 완료됐으면 Enter를 눌러 브라우저를 종료하세요")
driver.quit()