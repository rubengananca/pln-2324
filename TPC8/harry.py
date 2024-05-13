import re
from gensim.models import Word2Vec

filename1 = "Harry_Potter_Camara_Secreta-br.txt"
filename2 = "Harry_Potter_e_A_Pedra_Filosofal.txt"

with open(filename1, 'r', encoding='utf-8') as file:
    harry1 = file.read()
    
with open(filename2, 'r', encoding='utf-8') as file:
    harry2 = file.read()
    
    
linhas = harry1.split("\n")

tokens = []

for linha in linhas:
    linha = re.sub(r'[-!?–,.]',"",linha)
    linha = linha.lower()
    tokens.append(linha.split())
    
    
model = Word2Vec(tokens, vector_size=100, window=5, min_count=1, sg=1, epochs=5)    
    
    
def get_word(word):
    try:
        return model.wv[word]
    except KeyError:
        print('The word "'+word+'" does not appear in this model.')

def guardar_modelo(modelo):
    modelo.save("modelos/harry1.model")
    
def carregar_modelo():
    modelo = Word2Vec.load("models/word2vec.model")
    return modelo
        
#print(tokens)
print(model.wv.most_similar("harry"))