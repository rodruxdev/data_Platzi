from common import config  # Importa la función que creamos en common
import argparse  # Importa el parser
import logging  # Importa logging
logging.basicConfig(level=logging.INFO)  # Configura el logging como básico, de informacion


logger = logging.getLogger(__name__)  # Crea un logger para la terminal


def _news_scraper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']  # Devuelve el url del archivo yaml
    # De acuerdo a la llave obtenida en __main__

    # Con un formato obtiene la información en host
    logging.info('Beginning scraper for {}'.format(host))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # Para parsear textos, inicia el objeto para guardar los datos

    # Obtiene en una lista los datos del yaml
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site', help='The news site that you want to scrape',
                        type=str, choices=news_site_choices)  # De la lista de datos, la convierte en str
    # Hace que se agregue al parser.

    args = parser.parse_args()  # Parsea los argumentos y los guarda en args
    _news_scraper(args.news_site)  # Obtiene los valores parseados y los manda a _news_scraper
