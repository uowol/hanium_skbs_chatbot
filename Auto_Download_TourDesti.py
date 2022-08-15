from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os

file_path = 'C:/Users/user/Downloads'  # 다운로드 받을 곳. 이 폴더는 비워놓고 시작하는게 좋음.
driver = webdriver.Chrome() # 괄호 안에 '크롬 웹 드라이버 위치' 넣어주기
# 크롬 웹 드라이버는 자기 크롬 버전에 맞는 것 다운 받기. 크롬 -> 설정 -> 메뉴 맨 밑 크롬 정보 에서 버전 확인 가능
# 괄호 안에 위치 넣어 줄 때 (드라이버 속해있는 폴더 경로)/chromedriver.exe 까지 넣기
driver.implicitly_wait(5)

# 관광지별 대시보드 페이지
driver.get('https://datalab.visitkorea.or.kr/datalab/portal/loc/getTourDataForm.do')

# 로그인
sleep(0.5)
driver.find_element_by_css_selector('#wrap > header > div.util-wrap > div > div.member > a.btn_login.border-right').click()
sleep(0.5)
driver.find_element_by_css_selector('#mbrId').send_keys('wnstjq1254@naver.com')
sleep(0.5)
driver.find_element_by_css_selector('#mbrPw').send_keys('wnstjq12!')
sleep(0.5)
driver.find_element_by_css_selector('#content > div > div > input.table-btn.floatright.btn').click()

sleep(0.5)
driver.find_element_by_css_selector('#listView').click()  # 목록으로 보기 버튼

sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-next').click()
sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-back').click()
sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-back').click()
sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-back').click()
sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-back').click()
sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-back').click()
sleep(1.5)
driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-back').click()
sleep(1.5)
driver.find_element_by_css_selector(f'#tabCon2 > div.paging.mt55 > a:nth-child(3)').click()

for times in range(7):  # 장에 대한 반복문(10페이지씩 7장)
    for i in range(10):  # 페이지에 대한 반복문(10페이지 보고 다음 10페이지 반복)
        for j in range(10):  # 목록에 띄워진 10개의 여행지에 대한 반복문
            sleep(2)
            # 목록에 띄워진 여행지들 순서대로 클릭
            driver.find_element_by_css_selector(f'#tabCon2 > ul > li:nth-child({j+1}) > div:nth-child(1) > a').click()
            sleep(12)  # 여기선 로딩이 길어져서 슬립 많이 줌.
            try:
                # 전체 다운로드 버튼 클릭
                driver.find_element_by_css_selector('#btnAllDn').click()
                sleep(0.5)
                # 학술연구 및 과제수행 버튼 클릭
                driver.find_element_by_css_selector('#rdoDataUtilExmn5').click()
                sleep(0.5)
                #  제출 버튼 클릭
                driver.find_element_by_css_selector('#submit').click()
                sleep(15)
                #  파일 명을 바꾸기 페이지의 관광지 기본정보에서 주소, 관광지명 크롤링
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.select('#contInfo1')  # 관광지명 크롤링
                name = name[0].text
                # 관광지명에 '/'가 들어가 있으면 파일 생성에서 오류가 남. 그래서 '/'을 없애줌
                if '/' in name:
                    name = name.replace('/', '')
                # 주소명 크롤링
                loc = soup.select('#contInfo2')
                # 알집 파일 이름 바꾸고 옮겨줄 곳
                file_destination = 'C:/project/hanium/data'
                # 다운받은 폴더에 있는 파일 리스트.
                file_names = os.listdir(file_path)
                # 그 파일중 방금 다운받은 파일. 여기에서 그냥 편하게 [0]인덱스 이용하려고 맨 위에 다운받을 폴더 비워달라고 한 것.
                file_oldname = os.path.join(file_path, file_names[0])
                # 파일을 옮겨줄 위치와 새로 바꿀 이름(주소_관광지명.zip)
                file_newname_newfile = os.path.join(file_destination, f"{loc[0].text}_{name}.zip")
                # 이름, 폴더 바꿔주기
                os.rename(file_oldname, file_newname_newfile)
                sleep(0.5)
                # 다 다운 받았으면 뒤로가기
                driver.back()
                sleep(0.5)
                # 뒤로가기 누르면 지도별로 보여서 목록으로 보기 버튼 다시 클릭
                driver.find_element_by_css_selector('#listView').click()
            except:
                # 혹시 위에서 오류가 나면 그 url을 띄워주고 뒤로 가서 다른 것들을 다시 다운 받게끔 해줌.
                print(driver.current_url)
                if len(os.listdir(file_path)) == 1:
                    os.remove(file_path + '/' + os.listdir(file_path)[0])  # 이 파일이 다운 받아진 이후 오류가 생겼다면 그 파일 삭제
                sleep(0.5)
                driver.back()
                sleep(1.5)
                driver.find_element_by_css_selector('#listView').click()
        if i != 9:
            sleep(1.5)
            # 다음 페이지로 옮기기
            driver.find_element_by_css_selector(f'#tabCon2 > div.paging.mt55 > a:nth-child({i+4})').click()
        elif i == 9:
            sleep(1.5)
            # 만약 10페이지라면 다음 장으로 옮기기
            driver.find_element_by_css_selector('#tabCon2 > div.paging.mt55 > a.table-forward').click()