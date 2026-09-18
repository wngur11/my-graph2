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

# 3. 총 관객 수 히스토그램
st.subheader("3. 총 관객 수 구간별 분포")

# 히스토그램 생성
fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객 수 히스토그램",
    labels={"total_audi": "총 관객 수", "count": "영화 편수"},
)

fig3.update_traces(
    hovertemplate="관객 수 구간: %{x}<br>영화 편수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True)

# 최다 관객 수 영화 자동 계산
max_movie = df.loc[df["total_audi"].idxmax()]
max_movie_name = max_movie["movieNm"]
max_movie_audi = max_movie["total_audi"]

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    f"대부분의 영화가 비교적 적은 관객 수 구간(왼쪽 구간)에 몰려 있는 롱테일 분포를 보이며, "
    f"가장 많은 관객을 동원한 영화는 **'{max_movie_name}'** (약 {max_movie_audi:,.0f}명)입니다."
)
st.markdown("---")

# 4. 개봉일 스크린수 vs 총 관객 수 산점도
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계")

# 산점도 생성 (점 색상: 장르별 구분, 호버: 영화명 표시)
fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="개봉일 스크린수 대비 총 관객 수 산점도",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "genre_first": "장르",
    },
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "개봉일 스크린수가 많을수록 총 관객 수도 대체로 증가하는 양의 상관관계를 보이며, 장르별 분포 양상도 함께 확인할 수 있습니다."
)
st.markdown("---")

# 5. 주요 장르별(10편 이상) 총 관객 수 박스플롯
st.subheader("5. 주요 장르별 총 관객 수 분포 (10편 이상 장르)")

# 영화가 10편 이상인 장르 필터링
genre_counts_series = df["genre_first"].value_counts()
target_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered = df[df["genre_first"].isin(target_genres)]

# 박스플롯 생성 (outliers 점 표시 및 마우스 호버 시 영화명 표시)
fig5 = px.box(
    df_filtered,
    x="genre_first",
    y="total_audi",
    color="genre_first",
    points="outliers",
    hover_name="movieNm",
    title="10편 이상 영화가 존재하는 주요 장르별 총 관객 수 분포",
    labels={
        "genre_first": "장르",
        "total_audi": "총 관객 수",
    },
)

st.plotly_chart(fig5, use_container_width=True)

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "장르별 관객 수의 중앙값과 범위를 비교할 수 있으며, 상자 밖으로 튀어나온 이상치(Outlier) 점을 통해 해당 장르에서 압도적인 흥행을 기록한 대표 영화를 확인할 수 있습니다."
)
st.markdown("---")

# 6. 개봉일 스크린수, 첫 주 관객수, 총 관객수의 관계 (버블 차트)
st.subheader("6. 개봉일 스크린수, 첫 주 관객수, 총 관객수의 관계 (버블 차트)")

# 버블 차트 생성 (점 크기: 개봉 첫 주 관객 수)
fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre_first",
    hover_name="movieNm",
    title="스크린수·첫 주 관객수·총 관객수 관계 버블 차트",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "first_week_audi": "개봉 첫 주 관객 수",
        "genre_first": "장르",
    },
    size_max=50,
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,.0f}개<br>총 관객 수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "버블의 크기(개봉 첫 주 관객 수)를 통해 개봉 초기 흥행 화제성이 최종 총 관객 수 및 스크린 수 확보와 어떤 종합적인 관계를 가지는지 입체적으로 분석할 수 있습니다."
)
st.markdown("---")

# 7. 제작 국가 및 장르별 선버스트 차트
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 차트)")

# 선버스트 차트 생성 (계층 구조: 국가 > 장르, 크기: 영화 편수)
fig7 = px.sunburst(
    df,
    path=["nation", "genre_first"],
    title="제작 국가 및 장르별 영화 편수 계층 구조",
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

# 그래프 분석 및 구분선
st.markdown("---")
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.info(
    "전체 영화의 국가별 점유 비율과 함께, 특정 국가 내에서 주를 이루는 장르 구성을 원형 계층 구조로 명확하게 파악할 수 있습니다."
)
st.markdown("---")
