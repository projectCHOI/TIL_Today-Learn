# Word Representation-개념
# Word Representation(단어의 표현)-------------------------------
# 일반적으로 컴퓨터는 문자를 인지 하지 못 한다.[태어나길 0과 1로 만들어 졌다.)
# 즉, 문자의 자언어 처리(수치화) 해주어야 단어를 인지한다.

# 단어를 표현하는 종류
# [대] Local Representation
# [중] One-hot vector
# [중] N-gram 
# [중] Count based method (BOW, DTM, TDM, TF-IDF)
# [대] Discrete Representation

# Local Representation-------------------------------
# 개념 : 표현하고자하는 단어만 보고 수치화하는 표현
#       EX)[원숭이 엉덩이 빨간 사과]를 수치화 할 땐 인덱스 값을 준다.
#          [원숭이 엉덩이 빨간 사과] = [0, 1, 2, 3]

# One-hot vector : 표현하고자 하는 단어의 객수를 백터화 1과 0으로 의미부여.
#                EX)원숭이[1,0,0]
#                   엉덩이[0,1,0]
#                   바나나[0,0,1]
#                   
# One-hot vector 한계점 : 차원문제 - 표현하는 단어가 너무 많다. 100개만 해도 코드가 너무 길어짐.
#                        벡터가 단어의 의미를 담지 못한다. ex)타는 '배', 먹는 '배', 사람 '배'

# N-gram : n개의 연속된 단어 나열을 보고 문맥을 이해한다.
#        EX)나는 오늘 식당에서 쌀국수를 먹었어.
#    (2개)bigram : (나는;오늘) (오늘;식당에서) (식당에서;쌀국수를) (쌀국수를;먹었어.)
#   (3개)trigram : (나는;오늘;식당에서) (오늘;식당에서;쌀국수를) (식당에서;쌀국수를;먹었어.)

# Count based method (BOW, DTM, TDM, TF-IDF)-------------------------------
# BOW(Bag of Words) : 문서내 단어의 순서를 무시하고, 출현 빈도 수만으로 단어를 표현하는 것.
# 생성법 : 형태소 분석은 띄어쓰기 기준으로
#     1번 EX)나는 오늘 식당에서 쌀국수를 먹었어.
#     2번 EX)쌀국수를 먹으며 페이퍼 롤도 먹었어.
#          나는 : 1
#          오늘 : 2
#          식당에서 : 3
#          쌀국수를 : 4
#          먹었어 : 5
#          먹으며 : 6
#          페이퍼 : 7
#          롤도 : 8
# 등장횟수
# 1번 인덱스 : [1,1,3,2,2] 
# 2번 인덱스 : [2,1,1,1,2]

# BOW(Bag of Words) 한계점 : 1. 기억하는 단어의 갯수가 많아 연산이 오래 걸린다.
#                           2. 자주 나오는 단어가 중요하진 않다. (조사도 포함 해버림)
#                           3.전처리 과정이 어렵다.(뉴스 같은 정제된 메세지는 잘 받는데, SNS는 잡기 어려움)


# DTM(Document Term Matrix)와 TDM(Term Document Matrix)
# BOW의 장르. 단어 중요도에 따른 기능이 있다. 등장하는 단어의 등장빈도를 행렬로 표현
# 한계점 : 1. 기억하는 단어의 갯수가 많아 연산이 오래 걸린다.
#         2. 자주 나오는 단어가 중요하진 않다. (조사도 포함 해버림)
#         3. 단어의 순서를 고려려 하지 않는다.

# TF-IDF(Term Frequency-Inverse Document Frequency)
# 문서집합에서 단어와 문서의 관련성을 평가하는 방법
# 단어의 상대적 중요도를 계산하기 위해 TF-IDF 수식이 있다.

# TF : 한 문서에 단어가 얼마나 나타 났는지 빈도를 뜻 함
# TF가 높으면 그 단어는 중요한 단어다.

# IDF : 단어가 얼마나 많은 문서에 등장 했는지르 나타낸다.
# IDF가 낮으면 그 단어는 중요한 단어다.


