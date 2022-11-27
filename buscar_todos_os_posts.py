from requests import get as req_get
from json import loads as json_load
from json import dumps as json_dump


def api_uri(page: int) -> str:
    return f'https://www.tabnews.com.br/api/v1/contents?strategy=new&page={page}'


def buscar_todos_os_posts() -> None:
    with open('buscar_todos_os_posts.json', 'w') as file:
        resultado = []
        page = 1
        while True:
            temp = req_get(api_uri(page))
            res: list[dict] = json_load(temp.text)

            for item in res:
                titulo: str = item['title']
                resultado.append(item)
            print(titulo)

            if (res == []):
                break

            page += 1
        file.write(json_dump(resultado))
