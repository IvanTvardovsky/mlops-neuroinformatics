import unittest
import pandas as pd
import os

from data_transformer import transform_data

class TestPreprocessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = "temp_data"
        os.makedirs(self.temp_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(self.temp_dir)

    def test_data_transformation(self):
        data_dict = {
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [95, 96, 97, 98, 99],
            'close': [101, 102, 103, 104, 105],
            'volume': [1000, 1100, 1200, 1300, 1400],
            'movement': [1.0, 2.0, 1.5, -1.0, 0.5]
        }
        data_frame = pd.DataFrame(data_dict)
        file_path = os.path.join(self.temp_dir, "input_data.csv")
        data_frame.to_csv(file_path, index=False)

        transform_data(file_path, self.temp_dir)

        expected_files = [
            "training_features.csv",
            "testing_features.csv",
            "training_labels.csv",
            "testing_labels.csv"
        ]

        for file in expected_files:
            file_path = os.path.join(self.temp_dir, file)
            self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
