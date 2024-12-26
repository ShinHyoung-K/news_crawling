# news_crawling
#### 뉴스,댓글 크롤링 자동화프로젝트





#### TF-IDF 분석
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(nouns)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

![image](https://github.com/user-attachments/assets/25c4795f-0dcd-4bb3-a4f2-192607bcf77a)

#### 워드 클라우드 시각화
    from wordcloud import WordCloud

    word_scores = tfidf_df.sum(axis=0).sort_values(ascending=False)
    # 워드 클라우드 생성
    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/malgun.ttf",  # 한글 폰트 경로
        width=800,
        height=400,
        background_color="white",
        colormap="viridis"
    ).generate_from_frequencies(word_scores.to_dict())

    plt.show()
    
![image](https://github.com/user-attachments/assets/0eebcb2d-8fb8-47d0-aea5-8695d299fdab)
