
import urllib
import urllib.request
import pandas as pd
from pandas import DataFrame
import re
#get id from differnet database

## to get from kegg
def get_pathway_kegg(compund_ID , DB_id):

    try:
        kegg = urllib.request.urlopen(f"http://rest.kegg.jp/get/cpd:{compund_ID}").read()
                
        with open("temp_files\\kegg.txt","wb") as z:
            z.write(kegg)

        with open ("temp_files\\kegg.txt","r") as f:
            f = f.readlines()


        for i in f:
            if "map" in i:
                if "PATHWAY" in i:
                    i = i.replace("PATHWAY", "")
                else:
                    i = i

                remove = re.findall("(map\d*)",i)

                i = i.replace(remove[0],"")

                with open("temp_files\\kegg_new.txt","a") as e:
                    e.write(i)
        
        
        df = pd.read_table("temp_files\\kegg_new.txt" , header= None)
        df.columns = ["Pathway"]
        df["KEGG Compound ID"] = [compund_ID] * len(df)
        rename_dict = dict(zip( range(len(df)) , [DB_id]*len(df) ))
        df.rename(index=rename_dict, inplace = True)
    
        

        # to clear the file
        with open("temp_files\\kegg_new.txt","w") as e:
            e.write("")

        return df
    except:
        return False

#print (get_pathway_kegg("C00001","HMDB1111"))