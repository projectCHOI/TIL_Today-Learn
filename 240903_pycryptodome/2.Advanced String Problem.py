# 고급 문자열 문제

## 1. 정규표현식을 사용하여 이메일이나 전화번호 등 패턴을 찾는 코드

import re

def find_emails(input_string):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, input_string)

def find_phone_numbers(input_string):
    phone_pattern = r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b|\d{3}\s*\d{3}[-.\s]??\d{4}'
    return re.findall(phone_pattern, input_string)

# 사용 예시
input_string = "Contact us at example@mail.com or (123) 456-7890"
print(f"찾은 이메일: {find_emails(input_string)}")
print(f"찾은 전화번호: {find_phone_numbers(input_string)}")
