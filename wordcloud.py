from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# TF-IDF 결과 읽기
output_csv = "C:/work/news_crawler/tfidf_results.csv"
tfidf_df = pd.read_csv(output_csv)

# 단어별 TF-IDF 합산
word_scores = tfidf_df.sum(axis=0).sort_values(ascending=False)

# 워드 클라우드 생성
wordcloud = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf",  # 한글 폰트 경로
    width=800,
    height=400,
    background_color="white",
    colormap="viridis"
).generate_from_frequencies(word_scores.to_dict())

# 워드 클라우드 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("TF-IDF 기반 워드 클라우드", fontsize=16)
plt.show()
