# 필요한 라이브러리 가져오기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def crawl_dynamic_comments(start_url, output_file="dynamic_comments.txt", max_depth=2):
    """
    Selenium을 사용해 동적으로 로드되는 댓글 크롤링 함수.
    
    :param start_url: 크롤링 시작 URL (뉴스 사이트 메인 URL)
    :param output_file: 댓글 정보를 저장할 파일 이름
    :param max_depth: BFS 탐색 깊이 제한
    """
    # Chrome 드라이버 설정
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 브라우저를 표시하지 않음
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Chrome 드라이버 경로 설정
    service = Service('C:\\chromedriver\\chromedriver.exe')  # 크롬드라이버의 경로를 입력하세요
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 초기화
        visited = set()
        to_visit = [(start_url, 0)]
        results = []

        # BFS 방식으로 URL 탐색
        while to_visit:
            current_url, depth = to_visit.pop(0)

            # 깊이 초과 시 중단
            if depth > max_depth:
                continue

            if current_url in visited:
                continue

            visited.add(current_url)

            # 페이지 로드
            print(f"URL 로드 중: {current_url}")
            driver.get(current_url)
            time.sleep(3)  # 페이지 로드 대기

            # 댓글을 포함한 링크 탐색
            try:
                article_links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
                for link in article_links:
                    href = link.get_attribute("href")
                    if href and "section=politics" in href and href not in visited:
                        to_visit.append((href, depth + 1))

                # 댓글 섹션 탐색
                try:
                    # 댓글 컨테이너 대기
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "reply-wrapper"))
                    )
                    comments = driver.find_elements(By.CLASS_NAME, "reply-wrapper")

                    # 댓글 데이터 추출
                    comment_data = []
                    for comment in comments:
                        try:
                            writer = comment.find_element(By.CLASS_NAME, "writer-name-text").text.strip()
                            content = comment.find_element(By.CLASS_NAME, "reply-content").text.strip()
                            timestamp = comment.find_element(By.CLASS_NAME, "modify-time").get_attribute("title")
                            comment_data.append({
                                "writer": writer,
                                "content": content,
                                "timestamp": timestamp
                            })
                        except Exception as e:
                            print(f"댓글 추출 실패: {e}")
                            continue

                    # 결과 저장
                    if comment_data:
                        results.append({
                            "url": current_url,
                            "comments": comment_data
                        })
                except Exception as e:
                    print(f"댓글 섹션 로드 실패: {e}")

            except Exception as e:
                print(f"링크 추출 실패: {e}")
                continue

        # 결과를 파일에 저장
        if results:
            with open(output_file, "w", encoding="utf-8") as file:
                for result in results:
                    file.write(f"기사 URL: {result['url']}\n")
                    file.write("댓글:\n")
                    for comment in result["comments"]:
                        file.write(f"  작성자: {comment['writer']}\n")
                        file.write(f"  내용: {comment['content']}\n")
                        file.write(f"  작성 시간: {comment['timestamp']}\n")
                        file.write("\n")
                    file.write("\n")
            print(f"댓글 정보가 '{output_file}'에 저장되었습니다.")
        else:
            print("댓글이 포함된 기사를 찾을 수 없습니다.")
    finally:
        # 드라이버 종료
        driver.quit()

# 함수 호출 예시
start_url = "https://www.yna.co.kr/"  # 뉴스 사이트 메인 URL 입력
crawl_dynamic_comments(start_url, max_depth=2)


