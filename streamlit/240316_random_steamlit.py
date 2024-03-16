import streamlit as st
import random

def numbers(required_numbers, exclude_numbers):
    all_numbers = list(range(1, 46))
    
    # 반드시 포함해야 하는 숫자 추가
    for num in required_numbers:
        if num not in all_numbers:
            all_numbers.append(num)
    
    # 제외할 숫자 제거
    for num in exclude_numbers:
        if num in all_numbers:
            all_numbers.remove(num)
    
    return random.sample(all_numbers, 6)

# Streamlit 웹 애플리케이션 시작
st.title('랜덤 번호 생성기')

# 사용자 입력 받기
required_input = st.text_input("반드시 포함해야 하는 숫자(띄어쓰기로 구분):")
exclude_input = st.text_input("반드시 제외할 숫자(띄어쓰기로 구분):")

# 입력된 문자열을 숫자 리스트로 변환
try:
    required_list = [int(num) for num in required_input.split()]
    exclude_list = [int(num) for num in exclude_input.split()]
except ValueError:
    st.write("숫자를 올바르게 입력해주세요.")
    required_list = []
    exclude_list = []

# 숫자 생성 버튼
if st.button('번호 생성'):
    happy_numbers = numbers(required_list, exclude_list)
    st.write('생성된 번호:', happy_numbers)
