import data_initializer
import data_transformer
import model_constructor
import model_tester

if __name__ == "__main__":
    data_initializer.generate_dataset()
    data_transformer.transform_data()
    model_constructor.construct_model()
    model_tester.assess_model()