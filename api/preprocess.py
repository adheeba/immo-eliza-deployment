import pandas as pd
import numpy as np
import clean
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import category_encoders as ce
import joblib

def handle_null_values(df_preprocess, method_dict):
    pd.options.mode.copy_on_write = True
    #df_preprocess['property_area'] = df_preprocess[['terrace_surface', 'garden', 'land_area']].sum(axis=1)
    #df_preprocess = df_preprocess.drop(columns=['terrace_surface', 'garden', 'land_area'])
    for column, method in method_dict.items():
        if method == 'median':
            median = df_preprocess[column].median()
            df_preprocess.fillna({column:median}, inplace=True)

        elif method == 'mode':
            mode = df_preprocess[column].mode()
            df_preprocess.fillna({column:mode}, inplace=True)

        elif method == 'replace':
            df_preprocess.fillna({column:'UNKNOWN'}, inplace=True)

        elif method == 'drop':
            df_preprocess.dropna(subset=[column], inplace=True)
        else:
            print(f'{method} to handle null value not found for {column}')
            continue

    return df_preprocess

def group_categorical_columns(df_preprocess, column_group):
    for column, groups in column_group.items():
        for value, replacer in groups.items():
            df_preprocess[column] = df_preprocess[column].replace(value, replacer)
    return df_preprocess

def create_encoders(df_preprocess, method_dict):
    for column, method in method_dict.items():
        if method == 'onehotencoding':
            oh= OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform="pandas")
            one_hot_encoded=oh.fit(df_preprocess[[column]])
            filename = 'data/encoders/'+column + '_' + method+'.pkl'
            joblib.dump(one_hot_encoded, filename)

        elif method == 'ordinalencoding':
            df_column = pd.DataFrame(df_preprocess, columns= [column, 'price'])
            df_column_median = pd.DataFrame(df_column.groupby(column, as_index=False).median().sort_values(by='price'))
            category_ordered = np.array(df_column_median[column])

            encoder = OrdinalEncoder(categories=[category_ordered])
            filename = 'data/encoders/'+column + '_' + method+'.pkl'
            joblib.dump(encoder, filename)
            #df_preprocess[column] = encoder.fit_transform(df_preprocess[[column]])

        elif method == 'hashencoding':
            encoder = ce.HashingEncoder(cols=[column], n_components=3)
            df_encoded = encoder.fit(df_preprocess[[column]])
            filename = 'data/encoders/'+column + '_' + method+'.pkl'
            joblib.dump(encoder, filename)
            #df_preprocess = pd.concat([df_preprocess,df_encoded],axis=1).drop(columns=[column])

        else:
            print(f'method {method} not supported')
def encode_categorical_columns(df_preprocess, method_dict):
    for column, method in method_dict.items():
        if method == 'onehotencoding':
            filename = 'data/encoders/'+column + '_' + method+'.pkl'
            encoder = joblib.load(filename)
            one_hot_encoded=encoder.transform(df_preprocess[[column]])
            one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=encoder.get_feature_names_out([column]))
            df_preprocess = pd.concat([df_preprocess,one_hot_encoded_df],axis=1).drop(columns=[column])

        elif method == 'ordinalencoding':
            filename = 'data/encoders/'+column + '_' + method+'.pkl'
            encoder = joblib.load(filename)
            df_preprocess[column] = encoder.fit_transform(df_preprocess[[column]])

        elif method == 'hashencoding':
            filename = 'data/encoders/'+column + '_' + method+'.pkl'
            encoder = joblib.load(filename)
            df_encoded = encoder.fit_transform(df_preprocess[[column]])
            df_preprocess = pd.concat([df_preprocess,df_encoded],axis=1).drop(columns=[column])

        else:
            print(f'method {method} not supported')
            return df_preprocess

    return df_preprocess
