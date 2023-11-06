#외부 URL의 자료 가져오기
import requests
from bs4 import BeautifulSoup

URL = '# URL'
requests = requests.get(URL)
soup = BeautifulSoup(requests.text, "html.parser")

div = soup.find('div', class_='article-body fs-article fs-responsive-text current-article')
p_tag = div.find_all('p')
content=''
for i in p_tag:
    content+=i.text
content

#영문토큰화
#첫번째. word_tokenize() : 마침표와 구두점(온점(.), 컴마(,), 물음표(?), 세미콜론(:), 느낌표(!) 등과 같은 기호)으로 구분하여 토큰화
# word_tokenize
import nltk
# nltk punkt tokenizer download
nltk.download('punkt')

from nltk.tokenize import word_tokenize

token1 = word_tokenize(content)
print(token1)

#두번째. WordPunctTokenizer(): 알파벳이 아닌문자를 구분하여 토큰화
# WordPunctTokenizer():
import nltk

from nltk.tokenize import WordPunctTokenizer
token2 = WordPunctTokenizer().tokenize(content)

print(token2)
#세번째. TreebankWordTokenizer(): 정규표현식에 기반한 토큰화
# TreebankWordTokenizer() : 정규표현식에 기반한 토큰화
import nltk
from nltk.tokenize import TreebankWordTokenizer
token = TreebankWordTokenizer().tokenize (content)
print(token[:20])

#영문 품사 부착
from nltk import pos_tag
nltk.download("averaged_perceptron_tagger")

taggedToken = pos_tag(token1)

#영문 개체명 인식
# 예시 : Barack Obama likes fried chicken very much
# word_tokenize() : 마침표와 구두점(온점(.), 컴마(,), 물음표(?), 세미콜론(;), 느낌표(!) 등과 같은 기호로 구분해서 토큰
nltk.download ('words')
nltk.download ('maxent_ne_chunker')

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
#토큰화
token1 = word_tokenize('Barack Obama likes fried chicken very much')
print('token: ', token1)

# pos-tag
taggedToken = pos_tag(token1)
print('pos-tag: ', taggedToken)

# chunking
from nltk import ne_chunk
neToken=ne_chunk (taggedToken)
print (neToken)

print(taggedToken[:20])
