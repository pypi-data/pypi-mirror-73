import pandas as pd 
from pandas import DataFrame


def make_it_correct(df):

    def name_id_cas(x_str, name_ = False , IDs_ = False, cas_ = False):
        #name
        x_str_name1 = x_str.rfind("(")
        names = x_str[:x_str_name1]

        #id
        x_str_name2 = x_str.rfind(")")
        IDs = x_str[x_str_name1+1:x_str_name2]

        #cas num
        cas = x_str[x_str_name2+1:]

        if name_ == True:
            return names
        if IDs_ == True:
            return IDs
        if cas_ == True:
            return cas
        

    df[["Weight","C","Formula"]] = df['Weight/Formula'].str.split('([A-Z][1-9]*)', n = 1, expand=True)
    df['Formula'] = df[['C', 'Formula']].astype(str).apply(''.join, axis=1)
    df.drop( ["C","Weight/Formula"] , axis = 1, inplace = True ) 

    df["Name"] = df['Name/CAS Number'].astype(str).apply(name_id_cas , name_ = True )
    df["IDs"] = df['Name/CAS Number'].astype(str).apply(name_id_cas , IDs_ = True )
    df["CAS Number"] = df['Name/CAS Number'].astype(str).apply(name_id_cas , cas_ = True )
    df.drop( ["Name/CAS Number"] , axis = 1, inplace = True )

    return df