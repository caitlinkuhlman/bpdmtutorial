import numpy as np
import pandas as pd
import scipy

### Utility functions for the COMPAS tutorial ###


def clean_compas(df):
    
    # Clean the compas dataset according to the description provided by ProPublica of their analysis. 
    # In the original notebook the authors state:

    # There are a number of reasons remove rows because of missing data:
        
        # If the charge date of a defendants Compas scored crime was not within 30 days from when the person was arrested, 
        # we assume that because of data quality reasons, that we do not have the right offense.

        # We coded the recidivist flag -- `is_recid` -- to be -1 if we could not find a compas case at all.

        # In a similar vein, ordinary traffic offenses -- those with a `c_charge_degree` of 'O' -- will not result in Jail time 
        # are removed (only two of them).
 
        # We filtered the underlying data from Broward county to include only those rows representing people who had either 
        # recidivated in two years, or had at least two years outside of a correctional facility.

    # ix is the index of variables we want to keep.
    # Remove entries with inconsistent arrest information.
    rows_start = len(df)
    ix = df['days_b_screening_arrest'] <= 30
    ix = (df['days_b_screening_arrest'] >= -30) & ix

    # remove entries entries where compas case could not be found.
    ix = (df['is_recid'] != -1) & ix

    # remove traffic offenses.
    ix = (df['c_charge_degree'] != "O") & ix

    # remove entries without available text scores.
    ix = (df['score_text'] != 'N/A') & ix

    # trim dataset
    df = df.loc[ix,:]

    # create new attribute "length of stay" with total jail time.
    df['length_of_stay'] = (pd.to_datetime(df['c_jail_out'])-pd.to_datetime(df['c_jail_in'])).apply(lambda x: x.days)

    # print number of rows
    print('Number of rows removed: '+str(rows_start - len(df)))
    # print list of features again
    print('Features: '+str(list(df)))
    return df