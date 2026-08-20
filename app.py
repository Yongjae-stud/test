import streamlit as st
import random

# ==========================================
# 1. 단어장 데이터 (난이도별 10개 단어 구성)
# ==========================================
WORD_DICT = {
    "하급": {
        "apple": "사과", "school": "학교", "water": "물", "friend": "친구", "happy": "행복한",
        "book": "책", "family": "가족", "sun": "태양", "animal": "동물", "music": "음악"
    },
    "중급": {
        "experience": "경험", "believe": "믿다", "create": "창조하다", "effort": "노력", "future": "미래",
        "challenge": "도전", "advantage": "장점", "encourage": "격려하다", "improve": "향상시키다", "discover": "발견하다"
    },
    "상급": {
        "adequate": "적절한", "beneficial": "유익한", "comprehend": "이해하다", "diligent": "근면한", "evaluate": "평가하다",
        "substitute": "대체하다", "inevitable": "피할 수 없는", "persistent": "끈질긴", "facilitate": "용이하게 하다", "emphasize": "강조하다"
    },
    "최상급": {
        "ambiguous": "모호한", "benevolent": "자비로운", "dichotomy": "이분법", "ephemeral": "덧없는", "meticulous": "꼼꼼한",
        "ubiquitous": "어디에나 있는", "acquiesce": "묵인하다", "serendipity": "뜻밖의 행운", "ostentatious": "과시하는", "pragmatic": "실용적인"
    }
}

# ==========================================
# 2. 세션 상태(session_state) 초기화
# ==========================================
if "score" not in st.session_state:
    st.session_state.score = 0              # 현재까지 맞춘 점수
if "attempts" not in st.session_state:
    st.session_state.attempts = 0           # 총 시도 횟수
if "current_level" not in st.session_state:
    st.session_state.current_level = "하급" # 현재 난이도
if "current_word" not in st.session_state:
    st.session_state.current_word = None    # 현재 출제된 단어
if "answered" not in st.session_state:
    st.session_state.answered = False       # 정답 확인 여부
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False     # 정답 여부
if "used_words" not in st.session_state:
    st.session_state.used_words = set()     # 출제된 단어 기록 (중복 방지)

# ==========================================
# 3. 화면 디자인: 사이드바 (난이도 선택)
# ==========================================
st.sidebar.title("⚙️ 퀴즈 설정")
selected_level = st.sidebar.radio(
    "난이도를 선택하세요:", 
    ["하급", "중급", "상급", "최상급"], 
    index=["하급", "중급", "상급", "최상급"].index(st.session_state.current_level)
)

# 난이도 변경 시 세션 상태 초기화
if selected_level != st.session_state.current_level:
    st.session_state.current_level = selected_level
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.current_word = None
    st.session_state.answered = False
    st.session_state.used_words = set()
    if "user_input" in st.session_state:
        st.session_state.user_input = ""
    st.rerun()

# ==========================================
# 4. 화면 디자인: 메인 화면 상단 (점수판 및 진행 상황)
# ==========================================
st.title("🔠 수준별 중복 없는 영어 단어 퀴즈")
st.markdown("---")

total_words_in_level = len(WORD_DICT[st.session_state.current_level])
completed_words_count = len(st.session_state.used_words)

col1, col2, col3 = st.columns(3)
col1.metric(label="현재 난이도", value=st.session_state.current_level)
col2.metric(label="✅ 맞춘 점수", value=f"{st.session_state.score} 점")
col3.metric(label="📊 진행 상황", value=f"{completed_words_count} / {total_words_in_level} 개")

st.markdown("---")

# ==========================================
# 5. 중복 없는 단어 출제 로직
# ==========================================
all_words = set(WORD_DICT[st.session_state.current_level].keys())
remaining_words = list(all_words - st.session_state.used_words)

# 해당 난이도 모든 단어 완료 처리
if not remaining_words and st.session_state.current_word is None:
    st.balloons()
    st.success(f"🎊 축하합니다! **[{st.session_state.current_level}]** 난이도의 모든 단어({total_words_in_level}개)를 다 풀었습니다!")
    st.write(f"**최종 점수:** {st.session_state.score} / {st.session_state.attempts} 회 시도")
    
    def reset_current_level():
        st.session_state.used_words = set()
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.current_word = None
        st.session_state.answered = False
        if "user_input" in st.session_state:
            st.session_state.user_input = ""

    st.button("🔄 이 난이도 처음부터 다시 풀기", on_click=reset_current_level, type="primary")
    st.stop()

# 미출제 단어 중 무작위 추첨
if st.session_state.current_word is None:
    st.session_state.current_word = random.choice(remaining_words)
    st.session_state.used_words.add(st.session_state.current_word)

# 단어 크게 표시
st.markdown(
    f"<h1 style='text-align: center; font-size: 4rem; color: #1E90FF;'>"
    f"{st.session_state.current_word}</h1>", 
    unsafe_allow_html=True
)
st.write("")

# ==========================================
# 6. 정답 입력 및 확인 로직
# ==========================================
if not st.session_state.answered:
    user_answer = st.text_input(
        "이 단어의 한글 뜻은 무엇일까요?", 
        placeholder="예: 사과", 
        key="user_input"
    )
    
    if st.button("정답 확인", type="primary"):
        cleaned_answer = user_answer.strip()
        
        if not cleaned_answer:
            st.warning("⚠️ 단어의 뜻을 입력해 주세요!")
        else:
            correct_meaning = WORD_DICT[st.session_state.current_level][st.session_state.current_word]
            
            if cleaned_answer == correct_meaning:
                st.session_state.score += 1
                st.session_state.is_correct = True
            else:
                st.session_state.is_correct = False
            
            st.session_state.attempts += 1
            st.session_state.answered = True
            st.rerun()

else:
    correct_meaning = WORD_DICT[st.session_state.current_level][st.session_state.current_word]
    
    if st.session_state.is_correct:
        st.success(f"🎉 정답입니다! ({st.session_state.current_word} = {correct_meaning})")
        st.balloons()
    else:
        st.error(f"😢 틀렸습니다! 올바른 뜻은 **'{correct_meaning}'** 입니다.")

    def go_to_next():
        st.session_state.answered = False
        st.session_state.current_word = None
        if "user_input" in st.session_state:
            st.session_state.user_input = ""

    st.button("다음 문제 풀기 ➡️", on_click=go_to_next)
