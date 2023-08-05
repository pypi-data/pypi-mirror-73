from sklearn.pipeline import Pipeline
import xgboost as xgb

from xgboost_model.processing import preprocessing as pp
from xgboost_model.processing import features

price_pipe = Pipeline(
    [
        (
            "create_type_var", features.CreateTypeVar(),
        ),
        (
            "create_additional_vars", features.CreateAdditionalVars(),
        ),
        (
            "rename_cols", pp.RenameCols(),
        ),
        (
            "label_encoding", pp.LabelEncoding(),
        ),
        (
            "keep_features", pp.KeepFeatures(),
        ),
        (
            "xgboost_model", xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                                              max_depth=5, alpha=10, n_estimators=10)
        ),
    ]
)