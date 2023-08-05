import pathlib

import xgboost_model

PACKAGE_ROOT = pathlib.Path(xgboost_model.__file__).resolve().parent
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
TRAINING_DATA_FILE = "properties-80210.csv"

MODEL_NAME = "xgboost"
PIPELINE_SAVE_FILE = f"{MODEL_NAME}_v"

target = "price"
random_state = 17
test_size = 0.3

var_rename_dict = {
    "real estate provider": "provider"
}

KEEP_FEATURES = ['postal_code', 'provider', 'type', 'bed_count', 'bath_count', 'sqft']

categorical_vars = ['provider', 'type', 'postal_code']

sample_data={
    'title': 'Apartment for sale'
    ,'address': None
    ,'city': 'Denver'
    ,'state': 'CO'
    ,'postal_code': '80210'
    ,'price': "$875,000"
    ,'facts and features': '3 bds, 4.0 ba ,2821 sqft'
    ,'real estate provider': 'Re/max Alliance'
    ,'url': 'https://www.zillow.com/homedetails/2005-S-Washington-St-Denver-CO-80210/13378053_zpid/'
}