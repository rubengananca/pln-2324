# TPC5
## *Objetivo*: Criar um site do dicionário médico com etiquetas.

Na primeira etapa foi feita a leitura dos ficheiros (json e txt) em utf-8 para ler os caracteres especiais. Após a leitura destes ficheiros foi criado um dicionário com os conceitos presentes no documento json em que as chaves são o conceito e o valor é a descrição associada à chave.

Note-se que foi importante criar um  *blacklist* de forma a evitar que algumas palavras presentes no dicionário de conceitos fossem confundidas com preposições encontradas no decorrer do texto.

De seguida, foi separado no documento de termos traduzidos os termos portugueses e os termos ingleses, separados por um "@". Após esta separação foram criadas as etiquetas para serem acrescentados ao html. É importante realçar que só foram criadas etiquetas para palavras presentes nos conceitos e no dicionário de termos traduzidos (para evitar erros de KeyValue inexistentes) e não presentes na blacklist.

Foi importante também retirar as tags "<br>" existentes nas descrições, uma vez que essas tags servem de quebra de linha no documento html mas nas descrições não.