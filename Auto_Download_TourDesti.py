from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import os

file_path = 'C:/Users/user/Downloads'  # 다운로드 받을 곳
file_destination = 'C:/Users/user/Downloads/데이터'  # 알집 파일 이름 바꾸고 옮겨줄 곳
driver = webdriver.Chrome()
driver.implicitly_wait(5)

# 관광지별 대시보드 페이지
driver.get('https://datalab.visitkorea.or.kr/datalab/portal/loc/getTourDataForm.do')

# 로그인
sleep(0.2)
driver.find_element_by_css_selector('#wrap > header > div.util-wrap > div > div.member > a.btn_login.border-right').click()
sleep(0.2)
driver.find_element_by_css_selector('#mbrId').send_keys('wnstjq1254@naver.com')
sleep(0.2)
driver.find_element_by_css_selector('#mbrPw').send_keys('wnstjq12!')
sleep(0.2)
driver.find_element_by_css_selector('#content > div > div > input.table-btn.floatright.btn').click()

# 다운로드
sleep(0.5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
Do_times = soup.select('#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) > g > g:nth-child(4) > g > g')
for i in range(len(Do_times) - 2):
    sleep(0.5)
    driver.find_element_by_css_selector(f'#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) > g > g:nth-child(4) > g > g:nth-child({i+3})').click()
    sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    Si_times = soup.select('#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g > g:nth-child(2) > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) > g > g:nth-child(4) > g > g')
    for j in range(len(Si_times) - 4):
        try:
            sleep(0.5)
            driver.find_element_by_css_selector(f'#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g > g:nth-child(2) > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) > g > g:nth-child(4) > g > g:nth-child({j+5})').click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            gu_times = soup.select('#tourIdCnt')
        except:
            print(i, j)
            continue
        for k in range(int(gu_times[0].text)):
            try:
                sleep(0.5)
                driver.find_element_by_css_selector(f'#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g > g:nth-child(2) > g:nth-child(1) > g:nth-child(2) > g:nth-child(1) >  g > g:nth-child(4) > g > g:nth-child({k+3}) > g > g:nth-child(1)').click()
                sleep(6.5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.select('#contInfo1')
                if '/' in name:
                    name.replace('/', '')
                loc = soup.select('#contInfo2')
                sleep(0.5)
                driver.find_element_by_css_selector('#btnAllDn').click()
                sleep(0.5)
                driver.find_element_by_css_selector('#rdoDataUtilExmn5').click()
                sleep(0.5)
                driver.find_element_by_css_selector('#submit').click()
                sleep(7.5)
                driver.back()
                file_names = os.listdir(file_path)
                file_oldname = os.path.join(file_path, file_names[0])
                file_newname_newfile = os.path.join(file_path, f"{loc[0].text}_{name[0].text}.zip")
                os.rename(file_oldname, file_newname_newfile)
            except:
                print(i, j, k)
                continue
        sleep(0.5)
        driver.find_element_by_css_selector('#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g > g:nth-child(2) > g:nth-child(3) > g:nth-child(1)').click()
    sleep(0.5)
    driver.find_element_by_css_selector('#chart_01 > div > svg > g > g:nth-child(2) > g:nth-child(1) > g > g > g:nth-child(2) > g:nth-child(3) > g:nth-child(1)').click()

