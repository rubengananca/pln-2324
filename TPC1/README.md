# TPC 1 - Procura de Anagramas

#### *Objetivo*: Ver as palavras que são anagramas entre elas, presentes num dado documento de texto. 

Em primeiro lugar, foi necessário abrir o documento, com um encoding "utf-8" de maneira a conseguir ler caracteres especiais. Depois da abertura do ficheiro foram removidos alguns caracteres e substituídos por espaços, de forma a não interferirem com o objetivo do programa.

Para que várias palavras sejam detetadas como anagramas, independentemente da forma como estão escritas (ignorando letras maiúsculas e minúsculas), todo o texto foi passado para letras minúsculas. Posteriormente o texto foi dividido em tokens, em que cada token representa uma palavra.

#### Função verificaAnagramas

De seguida, para verificar os anagramas que existem no documento foram criadas na função duas estruturas de dados: um dicionário, que vai guardar na chave as letras ordenadas alfabeticamente de uma palavra e no valor vai ter uma lista com todas as palavras compostas por aquelas letras (anagramas); um set que armazena as palavras já verificadas e permite que cada palavra seja verificada apenas uma vez, evitando comparações desnecessárias.

