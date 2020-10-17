import pandas as pd
import numpy as np
import os
from env import host, user, password

###################### Acquire Zillow Data ######################

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
def new_zillow_data():
    '''
    This function reads the zillow data from the Codeup db into a df,
    write it to a csv file, and returns the df.
    '''
    sql_query = '''
            SELECT p1.*
            , p2.transactiondate
            , p2.logerror 
            , ac.airconditioningdesc
            , arch.architecturalstyledesc
            , bldg.buildingclassdesc
            , heat.heatingorsystemdesc
            , land.propertylandusedesc
            , stories.storydesc
            , const.typeconstructiondesc
    FROM zillow.properties_2017 p1
    LEFT JOIN zillow.airconditioningtype ac USING(airconditioningtypeid)
    LEFT JOIN zillow.architecturalstyletype arch USING(architecturalstyletypeid)
    LEFT JOIN zillow.buildingclasstype bldg USING(buildingclasstypeid)
    LEFT JOIN zillow.heatingorsystemtype heat USING(heatingorsystemtypeid)
    LEFT JOIN zillow.propertylandusetype land USING(propertylandusetypeid)
    LEFT JOIN zillow.storytype stories USING(storytypeid)
    LEFT JOIN zillow.typeconstructiontype const USING(typeconstructiontypeid)
    INNER JOIN (
	    SELECT p2.parcelid, p1.logerror, p2.max_transactiondate AS transactiondate 
            FROM zillow.predictions_2017 p1
            INNER JOIN (SELECT parcelid, MAX(transactiondate) AS max_transactiondate 
                    FROM zillow.predictions_2017 
                    GROUP BY parcelid) p2
            ON p1.parcelid = p2.parcelid AND p1.transactiondate = p2.max_transactiondate
        ) p2 USING(parcelid)
    INNER JOIN (
	    SELECT parcelid, logerror, MAX(transactiondate) AS transactiondate FROM zillow.predictions_2017 GROUP BY parcelid, logerror
        ) t2 USING(parcelid, transactiondate)
    WHERE (p1.bedroomcnt > 0 AND p1.bathroomcnt > 0 
            AND calculatedfinishedsquarefeet > 500
            AND latitude IS NOT NULL AND longitude IS NOT NULL)
            AND (unitcnt = 1 OR unitcnt IS NULL)
    ;
    '''
    df = pd.read_sql(sql_query, get_connection('zillow'))
    df.to_csv('zillow.csv')
    return df

def get_zillow_data(cached=False):
    '''
    This function reads in zillow data from Codeup database if cached == False 
    or if cached == True reads in zillow df from a csv file, returns df
    '''
    if cached or os.path.isfile('zillow_df.csv') == False:
        df = new_zillow_data()
    else:
        df = pd.read_csv('zillow_df.csv', index_col=0)
    return df