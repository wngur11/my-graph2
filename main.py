import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2", layout="wide")

# 앱 제목
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 216편의 영화 데이터를 통해 다양한 분포와 관계를 알아봅니다.")

# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: '|' 기호로 여러 개가 적힌 경우 첫 번째 장르만 사용
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0])
    
    return df

# 데이터 로드
movies_df = load_data()

st.divider() # 구역 나누기 선

# ==========================================
# 첫 번째 구역: 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = movies_df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# 플롯리 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    values='편수', 
    names='장르', 
    hole=0.4, 
    title="가장 많이 개봉한 장르는 무엇일까?"
)

# 호버 툴팁 설정
fig1.update_traces(
    textinfo='label+percent',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 알 수 있는 것 적을 자리 마련
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 장르 분포에 대한 핵심 인사이트를 한 문장으로 적어주세요!)")

st.divider() # 구역 나누기 선

# ==========================================
# 두 번째 구역: 장르별 총 관객 수 및 영화 분포 (트리맵)
# ==========================================
st.subheader("2. 장르별 총 관객 수와 주요 흥행작")

# 플롯리 트리맵 생성
# path: 계층 구조 (장르 안에 영화명) / values: 칸의 크기 (총 관객수)
fig2 = px.treemap(
    movies_df,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="어떤 장르, 어떤 영화가 관객을 많이 모았을까?"
)

# 칸에 마우스를 올렸을 때(호버) 이름(영화명/장르명)과 총 관객수가 보이도록 설정
# :, 포맷을 사용해 관객 수에 천 단위 콤마(,)를 찍어 가독성을 높입니다.
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 알 수 있는 것 적을 자리 마련
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 특정 장르나 영화의 관객 수 쏠림 현상 등에 대한 핵심 인사이트를 한 문장으로 적어주세요!)")

st.divider() # 다음 구역을 위해 나누기 선
