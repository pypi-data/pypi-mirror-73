########################
######## HMDB

def Geninfo_HMDB(accessions, what_to_get ):
    import urllib
    import urllib.request
    import pandas as pd
    from pandas import DataFrame



    if type(accessions) != list:
        raise TypeError ("Geninfo_HMDB takes list as an argument")

    main_url = "http://www.hmdb.ca/metabolites/"
    for i_acc in accessions:
        # creating the query search url by accessions
        api_request = main_url + i_acc
        # get the data in form of tables
    
        tables = pd.read_html(api_request)
        #removing row with no data
        tables0 = tables[0].iloc[:,0:2]
        #rename the col 
        tables0.columns = ["col1", "col2"]

        #take only the general information
        take_from_tables0 = [what_to_get] # Disposition , Process, ( Cellular Locations, Biospecimen Locations, Tissue Locations )	
        
        
        tables0 = tables0[tables0["col1"].isin(take_from_tables0)]

        tables0 = tables0.rename(index={ list(tables0.index)[0] : i_acc})

        yield tables0

########## for Disposition plot ( forund only in HMDB )
def Route(RofE_list):
    
    RofE_dict = {"Enteral" : 0 , "Parenteral" : 0}

    for RofE in RofE_list:
 
        #RofE = RofE[ :RofE.find("Source") ]

        #RofE = RofE[ RofE.find("Route of exposure"):RofE.find("Source") ]
        
        d = [ {i:RofE_dict[i]+1} for i in RofE_dict if i in RofE ]

        z = {}
        for i in d:
            z = {**z, **i} 
        RofE_dict = {**RofE_dict, **z} 

    return RofE_dict
    
def Source(source_list):

    source_dict = {"Endogenous": 0, "Synthetic": 0, "Environmental": 0, "Animal": 0, "Plant": 0, "Microbe": 0}

    for i_source in source_list:

        i_source = i_source[ i_source.find("Source"):i_source.find("Biological location") ]

        d = [ {i:source_dict[i]+1} for i in source_dict if i in i_source ]

        z = {}
        for i in d:
            z = {**z, **i} 
        source_dict = {**source_dict, **z} 

    return source_dict

def organC(organC_list):
    
    organC_dict = {"Gonad": 0, "Mouth": 0, "Lung": 0, "Pancreas": 0, "Prostate": 0, "Intestine": 0, "Testicle": 0, "Spleen": 0, "Bladder": 0, "Brain": 0,
    "Liver": 0, "Kidney": 0 }
    for i_organC in organC_list:

        i_organC = i_organC[ i_organC.find("Biological location") : ]

        d = [ {i:organC_dict[i]+1} for i in organC_dict if i in i_organC ]

        z = {}
        for i in d:
            z = {**z, **i} 
        organC_dict = {**organC_dict, **z} 

    return organC_dict

def subC(subC_list):
    
    subC_dict = {"Myelin sheath": 0, "Cytoplasm": 0, "Mitochondria": 0, "Nucleus": 0, 
    "Lysosome": 0, "ER": 0, "Peroxisome": 0, "Golgi": 0 }

    for i_subC in subC_list:

        i_subC = i_subC[ i_subC.find("Biological location") : ]

        d = [ {i:subC_dict[i]+1} for i in subC_dict if i in i_subC ]

        z = {}
        for i in d:
            z = {**z, **i} 
        subC_dict = {**subC_dict, **z} 

    return subC_dict

def Cell(Cell_list):
    
    Cell_dict = {"Nerve cell": 0, "Beta cell": 0, "Fibroblast": 0}

    for i_Cell in Cell_list:

        i_Cell = i_Cell[ i_Cell.find("Biological location") : ]

        d = [ {i:Cell_dict[i]+1} for i in Cell_dict if i in i_Cell ]

        z = {}
        for i in d:
            z = {**z, **i} 
        Cell_dict = {**Cell_dict, **z} 

    return Cell_dict

