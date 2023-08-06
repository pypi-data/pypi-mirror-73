# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

import pandas as pd

def concat_tablelist(table1=None,table2=None):
    if table1 is None or table2 is None:
        if table1 is not None:
            return table1
        else:
            return table2
    return pd.concat([table1,table2],ignore_index=True)
    