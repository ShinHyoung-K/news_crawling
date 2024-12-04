# # 필요한 라이브러리 가져오기
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# def crawl_dynamic_comments(start_url, output_file="dynamic_comments.txt", max_depth=2):
#     """
#     Selenium을 사용해 동적으로 로드되는 댓글 크롤링 함수.
    
#     :param start_url: 크롤링 시작 URL (뉴스 사이트 메인 URL)
#     :param output_file: 댓글 정보를 저장할 파일 이름
#     :param max_depth: BFS 탐색 깊이 제한
#     """
#     # Chrome 드라이버 설정
#     chrome_options = Options()
#     # chrome_options.add_argument("--headless")  # 브라우저를 표시하지 않음
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")

#     # Chrome 드라이버 경로 설정
#     service = Service('C:\\chromedriver\\chromedriver.exe')  # 크롬드라이버의 경로를 입력하세요
#     driver = webdriver.Chrome(service=service, options=chrome_options)

#     try:
#         # 초기화
#         visited = set()
#         to_visit = [(start_url, 0)]
#         results = []

#         # BFS 방식으로 URL 탐색
#         while to_visit:
#             current_url, depth = to_visit.pop(0)

#             # 깊이 초과 시 중단
#             if depth > max_depth:
#                 continue

#             if current_url in visited:
#                 continue

#             visited.add(current_url)

#             # 페이지 로드
#             print(f"URL 로드 중: {current_url}")
#             driver.get(current_url)
#             time.sleep(3)  # 페이지 로드 대기

#             # 댓글을 포함한 링크 탐색
#             try:
#                 article_links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
#                 for link in article_links:
#                     href = link.get_attribute("href")
#                     if href and "section=politics" in href and href not in visited:
#                         to_visit.append((href, depth + 1))

#                 # 댓글 섹션 탐색
#                 try:
#                     # 댓글 컨테이너 대기
#                     WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CLASS_NAME, "reply-wrapper"))
#                     )
#                     comments = driver.find_elements(By.CLASS_NAME, "reply-wrapper")

#                     # 댓글 데이터 추출
#                     comment_data = []
#                     for comment in comments:
#                         try:
#                             writer = comment.find_element(By.CLASS_NAME, "writer-name-text").text.strip()
#                             content = comment.find_element(By.CLASS_NAME, "reply-content").text.strip()
#                             timestamp = comment.find_element(By.CLASS_NAME, "modify-time").get_attribute("title")
#                             comment_data.append({
#                                 "writer": writer,
#                                 "content": content,
#                                 "timestamp": timestamp
#                             })
#                         except Exception as e:
#                             print(f"댓글 추출 실패: {e}")
#                             continue

#                     # 결과 저장
#                     if comment_data:
#                         results.append({
#                             "url": current_url,
#                             "comments": comment_data
#                         })
#                 except Exception as e:
#                     print(f"댓글 섹션 로드 실패: {e}")

#             except Exception as e:
#                 print(f"링크 추출 실패: {e}")
#                 continue

#         # 결과를 파일에 저장
#         if results:
#             with open(output_file, "w", encoding="utf-8") as file:
#                 for result in results:
#                     file.write(f"기사 URL: {result['url']}\n")
#                     file.write("댓글:\n")
#                     for comment in result["comments"]:
#                         file.write(f"  작성자: {comment['writer']}\n")
#                         file.write(f"  내용: {comment['content']}\n")
#                         file.write(f"  작성 시간: {comment['timestamp']}\n")
#                         file.write("\n")
#                     file.write("\n")
#             print(f"댓글 정보가 '{output_file}'에 저장되었습니다.")
#         else:
#             print("댓글이 포함된 기사를 찾을 수 없습니다.")
#     finally:
#         # 드라이버 종료
#         driver.quit()

# # 함수 호출 예시
# start_url = "https://www.yna.co.kr/"  # 뉴스 사이트 메인 URL 입력
# crawl_dynamic_comments(start_url, max_depth=2)


