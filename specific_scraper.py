from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

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

class ProgrammersScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터'] 

    def scrap(self):
        search_querys = self.search_querys

        with webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="129.0.6668.103").install())) as driver:  
            for keyword in search_querys:
                url = "https://career.programmers.co.kr/job?page=1&order=recent&job_category_ids=5&job_category_ids=11&job_category_ids=12&job_category_ids=92/?search_query={}".format(keyword)
                driver.get(url)

                while True:
                    try:
                        # 각 페이지가 완전히 로드될 때까지 대기
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#list-positions-wrapper > ul > li"))
                        )
                    except Exception as e:
                        print(f"Error extracting element data: {e}")
                        break

                    # BeautifulSoup으로 페이지 파싱
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    job_element = soup.select("#list-positions-wrapper > ul > li") # 페이지의 모든 공고 탐색

                    # 각 공고의 정보 추출
                    for element in job_element:
                        try:
                            company_name = element.select_one("h6.company-name > a")
                            title_tag = element.select_one("h5.position-title > a")
                            link_tag = element.select_one("a.company-link")
                            tech_stack_elements = element.select("ul.list-position-tags > li")
                            career_tag = element.select_one("li.experience")
                            region_tag = element.select_one("li.location")

                            job_info = {
                                "title": title_tag.get_text(strip=True) if title_tag else "제목 없음",
                                "company_name": company_name.get_text(strip=True) if company_name else "회사명 없음",
                                "detail_url": "https://career.programmers.co.kr" + link_tag["href"] if link_tag else "링크 없음",
                                "end_date": None, # 마감일 정보 없음
                                "platform_name": "programmers",
                                "category_name": None,  # 카테고리 정보 없음
                                "stack": [el.get_text(strip=True) for el in tech_stack_elements] if tech_stack_elements else None,
                                "region": region_tag.get_text(strip=True) if region_tag else "지역 없음",
                                "career": career_tag.get_text(strip=True) if career_tag else "경력/신입 없음"
                            }

                            # 요청 1개씩 바로바로 보내기
                            self.request_save(job_info)
                        except Exception as e:
                            print(f"Error extracting element data: {e}")

                    # 다음 페이지 버튼 탐색 및 클릭 (텍스트 '>' 활용)
                    try:
                        next_button = driver.find_element(By.XPATH, '//span[@class="page-link" and text()=">"]')
                        next_button.click()
                        time.sleep(2)  # 페이지 로딩 대기
                    except Exception as e:
                        print(f"No more pages or error navigating: {e}")
                        break  # 더 이상 페이지가 없으면 종료

        self.request_save(job_info)
        pass