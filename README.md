# [[ARTIGO] Sistema de Busca Burra para o TabsNews, por termo ou termos, feito em Python](https://www.tabnews.com.br/Diegiwg/tutorial-sistema-de-busca-burra-para-o-tabsnews-por-termo-ou-termos-feito-em-python) no [TabNews.com.br](https://www.tabnews.com.br/)

> A ideia foi escrever algum sisteminha que faça buscas nos topicos do site, por um unico termo, e depois como desafio complementar, fazer um que retornasse busca de multiplos termos.
>
> Sei que tem problemas de performace, pois faz uma quantidade absurda de requisições a cada busca. Mas não pretendo usar esse sistema, foi só para construir mesmo.

## Porque Busca Burra?

> Bom, resolvi nomear assim, pois, a forma que funciona é muito 'direta', basicamente, requesita para a API a lista de posts da página 1 até a ultima página disponivel no servidor, parando, caso atinja antes o limite de resultados estabelecido na chamada da função.
>
> Coisas como acentuação não são tratadas, então, caso você busque por 'Serviço'  no titulo do post, esteja escrito 'Servico' por algum motivo, o sistema vai dizer que não encontrou o termo, pois ele não sabe fazer a equivalencia entre 'Ç' e 'C'. Poderia escrever um sistema de equivalencia simples, mas não faz parte do escopo do projetinho.

## Vamos entender qual o endpoint que utilizaremos nesse projetinho

> Para esse projeto, o endpoint que resolvi utilizar foi o que ordena os posts pelos mais recentes, pois, não fica mudando a ordem com o tempo, como o dos relevantes.
>
> Porem, acredito que para o sistema de verdade, dar a escolha ao usuario seria interessante. Afinal, ele poderia pesquisar, e ter seus resultados organizados por posts mais relevantes primeiro. Como faz a busca do Google.
>
> ```python
> def api_uri(page: int) -> str:
>    return f'https://www.tabnews.com.br/api/v1/contents?strategy=new&page={page}'
> ```
>
> Montei essa pequena função que retorna a URI da api com a página a ser buscada.

## Vamos implementar uma busca por todo o conteudo do site?

> Essa é a primeira coisa que montei, e bom, ela não vai fazer filtro nenhum, trazendo assim todos os posts disponiveis na plataforma.
>
> Vamos primeiro importar as funções externas que usaremos em todos os esquemas de busca desse projeto.
>
> ```python
> from requests import get as req_get
> from json import loads as json_load
> from json import dumps as json_dump
> ```
>
> Agora, definimos a função **todos_os_posts**
>
> ```python
> def buscar_todos_os_posts() -> None:
>    with open('buscar_todos_os_posts.json', 'w') as file:
>        resultado = []
>        page = 1
>        while True:
>            temp = req_get(api_uri(page))
>            res: list[dict] = json_load(temp.text)
>
>            for item in res:
>                titulo: str = item['title']
>                resultado.append(item)
>                print(titulo)
>
>            if (res == []):
>                break
>
>            page += 1
>        file.write(json_dump(resultado))
> ```
>
> Essa função vai rodar todas as páginas, até encontrar uma que retorne **[]**, ou seja, daqui para frente, não tem mais posts, então pare o loop.

### O que estamos fazendo linha a linha?

> Primeiro, a linha:
>
>```python
> with open('buscar_todos_os_posts.json', 'w') as file:
>```
>
> É a responsavel por abrir/criar o arquivo **buscar_todos_os_posts** com o with, que gerencia todo o tempo de existencia desse arquivo, desse modo, não precisamos nos preocupar por gerenciar o **fechamento** deste arquivo depois.
>
> Dai, vamos definir algumas variaveis de utilidade:
>
>```python
> resultado = []
> page = 1
>```
>
> Vamos usar **resultado** para manter os dados dos posts achados, e mais para frente, tambem, como mecanismos para parar a busca.
>
> Vamos usar **page** para fazer a busca em todas as partes do site.
>
> Continuando, temos um Loop While que vai rodar até a API retornar **[]**.
>
> ```python
> temp = req_get(api_uri(page))
> res: list[dict] = json_load(temp.text)
>```
>
> Nessas duas linhas, estamos fazendo uma request GET na URL da API com o número de página atual do loop. E, convertando o resultado em um objeto (dicionario).
>
> ```python
> for item in res:
>   titulo: str = item['title']
>   resultado.append(item)
>   print(titulo)
> ```
>
> Agora, faremos um for na lista de posts que obtivemos no request, capturando o valor do campo **title** para printar o nome no Console, e ao mesmo tempo, por os dados do post em nossa lista (variavel resultado) de retorno.
>
> ```python
> if (res == []): break
> page += 1
> ```
>
> Aqui, temos a verificação se estamos na ultima página disponivel, e se sim, sai do loop while, e continua o script. Caso a variavel **res** ainda tenha dados, significa que devemos ir para a proxima página, logo, incrementamos a variavel **page** e deixamos o loop rodar mais uma vez.
>
> Por fim, mas não menos importante, vamos salvar nosso resultado, no arquivo que abrimos no contexto do with:
>
> ```python
> file.write(json_dump(resultado))
> ```
>
> E assim, terminamos a busca por todos os posts do site.

## Agora que temos uma busca por todo o conteudo, vamos filtrar por um termo?

