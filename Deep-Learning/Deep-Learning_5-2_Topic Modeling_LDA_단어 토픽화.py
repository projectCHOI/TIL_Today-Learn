# LDA : 단어가 특정 토큰에 존재할 활률과 문서에 특정이 존재할 활률 추정

# LDA : 토픽모델링 구현-------------------------------
#데이터 만들기
docs = ['바나나 사과 포도 포도',
         '사과 포도',
         '포도 바나나',
         '짜장면 짬뽕 탕수육',
         '볶음밥 탕수육',
         '짜장면 짬뽕',
         '된장찌개 김치찌개 김치 비빔밥',
         '김치 된장 비빔밥',
         '비빔밥 김치',
         '사과 볶음밥 김치 된장']

# 분석할 문서를 공백으로 토큰화-------------------------------
from gensim import corpora
from gensim.models import LdaModel, TfidfModel

tokenized_docs = []
for doc in docs:
    tokenized_docs.append(doc.split(' '))
tokenized_docs

# 출력 값 : (이어진 단어가 띄어쓰기 기준으로 토픽화)
#[['바나나', '사과', '포도', '포도'],
#['사과', '포도'],
#['포도', '바나나'],
#['짜장면', '짬뽕', '탕수육'],
#['볶음밥', '탕수육'],
#['짜장면', '짬뽕'],
#['된장찌개', '김치찌개', '김치', '비빔밥'],
#['김치', '된장', '비빔밥'],
#['비빔밥', '김치'],
#['사과', '볶음밥', '김치', '된장']]

# 노출 단어 벡터화-------------------------------
id2word = corpora. Dictionary (tokenized_docs)
for value in id2word:
    print(value, id2word [value])
#출력 값 : (문장에서 등장한 단어 벡터값)
#0 바나나
#1 사과
#2 포도
#3 짜장면
#4 짬뽕
#5 탕수육
#6 볶음밥
#7 김치
#8 김치찌개
#9 된장찌개
#10 비빔밥
#11 된장

# 과정 corpus_TDM = [id2word.doc2bow(doc) for doc in tokenized_docs]-------------------------------
corpus_TDM = []
for doc in tokenized_docs:
    # print(doc)확인
    result = id2word.doc2bow(doc)
    #print(result)# index, 등장 횟수 ( 순서는 index 순으로 sorting해서 출력됨
    #print('\n')
    corpus_TDM.append(result)
#corpus_TDM #확인 필요하면 한번 해주고.

tfidf = TfidfModel (corpus_TDM)
corpus_TFIDF = tfidf [corpus_TDM]
n = 3#토픽갯수 - 변경가능
lda = LdaModel(corpus=corpus_TFIDF,
               id2word=id2word,
               num_topics=n,
               random_state=100)
for t in lda.print_topics():
    print(t[0],":", t[1])

#출력 값 : (문장에서 등장한 단어 벡터값)
# 0 : 0.158*"탕수육" + 0.105*"볶음밥" + 0.100*"된장찌개" + 0.100*"짬뽕" + 0.099*"김치찌개" + 0.097*"짜장면" + 0.078*"비빔밥" + 0.071*"김치" + 0.056*"포도" + 0.049*"사과"
# 1 : 0.241*"포도" + 0.170*"바나나" + 0.158*"사과" + 0.053*"김치" + 0.051*"볶음밥" + 0.050*"된장" + 0.049*"짬뽕" + 0.048*"비빔밥" + 0.048*"짜장면" + 0.048*"탕수육"
# 2 : 0.154*"비빔밥" + 0.150*"김치" + 0.148*"된장" + 0.097*"짜장면" + 0.094*"짬뽕" + 0.089*"볶음밥" + 0.068*"사과" + 0.043*"포도" + 0.042*"바나나" + 0.042*"탕수육"

# 해석-------------------------------
# print_topics() : 출력된 결과는 토픽마다 주요 단어와 해당 단어의 가중치
# 앞에 t[0]는 토픽 번호 0, 1, 2
# 뒤에 t[1]은 문서의 주요 단어와 가중치
#