import streamlit as st 
import random
import json
import os

# 파일 저장 설정
DATA_FILE = "meal_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"main": [], "sub": [], "snack": []}
    return {"main": [], "sub": [], "snack": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 페이지 설정
st.set_page_config(page_title="아기 식단 매니저", layout="centered")
st.title("🍱 아기 식단 추천 앱")

# 데이터 로드
if 'data' not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# 상단 탭 구성 (추천 화면 / 메뉴 관리 화면)
tab1, tab2 = st.tabs(["✨ 일주일 식단 추천", "🛠️ 메뉴 관리 및 리스트"])

# --- [탭 2: 메뉴 관리 및 리스트] ---
with tab2:
    st.header("메뉴 추가 및 삭제")
    
    # 1. 메뉴 입력 구역
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            category = st.selectbox("어디에 추가할까요?", ["메인", "서브", "간식"])
            new_item = st.text_input("메뉴 이름 입력")
        with col2:
            st.write(" ") # 간격 맞추기
            st.write(" ")
            if st.button("추가", use_container_width=True):
                if new_item:
                    key = "main" if category == "메인" else "sub" if category == "서브" else "snack"
                    data[key].append(new_item)
                    save_data(data)
                    st.success(f"'{new_item}' 추가!")
                    st.rerun() # 화면 새로고침

    st.divider()

    # 2. 등록된 리스트 확인 및 삭제 구역
    st.subheader("📋 현재 등록된 메뉴 리스트")
    st.info("이름 옆의 'X' 버튼을 누르면 삭제됩니다.")
    
    # 메인, 서브, 간식 리스트를 3개의 칸으로 나누어 표시
    m_col, s_col, sn_col = st.columns(3)
    
    with m_col:
        st.markdown("**[메인]**")
        for i, item in enumerate(data['main']):
            cols = st.columns([4, 1])
            cols[0].write(f"- {item}")
            if cols[1].button("X", key=f"del_m_{i}"):
                data['main'].pop(i)
                save_data(data)
                st.rerun()

    with s_col:
        st.markdown("**[서브]**")
        for i, item in enumerate(data['sub']):
            cols = st.columns([4, 1])
            cols[0].write(f"- {item}")
            if cols[1].button("X", key=f"del_s_{i}"):
                data['sub'].pop(i)
                save_data(data)
                st.rerun()

    with sn_col:
        st.markdown("**[간식]**")
        for i, item in enumerate(data['snack']):
            cols = st.columns([4, 1])
            cols[0].write(f"- {item}")
            if cols[1].button("X", key=f"del_sn_{i}"):
                data['snack'].pop(i)
                save_data(data)
                st.rerun()

# --- [탭 1: 일주일 식단 추천] ---
with tab1:
    if st.button("✨ 일주일 식단 생성하기 ✨", use_container_width=True, type="primary"):
        # 필수 개수 체크
        if len(data["main"]) < 7 or len(data["sub"]) < 14 or len(data["snack"]) < 7:
            st.error(f"메뉴가 부족합니다.\n(현재 메인 {len(data['main'])}/7, 서브 {len(data['sub'])}/14, 간식 {len(data['snack'])}/7)")
        else:
            mains = random.sample(data["main"], 7)
            subs = random.sample(data["sub"], 14)
            snacks = random.sample(data["snack"], 7)
            days = ["월", "화", "수", "목", "금", "토", "일"]

            for i in range(7):
                with st.expander(f"📅 {days[i]}요일 식단"):
                    st.markdown(f"🌟 **메인**: {mains[i]}")
                    st.markdown(f"🥗 **서브**: {subs[i*2]}, {subs[i*2+1]}")
                    st.markdown(f"🍎 **간식**: {snacks[i]}")

