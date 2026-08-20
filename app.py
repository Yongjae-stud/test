import streamlit as st
import random

# ==========================================
# 1. 단어장 데이터 (Python 딕셔너리 활용)
# ==========================================
# 난이도별로 영단어와 한글 뜻을 딕셔너리 형태로 저장합니다.
# 학생이 직접 이 부분에 단어를 추가하거나 수정할 수 있습니다.
WORD_DICT = {
    "하급": {
        "apple": "사과", "school": "학교", "water": "물", 
        "friend": "친구", "happy": "행복한"
    },
    "중급": {
        "experience": "경험", "believe": "믿다", "create": "창조하다", 
        "effort": "노력", "future": "미래"
    },
    "상급": {
        "adequate": "적절한", "beneficial": "유익한", "comprehend": "이해하다", 
        "diligent": "근면한", "evaluate": "평가하다"
    },
    "최상급": {
        "ambiguous": "모호한", "benevolent": "자비로운", "dichotomy": "이분법", 
        "ephemeral": "덧없는", "meticulous": "꼼꼼한"
    }
}

# ==========================================
# 2. 세션 상태(session_state) 초기화
# ==========================================
# 앱이 처음 실행될 때 KeyError가 발생하지 않도록 기본값을 설정합니다.
if "score" not in st.session_state:
    st.session_state.score = 0              # 현재까지 맞춘 점수
if "attempts" not in st.session_state:
    st.session_state.attempts = 0           # 총 시도 횟수
if "current_level" not in st.session_state:
    st.session_state.current_level = "하급" # 현재 난이도
if "current_word" not in st.session_state:
    st.session_state.current_word = None    # 현재 출제된 단어
if "answered" not in st.session_state:
    st.session_state.answered = False       # 정답 확인 버튼을 눌렀는지 여부
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False     # 정답을 맞혔는지 여부

# ==========================================
# 3. 화면 디자인: 사이드바 (난이도 선택)
# ==========================================
st.sidebar.title("⚙️ 퀴즈 설정")
selected_level = st.sidebar.radio(
    "난이도를 선택하세요:", 
    ["하급", "중급", "상급", "최상급"], 
    index=["하급", "중급", "상급", "최상급"].index(st.session_state.current_level)
)

# [오류 처리] 사용자가 도중에 난이도를 변경한 경우 상태를 깔끔하게 초기화
if selected_level != st.session_state.current_level:
    st.session_state.current_level = selected_level
    st.session_state.score = 0
    st.session_state.attempts = 0
    st.session_state.current_word = None
    st.session_state.answered = False
    if "user_input" in st.session_state:
        st.session_state.user_input = "" # 입력창 초기화
    st.rerun() # 화면을 즉시 새로고침하여 초기화된 상태 반영

# ==========================================
# 4. 화면 디자인: 메인 화면 상단 (점수판)
# ==========================================
st.title("🔠 수준별 랜덤 영어 단어 퀴즈")
st.markdown("---")

# st.metric을 사용해 점수와 시도 횟수를 나란히 표시합니다.
col1, col2, col3 = st.columns(3)
col1.metric(label="현재 난이도", value=st.session_state.current_level)
col2.metric(label="✅ 맞춘 점수 (Score)", value=f"{st.session_state.score} 점")
col3.metric(label="🔄 시도 횟수", value=f"{st.session_state.attempts} 회")

st.markdown("---")

# ==========================================
# 5. 퀴즈 출제 로직
# ==========================================
# 현재 출제된 단어가 없다면 선택된 난이도에서 무작위로 하나 뽑습니다.
if st.session_state.current_word is None:
    words_list = list(WORD_DICT[st.session_state.current_level].keys())
    st.session_state.current_word = random.choice(words_list)

# 화면 중앙에 영단어를 크고 눈에 띄게 표시 (HTML 태그 사용)
st.markdown(
    f"<h1 style='text-align: center; font-size: 4rem; color: #1E90FF;'>"
    f"{st.session_state.current_word}</h1>", 
    unsafe_allow_html=True
)
st.write("") # 여백용

# ==========================================
# 6. 정답 입력 및 확인 로직
# ==========================================
# 사용자가 아직 정답을 확인하지 않은 상태
if not st.session_state.answered:
    # 텍스트 입력창 배치 (key를 부여하여 session_state로 관리 가능하게 함)
    user_answer = st.text_input(
        "이 단어의 한글 뜻은 무엇일까요?", 
        placeholder="예: 사과", 
        key="user_input"
    )
    
    # 확인 버튼
    if st.button("정답 확인", type="primary"):
        # 입력값 양쪽 공백 제거
        cleaned_answer = user_answer.strip()
        
        # [오류 처리] 아무것도 입력하지 않았을 때 경고
        if not cleaned_answer:
            st.warning("⚠️ 단어의 뜻을 입력해 주세요!")
        else:
            # 정답 판별
            correct_meaning = WORD_DICT[st.session_state.current_level][st.session_state.current_word]
            
            if cleaned_answer == correct_meaning:
                st.session_state.score += 1
                st.session_state.is_correct = True
            else:
                st.session_state.is_correct = False
            
            st.session_state.attempts += 1
            st.session_state.answered = True
            st.rerun() # 결과 화면으로 전환하기 위해 새로고침

# 정답을 확인한 후의 화면 상태
else:
    correct_meaning = WORD_DICT[st.session_state.current_level][st.session_state.current_word]
    
    # 맞혔을 경우
    if st.session_state.is_correct:
        st.success(f"🎉 정답입니다! ({st.session_state.current_word} = {correct_meaning})")
        st.balloons() # 풍선 효과
    # 틀렸을 경우
    else:
        st.error(f"😢 틀렸습니다! 올바른 뜻은 **'{correct_meaning}'** 입니다.")

    # '다음 문제'로 넘어가기 위한 콜백 함수
    def go_to_next():
        st.session_state.answered = False
        st.session_state.current_word = None
        if "user_input" in st.session_state:
            st.session_state.user_input = "" # 다음 문제를 위해 입력창 초기화

    st.button("다음 문제 풀기 ➡️", on_click=go_to_next)