def BioF(BioF_list):
    
    BioF_dict = {"Sweat": 0, "Breast milk": 0, "Urine": 0,
    "Saliva": 0, "Feces": 0, "Blood": 0, "Cerebrospinal fluid": 0}

    for i_BioF in BioF_list:

        i_BioF = i_BioF[ i_BioF.find("Biological location") : ]

        d = [ {i:BioF_dict[i]+1} for i in BioF_dict if i in i_BioF ]

        z = {}
        for i in d:
            z = {**z, **i} 
        BioF_dict = {**BioF_dict, **z} 

    return BioF_dict

########## for Process plot ( forund only in HMDB )

# z = [ "Biochemical process", "Chemical reaction", "System process", "Cellular process", "Biochemical pathway"]
def parse_Data(x):
    z = [ "Biochemical process", "Chemical reaction", "System process", "Cellular process", "Biochemical pathway"]

    by_order = {}
    for i in z:
        by_order[i] = x.find(i)

    order =   sorted (list(by_order.values())) 

    alll =  []

    for i in range(0,len(order)):
        try:
            alll.append(x[order[i]:order[i+2]] )
        except:
            alll.append( x[order[i]:] ) 
    return alll

#count data for ploting 

def count_data(count_data_list):
    import re
    delete_dict = [ "Biochemical process", "Chemical reaction", "System process", "Cellular process", "Biochemical pathway"]
    count_data_dict = {}
    for i_Bropro in count_data_list:
        #i_Bropro = i_Bropro[i_Bropro.find(":")+1:]
        i_Bropro = re.findall('[A-Z][^A-Z]*', i_Bropro)
    
        for j_count_data in i_Bropro:
            j_count_data = j_count_data.strip()
            j_count_data = j_count_data.replace(":","")
            j_count_data = j_count_data.replace("and","")
            if j_count_data not in count_data_dict:
                count_data_dict[j_count_data] = 1

            elif j_count_data in count_data_dict:
                count_data_dict[j_count_data] = count_data_dict[j_count_data] + 1

    for i_del in list( count_data_dict.values() ):
        if i_del in delete_dict:
            del count_data_dict[i_del]
    return count_data_dict


###### for Biological Properties for HMDB

## Biospecimen Locations	
	
def BioSloc(BioSloc_list):
    BioSloc_dict = {"Blood": 0, "Breast Milk": 0, "Cerebrospinal Fluid": 0, "Feces": 0, "Saliva": 0, "Sweat": 0, "Urine": 0, "Amniotic Fluid":0}

    for i_BioSloc in BioSloc_list:
        d = [ {i:BioSloc_dict[i]+1} for i in BioSloc_dict if i in i_BioSloc ]

        z = {}
        for i in d:
            z = {**z, **i} 
        BioSloc_dict = {**BioSloc_dict, **z} 

    return BioSloc_dict 

## Cellular Locations 

def Cellloc(Cellloc_list):
    
    Cellloc_dict = {"Myelin sheath": 0, "Cytoplasm": 0, "Mitochondria": 0, "Nucleus": 0, 
    "Lysosome": 0, "ER": 0, "Peroxisome": 0, "Golgi apparatus": 0, "Extracellular":0, "Membrane":0 }

    for i_Cellloc in Cellloc_list:

        d = [ {i:Cellloc_dict[i]+1} for i in Cellloc_dict if i in i_Cellloc ]

        z = {}
        for i in d:
            z = {**z, **i} 
        Cellloc_dict = {**Cellloc_dict, **z} 

    return Cellloc_dict

## Tissue Locations	

