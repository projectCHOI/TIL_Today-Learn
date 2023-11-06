from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('psy9.txt', 'r', encoding='utf-8') as file:
    text = file.read()

##파이썬에 쓸 수 있는 간략한 워드 클라우드에 표시할 텍스트 데이터
#text = "파이썬은 인공지능과 데이터 분석에 매우 유용한 언어입니다. 데이터 사이언스와 머신러닝을 공부하면 파이썬을 자주 사용하게 됩니다."

# 1. 외부 텍스트 파일을 읽기
# with open('외부텍스트파일.txt', 'r', encoding='utf-8') as file:
#     text = file.read()
#with open 열어라
#'외부 텍스트 파일.txt' : 이걸 열어라
#'r' 읽기모드로 ()
#'encoding='utf-8' : 텍스트 인코딩은 'utf-8'로 한다.
#'as file' : 파일을 열고 파일을 'file' 이라는 변수로 한다.

#text = file.read() : 읽어라, 가져온 파일을 이것은 텍스트다! 라는 뜻.


# WordCloud 객체 생성 및 설정
wordcloud = WordCloud(
    width=800, height=400,  # 워드 클라우드 이미지 크기
    background_color='white',  # 배경색
    font_path='./NanumGothic.ttf',  # 사용할 폰트 경로 (한글 폰트가 필요한 경우 설정)
    colormap='viridis',  # 색상 맵
    stopwords=None  # 워드 클라우드에서 무시할 단어 리스트 (None으로 설정하면 무시하지 않음)
)

# 워드 클라우드 생성
wordcloud.generate(text)

# 워드 클라우드 이미지 표시
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")  # 축 제거
plt.show()
