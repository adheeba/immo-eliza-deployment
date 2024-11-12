import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

def clean_data(df):
    """
    Takes a df as input and will clean the data.
    It will: capitalize the locality names, remove whitespaces, check for empty places, check if numeric colums are numeric
    """

    # remove whitespaces
    df = remove_whitespaces(df)

    # capitalizes the localities
    if 'locality_name' in df.columns:
        df['locality_name'] = df['locality_name'].str.capitalize()

    # check empty cells and fill them with na
    df = fill_empty_with_na(df)

    # check the selected columns are numeric same as the one specified
    df = check_type_numeric_cols(df)
    if 'postal_code' in df.columns:
        df['postal_code_str'] = df['postal_code'].astype(str)

    return df

def check_type_numeric_cols(df):
    '''
    Checks if all numeric columns are really numeric and changes them otherwise.
    It takes and returns a df.
    '''
    all_numeric_columns = ["property_id","living_area","price", "number_of_rooms","postal_code",
                          "terrace_surface","garden","land_area", "facades","open_fire","swimming_pool","furnished"]
    present_numeric_columns = [item for item in all_numeric_columns if item in df.columns]
    numeric_columns_df =  df[present_numeric_columns]


    # check the selected columns are numeric same as the one specified
    numeric_columns = df.select_dtypes(include=np.number).columns
    is_all_numeric = len(numeric_columns) == len(numeric_columns_df.columns)
    if(not is_all_numeric):
        convert_dict = { }
        for column in numeric_columns_df:
            # Select column contents by column
            try:
                columnSeriesObj = numeric_columns_df[column]
                if is_numeric_dtype(columnSeriesObj.dtype):
                    convert_dict[column] = columnSeriesObj.dtype
                else:
                    convert_dict[column] = np.float64
            except:
                if column == 'price':
                    print(f'{column} not present since it is a prediction')
                continue
        df = df.astype(convert_dict)

    return df


def fill_empty_with_na(df):
    if (df.isnull().sum().sum()) != 0:

        #Replace empty strings if any.
        df.replace('', np.nan, inplace=True)

        #Make NaN as the placeholder for every null value representation
        df.fillna(value=np.nan, inplace=True)

    return df

def remove_whitespaces(df):
    '''
    Takes a df and will remove all whitespaces from the object columns. It returns a df
    '''
    if 'locality_name' in df.columns:
        df['locality_name'] = df['locality_name'].str.strip()
    if 'link' in df.columns:
        df['link'] = df['link'].str.strip()
    df['type_of_property'] = df['type_of_property'].str.strip()
    df['subtype_of_property'] = df['subtype_of_property'].str.strip()
    df['equipped_kitchen'] = df['equipped_kitchen'].str.strip()
    df['state_of_building'] = df['state_of_building'].str.strip()

    return df
