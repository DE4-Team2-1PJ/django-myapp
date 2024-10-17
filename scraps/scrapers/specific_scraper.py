from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime

class TheteamsScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터', '백엔드']

    def scrap(self):
        search_querys = self.search_querys
        # data_list = []
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:  
            for keword in search_querys:
                url = "https://www.theteams.kr/results/recruit/?search_query={}".format(keword)
                driver.get(url)

                while True:
                    # 현재 URL 출력
                    # print(f"Current URL: {driver.current_url}")
                    # 캡션 클래스 내부에 data를 수집
                    for element in driver.find_elements(By.CLASS_NAME, "caption"):
                        try:
                            category_element = element.find_element(By.CLASS_NAME, "badge_occupation") #카테고리 이름, ex)데이터 사이언스
                            # carrer_element = element.find_elements(By.TAG_NAME, "div")[1] #carrer, ex)신입/경력 , 비고 : 크롤링 페이지에서 요소 안보임.
                            title_element = element.find_element(By.TAG_NAME, "h4") #공고제목, ex) [숨고] Business Data Analyst
                            company_nm_element = element.find_element(By.TAG_NAME, "p") #회사이름, ex) (주)브레이브모바일
                            detial_url_element = element.find_element(By.TAG_NAME, "a") #디테일 페이지 주소
                            

                            job_info = {
                                        "title" : title_element.text.strip(),
                                        "company_name" : company_nm_element.text.strip(),
                                        "detail_url" : detial_url_element.get_attribute("href"),
                                        "end_date" : None,
                                        "platform_name" : "theteams",
                                        "category_name" : category_element.text.strip(),
                                        "stack" : None,
                                        "region" : None,
                                        "career" : None,
                            }
                            #요청 1개씩 바로바로 보내기
                            self.request_save(job_info)
                        except Exception as e:
                            print(f"Error extracting element data: {e}")
                    
                    # 수집한 후 next_page가 있으면 next_page로 이동
                    try:
                        page = driver.find_element(By.CLASS_NAME, "pagination")
                        li_elements = page.find_elements(By.TAG_NAME, "li")
                        
                        # 맨 마지막 엘리먼트는 '다음'이어야 함.
                        li_element = li_elements[-1]
                        if li_element.text.strip() == "다음":
                            print("Moving to the next page...")
                            a_element = li_element.find_element(By.TAG_NAME, "a")
                            a_element.click()  # 다음 페이지 클릭
                            # dom을 다시 reload 하기위해 페이지 새로고침
                            driver.refresh()
                            # time.sleep(1) 
                        else:
                            # 마지막 페이지일 경우 다음 keyword로 넘어감
                            break
                    except Exception as e:
                        print(f"Error navigating to next page: {e}")
                        break
        # self.request_save(data_list)


'''ex) surfit 플랫폼의 경우
1. 클래스의 첫번째 문자는 대문자 입니다.
2. 자신의 Scraper클래스를 만들고 BaseScraper 클래스를 상속받으세요.
3. 생성자 def __init__(self)를 구현하고 super().__init__()으로 부모생성자를 호출해주세요, 그 외에 필요한 필드를 직접 정의하세요.
4. BaseScraper 클래스의 def scrap(self) 는 추상메서드로 구현되어있습니다. 자식클래스에서 반드시 생성하신 후 그 안에다가 크롤링 코드를 넣어주세요.
5. BaseScraper 클래스에 데이터를 저장할 수 있는 def request_save(self, data) 가 구현되어있습니다. data는 1개씩 요청하세요.
6. driver를 이용하실 땐  
' with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver ' 를 이용해서 브라우저가 종료될 수 있도록 해주세요.
7. 코드를 다 작성하셨다면 scrapers > apps.py 파일에 들어가셔서 주석을 확인해주세요.
'''
class SurfitScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터', '백엔드']    
    
    #반드시 구현
    def scrap(self):
        
        #서버에 저장 요청하는 메서드
        data = {
            
        }
        self.request_save(data)
        pass


class CatchScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    def scrap(self):
        # Selenium으로 브라우저 열기
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:

            # 현재 연도를 가져오기
            current_year = datetime.now().year
            
            # 페이지 순회 (1페이지만 수집)
            url = "https://www.catch.co.kr/NCS/RecruitSearch?page=1"  # 검색 키워드를 URL에 추가하지 않음
            driver.get(url)

            try:
                # 특정 요소가 나타날 때까지 기다림
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'tr td p.date'))
                )
            except Exception as e:
                print(f"요소를 찾을 수 없습니다: {e}")
                return  # 크롤링 중단

            # page_source로 페이지의 HTML 가져오기
            html = driver.page_source
            
            # BeautifulSoup을 사용해 HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')

            # 회사명 추출
            company_names = soup.select('tr td.al1 p.name')
            # 공고문 제목 추출
            job_titles = soup.select('tr td a.link')
            # 마감일 추출
            end_dates = soup.select('tr td p.date')

            # 결과 저장 및 출력
            for company, title, date in zip(company_names, job_titles, end_dates):
                # 마감일에서 "~" 이후의 날짜만 추출
                full_date_text = date.get_text().strip()
                if "~" in full_date_text:
                    end_date_str = full_date_text.split("~")[-1].strip()  # "~" 이후의 날짜만 추출
                else:
                    end_date_str = full_date_text  # "~"가 없는 경우 전체 날짜 사용
                
                # 현재 연도 추가 후 날짜 형식 변환
                try:
                    end_date_with_year = f"{current_year}.{end_date_str}"
                    end_date = datetime.strptime(end_date_with_year, '%Y.%m.%d').strftime('%y.%m.%d')
                except ValueError:
                    end_date = end_date_str  # 형식 변환 실패 시 원본 유지

                # 상세 URL 추출 (job_titles에서 href 가져오기)
                detail_url = title['href']  # title 객체에서 href 속성 가져오기
                detail_url = "https://www.catch.co.kr" + detail_url  # 전체 URL 형식으로 변환

                # 요청 1개씩 바로바로 보내기
                job_info = {
                    "title": title.get_text().strip(),  # 공고 제목
                    "company_name": company.get_text().strip(),  # 회사 이름
                    "detail_url": detail_url,  # 디테일 페이지 URL
                    "end_date": end_date,  # 마감일 (현재 연도 포함)
                    "platform_name": "Catch"  # 플랫폼 이름
                }

                self.request_save(job_info)  # 요청을 보내기