import streamlit as st
import time

# ---------------------------------------------------------
# 1. 페이지 설정 및 초기화
# ---------------------------------------------------------
st.set_page_config(page_title="⏱️ 나만의 반응형 타이머", page_icon="⏱️", layout="centered")

# 세션 상태(st.session_state) 초기화: 앱이 다시 실행되어도 값을 기억하는 저장소입니다.
if 'status' not in st.session_state:
    st.session_state.status = 'ready'  # 상태: 'ready'(준비), 'running'(실행중), 'paused'(일시정지), 'finished'(완료)
if 'total_seconds' not in st.session_state:
    st.session_state.total_seconds = 0
if 'remaining_seconds' not in st.session_state:
    st.session_state.remaining_seconds = 0
if 'end_time' not in st.session_state:
    st.session_state.end_time = 0.0

# ---------------------------------------------------------
# 2. 디자인 (CSS 설정)
# ---------------------------------------------------------
# 화면 크기에 따라 글자 크기가 변하는 clamp()와 깔끔한 카드 디자인을 적용합니다.
st.markdown("""
<style>
    /* 타이머 숫자를 보여주는 큰 텍스트 스타일 */
    .timer-text {
        font-size: clamp(3rem, 10vw, 8rem); /* 모바일에서는 작게, PC에서는 크게 자동 조절 */
        font-weight: bold;
        text-align: center;
        color: #FF4B4B; /* 밝은 빨간색 */
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }
    /* 타이머를 감싸는 카드 모양 배경 */
    .timer-card {
        background-color: #f8f9fa;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. 기능 함수 (버튼을 눌렀을 때 실행될 동작들)
# ---------------------------------------------------------
def set_quick_time(minutes):
    """빠른 설정 버튼을 누르면 분/초를 설정하고 타이머를 준비 상태로 만듭니다."""
    st.session_state.input_min = minutes
    st.session_state.input_sec = 0
    st.session_state.status = 'ready'

def start_timer():
    """타이머 시작 버튼을 눌렀을 때의 동작입니다."""
    total_sec = st.session_state.input_min * 60 + st.session_state.input_sec
    if total_sec <= 0:
        st.toast("⚠️ 0분 0초로는 시작할 수 없습니다!", icon="⚠️")
        return
    
    st.session_state.total_seconds = total_sec
    # time.monotonic()은 시스템의 절대 시간을 가져와 정확한 시간 계산을 가능하게 합니다.
    st.session_state.end_time = time.monotonic() + total_sec
    st.session_state.status = 'running'

def pause_timer():
    """일시정지 버튼: 현재 남은 시간을 계산하여 저장해 둡니다."""
    if st.session_state.status == 'running':
        st.session_state.remaining_seconds = st.session_state.end_time - time.monotonic()
        st.session_state.status = 'paused'

def resume_timer():
    """계속 버튼: 저장해둔 남은 시간을 바탕으로 종료 시간을 다시 계산합니다."""
    if st.session_state.status == 'paused':
        st.session_state.end_time = time.monotonic() + st.session_state.remaining_seconds
        st.session_state.status = 'running'

def reset_timer():
    """초기화 버튼: 모든 상태를 처음으로 되돌립니다."""
    st.session_state.status = 'ready'

# ---------------------------------------------------------
# 4. 화면 구성 (UI)
# ---------------------------------------------------------
st.title("⏱️ 나만의 반응형 타이머")
st.write("시간을 설정하고 시작 버튼을 눌러보세요!")

# 실행 중이거나 일시정지 상태일 때는 시간 설정을 변경하지 못하게 막습니다(disabled).
is_disabled = st.session_state.status in ['running', 'paused']

# [빠른 설정 버튼 영역] - 4개의 열로 나누어 모바일에서도 자연스럽게 배치합니다.
q_col1, q_col2, q_col3, q_col4 = st.columns(4)
with q_col1: st.button("+ 1분", on_click=set_quick_time, args=(1,), disabled=is_disabled, use_container_width=True)
with q_col2: st.button("+ 3분", on_click=set_quick_time, args=(3,), disabled=is_disabled, use_container_width=True)
with q_col3: st.button("+ 5분", on_click=set_quick_time, args=(5,), disabled=is_disabled, use_container_width=True)
with q_col4: st.button("+ 10분", on_click=set_quick_time, args=(10,), disabled=is_disabled, use_container_width=True)

# [사용자 직접 입력 영역] - 분과 초를 직접 입력받습니다. 음수를 막기 위해 min_value=0 설정.
input_col1, input_col2 = st.columns(2)
with input_col1:
    st.number_input("분 (Minutes)", min_value=0, max_value=999, step=1, key="input_min", disabled=is_disabled)
with input_col2:
    st.number_input("초 (Seconds)", min_value=0, max_value=59, step=1, key="input_sec", disabled=is_disabled)

# [조작 버튼 영역] - 현재 상태에 따라 보여지는 버튼이 다릅니다.
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.session_state.status in ['ready', 'finished']:
        st.button("▶️ 시작", on_click=start_timer, use_container_width=True, type="primary")
    elif st.session_state.status == 'running':
        st.button("⏸️ 일시정지", on_click=pause_timer, use_container_width=True)
    elif st.session_state.status == 'paused':
        st.button("▶️ 계속", on_click=resume_timer, use_container_width=True, type="primary")

with btn_col2:
    st.button("🔄 초기화", on_click=reset_timer, use_container_width=True)

# ---------------------------------------------------------
# 5. 타이머 디스플레이 (st.fragment 적용)
# ---------------------------------------------------------
# @st.fragment(run_every="1s")는 이 함수 안의 화면만 1초마다 다시 그리도록 만듭니다.
@st.fragment(run_every="1s")
def display_timer():
    # 진행 상황 계산을 위한 기본값
    current_remaining = 0
    
    if st.session_state.status == 'running':
        # 현재 시간과 종료 시간을 비교하여 남은 시간을 구합니다.
        now = time.monotonic()
        current_remaining = st.session_state.end_time - now
        
        # 타이머 종료 조건
        if current_remaining <= 0:
            current_remaining = 0
            st.session_state.status = 'finished'
            st.balloons() # 성공 풍선 효과
            st.rerun()    # 상태가 변경되었으므로 전체 화면을 한 번 새로고침합니다.
            
    elif st.session_state.status == 'paused':
        # 일시정지 중일 때는 멈춘 시간을 그대로 보여줍니다.
        current_remaining = st.session_state.remaining_seconds
    elif st.session_state.status == 'ready':
        # 준비 상태일 때는 사용자가 입력한 시간(분+초)을 보여줍니다.
        current_remaining = st.session_state.input_min * 60 + st.session_state.input_sec
    else:
        # 종료(finished) 상태
        current_remaining = 0

    # 남은 시간을 MM:SS 형태의 문자열로 만듭니다.
    mins, secs = divmod(int(current_remaining), 60)
    time_str = f"{mins:02d}:{secs:02d}"
    
    # 카드 디자인과 타이머 숫자를 화면에 그립니다.
    st.markdown(f"""
        <div class="timer-card">
            <p class="timer-text">{time_str}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 진행률 막대 (Progress Bar) 그리기
    if st.session_state.status in ['running', 'paused']:
        # 남은 시간의 비율을 0.0 ~ 1.0 사이로 계산합니다.
        total = st.session_state.total_seconds
        progress_val = max(0.0, min(current_remaining / total, 1.0)) if total > 0 else 0.0
        st.progress(progress_val, text="타이머 진행 중...")
    
    # 완료 메시지
    if st.session_state.status == 'finished':
        st.success("🎉 시간이 다 되었습니다! 수고하셨어요!")

# 타이머 화면 표시 함수 호출
display_timer()