# 필요한 라이브러리 가져오기
import csv
from bs4 import BeautifulSoup
import requests
import re
import os

# 댓글 수집 함수 정의
# 댓글 수집 함수 수정
def collect_comments(url):
    """
    네이버 뉴스 URL에서 댓글을 수집하여 리스트로 반환합니다.
    :param url: 네이버 뉴스 URL
    :return: 수집된 댓글 리스트
    """
    try:
        # 새로운 URL 형식에서 oid와 aid 추출
        match = re.search(r'article/(\d+)/(\d+)', url)
        if not match:
            print(f"URL에서 oid와 aid를 추출할 수 없습니다: {url}")
            return []

        oid = match.group(1)  # 기사 소속 매체 ID
        aid = match.group(2)  # 기사 고유 ID
        page = 1
        header = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "referer": url,
        }
        comments = []

        while True:
            c_url = (
                f"https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society"
                f"&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"
                f"{oid}%2C{aid}&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page={page}"
                f"&refresh=false&sort=FAVORITE"
            )

            # HTML 요청 및 파싱
            response = requests.get(c_url, headers=header)
            if response.status_code != 200:
                print(f"URL 요청 실패: {url}, 상태 코드: {response.status_code}")
                break

            cont = BeautifulSoup(response.content, "html.parser")
            total_comm_match = re.search(r'"comment":(\d+)', str(cont))
            if not total_comm_match:
                print(f"댓글 정보를 찾을 수 없습니다: {url}")
                break

            total_comm = int(total_comm_match.group(1))

            # 댓글 추출
            match = re.findall(r'"contents":"(.*?)"', str(cont))
            comments.extend(match)

            # 댓글이 모두 수집되면 중단
            if total_comm <= page * 20:
                break
            else:
                page += 1

        return comments

    except Exception as e:
        print(f"오류 발생: {e}")
        return []

# CSV에서 URL 읽기
def read_urls_from_csv(input_csv):
    """
    입력된 CSV 파일에서 URL 목록을 읽습니다.
    :param input_csv: 입력 CSV 파일 경로
    :return: URL 리스트
    """
    urls = []
    try:
        with open(input_csv, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 스킵
            for row in reader:
                if row:
                    urls.append(row[0])  # 첫 번째 열에 URL 저장
        return urls
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {input_csv}")
        return []

# 댓글 결과를 CSV로 저장
def save_comments_to_csv(output_csv, results):
    """
    수집된 댓글을 CSV 파일에 저장합니다.
    :param output_csv: 출력 CSV 파일 경로
    :param results: {URL: [댓글 리스트]} 형태의 딕셔너리
    """
    try:
        with open(output_csv, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Comment"])  # 헤더 작성
            for url, comments in results.items():
                for comment in comments:
                    writer.writerow([url, comment])
        print(f"댓글이 '{output_csv}'에 저장되었습니다.")
    except Exception as e:
        print(f"저장 중 오류 발생: {e}")

# 메인 실행 함수
def main(input_csv, output_csv):
    """
    CSV 파일에서 URL을 읽고 댓글을 수집하여 CSV로 저장합니다.
    :param input_csv: 입력 URL 리스트 CSV 파일 경로
    :param output_csv: 출력 댓글 저장 CSV 파일 경로
    """
    urls = read_urls_from_csv(input_csv)
    if not urls:
        print("URL 목록이 비어 있습니다. 종료합니다.")
        return

    results = {}
    for url in urls:
        print(f"댓글 수집 중: {url}")
        comments = collect_comments(url)
        results[url] = comments

    save_comments_to_csv(output_csv, results)

# CSV 파일 경로 설정 및 실행
if __name__ == "__main__":
    input_csv = "C:/work/news_crawling/political_articles.csv"  # 입력 파일 경로 (URL 리스트가 포함된 CSV)
    output_csv = "comments_output.csv"  # 출력 파일 경로 (댓글이 저장될 CSV)
    main(input_csv, output_csv)
