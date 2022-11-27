from requests import get as req_get
from json import loads as json_load
from json import dumps as json_dump


def api_uri(page: int) -> str:
    return f'https://www.tabnews.com.br/api/v1/contents?strategy=new&page={page}'


def buscar_lista_termos(lista_termos: list[str], limite: int) -> None:
    with open('buscar_lista_termos.json', 'w') as file:
        resultado = []
        page = 1
        while True:
            temp = req_get(api_uri(page))
            res: list[dict] = json_load(temp.text)

            tem_todos_os_termos: bool = True
            for item in res:
                titulo: str = item['title'].lower()

                for termo in lista_termos:
                    if (titulo.find(termo.lower()) == -1):
                        tem_todos_os_termos = False
                        continue

                if (tem_todos_os_termos == False):
                    continue

                resultado.append(item)
            print(titulo)

            if (res == [] or len(resultado) >= limite):
                break

            page += 1
        file.write(json_dump(resultado))