def Tissloc(Tissloc_list):
    
    Tissloc_dict = {"Beta Cell": 0, "Brain Plaques": 0, "Eye Lens": 0, "Fetus": 0, 
    "Gonads": 0, "Gut reticulum": 0, "Intestine": 0, "Liver": 0, "Lung":0,
    "Mouth":0, "Prostate":0, "Adipose Tissue":0, "Adrenal Cortex":0,
    "Adrenal Gland":0, "Adrenal Medulla":0, "Bladder":0, "Brain":0,
    "Epidermis":0, "Fibroblasts":0, "Kidney":0, "Muscle":0,
    "Myelin":0, "Nerve Cells":0, "Neuron":0, "Pancreas":0, "Placenta":0,
    "Platelet":0, "Skeletal Muscle":0, "Spleen":0, "Striatum":0, "Testes":0}

    for i_Tissloc in Tissloc_list:

        d = [ {i:Tissloc_dict[i]+1} for i in Tissloc_dict if i in i_Tissloc ]

        z = {}
        for i in d:
            z = {**z, **i} 
        Tissloc_dict = {**Tissloc_dict, **z} 

    return Tissloc_dict


###### for Biological Properties for YMDB

def Geninfo_YMDB(accessions, what_to_get):
    import urllib
    import urllib.request
    import pandas as pd
    from pandas import DataFrame



    if type(accessions) != list:
        raise TypeError ("Geninfo_YMDB takes list as an argument")

    main_url = "http://www.ymdb.ca/compounds/"
    for i_acc in accessions:
        # creating the query search url by accessions
        api_request = main_url + i_acc
        # get the data in form of tables
        try:
            tables = pd.read_html(api_request)
            #removing row with no data
            tables0 = tables[0].iloc[:,0:2]
            #rename the col 
            tables0.columns = ["col1", "col2"]

            #take only the general information
            take_from_tables0 = [what_to_get] # Cellular Locations	
            
            
            tables0 = tables0[tables0["col1"].isin(take_from_tables0)]

            tables0 = tables0.rename(index={ list(tables0.index)[0] : i_acc})
        except:
            take_from_tables0 = ["col1", "col2"]
            not_found = ["NaN"] * len(take_from_tables0)
            not_found = dict( zip(take_from_tables0,not_found) )
            tables0 = pd.DataFrame(data=not_found , index= [0])

            tables0 = tables0.rename(index={0:i_acc })

        yield tables0

def Cellloc_YMDB(Cellloc_list):
    
    Cellloc_dict = {"Myelin sheath": 0, "Cytoplasm": 0, "Mitochondria": 0, "Vacuole": 0, 
    "Lysosome": 0, "ER": 0, "Peroxisome": 0, "Golgi apparatus": 0, "Extracellular":0, 
    "Nucleus":0 }

    for i_Cellloc in Cellloc_list:
        
        d = [ {i:Cellloc_dict[i]+1} for i in Cellloc_dict if i in i_Cellloc ]

        z = {}
        for i in d:
            z = {**z, **i} 
        Cellloc_dict = {**Cellloc_dict, **z} 

    return Cellloc_dict








###### for Biological Properties for LMDB

def Geninfo_LMDB(accessions, what_to_get):
    import urllib
    import urllib.request
    import pandas as pd
    from pandas import DataFrame



    if type(accessions) != list:
        raise TypeError ("Geninfo_YMDB takes list as an argument")

    main_url = "http://lmdb.ca/metabolites/"
    for i_acc in accessions:
        # creating the query search url by accessions
        api_request = main_url + i_acc
        # get the data in form of tables
        try:
            tables = pd.read_html(api_request)
            #removing row with no data
            tables0 = tables[0].iloc[:,0:2]
            #rename the col 
            tables0.columns = ["col1", "col2"]

            #take only the general information
            take_from_tables0 = [what_to_get] # Biofluid Locations and Tissue Locations
            
            
            tables0 = tables0[tables0["col1"].isin(take_from_tables0)]

            tables0 = tables0.rename(index={ list(tables0.index)[0] : i_acc})
        except:
            take_from_tables0 = ["col1", "col2"]
            not_found = ["NaN"] * len(take_from_tables0)
            not_found = dict( zip(take_from_tables0,not_found) )
            tables0 = pd.DataFrame(data=not_found , index= [0])

            tables0 = tables0.rename(index={0:i_acc })
        yield tables0

