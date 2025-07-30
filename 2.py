import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="케이크 던지기 타자 게임", page_icon="🎂")
st.title("🎂 한컴 타자연습 케이크 던지기 게임 🎂")
st.write("적이 6초 안에 다가옵니다! 단어를 빨리 맞혀 케이크를 던져 적을 막으세요!")

# 단어 리스트 대폭 확장 (한글 단어)
easy_words = [
    "나무", "물", "바다", "집", "하늘", "책", "고양이", "강아지",
    "달", "꽃", "산", "강", "별", "구름", "비", "눈", "바람", "불"
]
medium_words = [
    "친구들", "학교생활", "컴퓨터", "생일파티", "자동차", "음악감상",
    "영화관", "맛집", "여행", "운동장", "도서관", "축구공", "자전거", "게임기"
]
hard_words = [
    "프로그래밍", "데이터과학", "인공지능", "환경보호", "자연현상",
    "사회복지", "컴퓨터비전", "머신러닝", "알고리즘", "인터페이스",
    "운영체제", "네트워크", "데이터베이스", "소프트웨어", "하드웨어"
]

MONSTER_TIME_LIMIT = 6  # 적 다가오는 시간(초)
MONSTER_DISTANCE_MAX = 10  # 적 초기 거리

# 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_word" not in st.session_state:
    st.session_state.current_word = ""
if "prev_word" not in st.session_state:
    st.session_state.prev_word = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "monster_distance" not in st.session_state:
    st.session_state.monster_distance = MONSTER_DISTANCE_MAX

def get_word_by_level(score, prev_word):
    if score < 5:
        pool = easy_words
    elif score < 10:
        pool = medium_words
    else:
        pool = hard_words

    # 이전 단어와 다르게 무작위 선택
    candidates = [w for w in pool if w != prev_word]
    if not candidates:
        candidates = pool  # 모든 단어가 같으면 그냥 풀 사용
    word = random.choice(candidates)
    return word

def next_monster():
    new_word = get_word_by_level(st.session_state.score, st.session_state.prev_word)
    st.session_state.prev_word = new_word
    st.session_state.current_word = new_word
    st.session_state.user_input = ""
    st.session_state.start_time = time.time()
    st.session_state.monster_distance = MONSTER_DISTANCE_MAX

def check_input():
    if st.session_state.user_input.strip() == st.session_state.current_word:
        st.session_state.score += 1
        next_monster()

# 게임 시작 버튼
if st.button("게임 시작"):
    st.session_state.score = 0
    st.session_state.game_over = False
    next_monster()

if not st.session_state.game_over and st.session_state.start_time is not None:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, MONSTER_TIME_LIMIT - elapsed)

    # 적 위치 계산
    progress_ratio = elapsed / MONSTER_TIME_LIMIT
    distance = int(MONSTER_DISTANCE_MAX * (1 - progress_ratio))
    st.session_state.monster_distance = max(0, distance)

    st.write(f"점수: {st.session_state.score}")
    st.write(f"적이 다가오는 시간 남음: {remaining:.1f}초")
    st.write(f"단어: **{st.session_state.current_word}**")

    # 적 위치 시각화
    track = ["-"] * MONSTER_DISTANCE_MAX
    if st.session_state.monster_distance > 0:
        track[st.session_state.monster_distance - 1] = "👹"
    else:
        track[0] = "👹"
    track.append("  🏃‍♂️")
    st.text("".join(track))

    st.text_input("단어 입력", key="user_input", on_change=check_input)

    if remaining <= 0:
        st.session_state.game_over = True

if st.session_state.game_over:
    st.error("👹 적이 너무 가까이 왔습니다! 게임 오버!")
    st.write(f"최종 점수: {st.session_state.score}")
    st.write("게임을 다시 시작하려면 '게임 시작' 버튼을 눌러주세요.")

# 1초마다 자동 새로고침
count = st_autorefresh(interval=1000, limit=None, key="refresh")
