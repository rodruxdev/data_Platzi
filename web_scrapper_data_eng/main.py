import re  # Expresiones regulares
from urllib3.exceptions import MaxRetryError
from requests.exceptions import HTTPError
from common import config  # Importa la función que creamos en common
import news_page_objects as news  # Importa news_page_objects y su clase como news
import argparse  # Importa el parser
import datetime  # importa una libreria del tiempo y fechas
import csv  # importa la libreria para archivos csv
import logging  # Importa logging
logging.basicConfig(level=logging.INFO)  # Configura el logging como básico, de informacion


logger = logging.getLogger(__name__)  # Crea un logger para la terminal
# Expresion regular para links Ex: https://example.com/hello
is_well_formed_link = re.compile(r'^https?://.+/.+$')
is_root_path = re.compile(r'^/.+$')  # Otra expresion regular


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']  # Devuelve el url del archivo yaml
    # De acuerdo a la llave obtenida en __main__

    # Con un formato obtiene la información en host
    logging.info('Beginning scraper for {}'.format(host))
    # Crea una instancia de HomePage con las llaves del archivo yaml y con los url
    homepage = news.HomePage(news_site_uid, host)

    articles = []
    for link in homepage.article_links:
        #   print(link)  # Obtiene uno a uno los links en homepage
        # Genera un articulo con la funcion _fetch_article
        article = _fetch_article(news_site_uid, host, link)
        # Si hay articulo lo guarda e imprime su título
        if article:
            logger.info('Article fetched!!')
            articles.append(article)
            print(article.title)
            break
    # Imprime el largo del articulo
    # print(len(articles))
    _save_articles(news_site_uid, articles)  # Guarda los articulos en formato csv


def _save_articles(news_site_uid, articles):
    # Obtiene la fecha en la que guardamos el archivo
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    # Guarda el nombre del archivo csv a crearse
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(
        news_site_uid=news_site_uid,
        datetime=now)
    # Establece el header del csv sin '_' al inicio del header y es una lista de todos los articulos
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+') as f:
        # Crea un writer para el archivo
        writer = csv.writer(f)
        # Escribe los headers en el archivo
        writer.writerow(csv_headers)
        # Escribe por cada articulo una columna de acuerdo a los headers
        for article in articles:
            row = [str(getattr(article, prop)) for prop in csv_headers]
            writer.writerow(row)


def _fetch_article(news_site_uid, host, link):
    # Manda un mensaje de donde obtendrá el articulo
    logger.info('Start fetching article at {}'.format(link))
    # Obtiene el articulo
    article = None
    try:
        # Para obtener el articulo necesita un link especifico
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    # Atrapa el error si no existe la página y elimina la posibilidad de seguir demasiadas urls
    except (HTTPError, MaxRetryError) as e:
        # Mensaje de error sin mostrarlo
        logger.warning('Error while fechting the article', exc_info=False)

    # Verifica que exista el articulo y su body
    if article and article.body:
        logger.warning('Invalid article. There is no body')
        return None
    # Devuelve el articulo o no devuelve nada
    return article


def _build_link(host, link):  # Verifica el link del articulo
    if is_well_formed_link.match(link):  # Detecta si el link esta bien construido
        return link  # Devuelve el link del articulo
    elif is_root_path.match(link):  # Verifica si el link coincide con la expresioón regular
        return '{}{}'.format(host, link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # Para parsear textos, inicia el objeto para guardar los datos

    # Obtiene en una lista los datos del yaml
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site', help='The news site that you want to scrape',
                        type=str, choices=news_site_choices)  # De la lista de datos, la convierte en str
    # Hace que se agregue al parser.

    args = parser.parse_args()  # Parsea los argumentos y los guarda en args
    _news_scraper(args.news_site)  # Obtiene los valores parseados y los manda a _news_scraper
