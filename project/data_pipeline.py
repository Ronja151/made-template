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

    return deforestation_df, co2_df


def save_deforestation_to_sqlite(deforestation_df: pd.DataFrame) -> None:
    """
    Saves the deforestation data to a SQLite database.
    """
    conn = sqlite3.connect(DEForestation_DB_PATH)
    deforestation_df.to_sql('deforestation', conn, if_exists='replace', index=False)
    conn.close()


def save_co2_to_sqlite(co2_df: pd.DataFrame) -> None:
    """
    Saves the CO2 emissions data to a SQLite database.
    """
    conn = sqlite3.connect(CO2_DB_PATH)
    co2_df.to_sql('co2_emissions', conn, if_exists='replace', index=False)
    conn.close()


def main() -> None:
    """
    Downloads the data sets used for the project,
    preprocesses the data and fixes errors in them and
    saves the data in the ./data directory as sqlite.
    """
    kaggle_api = authenticate_kaggle_api()
    deforestation_df, co2_df = download_datasets(kaggle_api)
    save_deforestation_to_sqlite(deforestation_df)
    save_co2_to_sqlite(co2_df)


if __name__ == "__main__":
    main()
