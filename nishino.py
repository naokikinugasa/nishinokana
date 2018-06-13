from gensim import corpora
from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import requests
from bs4 import BeautifulSoup

with open("kashi.txt", "r", encoding="utf-8") as f:
    kashi = f.read()

# 英数字の削除
kashi = re.sub("[a-xA-Z0-9_]","",kashi)
# 記号の削除
kashi = re.sub("[!-/:-@[-`{-~]","",kashi)
# 空白・改行の削除
kashi = re.sub(u'\n\n', '\n', kashi)
kashi = re.sub(u'\r', '', kashi)
# counter = {}
# 品詞を取り出し「名詞、動詞、形容詞、形容動詞」のリスト作成
def tokenize(text):
    t = Tokenizer()
    tokens = t.tokenize(text)
    word = []
    stop_word = create_stop_word()
    for token in tokens:
        part_of_speech = token.part_of_speech.split(",")[0]
        if part_of_speech == "名詞":
            if not token.surface in stop_word:
                word.append(token.surface)        
        if part_of_speech == "動詞":
            if not token.base_form in stop_word:
                word.append(token.base_form)
        if part_of_speech == "形容詞":
            if not token.base_form in stop_word:
                word.append(token.base_form)        
        if part_of_speech == "形容動詞":        
            if not token.base_form in stop_word:
                word.append(token.base_form)

    # for wo in word:
    #     if not wo in counter: counter[wo] = 0
    #     counter[wo] += 1
    return word

def create_stop_word():
    target_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    r =requests.get(target_url)
    soup=BeautifulSoup(r.text, "html.parser")
    stop_word=str(soup).split()
    #自分で追加
    my_stop_word=['いる','する','させる','の','色','真夏','身体','最初','知る','られる','出会える','出会う','距離','この世']
    stop_word.extend(my_stop_word)
    return stop_word

sentence = [tokenize(kashi)]
model = word2vec.Word2Vec(sentence, size=200, min_count=4, window=5, iter=40)
love = model.wv.most_similar(positive=[u"恋"], topn=10)
for i, lv in enumerate(love):
    print(str(i) + "    " + lv[0] + "    " + str(lv[1]))
# fpath = "/Library/Fonts/ヒラギノ角ゴ Pro W3.otf"
# wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500).generate(kashi)

# plt.figure(figsize=(15,12))
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()

# sc = sorted(counter.items(), key=lambda x: x[1], reverse=True)
# for i, t in enumerate(sc):
#     if i >= 100: break
#     key, cnt = t
#     print((i + 1), ".", key, "=", cnt)