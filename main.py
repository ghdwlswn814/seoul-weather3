import streamlit as st
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ 서울의 연평균 기온 변화")
st.write("서울의 일별 기온 데이터를 연도별로 평균내어, 장기간의 기온 변화를 한눈에 살펴봅니다.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")
    df = df.dropna(subset=["날짜", "평균기온"]).copy()
    df["연도"] = df["날짜"].dt.year

    annual = (
        df.groupby("연도", as_index=False)["평균기온"]
        .mean()
        .rename(columns={"평균기온": "연평균기온"})
        .sort_values("연도")
    )
    return df, annual

try:
    df, annual = load_data()

    st.subheader("100년 이상의 서울 연평균 기온")

    st.line_chart(
        annual,
        x="연도",
        y="연평균기온",
        x_label="연도",
        y_label="연평균 기온 (℃)",
        height=500,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("관측 시작 연도", f"{annual['연도'].min()}년")
    with col2:
        st.metric("최근 연도", f"{annual['연도'].max()}년")
    with col3:
        change = annual.iloc[-1]["연평균기온"] - annual.iloc[0]["연평균기온"]
        st.metric("시작 연도 대비 변화", f"{change:+.1f} ℃")

    st.caption(
        "※ 각 연도의 일평균 기온을 평균하여 연평균 기온을 계산했습니다. "
        "자료에 없는 날짜는 해당 연도의 평균 계산에서 제외됩니다."
    )

    with st.expander("연도별 데이터 보기"):
        display = annual.copy()
        display["연평균기온"] = display["연평균기온"].round(1)
        st.dataframe(display, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("기온 데이터를 불러오는 중 문제가 발생했습니다.")
    st.write("잠시 후 다시 실행하거나 데이터 주소를 확인해 주세요.")
    st.exception(e)
