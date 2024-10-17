from .base_scraper import BaseScraper
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
from datetime import datetime

class TheteamsScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.search_querys = ['데이터', '백엔드']

    # def scrap(self):
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


class IncruitScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.all_jobs = []

    # 지역명 정리
    def clean_region_name(self, region):
        cleaned_region = re.sub(r'\s외.*$', '', region)
        return cleaned_region

    # 경력 정리
    def clean_career(self, career):
        if '신입' in career:
            return '신입'
        return career

    # 마감일 변환
    def convert_end_date(self, end_date):
        today = datetime.now()

        # "23시 마감" 형식 처리
        if "마감" in end_date:
            return today.strftime('%Y-%m-%d')

        # "~10.21 (월)" 형식 처리
        match = re.search(r'~(\d{1,2})\.(\d{1,2})', end_date)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            return today.replace(month=month, day=day).strftime('%Y-%m-%d')

        # 다른 형식은 그대로 반환
        return end_date
    
    def scrap(self):
        with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
            url = 'https://job.incruit.com/jobdb_list/searchjob.asp?occ3=16935&occ3=16501&occ3=16182&occ3=14780&occ3=17030&occ3=16895&occ3=16865&occ3=16761&occ3=16903&occ2=632&page=1'
            driver.get(url)
            time.sleep(3)
            page_num = 1  # 페이지 번호를 추적하기 위한 변수 추가
            while True:
                print(f"현재 {page_num} 페이지 크롤링 중입니다.")
                jobs = driver.find_elements(By.CLASS_NAME, 'c_col')

                for job in jobs:
                    try:
                        company_name = job.find_element(By.CLASS_NAME, 'cell_first').find_element(By.TAG_NAME, 'a').text
                        mid = job.find_element(By.CLASS_NAME, 'cell_mid')
                        title = mid.find_element(By.TAG_NAME, 'a').text
                        detail_url = mid.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        spans = mid.find_elements(By.TAG_NAME, 'span')

                        filtered_spans = [span for span in spans if 'highlight' not in span.get_attribute('class')]

                        if len(filtered_spans) > 2:
                            region = filtered_spans[2].text
                        else:
                            region = ""
                        if len(filtered_spans) > 0:
                            career = filtered_spans[0].text
                        else:
                            career = ""
                        end_date = job.find_element(By.CLASS_NAME, 'cell_last').find_element(By.CLASS_NAME, 'cl_btm').find_element(By.TAG_NAME, 'span').text

                        job_info = {
                            "title": title,
                            "company_name": company_name,
                            "detail_url": detail_url,
                            "end_date": self.convert_end_date(end_date),
                            "platform_name": "incruit",
                            "category_name": "",  
                            "stack": "",  
                            "region": self.clean_region_name(region),
                            "career": self.clean_career(career)
                        }

                        print(job_info)
                        self.request_save(job_info)

                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                
                try:
                    next_button = driver.find_element(By.CLASS_NAME, 'next_n')
                    if "disabled" in next_button.get_attribute("class"):
                        print("마지막 페이지입니다. 크롤링을 종료합니다.")
                        break

                    print(f"{page_num} 페이지에서 다음 페이지로 이동 중입니다.")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                    page_num += 1
                except Exception as e:
                    print(f"페이지 이동 중 오류 발생: {e}")
                    break