def BioTissloc_LMDB(BioTissloc_list):
    
    BioTissloc_dict = {"CSF": 0, "Colostrum": 0, "Feces": 0, "Follicular Fluid": 0, 
    "Kidney perfusate": 0, "Lung": 0, "Meat": 0, "Milk": 0, "Plasma":0, "Ruminal Fluid":0, "Serum":0,
     "Synovial Fluid":0, "Urine":0, "Vitreous Humour":0 }

    for i_BioTissloc in BioTissloc_list:
        
        d = [ {i:BioTissloc_dict[i]+1} for i in BioTissloc_dict if i in i_BioTissloc ]

        z = {}
        for i in d:
            z = {**z, **i} 
        BioTissloc_dict = {**BioTissloc_dict, **z} 

    return BioTissloc_dict











###### for Biological Properties for T3DB

def Geninfo_T3DB(accessions, what_to_get):
    import urllib
    import urllib.request
    import pandas as pd
    from pandas import DataFrame



    if type(accessions) != list:
        raise TypeError ("Geninfo_YMDB takes list as an argument")

    main_url = "http://www.t3db.ca/toxins/"
    for i_acc in accessions:
        # creating the query search url by accessions
        api_request = main_url + i_acc
        # get the data in form of tables
        try:
            tables = pd.read_html(api_request)
            #removing row with no data
            tables0 = tables[0].iloc[:,0:2]
            #rename the col 
            tables0.columns = ["col1", "col2"]

            #take only the general information
            take_from_tables0 = [what_to_get] # Cellular Locations, Tissue Locations
            
            
            tables0 = tables0[tables0["col1"].isin(take_from_tables0)]

            tables0 = tables0.rename(index={ list(tables0.index)[0] : i_acc})
        except:
            take_from_tables0 = ["col1", "col2"]
            not_found = ["NaN"] * len(take_from_tables0)
            not_found = dict( zip(take_from_tables0,not_found) )
            tables0 = pd.DataFrame(data=not_found , index= [0])

            tables0 = tables0.rename(index={0:i_acc })
        yield tables0

def Cellloc_T3DB(Cellloc_T3DB_list):
    
    Cellloc_T3DB_dict = {"Myelin sheath": 0, "Cytoplasm": 0, "Mitochondria": 0, "Nucleus": 0, 
    "Lysosome": 0, "ER": 0, "Peroxisome": 0, "Golgi apparatus": 0, "Extracellular":0, "Membrane":0 }

    for i_Cellloc_T3DB in Cellloc_T3DB_list:

        d = [ {i:Cellloc_T3DB_dict[i]+1} for i in Cellloc_T3DB_dict if i in i_Cellloc_T3DB ]

        z = {}
        for i in d:
            z = {**z, **i} 
        Cellloc_T3DB_dict = {**Cellloc_T3DB_dict, **z} 

    return Cellloc_T3DB_dict
 
def Tissloc_T3DB(Tissloc_T3DB_list):
    
    Tissloc_T3DB_dict = {"Beta Cell": 0, "Brain Plaques": 0, "Eye Lens": 0, "Fetus": 0, 
    "Gonads": 0, "Gut reticulum": 0, "Intestine": 0, "Liver": 0, "Lung":0,
    "Mouth":0, "Prostate":0, "Adipose Tissue":0, "Adrenal Cortex":0,
    "Adrenal Gland":0, "Adrenal Medulla":0, "Bladder":0, "Brain":0,
    "Epidermis":0, "Fibroblasts":0, "Kidney":0, "Muscle":0,
    "Myelin":0, "Nerve Cells":0, "Neuron":0, "Pancreas":0, "Placenta":0,
    "Platelet":0, "Skeletal Muscle":0, "Spleen":0, "Striatum":0, "Testes":0}

    for i_Tissloc_T3DB in Tissloc_T3DB_list:

        d = [ {i:Tissloc_T3DB_dict[i]+1} for i in Tissloc_T3DB_dict if i in i_Tissloc_T3DB ]

        z = {}
        for i in d:
            z = {**z, **i} 
        Tissloc_T3DB_dict = {**Tissloc_T3DB_dict, **z} 

    return Tissloc_T3DB_dict

######## respect data classes