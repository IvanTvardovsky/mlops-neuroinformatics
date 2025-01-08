import unittest
import os
import shutil
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from model_tester import assess_model


class TestModel(unittest.TestCase):
    def setUp(self):
        self.base_dir = 'test_dir'
        os.mkdir(self.base_dir)

        self.data_dir = os.path.join(self.base_dir, 'data')
        os.mkdir(self.data_dir)

        features_data = pd.DataFrame({
            'open': [0.6095, 0.5759, 0.6418],
            'high': [0.6112, -0.7703, 0.13523],
            'low': [1.7676, 0.23695, 0.6469],
            'close': [1.0887, 0.4828, 2.657],
            'volume': [-0.10299, 1.173, 1.345]
        })

        target_data = pd.Series([1.624, 2.223, 0.064], name='target')

        features_data.to_csv(os.path.join(self.data_dir, 'training_features.csv'), index=True)
        target_data.to_csv(os.path.join(self.data_dir, 'training_labels.csv'), index=True)

        features_data.to_csv(os.path.join(self.data_dir, 'testing_features.csv'), index=True)
        target_data.to_csv(os.path.join(self.data_dir, 'testing_labels.csv'), index=True)

        model = LinearRegression()
        model.fit(features_data, target_data)
        with open(os.path.join(self.base_dir, 'model.pkl'), 'wb') as model_file:
            pickle.dump(model, model_file)

    def tearDown(self):
        shutil.rmtree(self.base_dir)

    def test_model_assessment(self):
        result = assess_model(model_file=os.path.join(self.base_dir, 'model.pkl'),
                              dataset_path=self.data_dir)

        self.assertTrue("Testing Results:" in result)
        self.assertTrue("MSE:" in result)
        self.assertTrue("R2:" in result)


if __name__ == '__main__':
    unittest.main()
