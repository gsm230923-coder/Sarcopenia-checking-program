import streamlit as st
from PIL import Image

st.set_page_config(page_title="근감소증 진단 프로그램", layout="centered")

st.title("💪 근감소증 간이 진단 프로그램")
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
    # 악력
    if gender == "남":
        grip_score = 0 if grip >= 28 else 1 if grip >= 24 else 2
    else:
        grip_score = 0 if grip >= 18 else 1 if grip >= 15 else 2

    # 보행
    speed = 6 / time
    walk_score = 0 if speed >= 1.0 else 1 if speed >= 0.8 else 2

    # 의자
    if gender == "남":
        chair_score = 0 if chair >= 14 else 1 if chair >= 10 else 2
    else:
        chair_score = 0 if chair >= 12 else 1 if chair >= 8 else 2

    # 계단
    stair_score = 0 if stairs >= 20 else 1 if stairs >= 10 else 2

    # 낙상
    fall_score = 0 if fall == 0 else 1 if fall <= 3 else 2

    total = grip_score + walk_score + chair_score + stair_score + fall_score

    strength = grip_score
    balance = walk_score + fall_score
    lower = chair_score + stair_score

    return total, strength, balance, lower

# ---------------------------
# 결과 보기
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
# 결과 출력 (항상 유지됨)
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
# 정상일 때 안내
# ---------------------------
if st.session_state.calculated and st.session_state.total < 4:
    st.info("현재 상태가 양호하여 추가 운동 추천은 제공되지 않습니다 👍")

# ---------------------------
# 운동 추천 버튼 (밖으로 빼기🔥)
# ---------------------------
if st.session_state.calculated and st.session_state.total >= 4:
    if st.button("운동 추천 받기"):
        st.subheader("🏃 맞춤 운동 추천")

        total = st.session_state.total
        strength = st.session_state.strength
        balance = st.session_state.balance
        lower = st.session_state.lower

        if total >= 4:
            st.write("👉 1번, 2번, 7번 추천")
        else:
            if lower >= 3:
                st.write("👉 하체: 2번, 6번")
            if balance >= 3:
                st.write("👉 균형: 7번, 8번")
            if strength >= 2:
                st.write("👉 근력: 1번, 5번")
