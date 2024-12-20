import logging
import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
import requests
import sqlite3

DATASET_NAMES = {
    "brazilian_amazon": "mbogernetto/brazilian-amazon-rainforest-degradation",
}
FILE_NAMES = {
    "deforestation_data": "def_area_2004_2019.csv",
    "co2_data": "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
}
DATA_PATH = "../data"
DEForestation_DB_PATH = "../data/deforestation_data.sqlite"
CO2_DB_PATH = "../data/co2_data.sqlite"


def main() -> None:
    """
    Downloads the data sets used for the project,
    preprocesses the data and fixes errors in them and
    saves the data in the ./data directory as sqlite.
    """
    try:
        logging.info("Authenticating Kaggle API.")
        kaggle_api = authenticate_kaggle_api()

        logging.info("Downloading datasets.")
        deforestation_df, co2_df = download_datasets(kaggle_api)

        logging.info("Cleaning CO2 data.")
        co2_df_cleaned = clean_co2_data(co2_df)

        if validate_data(deforestation_df, ['Ano/Estados', 'AMZ LEGAL']):
            logging.info("Saving deforestation data to SQLite.")
            save_deforestation_to_sqlite(deforestation_df)
        else:
            logging.error("Deforestation data failed validation.")

        if validate_data(co2_df_cleaned, ['country', 'year', 'co2', 'co2_including_luc', 'cumulative_co2',
                                          'cumulative_co2_including_luc', 'cumulative_luc_co2', 'land_use_change_co2']):
            logging.info("Saving CO2 data to SQLite.")
            save_co2_to_sqlite(co2_df_cleaned)
        else:
            logging.error("CO2 data failed validation.")

        logging.info("Pipeline completed successfully.")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


def authenticate_kaggle_api() -> KaggleApi:
    """
    Authenticates the Kaggle API.
    """
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()
    return kaggle_api


def download_datasets(kaggle_api: KaggleApi) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Downloads data on deforestation in the Brazilian Amazon region and
    data on CO2 and greenhouse gas emissions.
    """
    try:
        # Download deforestation data
        kaggle_api.dataset_download_file(DATASET_NAMES["brazilian_amazon"], FILE_NAMES["deforestation_data"],
                                         path=DATA_PATH)
        deforestation_file_path = os.path.join(DATA_PATH, FILE_NAMES["deforestation_data"])

        # Download CO2 data
        co2_data = requests.get(FILE_NAMES["co2_data"]).content
        co2_file_path = os.path.join(DATA_PATH, "owid-co2-data.csv")
        with open(co2_file_path, 'wb') as f:
            f.write(co2_data)

        # Load datasets into pandas DataFrames
        deforestation_df = pd.read_csv(deforestation_file_path)
        co2_df = pd.read_csv(co2_file_path)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error downloading CO2 data: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while downloading datasets: {e}")

    return deforestation_df, co2_df


def validate_data(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validates the structure and content of a pandas DataFrame.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.warning(f"Missing columns in data: {missing_columns}")
        return False
    if df.empty:
        logging.warning("DataFrame is empty.")
        return False
    return True


def save_deforestation_to_sqlite(deforestation_df: pd.DataFrame) -> None:
    """
    Saves the deforestation data to a SQLite database.
    """
    os.makedirs(os.path.dirname(DEForestation_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DEForestation_DB_PATH)
    deforestation_df.to_sql('deforestation', conn, if_exists='replace', index=False)
    conn.close()


def save_co2_to_sqlite(co2_df: pd.DataFrame) -> None:
    """
    Saves the CO2 emissions data to a SQLite database.
    """
    os.makedirs(os.path.dirname(CO2_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(CO2_DB_PATH)
    co2_df.to_sql('co2_emissions', conn, if_exists='replace', index=False)
    conn.close()


def clean_co2_data(co2_df) -> pd.DataFrame:
    co2_df = co2_df[['country', 'year', 'co2', 'co2_including_luc', 'cumulative_co2', 'cumulative_co2_including_luc',
                     'cumulative_luc_co2', 'land_use_change_co2']]
    co2_df = co2_df[co2_df['country'].isin(['Brazil'])]
    co2_df = co2_df[(co2_df['year'] >= 2004) & (co2_df['year'] <= 2019)]
    return co2_df


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    main()
