import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide"
)

# 데이터 불러오기 및 전처리
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    # 장르 구분자(|) 처리: 첫 번째 장르만 추출
    df["genre_first"] = (
        df["genre"].fillna("미상").astype(str).str.split("|").str[0].str.strip()
    )
    return df


df = load_data()

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("---")

# 1. 장르별 영화 편수 도넛 그래프
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df["genre_first"].value_counts().reset_index()
genre_counts.columns = ["장르", "편수"]

# 도넛 그래프 생성
fig1 = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.4,
    title="장르별 영화 비율",
)

# 마우스 오버(호버) 시 편수와 비율 표기
fig1.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "박스오피스 상위권에 도달한 영화들 중 특정 주요 장르가 차지하는 비중과 편수 집중도를 한눈에 비교할 수 있습니다."
)
st.markdown("---")

# 2. 장르 및 영화별 총 관객 수 트리맵
st.subheader("2. 장르 및 영화별 총 관객 수 분포")

# 트리맵 그래프 생성 (계층 structure: 장르 > 영화명, 크기: total_audi)
fig2 = px.treemap(
    df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르 및 영화별 총 관객 수 트리맵",
)

# 마우스 오버(호버) 시 영화명(또는 장르명)과 총 관객 수 표기
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객 수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르별 총 관객 수 규모와 함께, 각 장르 내부에서 어떤 영화가 흥행을 주도했는지 계층 구조로 한눈에 파악할 수 있습니다."
)
st.markdown("---")
