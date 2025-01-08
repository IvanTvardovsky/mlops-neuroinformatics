import unittest
from data_initializer import generate_dataset


class TestDatasetGeneration(unittest.TestCase):
    def test_data_processing(self):

        output_df = generate_dataset()

        self.assertFalse(output_df.empty)

        expected_cols = ['open', 'high', 'low', 'close', 'volume',
                         'movement', '000001.SS', 'AAPL', 'CL=F',
                         'GC=F', 'HG=F', 'NVDA', '^DJI', '^GSPC',
                         '^N100', '^N225']

        for col in expected_cols:
            self.assertIn(col, output_df.columns)

        self.assertGreater(len(output_df), 3000)


if __name__ == '__main__':
    unittest.main()
