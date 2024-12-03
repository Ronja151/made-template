import os
import unittest
from unittest.mock import MagicMock, patch
import data_pipeline
from pandas.testing import assert_frame_equal

import pandas as pd
from data_pipeline import (
    authenticate_kaggle_api,
    download_datasets,
    validate_data,
    save_co2_to_sqlite,
    save_deforestation_to_sqlite,
    clean_co2_data,
    main
)

class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
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
    @patch('data_pipeline.save_deforestation_to_sqlite')
    @patch('data_pipeline.save_co2_to_sqlite')
    def test_pipeline_output(self, mock_save_co2, mock_save_deforestation, mock_download_datasets, mock_authenticate_kaggle_api):
        mock_kaggle_api_instance = MagicMock()
        mock_authenticate_kaggle_api.return_value = mock_kaggle_api_instance
        mock_deforestation_df = pd.DataFrame({
            'Ano/Estados': ['Brazil', 'Brazil'],
            'AMZ LEGAL': [2004, 2005]
        })
        mock_co2_df = pd.DataFrame({
            'country': ['Brazil', 'Brazil'],
            'year': [2004, 2005],
            'co2': [1.1, 1.2],
            'co2_including_luc': [1.5, 1.7],
            'cumulative_co2': [10, 15],
            'cumulative_co2_including_luc': [15, 20],
            'cumulative_luc_co2': [5, 6],
            'land_use_change_co2': [0.1, 0.2]
        })
        mock_download_datasets.return_value = (mock_deforestation_df, mock_co2_df)
        mock_save_deforestation.return_value = None
        mock_save_co2.return_value = None
        main()

        mock_authenticate_kaggle_api.assert_called_once()
        mock_download_datasets.assert_called_once_with(mock_kaggle_api_instance)
        mock_save_deforestation.assert_called_once()  
        mock_save_co2.assert_called_once()  
    
    def test_validate_data(self):
        required_columns = list(['country', 'year', 'co2'])
        valid_data = pd.DataFrame({
            'country': ['Brazil', 'Brazil'],
            'year': [2004, 2005],
            'co2': [1.1, 1.2]
        })
        invalid_data_missing_columns = pd.DataFrame({'country': ['Brazil']})
        invalid_data_empty = pd.DataFrame()

        self.assertTrue(validate_data(valid_data, required_columns))
        self.assertFalse(validate_data(invalid_data_missing_columns,required_columns))
        self.assertFalse(validate_data(invalid_data_empty,required_columns))

    def test_clean_co2_data(self):
        input_data = pd.DataFrame({
            'country': ['Brazil', 'USA', 'Brazil', 'India'],
            'year': [2000, 2005, 2010, 2019],
            'co2': [1.1, 5.2, 3.1, 2.9],
            'co2_including_luc': [1.5, 5.7, 3.6, 3.3],
            'cumulative_co2': [10, 50, 70, 20],
            'cumulative_co2_including_luc': [15, 60, 80, 25],
            'cumulative_luc_co2': [5, 10, 15, 5],
            'land_use_change_co2': [0.1, 0.2, 0.3, 0.4]
        })
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
        output_data = clean_co2_data(input_data)
        assert_frame_equal(expected_output.reset_index(drop=True), output_data.reset_index(drop=True))

if __name__ == '__main__':
    unittest.main()