'''        
def encode_categorical_columns(df_preprocess, method_dict):
    for column, method in method_dict.items():
        if method == 'onehotencoding':
            oh= OneHotEncoder(sparse_output=False).set_output(transform="pandas")
            one_hot_encoded=oh.fit_transform(df_preprocess[[column]])
            df_preprocess = pd.concat([df_preprocess,one_hot_encoded],axis=1).drop(columns=[column])

        elif method == 'ordinalencoding':
            df_column = pd.DataFrame(df_preprocess, columns= [column, 'price'])
            df_column_median = pd.DataFrame(df_column.groupby(column, as_index=False).median().sort_values(by='price'))
            category_ordered = np.array(df_column_median[column])

            encoder = OrdinalEncoder(categories=[category_ordered])
            df_preprocess[column] = encoder.fit_transform(df_preprocess[[column]])

        elif method == 'hashencoding':
            encoder = ce.HashingEncoder(cols=[column], n_components=3)
            df_encoded = encoder.fit_transform(df_preprocess[[column]])
            df_preprocess = pd.concat([df_preprocess,df_encoded],axis=1).drop(columns=[column])

        else:
            print(f'method {method} not supported')
            return df_preprocess

    return df_preprocess
'''
def preprocess_data(raw_df, type):
    #data_path = "../data/raw/raw_properties_new.csv"
    
    df = clean.clean_data(raw_df)

    important_columns_all = ['price','type_of_property', 'subtype_of_property', 'number_of_rooms',
        'living_area', 'furnished', 'open_fire', 'terrace_surface', 'garden',
        'facades', 'swimming_pool', 'land_area', 'equipped_kitchen',
        'state_of_building']
    
    important_columns = [item for item in important_columns_all if item in df.columns]

    removable_columns = ['link', 'property_id', 'locality_name', 'type_of_sale', 'postal_code_str']

    categorical_columns = ['furnished', 'open_fire', 'swimming_pool', 'equipped_kitchen', 'state_of_building',
                        'type_of_property', 'subtype_of_property']

    quantitative_columns = ['price', 'number_of_rooms', 'living_area', 'terrace_surface', 'garden',
                            'facades', 'land_area']

    target = 'price'

    df_preprocess = df[important_columns]
    handle_null_methods = {}

    for column in df_preprocess.columns:
        if(df_preprocess[column].isnull().sum() != 0):
            
            if column == target:
                handle_null_methods[column] = 'drop'
            else:
                if is_string_dtype(df_preprocess[column]):
                    handle_null_methods[column] = 'replace'
                elif is_numeric_dtype(df_preprocess[column]):
                    handle_null_methods[column] = 'median'
                else:
                    handle_null_methods[column] = 'replace'

    df_preprocess = handle_null_values(df_preprocess, handle_null_methods)

    if 1:
        column_group = {
            'equipped_kitchen':
                {
                'USA_SEMI_EQUIPPED':'SEMI_EQUIPPED',
                'USA_INSTALLED':'INSTALLED',
                'USA_HYPER_EQUIPPED':'HYPER_EQUIPPED'
                },
            'state_of_building':
                {
                    'TO_BE_DONE_UP':'TO_RENOVATE',
                    'TO_RESTORE':'TO_RENOVATE',
                    'JUST_RENOVATED':'GOOD'
                }
        }

        df_preprocess = group_categorical_columns(df_preprocess, column_group)

        if type == 'train':  
            categorical_encoding = {
                'state_of_building': 'ordinalencoding',
                'equipped_kitchen': 'ordinalencoding',
                'type_of_property': 'onehotencoding',
                'subtype_of_property': 'ordinalencoding',
            }

            create_encoders(df_preprocess, categorical_encoding)

        if 1:#type == 'train':  
            categorical_encoding = {
                'state_of_building': 'ordinalencoding',
                'equipped_kitchen': 'ordinalencoding',
                'type_of_property': 'onehotencoding',
                'subtype_of_property': 'ordinalencoding',
            }

            df_preprocess = encode_categorical_columns(df_preprocess, categorical_encoding)

    #df_preprocess.to_csv(out_path)
    return df_preprocess