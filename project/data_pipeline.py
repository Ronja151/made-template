import os
import zipfile

from kaggle.api.kaggle_api_extended import KaggleApi

DATASET_NAMES = {
    "brazilian_amazon": "mbogernetto/brazilian-amazon-rainforest-degradation",
    "global_fossil_co2": "thedevastator/global-fossil-co2-emissions-by-country-2002-2022"
}
FILE_NAMES = {
    "deforestation_data": "def_area_2004_2019.csv",
    "co2_data": "GCB2022v27_MtCO2_flat.csv"
}
ZIP_FILE_PATH = "../data/GCB2022v27_MtCO2_flat.csv.zip"
DATA_PATH = "../data"


def authenticate_kaggle_api() -> KaggleApi:
    """
    Authenticates the Kaggle API.
    """
    kaggle_api = KaggleApi()
    kaggle_api.authenticate()
    return kaggle_api


def download_datasets(kaggle_api: KaggleApi) -> None:
    """
    Downloads data on deforestation in the Brazilian Amazon and global CO2 emissions data from fossil fuels.
    """
    kaggle_api.dataset_download_file(DATASET_NAMES["brazilian_amazon"], FILE_NAMES["deforestation_data"], path=DATA_PATH)
    kaggle_api.dataset_download_file(DATASET_NAMES["global_fossil_co2"], FILE_NAMES["co2_data"], path=DATA_PATH)


def extract_co2_data_zip() -> None:
    """
    Unpacks the CO2 data from the ZIP file.
    """
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zip_ref:
        zip_ref.extract(FILE_NAMES["co2_data"], DATA_PATH)
    os.remove(ZIP_FILE_PATH)


def main() -> None:
    """
    Downloads the data sets used for the project,
    preprocesses the data and fixes errors in them and
    saves the data in the /data directory as sqlite.
    """
    kaggle_api = authenticate_kaggle_api()
    download_datasets(kaggle_api)
    extract_co2_data_zip()


if __name__ == "__main__":
    main()
