import streamlit as st
import random
import json
import os

# 파일 저장 설정
DATA_FILE = "meal_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"main": [], "sub": [], "snack": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 페이지 설정
st.set_page_config(page_title="아기 식단 매니저", layout="centered")
st.title("🍱 아기 식단 추천 앱")

data = load_data()

# 사이드바에서 메뉴 관리
st.sidebar.header("🛠️ 메뉴 관리")
category = st.sidebar.selectbox("카테고리 선택", ["메인", "서브", "간식"])
new_item = st.sidebar.text_input(f"{category} 추가")

if st.sidebar.button("추가하기"):
    key = "main" if category == "메인" else "sub" if category == "서브" else "snack"
    data[key].append(new_item)
    save_data(data)
    st.sidebar.success(f"'{new_item}' 추가 완료!")

# 메인 화면 - 추천 버튼
if st.button("✨ 일주일 식단 생성하기 ✨", use_container_width=True):
    if len(data["main"]) < 7 or len(data["sub"]) < 14 or len(data["snack"]) < 7:
        st.error("메뉴 개수가 부족해요! (메인 7, 서브 14, 간식 7 필요)")
    else:
        mains = random.sample(data["main"], 7)
        subs = random.sample(data["sub"], 14)
        snacks = random.sample(data["snack"], 7)
        days = ["월", "화", "수", "목", "금", "토", "일"]

        for i in range(7):
            with st.expander(f"📅 {days[i]}요일 식단"):
                st.write(f"🌟 **메인**: {mains[i]}")
                st.write(f"🥗 **서브**: {subs[i*2]}, {subs[i*2+1]}")
                st.write(f"🍎 **간식**: {snacks[i]}")

# 현재 저장된 리스트 보여주기
st.divider()
st.subheader("📋 현재 등록된 메뉴")
st.write(f"메인 {len(data['main'])}개 / 서브 {len(data['sub'])}개 / 간식 {len(data['snack'])}개")

