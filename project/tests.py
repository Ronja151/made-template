import os
import sqlite3
import unittest
from unittest.mock import MagicMock, patch
from pandas.testing import assert_frame_equal
import pandas as pd
from data_pipeline import (
    save_co2_to_sqlite,
    save_deforestation_to_sqlite,
    validate_data,
    clean_co2_data,
    main
)


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.co2_data = pd.DataFrame({
            'country': ['Brazil', 'USA', 'Brazil', 'India'],
            'year': [2000, 2005, 2010, 2019],
            'co2': [1.1, 5.2, 3.1, 2.9],
            'co2_including_luc': [1.5, 5.7, 3.6, 3.3],
            'cumulative_co2': [10, 50, 70, 20],
            'cumulative_co2_including_luc': [15, 60, 80, 25],
            'cumulative_luc_co2': [5, 10, 15, 5],
            'land_use_change_co2': [0.1, 0.2, 0.3, 0.4]
        })
        self.deforestation_data = pd.DataFrame({
            'Ano/Estados': ['Brazil', 'Brazil'],
            'AMZ LEGAL': [2004, 2005]
        })
        self.deforestation_db_path = "../data/deforestation_data.sqlite"
        self.co2_db_path = "../data/co2_data.sqlite"

        if os.path.exists(self.deforestation_db_path):
            os.remove(self.deforestation_db_path)
        if os.path.exists(self.co2_db_path):
            os.remove(self.co2_db_path)

    def tearDown(self) -> None:
        if os.path.exists(self.deforestation_db_path):
            os.remove(self.deforestation_db_path)
        if os.path.exists(self.co2_db_path):
            os.remove(self.co2_db_path)

    @patch('data_pipeline.authenticate_kaggle_api')
    @patch('data_pipeline.download_datasets')
    def test_pipeline_output(self, mock_download_datasets,
                             mock_authenticate_kaggle_api):
        mock_kaggle_api_instance = MagicMock()
        mock_authenticate_kaggle_api.return_value = mock_kaggle_api_instance
        mock_download_datasets.return_value = (self.deforestation_data, self.co2_data)
        main()

        mock_authenticate_kaggle_api.assert_called_once()
        mock_download_datasets.assert_called_once_with(mock_kaggle_api_instance)

        self.assertTrue(os.path.exists(self.co2_db_path))
        self.assertTrue(os.path.exists(self.deforestation_db_path))

    def test_validate_data(self):
        required_columns = list(['country', 'year', 'co2'])
        invalid_data_missing_columns = pd.DataFrame({'country': ['Brazil']})
        invalid_data_empty = pd.DataFrame()

        self.assertTrue(validate_data(self.co2_data, required_columns))
        self.assertFalse(validate_data(invalid_data_missing_columns, required_columns))
        self.assertFalse(validate_data(invalid_data_empty, required_columns))

    def test_clean_co2_data(self):
        expected_output = pd.DataFrame({
            'country': ['Brazil'],
            'year': [2010],
            'co2': [3.1],
            'co2_including_luc': [3.6],
            'cumulative_co2': [70],
            'cumulative_co2_including_luc': [80],
            'cumulative_luc_co2': [15],
            'land_use_change_co2': [0.3]
        })
        output_data = clean_co2_data(self.co2_data)
        assert_frame_equal(expected_output.reset_index(drop=True), output_data.reset_index(drop=True))

    def test_save_co2_to_sqlite(self):
        save_co2_to_sqlite(self.co2_data)
        conn = sqlite3.connect(self.co2_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM co2_emissions")
        row_count = cursor.fetchone()[0]

        self.assertGreater(row_count, 0)
        conn.close()

    def test_save_deforestation_to_sqlite(self):
        save_deforestation_to_sqlite(self.deforestation_data)
        conn = sqlite3.connect(self.deforestation_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM deforestation")
        row_count = cursor.fetchone()[0]

        self.assertGreater(row_count, 0)
        conn.close()


if __name__ == '__main__':
    unittest.main()
