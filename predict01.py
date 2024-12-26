import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pandas as pd
import numpy as np
import csv

# 1. 학습된 모델과 토크나이저 로드
model_path = './trained_model'
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

# GPU 사용 가능한 경우 GPU로 모델 이동
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
model.to(device)
model.eval()  # 평가 모드로 설정

# 2. 분류 함수 정의
def classify_text(texts):
    """
    텍스트를 분류하는 함수
    
    Parameters:
    texts (list or str): 분류할 텍스트 (문자열 또는 문자열 리스트)
    
    Returns:
    predictions (list): 각 텍스트의 예측 라벨
    probabilities (list): 각 라벨에 대한 확률
    """
    # 단일 텍스트를 리스트로 변환
    if isinstance(texts, str):
        texts = [texts]
    
    # 텍스트 토큰화
    inputs = tokenizer(
        texts, 
        padding=True, 
        truncation=True, 
        max_length=512, 
        return_tensors='pt'
    ).to(device)
    
    # 추론
    with torch.no_grad():
        outputs = model(**inputs)
    
    # 확률 계산 (softmax 적용)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    # 예측 라벨 추출
    predictions = torch.argmax(probabilities, dim=-1).cpu().numpy()
    
    # 확률 값 추출
    probabilities = probabilities.cpu().numpy()
    
    return predictions, probabilities

# 실제 CSV 파일에서 텍스트 분류 함수
def classify_csv(csv_path):
    """
    CSV 파일의 텍스트를 분류하는 함수
    
    Parameters:
    csv_path (str): CSV 파일 경로
    
    Returns:
    DataFrame: 원본 데이터에 예측 결과 추가
    """
    # CSV 파일 로드
    df = pd.read_csv(csv_path)
    
    # 텍스트 컬럼 이름 확인 (필요에 따라 'Comment'를 적절한 컬럼명으로 변경)
    text_column = 'Comment'
    result = pd.DataFrame()
    result['comment'] = df[text_column]
    print(result.dtypes)
    # 텍스트 분류
    preds, probs = classify_text(df[text_column].tolist())
    
    # 결과 추가
    result['predicted_tendency'] = preds
    result['보수'] = probs[:, 0]
    result['진보'] = probs[:, 1]
    
    return result

# 스크립트 직접 실행 시
if __name__ == "__main__":
    
    # CSV 파일 분류 예시 (필요시 주석 해제)
    result_df = classify_csv('comments.csv')
    output_csv = "comments_analysis.csv"
    result_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(result_df)
