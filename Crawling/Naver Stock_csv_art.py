# csv를 열어 그래프 만들기
#필요하면 설치
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로를 지정
csv_file_path = "복사 후 넣기"

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv(csv_file_path)

#레이블 값 정하기
x = df['Date']
y = df['Stock_Price_Open']
#y = df['Stock_Volume']

# 그래프 그리기
plt.plot(x, y)
plt.xlabel('Date')
plt.ylabel('Stock_Price_Open')
plt.title('title')

# X 축 눈금을 회전 코트
plt.xticks(rotation=45)

plt.show()
