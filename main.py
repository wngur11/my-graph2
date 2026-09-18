import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # 파일 경로를 실제 CSV 파일 이름으로 지정해 주세요
    df = pd.read_csv("movies.csv")
    
    # genre 컬럼 안전 분할 (오류 수정 적용)
    df['genre'] = df['genre'].astype(str).str.split('|').str[0]
    return df

st.title("영화 데이터 분석")

# 데이터 로드
movies_df = load_data()

# 데이터 및 시각화 예시
st.write("### 영화 데이터 목록", movies_df.head())
st.bar_chart(movies_df['genre'].value_counts())
