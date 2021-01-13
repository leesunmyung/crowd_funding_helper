
import sys
import io
# 저장 -> open('r') -> 변수 할당 -> 파싱 -> 저장
# 파싱 필요 없을 때

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from gensim.models import word2vec

model = word2vec.Word2Vec.load("okt_word2vec_model0113okt_word2vec_model0113.model")

print(model.most_similar(positive=["영화"]))

print(model.most_similar(positive=["회사"]))
