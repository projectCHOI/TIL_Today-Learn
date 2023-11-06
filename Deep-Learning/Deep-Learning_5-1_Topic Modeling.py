# Topic Modeling(토픽 모델링)-------------------------------
# 정의 : 추상적인 문서 집합에서 주제를 찾기 위한 통계적 모델
#            텍스트 본문의 숨겨진 의미 구조를 찾기 위해 만들어 졌다.
#            EX)문서에 야옹, 츄르 라는 단어가 등장하면 고양이에 관련 있다고 판단한다.
# 토픽을 추출 함으로써 문서의 내용을 파악한다.
# 사용 : 수 많은 뉴스 중 특정 단어가 많이 들어가 이슈를 찾는다.
#           비 정형화된 SNS를 분석한다./고개의 리뷰에서 개선점을 찾는다.

# 종류 3종--------------------------------------------------------------
# LSA : 잠재의미 분석-------------------------------
# 정의 :텍스트 문서에서 발생하는 단어들간의 연관 관계를 분석하여 잠재 의미 도출
#          문서 안에 단어를 SVD를 사용해 행렬을 분해. 차원을 축소해 근접 단어끼리 묶어준다.
#          동일한 의미를 공유하는 단어들은 같은 텍스트 안에서 발생한다.
# 사용 : 문서의 집합을 이전에 TDM(단어- 문서)로 표현하고, 이것을 SVD 분해를 통해 차원수를 줄인다.
#           이렇게 하여, 계산 속도를 높이고 잠재 의미도 찾아낸다.
# 토픽모델링 과정 : TDM, DTM, TF-IDF > SVD 분해 > Truncated SVD(사용자가 정한 주제 수) > 토픽모델링 완성
# 벡터 과정 : 토픽 모델링 > 단어간 유사도 분석 > 문서간 유사도 분석 > 문서-단어간 유사도 분석

# pLSA : 확률적 잠재의미 분석-------------------------------
# 정의 : SVD 분대 대신에 확률적 방법을 사용
#           p(zld) : 문서가 하나 주어 졌을 때 특정 주제(토픽)가 나타날 확률
#           p(wlz) : 주제가 정해 졌을 때 특정 단어가 나타날 확률
# 문서에 단어를 계산하고 특정 키워드가 동일할 때 문서를 구분.
# 한계점 : 새로운 문서가 들어왔을 때, 이것을 추정하기 어렵다.
#                 분석할 문서가 많을 수록 파라미터가 늘어난다.

# LDA : 잠재 디리클레 할당-------------------------------
# 정의 : 주어진 문서에 대해 어떠한 주제가 존재하는지에 대한 확률 모형을 의미
#           분포를 추정할 때 [디리클레 다항분포]를 사용한다.
#           [디리클레 다항분포]연속확률 분포중 하나임
# 용어 : 잠재 :문서에 있는 숨겨진 내용
#           디리클레 : 수학자 디클레의 디리클레 분보를 사용한다.
#           할당 : 주제를 정하고 그 주제에 대한 단어만을 추출한다.
# 과정
#            1단계 : 전체 문서에서 토픽 k개 추출
#            2단계 : 토픽에 인덱스 값 부여
#            3단계 : 문서내 특정 토픽이 등장할 확률 p(zld)과 지정한 주제 안에서 토픽 단어가 나올 확률 p(wlz)
#                        두가지를 구하고 둘을 더한다.
#            4단계 : 토픽을 재 할당 후 계산
#한계점 : 실행마다 결과가 다를 수 있다.
#              단어의 분포와 사람이 인지하는 주제가 다를 수 있어 분석 내용에 오류가 생긴다.
#              토픽의 가중치를 정하기 어렵다.

# LSA, LDA의 비교-------------------------------
# LSA : 단어-문서 행렬을 SVD 행렬 분해를 사용해 행렬 차원을 축소해 근접 단어로 토픽 선정
# LDA : 단어가 특정 토큰에 존재할 활률과 문서에 특정이 존재할 활률 추정


# LSA : 간단한 토픽모델링 구현-------------------------------
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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

n_topic= 3
#선언-------------------------------
tfidf_vect = TfidfVectorizer()
tfidf = tfidf_vect. fit_transform(docs)
svd = TruncatedSVD (n_components=n_topic)
u_sigma = svd. fit_transform(tfidf)
svd.components_
#
vocab= tfidf_vect.get_feature_names_out()
n=3
for idx, topic in enumerate(svd.components_):
    print("Topic %d" % (idx), [(vocab[i], topic[i].round(5)) for i in topic.argsort() [:-n - 1:-1]])

#단어 벡터간 상관관계-------------------------------
for i in range(len(vocab)) :
    print("{} : {}".format(vocab[i], svd.components_.T[i]))
#
import numpy as np
from numpy import dot
from numpy.linalg import norm
# 코사인유사도
def cosine_similarity(a, b) :
    return dot(a, b)/(norm(a) *norm(b))
#코사인유사도를 사용해서 행렬의 유사도 구하기.
def calc_similarity_matrix(vectors) :
    n_word = len(vectors)
    similarity_matrix = np.zeros((n_word, n_word))
    
    for i in range(n_word) :
        #위에서 정의한 코사인 유사도 사용
        for j in range(i, n_word):
            similarity_matrix[j, i] = cosine_similarity(vectors [i], vectors [j]).round(4)
            
    return similarity_matrix
#
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_similarity(similarity_matrix) :
    uniform_data = similarity_matrix
    mask= np.triu(np.ones_like(similarity_matrix, dtype=np.bool))
    plt.rcParams['figure.figsize'] = [8, 6]
    ax = sns.heatmap(uniform_data, mask=mask,
                     annot=True, fmt=".2f",annot_kws={'size':8},
                     cmap='coolwarm')
print(vocab)
#
word_vectors = svd.components_.T
word_similarity_matrix = calc_similarity_matrix (word_vectors)
visualize_similarity(word_similarity_matrix)

#단어벡터 시각화-------------------------------
# 한글 폰트 설정
# 설치하고 한글 적용이 안된다면, 런타임> 런타임 다시시작; 하고 설치코드 제외하고 나머지 코드 실행
#sudo apt-get install -y fonts-nanum
#sudo fc-cache -fv
#rm ~/.cache/matplotlib -rf

#시각화(점 그래프)-------------------------------
#%matplotlib inline
import matplotlib. font_manager as fm
import matplotlib
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
fontprop = fm. FontProperties(fname=font_path, size=12)
#
from sklearn.manifold import TSNE
import numpy as np
vectors = word_vectors
labels = tfidf_vect.get_feature_names_out()

def visualize_vectors (vectors, labels):
    tsne = TSNE(n_components=2, random_state=0, n_iter=10000, \
                perplexity=2)
    np.set_printoptions(suppress=True)
    T = tsne.fit_transform(vectors)

    plt.figure(figsize=(10, 6))
    plt.scatter(T[:, 0], T[:, 1], c='orange', edgecolors='r')
    for label, x, y in zip(labels, T[:, 0], T[:, 1]):
        plt.annotate(label, xy=(x+1, y+1), xytext=(0, 0), \
                     textcoords='offset points',\
                     fontproperties=fontprop)
visualize_vectors(vectors, labels)
