import pandas as pd

from xgboost_model.config import config
from xgboost_model.processing.data_management import load_pipeline
from xgboost_model import __version__ as _version

import logging

_logger = logging.getLogger(__name__)

pipeline_file_name = f"{config.PIPELINE_SAVE_FILE}{_version}.pkl"
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(input_data):
    """Make a prediction using the saved model pipeline."""

    data = pd.DataFrame(input_data, index=[len(input_data)-1])
    # validated_data = validate_inputs(input_data=data)
    prediction = _price_pipe.predict(data)
    # output = np.exp(prediction)

    results = {"predictions": prediction, "version": _version}

    print(f"Making predictions with model version: {_version} ")
    print(f"Inputs: {data} ")
    print(f"Predictions: {results}")

    return results


if __name__ == "__main__":
    make_prediction(config.sample_data)
