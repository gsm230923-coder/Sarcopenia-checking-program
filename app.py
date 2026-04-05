import streamlit as st
from PIL import Image

st.set_page_config(page_title="근감소증 진단 프로그램", layout="centered")

st.title("💪 근감소증 간이 진단 프로그램")

# ---------------------------
# 상태 초기화
# ---------------------------
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# ---------------------------
# 입력
# ---------------------------
gender = st.radio("성별", ["남", "여"])
grip = st.text_input("악력 (kg)")
time = st.text_input("6m 걷는 시간 (초)")
chair = st.text_input("30초 의자 일어나기 횟수")
stairs = st.text_input("30초 계단 오르기 개수")
fall = st.text_input("1년 낙상 횟수")

# ---------------------------
# 점수 계산 함수
# ---------------------------
def calculate(grip, time, chair, stairs, fall):
    if gender == "남":
        grip_score = 0 if grip >= 28 else 1 if grip >= 24 else 2
    else:
        grip_score = 0 if grip >= 18 else 1 if grip >= 15 else 2

    speed = 6 / time
    walk_score = 0 if speed >= 1.0 else 1 if speed >= 0.8 else 2

    if gender == "남":
        chair_score = 0 if chair >= 14 else 1 if chair >= 10 else 2
    else:
        chair_score = 0 if chair >= 12 else 1 if chair >= 8 else 2

    stair_score = 0 if stairs >= 20 else 1 if stairs >= 10 else 2
    fall_score = 0 if fall == 0 else 1 if fall <= 3 else 2

    total = grip_score + walk_score + chair_score + stair_score + fall_score

    strength = grip_score
    balance = walk_score + fall_score
    lower = chair_score + stair_score

    return total, strength, balance, lower

# ---------------------------
# 운동 출력 함수 ⭐
# ---------------------------
def show_exercise(name, img_file, desc):
    try:
        img = Image.open(f"images/{img_file}")
        st.image(img, width=200)
    except:
        st.warning(f"{img_file} 이미지를 찾을 수 없습니다.")

    st.markdown(f"### {name}")
    st.write(desc)
    st.divider()

# ---------------------------
# 결과 보기 버튼
# ---------------------------
if st.button("결과 보기"):
    try:
        grip_val = float(grip)
        time_val = int(time)
        chair_val = int(chair)
        stairs_val = int(stairs)
        fall_val = int(fall)
    except:
        st.error("⚠ 숫자를 올바르게 입력해주세요!")
        st.stop()

    total, strength, balance, lower = calculate(
        grip_val, time_val, chair_val, stairs_val, fall_val
    )

    st.session_state.total = total
    st.session_state.strength = strength
    st.session_state.balance = balance
    st.session_state.lower = lower
    st.session_state.calculated = True

# ---------------------------
# 결과 출력
# ---------------------------
if st.session_state.calculated:
    total = st.session_state.total

    st.subheader("📊 진단 결과")
    st.write(f"총 점수: **{total}점**")

    if total >= 4:
        st.error("근감소증 의심군입니다.")
    else:
        st.success("정상 범위입니다.")

# ---------------------------
# 정상 안내
# ---------------------------
if st.session_state.calculated and st.session_state.total < 4:
    st.info("현재 상태가 양호하여 추가 운동 추천은 제공되지 않습니다 👍")

# ---------------------------
# 운동 추천
# ---------------------------
if st.session_state.calculated and st.session_state.total >= 4:
    if st.button("운동 추천 받기"):
        st.subheader("🏃 맞춤 운동 추천")

        total = st.session_state.total
        strength = st.session_state.strength
        balance = st.session_state.balance
        lower = st.session_state.lower

        if total >= 4:
            show_exercise("무릎-팔꿈치 터치", "1.png", "전신 근력과 코어 강화")
            show_exercise("한쪽 다리 들고 무릎 펴기", "2.png", "하체 근력 강화")
            show_exercise("누워서 다리 올리기", "7.png", "코어 안정성 향상")

        else:
            if lower >= 3:
                show_exercise("한쪽 다리 들고 무릎 펴기", "2.png", "하체 근력 강화")
                show_exercise("하체 확장 운동", "6.png", "대퇴근 강화")

            if balance >= 3:
                show_exercise("누워서 다리 올리기", "7.png", "균형 및 코어 강화")
                show_exercise("무릎 당기기", "8.png", "골반 안정성 향상")

            if strength >= 2:
                show_exercise("무릎-팔꿈치 터치", "1.png", "전신 근력 강화")
                show_exercise("팔굽혀펴기", "5.png", "상체 근력 강화")
