import streamlit as st

# 제목 설정
st.title('처음하는 Streamlit 연습 문제')

# 버튼 클릭 수를 저장하기 위한 세션 상태 초기화
if 'count' not in st.session_state:
    st.session_state['count'] = 0  # 'count' 키를 명시적으로 추가

# 버튼을 만들고, 버튼이 클릭되면 count 변수를 증가시킴
if st.button('누르면 카운터 증가'):
    st.session_state.count += 1

# 현재 카운터 값을 화면에 표시
st.write('카운터:', st.session_state.count)

# 코드 종료
# 터미널 입력 : streamlit run app.py