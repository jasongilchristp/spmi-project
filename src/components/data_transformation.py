import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_objects

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts", "preprocessor.pkl")  ## Pickel file path

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            logging.info(f"Numerical COlumns {numerical_columns}")
            logging.info(f"Categorical COlumns {categorical_columns}")

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  ## median imputation because of the presense of outliers
                    ("scaler", StandardScaler())
                ]
            )
            logging.info("Numerical columns scaling completed")
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")), ## mode impuation since it's categorical columns
                    ("one_hot_encoder", OneHotEncoder())
                ]
            )
            logging.info("Categorical columns encoding completed")

            preprocessor = ColumnTransformer( 
                [
                    ("num_pipeline", num_pipeline,numerical_columns), ## pipeline name, what pipeline it is, columns
                    ("cat_pipeline", cat_pipeline,categorical_columns) ## column transformer is a combination of numerical and categorical pipelines
                ]
            )
        except Exception as e:
            raise CustomException(e, sys)
        return preprocessor
        
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column = "math_score"
            
            input_feature_train_df = train_df.drop(target_column, axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(target_column, axis=1)
            target_feature_test_df = test_df[target_column]


            logging.info("Appling preprocesssing object on training dataframe and test dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Saved preprocessing object")

            save_objects(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
                    
        except Exception as e:
            raise CustomException(e,sys)
    