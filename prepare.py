import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from acquire import get_zillow_data




######################## Helper Functions #######################################

def fips_labels(x):
    if x['fips'] == 6037:
        return 'Los Angeles County'
    elif x['fips'] == 6059:
        return 'Orange County'
    elif x['fips'] == 6111:
        return 'Ventura County'

def handle_missing_values(df, prop_required_column = .60, prop_required_row = .60):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df 

def zillow_split(df):
    train_and_validate, test = train_test_split(df, test_size=.12, random_state=27)
    train, validate = train_test_split(train_and_validate, test_size=.22, random_state=27)
    return train, validate, test


######################## FINAL PREP #######################################

def prep_zillow():
    # create dataframe from local cached csv
    df = pd.read_csv('zillow.csv')

    # add a county column from function
    df['county'] = df.apply(lambda x: fips_labels(x), axis=1)

    # filter for single unit properties
    df = df[df.propertylandusetypeid.isin([260, 261, 263, 264, 266, 270, 273, 274, 275, 279])]

    # dropping desciption, id, irrelevant, or redundant columns
    df = df.drop(columns=['id', 'roomcnt', 'fips', 'rawcensustractandblock', 
                      'propertycountylandusecode', 'fullbathcnt', 'parcelid',
                      'heatingorsystemtypeid', 'unitcnt', 'buildingqualitytypeid',
                      'propertyzoningdesc','heatingorsystemtypeid', 
                      'heatingorsystemdesc', 'calculatedbathnbr','finishedsquarefeet12',
                      'assessmentyear', 'propertylandusedesc', 'censustractandblock',
                      'regionidcity', 'regionidcounty'])

    # drop columns and rows with over 60% values missing: from function
    df = handle_missing_values(df)

    # Function to split data into train, validate, test datasets
    train, validate, test = zillow_split(df)

    # Categorical/Discrete columns to use mode to replace nulls
    cols = ["regionidzip", "yearbuilt"]
    for col in cols:
        mode = int(train[col].mode()) 
        train[col].fillna(value=mode, inplace=True)
        validate[col].fillna(value=mode, inplace=True)
        test[col].fillna(value=mode, inplace=True)
    
    # Continuous valued columns to use median to replace nulls
    cols = [
        "structuretaxvaluedollarcnt", "taxamount",
        "taxvaluedollarcnt", "landtaxvaluedollarcnt",
        "structuretaxvaluedollarcnt", "calculatedfinishedsquarefeet",
        "lotsizesquarefeet"]
    for col in cols:
        median = train[col].median()
        train[col].fillna(median, inplace=True)
        validate[col].fillna(median, inplace=True)
        test[col].fillna(median, inplace=True)
    
    # rename columns for easy reading
    cols_to_rename = {
        'regionidzip': 'zipcode',
        'calculatedfinishedsquarefeet': 'sqft',
        'taxvaluedollarcnt': 'home_value',
        'lotsizesquarefeet': 'lot_sqft',
        'propertylandusetypeid': 'property_type',
        'structuretaxvaluedollarcnt': 'structure_value',
        'landtaxvaluedollarcnt': 'land_value'
        ''}
    train = train.rename(columns=cols_to_rename)
    validate = validate.rename(columns=cols_to_rename)
    test = test.rename(columns=cols_to_rename)

    return train, validate, test