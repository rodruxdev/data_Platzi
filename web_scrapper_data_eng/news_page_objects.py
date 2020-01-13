import bs4  # Importa BeautifulSoup4
import requests  # Importa requests

from common import config  # Importa config de common


class NewsPage:

    def __init__(self, news_site_uid, url):  # Se copio y pego el código que habia en init de HomePage
        # Define _config con las llaves del yaml
        self._config = config()['news_sites'][news_site_uid]
        # Define la variable queries con los queries del yaml
        self._queries = self._config['queries']
        self._html = None  # Define como vacia la variable html

        self._visit(url)  # Obtiene el _html con el url que se genera al crear la instancia

    def _select(self, query_string):
        return self._html.select(query_string)  # Obtiene los queries del html

    def _visit(self, url):
        response = requests.get(url)  # Guarda en response el url mandado

        response.raise_for_status()  # Arroja un error si no hay una conexión correcta con el url

        self._html = bs4.BeautifulSoup(response.text, 'html.parser')  # Obtiene el html del url


class HomePage(NewsPage):  # HomePage ahora extiende a NewsPage

    def __init__(self, news_site_uid, url):  # Constructor
        # Define _config con las llaves del yaml
        #self._config = config()['news_sites'][news_site_uid]
        # Define la variable queries con los queries del yaml
        #self._queries = self._config['queries']
        # self._html = None  # Define como vacia la variable html
        # self._visit(url)  # Obtiene el _html con el url que se genera al crear la instancia
        super().__init__(news_site_uid, url)  # Inicia la clase con el Constructor de NewsPage

    @property
    def article_links(self):  # Define la propiedad
        link_list = []  # Crea una lista de links
        # Recorre los links obtenidos del query
        for link in self._select(self._queries['homepage_article_links']):
            if (link and link.has_attr('href')):  # Verifica que exista el link
                link_list.append(link)  # Une los links a la lista
        # Devuelve los links en una tupla ¡Si no estoy mal xD
        return set(link['href'] for link in link_list)
    #
    # def _select(self, query_string):
    #     return self._html.select(query_string)  # Obtiene los queries del html
    #
    # def _visit(self, url):
    #     response = requests.get(url)  # Guarda en response el url mandado
    #
    #     response.raise_for_status()  # Arroja un error si no hay una conexión correcta con el url
    #
    #     self._html = bs4.BeautifulSoup(response.text, 'html.parser')  # Obtiene el html del url
    # Funciones copiadas a NewsPage


class ArticlePage(NewsPage):  # Clase para las páginas de articulos

    def __init__(self, news_site_uid, url):  # Constructor de la clase con extension a NewsPage
        super().__init__(news_site_uid, url)

    @property
    def body(self):  # Cuerpo del articulo
        # Guarda en una variable el resultado del cuerpo del articulo
        result = self._select(self._queries['article_body'])
        # Verifica si hay algo en resultados y  lo envia, si no manda algo vacio
        return result[0].text if len(result) else ''

    @property
    def title(self):  # Titulo del articulo
        # Guarda en una variable el resultado del titulo del articulo
        result = self._select(self._queries['article_title'])
        # Verifica si hay algo en resultados y  lo envia, si no manda algo vacio
        return result[0].text if len(result) else ''
