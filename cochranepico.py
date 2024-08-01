from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
    # 웹 페이지 열기
    driver.get('https://www.cochranelibrary.com/')

    # 로그인 버튼 클릭
    print("로그인 버튼을 찾는 중...")
    try:
        sign_in_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.auxiliary-menu-item.signin.last'))
        )
        print("로그인 버튼 클릭 중...")

        # 버튼이 보일 때까지 대기
        driver.execute_script("arguments[0].scrollIntoView(true);", sign_in_button)
        time.sleep(1)

        # JavaScript를 사용하여 클릭
        driver.execute_script("arguments[0].click();", sign_in_button)
        print("로그인 버튼 클릭 완료")
    except Exception as e:
        print("로그인 버튼 클릭 실패:", e)
        driver.save_screenshot('/Users/myo/Desktop/Kangs/signin_button_error.png')

    # 로그인 창 로딩 대기
    print("로그인 창 로딩 대기 중...")
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.scolaris-modal-content'))
        )
        print("로그인 창 로드 완료")
    except Exception as e:
        print("로그인 창 로딩 실패:", e)
        driver.save_screenshot('/Users/myo/Desktop/Kangs/login_modal_error.png')

    # 로그인 필드 찾기 및 데이터 입력
    print("로그인 필드 찾는 중...")
    try:
        username_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, '_58_INSTANCE_MODAL_login'))
        )
        password_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, '_58_INSTANCE_MODAL_password'))
        )
        print("로그인 필드 찾기 완료")

        username_input.send_keys('id@gmail.com') # 여기에 실제 이메일을 입력
        password_input.send_keys('pw') # 여기에 실제 비밀번호를 입력

        # 로그인 버튼 클릭
        print("로그인 버튼 클릭 중...")
        try:
            login_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.primary'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)

            # JavaScript를 사용하여 클릭
            driver.execute_script("arguments[0].click();", login_button)
            print("로그인 버튼 클릭 완료")

            # 로그인 후 리디렉션 확인
            WebDriverWait(driver, 30).until(
                EC.url_changes('https://www.cochranelibrary.com/')
            )
            print("리디렉션 완료")
        except Exception as e:
            print("로그인 버튼 클릭 실패:", e)
            driver.save_screenshot('/Users/myo/Desktop/Kangs/login_button_error.png')
    except Exception as e:
        print("로그인 필드 찾기 또는 로그인 버튼 클릭 실패:", e)
        driver.save_screenshot('/Users/myo/Desktop/Kangs/login_field_error.png')

    # 검색창에 논문 제목 입력
    print("검색창에 논문 제목 입력 중...")
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'searchText'))
        )
        search_box.send_keys('Immunosuppressive therapy for IgA nephropathy in children')
        search_box.submit()
        
        # 논문 클릭
        print("논문 클릭 중...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="10.1002/14651858.CD015060.pub2/full"]'))
        ).click()

        # PICO 섹션 로딩 대기
        print("PICO 섹션 로딩 대기 중...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'pico'))
        )

        # PICO 데이터 추출
        pico_section = driver.find_element(By.ID, 'pico')

        def extract_pico_data(pico_section):
            def extract_pico_category(category):
                elements = pico_section.find_elements(By.CSS_SELECTOR, f'div.pico-column.{category.lower()} a.pico-link-{category.lower()}')
                return [elem.text for elem in elements]

            data = {
                'Population': extract_pico_category('Population'),
                'Intervention': extract_pico_category('Intervention'),
                'Comparison': extract_pico_category('Comparison'),
                'Outcome': extract_pico_category('Outcome')
            }
            return data

        pico_data = extract_pico_data(pico_section)
        print("PICO 데이터:", pico_data)

    except Exception as e:
        print("검색 또는 PICO 데이터 추출 실패:", e)
        driver.save_screenshot('/Users/myo/Desktop/Kangs/pico_data_error.png')

finally:
    # 브라우저 종료
    driver.quit()
