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

genre_counts = movies_df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

fig1 = px.pie(
    genre_counts, 
    values='편수', 
    names='장르', 
    hole=0.4, 
    title="가장 많이 개봉한 장르는 무엇일까?"
)
fig1.update_traces(
    textinfo='label+percent',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# 중복 에러 방지를 위해 key="genre_donut_chart" 추가
st.plotly_chart(fig1, use_container_width=True, key="genre_donut_chart")

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 장르 분포에 대한 핵심 인사이트를 한 문장으로 적어주세요!)")

st.divider() 

# ==========================================
# 두 번째 구역: 장르별 총 관객 수 및 영화 분포 (트리맵)
# ==========================================
st.subheader("2. 장르별 총 관객 수와 주요 흥행작")

fig2 = px.treemap(
    movies_df,
    path=['genre', 'movieNm'],
    values='total_audi',
    title="어떤 장르, 어떤 영화가 관객을 많이 모았을까?"
)
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객: %{value:,}명<extra></extra>"
)

# 중복 에러 방지를 위해 key="genre_movie_treemap" 추가
st.plotly_chart(fig2, use_container_width=True, key="genre_movie_treemap")

st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 특정 장르나 영화의 관객 수 쏠림 현상 등에 대한 핵심 인사이트를 한 문장으로 적어주세요!)")

st.divider() 

# ==========================================
# 세 번째 구역: 총 관객 수 분포 (히스토그램)
# ==========================================
st.subheader("3. 총 관객 수 분포")

# 히스토그램 그리기
fig3 = px.histogram(
    movies_df, 
    x='total_audi', 
    nbins=30, # 구간 개수 설정
    title="영화들은 보통 관객을 얼마나 모을까?",
    labels={'total_audi': '총 관객 수 (명)'}
)
fig3.update_traces(
    hovertemplate="총 관객 수 범위: %{x}<br>영화 편수: %{y}편<extra></extra>"
)

st.plotly_chart(fig3, use_container_width=True, key="total_audi_histogram")

# 1) 가장 관객이 많은 영화 계산
top_movie = movies_df.loc[movies_df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 2) 대부분의 영화가 몰려 있는 구간 계산 (데이터를 30개 구간으로 나누어 가장 편수가 많은 구간 찾기)
bins = pd.cut(movies_df['total_audi'], bins=30)
most_common_bin = movies_df['total_audi'].groupby(bins, observed=False).count().idxmax()

# 판다스의 첫 구간은 음수로 표기될 수 있으므로 최솟값을 0으로 보정
start_range = max(0, int(most_common_bin.left))
end_range = int(most_common_bin.right)

# 분석 결과를 문구로 출력 (f-string 사용)
st.info(
    f"💡 **이 그래프로 알 수 있는 것:** "
    f"대부분의 영화가 총 관객 **{start_range:,}명 ~ {end_range:,}명** 구간에 몰려 있으며, "
    f"가장 관객이 많은 영화는 **'{top_movie_name}'** ({top_movie_audi:,}명)입니다."
)

st.divider()
