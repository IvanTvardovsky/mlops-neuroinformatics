import pickle
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

def assess_model(model_file="svr_model.pkl", dataset_path="storage"):
    with open(model_file, "rb") as file:
        loaded_model = pickle.load(file)

    test_x = pd.read_csv(f"{dataset_path}/testing_features.csv", index_col=0)
    test_y = pd.read_csv(f"{dataset_path}/testing_labels.csv", index_col=0)

    predictions = loaded_model.predict(test_x)
    mse_score = mean_squared_error(test_y, predictions)
    r2_value = r2_score(test_y, predictions)

    result = f"Testing Results:\nMSE: {mse_score}\nR2: {r2_value}"
    print(result)

    pd.DataFrame(predictions, index=test_x.index, columns=["Prediction"]).to_csv(f"{dataset_path}/testing_forecasts.csv")

    return result

if __name__ == '__main__':
    assess_model()