# Discrete Representation-------------------------------
# 개념 : 단어를 표현할 때 주변단어를 함께 참고하여 수치화
#       EX)[원숭이 엉덩이 빨간 사과]를 수치화 할 땐 인덱스 값을 준다.
#          [원숭이 엉덩이 빨간 사과] = [원숭이, 엉덩이]
#          [원숭이 엉덩이 빨간 사과] = [빨간, 사과]


# 구현 준비하기-------------------------------
docs = ['오늘 동물원에서 코끼리 원숭이를 보고 원숭이에게 먹이를 줬어',
       '오늘 동물원에서 원숭이에게 사과를 줬어']
print(docs)
#출력 값 : ['오늘 동물원에서 코끼리 원숭이를 보고 원숭이에게 먹이를 줬어', '오늘 동물원에서 원숭이에게 사과를 줬어']

#분해 프린트
docs_as_string = ' '.join(docs)  # 리스트의 요소를 공백으로 구분된 문자열로 결합
print(docs_as_string.split(' '))  # 이제 'split' 함수 사용 가능
#출력 값 :  ['오늘', '동물원에서', '코끼리', '원숭이를', '보고', '원숭이에게', '먹이를', '줬어', '오늘', '동물원에서', '원숭이에게', '사과를', '줬어']

#토큰화 : 공백으로 토큰화 만들기
#프레임 프린트
doc_ls = []
for doc in docs:
    doc_ls.append(doc.split(' '))

doc_ls
#출력 값 : [['오늘', '동물원에서', '코끼리', '원숭이를', '보고', '원숭이에게', '먹이를', '줬어'],
#          ['오늘', '동물원에서', '원숭이에게', '사과를', '줬어']]

# 유니크한 토큰 사전 구하기
# 2-1 빈 딕셔너리 생성
from collections import defaultdict

word2id = defaultdict(lambda : len(word2id))
word2id
# 2-2, 위에 빈 딕셔너리 안에 유니크 토큰 넣기
for doc in doc_ls:
    # print(doc) 이건 잘 나오는지 확인
    for token in doc:
        word2id[token]
        print(token)
        print('\t', word2id)

#결국 찾는건 이거임,
word2id
#출력 값 : defaultdict(<function __main__.<lambda>()>,
#            {'오늘': 0,
#             '동물원에서': 1,
#             '코끼리': 2,
#             '원숭이를': 3,
#             '보고': 4,
#             '원숭이에게': 5,
#             '먹이를': 6,
#             '줬어': 7,
#             '사과를': 8})

# BOW 구하기-------------------------------
import numpy as np

Bow_ls = []
for i, doc in enumerate(doc_ls):
    bow = np.zeros(len(word2id), dtype=int)
    print(bow)
    for token in doc:
        bow[word2id[token]] += 1
        print(token, '=>', bow)
    Bow_ls.append(bow.tolist())
#출력 값 : 오늘 => [1 0 0 0 0 0 0 0 0]
#         동물원에서 => [1 1 0 0 0 0 0 0 0]
#         코끼리 => [1 1 1 0 0 0 0 0 0]
#         ....
#         줬어 => [1 1 1 1 1 1 1 1 0]

from IPython.core import display as ICD
import pandas as pd
sorted_vocab = sorted((value, key) for key, value in word2id.items())
print('sorted_vocab', sorted_vocab)

vocab = []
for v in sorted_vocab :
    vocab.append(v[1])
print('vocab', vocab)

for i in range(len(docs)) :
    print("문서{} : {}".format(i, docs [i]))
    ICD.display(pd.DataFrame([Bow_ls[i]], columns=vocab))
    print("\n\n")

#단어순서를 고려하지 않는 BOW
docs = ['나는 양념 치킨을 좋아해 하지만 후라이드 치킨을 싫어해',
        '나는 후라이드 치킨을 좋아해 하지만 양념 치킨을 싫어해']

