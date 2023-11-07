import MeCab
mecab = MeCab.Tagger()
out = mecab.parse("싹쓰리가 이번에 싹 쓸어버리네.")
print(out)

# MeCab을 위해 3.1버젼에서 3.7로 업데이트 했다.
# MeCab은 3.7에서 사용 해야한다.
# 바꾸는건 VS의 우측 하단!

# MeCab은 형태소 분석기다. 우수해~