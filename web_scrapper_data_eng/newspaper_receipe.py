import pandas as pd  # Importa pandas
from urllib.parse import urlparse  # Importa urlparse
import argparse  # Importa el parser
import logging  # Importa el logging
logging.basicConfig(level=logging.INFO)  # Configura el logging


logger = logging.getLogger(__name__)  # obtiene el logger de main


def main(filename):
    logger.info('Starting cleaning process')

    df = _read_data(filename)  # Leemos el filename
    newspaper_uid = _extract_newspaper_uid(filename)  # Extraemos el uid del filename
    df = _add_newspaper_uid_column(df, newspaper_uid)  # Agregamos la columna del uid
    df = _extract_host(df)  # Obtener la columna de los hosts

    return df


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename)  # Devuelve el csv en data frame


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]  # obtiene el uid

    logger.info('Newspaper uid detected: {}'.format(newspaper_uid))
    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid  # Agrega la columna con el uid

    return df


def _extract_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)  # Agrega la columna del host
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # Inicia un parser
    # Obtienela dirección del archivo que se va a limpiar
    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename)  # Envia el parser a la función main y obtiene el data frame
    print(df)
