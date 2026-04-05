import streamlit as st
from PIL import Image

st.set_page_config(page_title="근감소증 진단 프로그램", layout="centered")

st.title("💪 근감소증 간이 진단 프로그램")

# ---------------------------
# 입력
# ---------------------------
gender = st.radio("성별", ["남", "여"])
grip = st.number_input("악력 (kg)", min_value=0.0, step=0.1, format="%.1f")
time = st.number_input("6m 걷는 시간 (초)", min_value=0.1, step=1, value=5)
chair = st.number_input("30초 의자 일어나기 횟수", min_value=0)
stairs = st.number_input("30초 계단 오르기 개수", min_value=0)
fall = st.number_input("1년 낙상 횟수", min_value=0)

# ---------------------------
# 점수 계산 함수
# ---------------------------
def calculate():
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
    total, strength, balance, lower = calculate()

    st.subheader("📊 진단 결과")
    st.write(f"총 점수: **{total}점**")

    if total >= 4:
        st.error("근감소증 의심군입니다.")
    else:
        st.success("정상 범위입니다.")

# ---------------------------
# 운동 추천
# ---------------------------
if st.button("운동 추천 받기"):
    total, strength, balance, lower = calculate()

    st.subheader("🏃 맞춤 운동 추천")

    def show_exercise(name, img_file, desc):
        img = Image.open(f"images/{img_file}")
        st.image(img, width=200)
        st.markdown(f"**{name}**")
        st.write(desc)
        st.divider()

    if total >= 4:
        show_exercise("1번: 무릎-팔꿈치 터치", "1.png", "전신 근력 및 코어 강화")
        show_exercise("2번: 한쪽 다리 들고 무릎 펴기", "2.png", "하체 근력 강화")
        show_exercise("7번: 누워서 다리 올리기", "7.png", "코어 안정성 향상")

    else:
        if lower >= 3:
            show_exercise("2번: 한쪽 다리 운동", "2.png", "하체 근력 강화")
            show_exercise("6번: 하체 확장 운동", "6.png", "대퇴근 강화")

        if balance >= 3:
            show_exercise("7번: 다리 올리기", "7.png", "균형 및 코어 강화")
            show_exercise("8번: 무릎 당기기", "8.png", "골반 안정성 향상")

        if strength >= 2:
            show_exercise("1번: 전신 운동", "1.png", "코어 및 전신 근력")
            show_exercise("5번: 팔굽혀펴기", "5.png", "상체 근력 강화")

        if total < 4 and lower < 3 and balance < 3 and strength < 2:
            st.info("현재 상태가 양호합니다 👍")