> Vamos fazer o filtro mais basico, um termo, para entender onde precisamos modificar a função anterior.
>
> Então, vamos definir uma nova função para essa busca, e trocar o nome do arquivo aberto/criado no with:
>
> ```python
> def buscar_unico_termo(termo: str, limite: int) -> None:
>    with open('buscar_unico_termo.json', 'w') as file:
>       ...
>   file.write(json_dump(resultado))
>```
>
> Agora temos novidades, os famosos, argumentos de função. Em nosso caso, temos o **termo**, que é uma String a ser buscada no titulo dos posts, e o **limite**, que é um número Inteiro limitador da quantidade de posts que queremos buscar.
>
> Com nosso novo arquivo aberto e os argumentos preenchidos, vamos modificar o loop que ler os titulos dos posts recebidos na request, para aplicar o filtro.
>
> Nosso trecho de codigo modificado ficará assim:
>
> ```python
> ...
> for item in res:
>   titulo: str = item['title'].lower()
>   if (titulo.find(termo.lower()) == -1): continue
>   ...
> ```
>
> Primeiro, modificamos o **titulo**, deixando todas as letras em 'minusculo'. Depois, aplicamos o filtro.
>
> Para filtrar, usamos o IF para buscar, com a função *Find*, o **termo**, que tambem está em minusculo (com o uso da função *lower*).
>
> *Find* retorna **-1** sempre que não encontra a 'palavra' em alguma parte qualquer da string que está sendo analisada.
>
> Portanto, se tivermos um **-1** como resultado, devemos dar **continue** para pular esse *post*, pois ele não tem o termo que estamos filtrando.
>
> Agora, temos que dar um jeito de parar o loop, caso a quantidade de posts encontrados seja igual ou supere o limite estabelecido em nossa chamada de função. Para tanto vamos modificar o antigo IF que verificava se tinhamos chegado em uma página vazia, de:
>
> ```python
> if (res == []):
>   break
> ```
>
> Para:
>
> ```python
> if (res == [] or len(resultado) >= limite):
>   break
>```
>
> No restante, a função continua igual a que faz buscas sem filtros. Codigo completo da Busca por Unico Termo:
>
> ```python
> def buscar_unico_termo(termo: str, limite: int) -> None:
>    with open('buscar_unico_termo.json', 'w') as file:
>        resultado = []
>        page = 1
>        while True:
>            temp = req_get(api_uri(page))
>            res: list[dict] = json_load(temp.text)
>
>            for item in res:
>                titulo: str = item['title'].lower()
>                if (titulo.find(termo.lower()) == -1): continue
>
>                resultado.append(item)
>                print(_)
>
>            if (res == [] or len(resultado) >= limite):
>                break
>
>            page += 1
>        file.write(json_dump(resultado))
> ```
>
> E assim, temos uma função que retorna todos os posts, até o **limite** definido, que tenha em seus Titulos, o **termo** buscado.

## Estamos chegando ao fim, falta agora implementar a busca por multiplos termos, vamos?

> Ja temos uma função que faz o filtro, então, só precisamos fazer ela ser mais inteligente, e suportar mais de um termo, certo?
>
> Então, vamos definir uma nova função para essa busca, e trocar o nome do arquivo aberto/criado no with:
>
> ```python
> def buscar_lista_termos(lista_termos: list[str], limite: int) -> None:
>    with open('buscar_lista_termos.json', 'w') as file:
>       ...
>   file.write(json_dump(resultado))
>```
>
> Agora, não temos mais um unico termo, por isso, mudamos o nosso tipo de variavel para uma Lista de Strings, que é a nossa **lista_termos**. No mais, ainda temos nosso **limite**, para novamente, ser usado como um dos possiveis motivos para sair do loop.
>
> Com nosso novo arquivo aberto e os argumentos preenchidos, vamos precisar criar uma 'trava' para saber se todos os termos, estão presentes dentro do titulo do post analisado.
>
> Nosso trecho de codigo modificado ficará assim:
>
> ```python
> ...
> tem_todos_os_termos: bool = True
> for item in res:
>    ...
> ```
>
> Agora, precisamos mudar o filtro, trocando o IF direto, por um loop na lista de termos, assim, o codigo antigo:
>
> ```python
> ...
> if (titulo.find(termo.lower()) == -1): continue
> ...
> ```
>
> Será modificado para ter um loop nos termos, além de atualizar a 'trava', representada por **tem_todos_os_termos** para **False** caso algum dos termos filtrados não exista no titulo do post.
>
> Ficando assim o novo codigo:
>
> ```python
> ...
> for termo in lista_termos:
>   if (titulo.find(termo.lower()) == -1):
>       tem_todos_os_termos = False
>       continue
> ...
>```
>
> Logo abaixo desse trecho atualizado de codigo, devemos por uma verificação, que irá pular o post (não irá salvar ele na varival **resultados**) caso o valor de **tem_todos_os_termos** seja igual a **False**, com o seguinte codigo:
>
> ```python
> ...
>   if (tem_todos_os_termos == False): continue
> ...
>```
>
> No restante, a função continua igual a que faz buscas com filtro de termo unico. Codigo completo da Busca por Multiplos Termos:
>
> ```python
> def buscar_lista_termos(lista_termos: list[str], limite: int):
>    with open('buscar_lista_termos.json', 'w') as file:
>        resultado = []
>        page = 1
>        while True:
>            print(f'Buscando na página {page}')
>            temp = req_get(api_uri(page))
>            res: list[dict] = json_load(temp.text)
>
>            tem_todos_os_termos: bool = True
>            for item in res:
>                titulo: str = item['title'].lower()
>
>                for termo in lista_termos:
>                    if (titulo.find(termo.lower()) == -1):
>                        tem_todos_os_termos = False
>                        continue
>
>                if (tem_todos_os_termos == False): continue
>
>                resultado.append(item)
>                print(titulo)
>
>            if (res == [] or len(resultado) >= limite): break
>
>            page += 1
>        file.write(json_dump(resultado))
>```
>
> E assim, finalizamos nosso projetinho, e gora, voce tem um sistema basico de Buscas, que poderia facilmente ser adptado para outras API's e Sistemas, bastando compreender o valor de retorno das requisições inicias.