#토큰화
doc_ls = []
for doc in docs:
    doc_ls.append(doc.split(' '))

doc_ls

# 2-1 빈 딕셔너리 생성
from collections import defaultdict

word2id = defaultdict(lambda : len(word2id))
word2id

# 2-2 딕셔너리에 토큰 넣기
for doc in doc_ls:
    # print(doc) 이건 잘 나오는지 확인
    for token in doc:
        word2id[token]
        print(token)
        print('\t', word2id)

# BOW 구하기-------------------------------
import numpy as np

Bow_ls = []
for i, doc in enumerate(doc_ls):
    bow = np.zeros(len(word2id), dtype=int)
    print(bow)
    for token in doc:
        bow[word2id[token]] += 1
        print(token, '=>', bow)
    Bow_ls.append(bow.tolist())

from IPython.core import display as ICD
import pandas as pd
sorted_vocab = sorted((value, key) for key, value in word2id.items())
print('sorted_vocab', sorted_vocab)

vocab = []
for v in sorted_vocab :
    vocab.append(v[1])
print('vocab', vocab)

for i in range(len(docs)) :
    print("문서{} : {}".format(i, docs [i]))
    ICD.display(pd.DataFrame([Bow_ls[i]], columns=vocab))
    print("\n\n")

# TEM 직접구현-------------------------------
docs = ['동물원 코끼리',
        '동물원 원숭이 바나나',
        '엄마 코끼리 아기 코끼리',
        '원숭이 바나나 코끼리 바나나']

doc_ls = []
for doc in docs:
    doc_ls.append(doc.split(' '))
doc_ls

from sklearn.feature_extraction.text import CountVectorizer

# 문서 리스트
docs = ['동물원 코끼리',
        '동물원 원숭이 바나나',
        '엄마 코끼리 아기 코끼리',
        '원숭이 바나나 코끼리 바나나']

# CountVectorizer 객체 생성
vectorizer = CountVectorizer()
tdm = vectorizer.fit_transform(docs)

# 용어 목록 및 TDM 출력
print("용어 목록:")
print(vectorizer.get_feature_names_out())

print("TDM:")
print(tdm.toarray())
#출력 값 : TDM:
#[[1 0 0 0 0 1]
# [1 1 0 0 1 0]
# [0 0 1 1 0 2]
# [0 2 0 0 1 1]]

# TF-IDF 직접구현-------------------------------

# 문서 리스트
d1 = ['오늘 동물원에서 원숭이와 코끼리를 봤어',
      '동물원에서 원숭이에게 바나나를 줬어 바나나를']

doc_ls = []
for doc in d1:
    doc_ls.append(doc.split(' '))

doc_ls

# index 부여
# 각 토큰에 인덱스 부여
indexed_tokens = {}
for doc in doc_ls:
    for token in doc:
        if token not in indexed_tokens:
            indexed_tokens[token] = len(indexed_tokens)

# 인덱스가 부여된 토큰 출력
print("각 토큰에 부여된 인덱스:")
for token, index in indexed_tokens.items():
    print(f"{token}: {index}")

import numpy as np
TDM = np
from collections import Counter
# TF (단어 빈도) 계산 및 출력
for doc_index, doc in enumerate(doc_ls):
    tf = Counter(doc)
    print(f"문서 {doc_index}의 TF:")
    for token, count in tf.items():
        print(f"{token}: {count}")
    print()

from sklearn.feature_extraction.text import TfidfVectorizer
# 문서 텍스트를 하나로 합침
combined_docs = [' '.join(d1)]

# TfidfVectorizer 객체 생성
vectorizer = TfidfVectorizer()

# TF-IDF 행렬 계산
tfidf_matrix = vectorizer.fit_transform(combined_docs)

# TF-IDF 행렬 출력
print("TF-IDF 행렬:")
print(tfidf_matrix.toarray())
#출력 값 : TF-IDF 행렬:
#[[0.53452248 0.53452248 0.26726124 0.26726124 0.26726124 0.26726124
#  0.26726124 0.26726124]]