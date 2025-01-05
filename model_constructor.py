from sklearn.svm import LinearSVR
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import pickle

def construct_model(dataset_path="storage", output_model="svr_model.pkl"):
    train_x = pd.read_csv(f"{dataset_path}/training_features.csv", index_col=0)
    train_y = pd.read_csv(f"{dataset_path}/training_labels.csv", index_col=0).values.ravel()

    model = LinearSVR(random_state=42, max_iter=10000)
    model.fit(train_x, train_y)

    predictions = model.predict(train_x)
    mse_value = mean_squared_error(train_y, predictions)
    r2_value = r2_score(train_y, predictions)

    print(f"Training MSE: {mse_value}\nR2: {r2_value}")

    with open(output_model, "wb") as model_file:
        pickle.dump(model, model_file)

    pd.DataFrame(predictions, index=train_x.index, columns=["Forecast"]).to_csv(f"{dataset_path}/training_forecasts.csv")

if __name__ == '__main__':
    construct_model()