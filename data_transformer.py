import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

def transform_data(input_file="storage/dataset.csv", output_folder="storage"):
    os.makedirs(output_folder, exist_ok=True)
    data = pd.read_csv(input_file, index_col=0)

    for col in data.drop(columns='movement').columns:
        data[f'{col}_rate'] = data[col] / data.shift(1)[col]

    data.dropna(inplace=True)
    features = data.drop('movement', axis=1)
    target = data['movement']

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    scaled_df = pd.DataFrame(scaled_features, index=features.index, columns=features.columns)

    split_point = len(data) - 90
    scaled_df[:split_point].to_csv(f"{output_folder}/training_features.csv")
    scaled_df[split_point:].to_csv(f"{output_folder}/testing_features.csv")
    target[:split_point].to_csv(f"{output_folder}/training_labels.csv")
    target[split_point:].to_csv(f"{output_folder}/testing_labels.csv")

if __name__ == '__main__':
    transform_data()