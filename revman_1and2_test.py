from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
import time
import os
import zipfile 

# STEP1 RevMan(.rm5)파일을 코크란 웹페이지 서비스를 이용해 .zip파일로 변환해서 디렉터리에 저장하기

# Chrome 드라이버 설정
driver = webdriver.Chrome()

# 로그인 페이지 접속
driver.get("https://login.cochrane.org/realms/cochrane/protocol/openid-connect/auth?client_id=revman-web&redirect_uri=https%3A%2F%2Frevman.cochrane.org&response_type=code&scope=openid%20profile&nonce=f877d7f1073b4d3c626f529c30ed00116bls6C5Si&state=498cbfe6935e9c812e1f33437daa562f957MAN7MV&code_challenge=DozOT2QUNGgVCQwVoQuhmnIII3DjRi2B3cNl3CFvzvk&code_challenge_method=S256")

# 아이디와 비밀번호 입력
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")
username_field.send_keys("kevinkim1709@gmail.com")
password_field.send_keys("Kingkang11980!")

# 로그인 버튼 클릭
login_button = driver.find_element(By.ID, "btnLogin")
login_button.click()

# 페이지 로딩 대기
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Convert Revman 5 file 버튼 클릭
convert_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[_ngcontent-ng-c822509047][href='/rm5Converter']")))
convert_button.click()

# .rm5 파일이 있는 디렉토리
rm5_dir = r"C:\Users\SAMSUNG\Desktop\rm5 files"

# 모든 .rm5 파일에 대해 작업 수행
for rm5_file in os.listdir(rm5_dir):
    if rm5_file.endswith('.rm5'):
        file_path = os.path.join(rm5_dir, rm5_file)
        
        # 파일 선택 버튼 찾기
        file_picker = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-test='file-picker']")))
        
        # 파일 경로 입력
        file_picker.send_keys(os.path.abspath(file_path))
        
        # 파일 업로드 완료 대기
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span")))

        # 버튼이 활성화될 때까지 대기
        export_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()=' Export data package']]")))

        # 버튼 클릭해서 .zip 파일 다운로드
        export_button.click()

        # 파일이 다운로드될 때까지 대기
        time.sleep(10)  # 필요에 따라 대기 시간 조정

        # 다운로드된 .zip 파일이 있는 디렉토리
        source_dir = r"C:\Users\SAMSUNG\Downloads"
        # 이동할 디렉토리
        destination_dir = r"C:\Users\SAMSUNG\Desktop\zip files"

        # 다운로드된 모든 .zip 파일 찾기
        files = [f for f in os.listdir(source_dir) if f.endswith('.zip')]
        for file in files:
            src = os.path.join(source_dir, file)
            dst = os.path.join(destination_dir, file)
            
            # 파일 이동
            shutil.move(src, dst)
            print(f"Moved file {file} to {destination_dir}")

# 브라우저 종료
driver.quit()


#STEP2 .zip 파일 내의 CSV파일을 읽어서 별도의 디렉터리에 CSV파일만 저장하기

# 경로 설정
zip_dir = "C:\\Users\\SAMSUNG\\Desktop\\zip files"
output_dir = "C:\\Users\\SAMSUNG\\Desktop\\included_articles"

def extract_zip(file_path, extract_to):
    """압축 해제 함수"""
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted {file_path} to {extract_to}")

def find_and_move_excel_files(directory_path):
    """-study-information 엑셀 파일을 output_dir로 이동"""
    print(f"Searching for Excel files in {directory_path}")
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('-study-information.csv'):
                source_path = os.path.join(root, file)
                destination_path = os.path.join(output_dir, file)
                try:
                    shutil.move(source_path, destination_path)
                    print(f"Moved {file} from {source_path} to {destination_path}")
                except Exception as e:
                    print(f"Failed to move {file} from {source_path} to {destination_path}: {e}")

def process_zip(file_path, processed_files):
    """ZIP 파일 처리 함수"""
    extract_to = os.path.join(zip_dir, os.path.splitext(os.path.basename(file_path))[0])
    
    # 이미 처리된 파일이면 건너뜁니다.
    if file_path in processed_files:
        return

    processed_files.add(file_path)
    extract_zip(file_path, extract_to)
    
    # 새로 생성된 파일들 확인
    for item in os.listdir(extract_to):
        item_path = os.path.join(extract_to, item)
        if os.path.isdir(item_path):
            print(f"Found directory: {item_path}")
            # -study-data 폴더를 찾기 위해 확인
            if item.endswith('-data'):
                # -study-data 폴더 내에서 엑셀 파일 찾기
                find_and_move_excel_files(item_path)
            else:
                # 다른 디렉토리인 경우 재귀적으로 처리
                process_directory(item_path, processed_files)
        elif item.endswith('.zip'):
            process_zip(item_path, processed_files)

def process_directory(directory_path, processed_files):
    """디렉토리 내의 파일 처리"""
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            print(f"Found directory: {item_path}")
            process_directory(item_path, processed_files)
        elif item.endswith('.zip'):
            process_zip(item_path, processed_files)

def main():
    processed_files = set()
    
    for filename in os.listdir(zip_dir):
        if filename.endswith('.zip'):
            file_path = os.path.join(zip_dir, filename)
            process_zip(file_path, processed_files)

if __name__ == "__main__":
    main()
