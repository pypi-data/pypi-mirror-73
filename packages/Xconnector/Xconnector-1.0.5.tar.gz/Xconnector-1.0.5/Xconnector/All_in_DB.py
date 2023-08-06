import pandas as pd 
from pandas import DataFrame

##### get all id from all DB with text search

def get_id_all(search_by):
    search_by = search_by.strip()
    #search_by = f'"{search_by}"'
    all_ids = []

    from HMDB import Search as search_hmdb
    all_ids.append( search_hmdb(query = search_by , searcher= "metabolites") )

    from LMDB import txtsearch as search_lmdb
    all_ids.append( search_lmdb( query = search_by ) )
 
    from YMDB import txtsearch as search_ymdb
    all_ids.append( search_ymdb( query = search_by ) )

    from T3DP import txtsearch as search_t3db
    all_ids.append( search_t3db(query= search_by) )


    all_ids = [z for i in all_ids for z in i]
    
    return all_ids

#print ( get_id_all( "1-Methylhistidine" ) )
#### function to count how ids are collected and from where

def stat_db(list_ids):
    HMDB = 0
    LMDB = 0
    YMDB = 0
    T3DB = 0
    for i_id in list_ids:
        if "HMDB" in i_id:
            HMDB += 1
        elif "LMDB" in i_id:
            LMDB += 1
        elif "YMDB" in i_id:
            YMDB += 1
        elif "T3D" in i_id:
            T3DB += 1
    dict_all = {"HMDB": HMDB, "LMDB": LMDB, "YMDB": YMDB, "T3DB": T3DB }

    return dict_all

#print ( stat_db( get_id_all( "1-Methylhistidine" ) ) )

##### get the information of each ID from its DB

def get_info_ids(list_ids):
    """
    
    print ( get_info_ids( get_id_all( "1-Methylhistidine" ) ) )

    """
    all_df = pd.DataFrame()

    HMDB_ids = [i for i in list_ids if "HMDB" in i]
    LMDB_ids = [i for i in list_ids if "LMDB" in i]
    YMDB_ids = [i for i in list_ids if "YMDB" in i]
    T3DB_ids = [i for i in list_ids if "T3D" in i]

    if len(HMDB_ids) != 0:

        from HMDB import Geninfo as info_hmdb

        for i_data in info_hmdb(HMDB_ids):
            all_df = pd.concat([all_df, i_data], axis=0,sort=False)

    else:
        pass

    if len(LMDB_ids) != 0:

        from LMDB import Geninfo as info_lmdb

        for i_data in info_lmdb(LMDB_ids):
            all_df = pd.concat([all_df, i_data], axis=0,sort=False)

    if len(YMDB_ids) != 0:

        from YMDB import Geninfo as info_ymdb

        for i_data in info_ymdb(YMDB_ids):
            all_df = pd.concat([all_df, i_data], axis=0,sort=False)
    else:
        pass

    if len(T3DB_ids) != 0:
        from T3DP import Geninfo as info_t3db

        for i_data in info_t3db(T3DB_ids):
            all_df = pd.concat([all_df, i_data], axis=0,sort=False)
    else:
        pass

    return all_df

#print ( get_info_ids( get_id_all( "Glutathione" ) ) )


def PredProp_all(accessions , db = ""):


    if type(accessions) != list:
        raise TypeError ("SynonymsData takes list as an argument")
    
    if db == "HMDB":
        main_url = "http://www.hmdb.ca/metabolites/"
    elif db == "LMDB":
        main_url = "http://lmdb.ca/metabolites/"
    elif db == "YMDB":
        main_url = "http://www.ymdb.ca/compounds/"
    elif db == "T3D":
        main_url = "http://www.t3db.ca/toxins/"
    

    for i_acc in accessions:
        # creating the query search url by accessions
        api_request = main_url + i_acc
        try:
            tables = pd.read_html(api_request)
            tables = tables[3]
        except:
            tables = pd.DataFrame(data = {"Property":["NA"],"Value":["NA"],"Source":["NA"]})

        # to make the row.names =  to the id 
        index_name = range(0,len(tables))
        index_value = f"{i_acc}," *len(index_name)
        index_value = index_value.split(",")
        dictionary = dict(zip(index_name, index_value))
        tables = tables.rename(index= dictionary )

        yield tables


