filename = "C:/Users/ruben/OneDrive - Universidade do Minho/4ºAno/2ºSemestre/PLN/pln-2324/TPC1/CIH Bilingual Medical Glossary English-Spanish.txt"

with open(filename, 'r', encoding='utf-8') as file:
    text = file.read()

#Remover Pontuação
text.replace("."," ")
text.replace(","," ")
text.replace("-"," ")
text.replace(":"," ")
text.replace("/"," ")
text.replace("'"," ")
text.replace("("," ")
text.replace(")"," ")

text = text.lower()
tokens = text.split()

# Função para verificar se duas palavras são anagramas
def anagrama(s1,s2):
    return sorted(s1) == sorted(s2)

# Função para verificar os anagramas do documento
def verificarAnagramas(string):
    palavrasVerificadas = set()
    anagramas = {}
    
    for i in range(len(tokens)):
        for j in range(i+1, len(tokens)):
            if tokens[i] not in palavrasVerificadas and anagrama(tokens[i], tokens[j]):
                palavra = ''.join(sorted(tokens[i]))
                if palavra not in anagramas:
                    anagramas[palavra] = [tokens[i]]
                else:
                    anagramas[palavra].append(tokens[i])
                palavrasVerificadas.add(tokens[i])

    return anagramas
    
resultado = verificarAnagramas(tokens)
for chave, valores in resultado.items():
    print(f'{chave}: {valores}')

    