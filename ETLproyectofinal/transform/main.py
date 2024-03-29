import pandas as pd  # Importa pandas
import hashlib
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
    df = _fill_missing_tittles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
    df = _remove_duplicate_entries(df, 'title')
    df = _drop_rows_with_missing_values(df)
    _save_data(df, filename)

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


def _fill_missing_tittles(df):
    logger.info('Filling missing titles')
    # Repite lo hecho en jupyter notebooks para obtener los titulos vacios de las urls
    missing_titles_mask = df['titles'].isna()
    missing_titles = (df[missing_titles_mask]['url']
                      .str.extract(r'()?P<missing_titles>[^/]+)$')
                      .applymap(lambda title: title.split('-'))
                      .applymap(lambda title_word_list: ' '.join(title_word_list))
                      )
    # Une los titulos faltantes con los titulos obtenidos de las urls
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df


def _generate_uids_for_rows(df):
    logger.info('Generating uids for each row')
    uids = (df
            .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uid'] = uids

    return df.set_index('uid')


def _remove_new_lines_from_body(df):
    logger.info('Remove new lines from body')

    stripped_body = (df
                     .apply(lambda row: row['body'], axis=1)
                     .apply(lambda body: list(body))
                     .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters)))
                     .apply(lambda letters: ''.join(letters))
                     )
    df['body'] = stripped_body

    return df


def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')

    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)
    return df


def _drop_rows_with_missing_values(df):
    logging.info('Dropping rows with missing values')

    return df.dropna()


def _save_data(df, filename):
    clean_filename = 'clean_{}'.format(filename)
    logging.info('Saving data at location {}'.format(clean_filename))
    df.to_csv(clean_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # Inicia un parser
    # Obtienela dirección del archivo que se va a limpiar
    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename)  # Envia el parser a la función main y obtiene el data frame
    print(df)
