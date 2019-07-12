Coletando Tweets e enviando ao banco de dados Postgresql:

O twitter possui uma API própria para coleta de textos na sua base de dados, porém para um usuário normal só é possível acessar
uma quantidade limitada de tweets e um determinado tempo também (7 dias atrás se não me engano).

Diante destas limitações utilizei o seguinte método:

1º)
Acesso ao site:
https://twitter.com/search-advanced

2º)
pesquisa rápida sobre palavra-chave, contas, linguagem e período.

3º)
para o resultado coletei o link e criei um coletor com a ajuda do site:
https://www.import.io/

4º)
Download dos dados pelo arquivo .csv

5º)
Criação e utilização do algoritmo code.py.




