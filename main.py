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
# 첫 번째 구역: 장르별 영화 편수
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = movies_df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# 플롯리 도넛 그래프 생성 (hole 파라미터로 가운데 구멍을 뚫어 도넛 모양을 만듭니다)
fig1 = px.pie(
    genre_counts, 
    values='편수', 
    names='장르', 
    hole=0.4, 
    title="가장 많이 개봉한 장르는 무엇일까?"
)

# 마우스를 올렸을 때(호버) 편수와 비율이 보이도록 설정
fig1.update_traces(
    textinfo='label+percent',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# 그래프 화면에 그리기
st.plotly_chart(fig1, use_container_width=True)

# 알 수 있는 것 적을 자리 마련
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 장르 분포에 대한 핵심 인사이트를 한 문장으로 적어주세요!)")

st.divider() # 다음 구역을 위해 나누기 선

# ==========================================
# 두 번째 구역: (여기에 다음 그래프 코드를 추가해 나갈 수 있습니다)
# ==========================================
