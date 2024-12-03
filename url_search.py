# 필요한 라이브러리 가져오기
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from queue import Queue

# 정치 관련 URL 탐색 및 큐에 추가된 URL도 기록하는 BFS 함수
def bfs_record_all_with_queue(news_site_url, output_file="political_articles.txt", queue_log_file="queue_log.txt", max_depth=2):
    try:
        # BFS 탐색에 사용할 큐와 방문 기록 집합
        to_visit = Queue()
        visited = set()

        # 초기 URL 추가
        to_visit.put((news_site_url, 0))  # (URL, 깊이)
        visited.add(news_site_url)

        # 정치 기사 URL 저장 리스트
        political_urls = []
        queued_urls = []

        # BFS 탐색 시작
        while not to_visit.empty():
            current_url, depth = to_visit.get()

            # 큐에서 URL을 꺼낼 때 기록
            if current_url not in queued_urls:
                queued_urls.append(current_url)

            # 최대 깊이 초과 시 중단
            if depth > max_depth:
                continue

            try:
                # 현재 URL의 HTML 가져오기
                response = requests.get(current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                print(f"URL 요청 실패: {current_url}, 오류: {e}")
                continue

            # 정치 기사 링크 추출 및 탐색
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)  # 절대 URL로 변환

                # URL이 정치 관련인지 확인
                if '정치' in href or 'politics' in href:
                    # 방문 기록 처리
                    if full_url not in political_urls and 'section=politics' in full_url:
                        political_urls.append(full_url)

                    # BFS 큐에 추가
                    if full_url not in visited:
                        visited.add(full_url)
                        to_visit.put((full_url, depth + 1))

        # 정치 관련 URL 저장
        with open(output_file, 'w', encoding='utf-8') as file:
            for url in political_urls:
                file.write(url + '\n')

        print(f"정치 관련 URL {len(political_urls)}개를 '{output_file}'에 저장했습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

# 함수 호출 예시
news_site_url = "https://www.yna.co.kr/"  # 뉴스 사이트 메인 URL 입력
bfs_record_all_with_queue(news_site_url)
