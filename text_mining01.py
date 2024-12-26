from kiwipiepy import Kiwi
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import pandas as pd

# Kiwi 객체 생성
kiwi = Kiwi()

# 입력 CSV 파일 경로
input_csv = "C:/work/news_crawler/test.csv"

# 명사 추출 리스트
nouns = []

# CSV 파일에서 텍스트 읽기 및 전처리
with open(input_csv, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 헤더 스킵
    for row in reader:
        # CSV의 첫 번째 컬럼(row[0])에서 텍스트 추출
        tokens = kiwi.tokenize(row[0], normalize_coda=False)
        temp = []
        for token in tokens:
            # 명사(NNG, NNP)만 추출
            if token[1] in ['NNG', 'NNP']:
                temp.append(token[0])
        # 하나의 문서를 리스트로 저장
        nouns.append(" ".join(temp))  # TF-IDF 계산을 위해 문자열로 변환

# TF-IDF 계산
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(nouns)

# TF-IDF 결과를 Pandas DataFrame으로 변환
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# TF-IDF 데이터 확인
print("TF-IDF DataFrame:")
print(tfidf_df)

# 결과 저장 (선택)
output_csv = "C:/work/news_crawler/tfidf_results.csv"
tfidf_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"TF-IDF 결과가 {output_csv}에 저장되었습니다.")
