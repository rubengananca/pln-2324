# TPC 2 - Ficha de Expressões Regulares

#### *Objetivo*: Entender os conceitos básicos de expressões regulares em Python e resolver exercícios usando os mesmos.

No *exercício 6*, de forma a encontrar todos os pronomes pessoais numa string foi necessário recorrer ao "\b" para marcar o início e fim de uma palavra, de modo a que, por exemplo, quando fosse encontrado o pronome "eles" fosse retornado "eles" e não "ele".

No *exercício 8*, foi crucial observar que um número inteiro pode conter um ou mais dígitos e pode ser positivo ou negativo. Nesse contexto, foi necessário considerar os números decimais representados por "," ou ".". Assim, no pattern, foi implementado um raciocínio para verificar a presença de caracteres antes ou depois de um dígito. 

O raciocínio envolve a aplicação dos métodos "lookbehind" e "lookahead" para garantir que a correspondência não seja precedida por um ponto ou vírgula "[,.]". Isso é crucial, pois um número só é decimal se houver dígitos antes e depois da vírgula.

