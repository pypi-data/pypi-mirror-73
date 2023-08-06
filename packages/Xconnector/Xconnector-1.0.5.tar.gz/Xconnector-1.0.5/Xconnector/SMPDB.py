import urllib
import urllib.request
import re
import html
#get all pathway of HUMDB IDs from SMPDB then get the name by dowloading SMBL file and get the name from it


def find_smpdb_ids(HMDB_id, filter_by = ""):
    """
    searching by HMDB ids and get all SMPDB for that ID.
    """
    ## filter_by = "Physiological", "Metabolic", "Signaling", "Drug+Metabolism", "Drug+Action", "Disease", "Metabolic"
        
    def find_SMPDB(xml_str):
        import re
        xml_str = str(xml_str)

        end_of_lmdb = (lmdb.end() for lmdb in re.finditer("SMP",xml_str))
        final_SMD = list( set( [ f"SMP{xml_str[end:end+7]}" for end in end_of_lmdb if xml_str[end:end+7].isdigit()] ) )

        return final_SMD

    all_ids = []
    HMDB_id = HMDB_id.strip()
    for i in range(1, 1000):

        if filter_by == "":
            main_url = f"http://smpdb.ca/search?page={i}&q={HMDB_id}"
        else:
            main_url = f"http://smpdb.ca/search?page={i}&q={HMDB_id}&subject={filter_by}"

        xml = urllib.request.urlopen(main_url).read()
        xml = str(xml)

        if xml.find("next") != -1 or xml.find("Next") != -1:
            all_ids.append(find_SMPDB(xml))
        else:
            z = 1
            break

    main_url = f"http://smpdb.ca/search?page={z}&q={HMDB_id}&subject={filter_by}"

    xml = urllib.request.urlopen(main_url).read()
    xml = str(xml)
    all_ids.append(find_SMPDB(xml))

    all_ids = set( [ j for i in all_ids for j in i  ] )

    return all_ids

#print (find_smpdb_ids("HMDB0000001","Metabolic"))

def get_pathway_name(smpdb_id):
    main_url = f"http://smpdb.ca/view/{smpdb_id}/download?type=pwml_markup"

    pwml = urllib.request.urlopen(main_url).read()

    pwml = str(pwml) 

    find_name1 = pwml.find("<cached-name>")

    find_name2 = pwml.find("</cached-name>")

    return str(pwml[find_name1+len("<cached-name>"):find_name2])

#print (get_pathway_name("SMP0000044"))
def smpdb_download_image(SMPDB_id, type_iamge , save_as):

    # type_iamge = [ "full_vector_image", "simple_vector_image", "greyscale_vector_image""  ]
    
    main_url = f"http://smpdb.ca/view/{SMPDB_id}/download?type={type_iamge}"

    # creating the query search url by accessions to get the image 
    #save_as = f"{SMPDB_id}.svg"
    image= urllib.request.urlretrieve(main_url, save_as)

    return image


#smpdb_download_image("SMP0000044", type_iamge = "simple_vector_image" , save_as = None)


# get all metabolites names from smp ids

def smpdb_id_to_file_metabolits(smpdb_id):


    main_url = f"http://smpdb.ca/view/{smpdb_id}/download?type=owl_markup"

    file_BioPAX = urllib.request.urlopen(main_url).read()

    return file_BioPAX, smpdb_id

def parse_BioPAX(file_BioPAX , smpdb_id):
    """
    file_biopax, id_smp  = smpdb_id_to_file_metabolits("SMP0000044")
    print ( parse_BioPAX( file_biopax, id_smp  ) )
    """
    biopax = str(file_BioPAX)
    
    start = [ i.start() for i in re.finditer("<bp:SmallMolecule rdf",biopax)]
    end = [ i.start() for i in re.finditer("</bp:SmallMolecule>" , biopax) ]

    all_metabolite =  []
    if len(start) == len(end):
        for i_start , i_end in zip(start,end):
            if i_start < i_end:
                
                #get the whole line
                start_end = biopax[ i_start:i_end+1 ]
                start_name = start_end.find("<bp:displayName")
                end_name = start_end.find("</bp:displayName>")

                if start_end != -1 and end_name != -1:
                    start_name = start_name + 1
                    start_end = start_end[start_name:end_name+2]
                    #get the name only
                    start_name = start_end.find(">")
                    end_name = start_end.find("<") 
                    start_end = start_end[start_name+1:end_name]
                    
                    if "&#946;" in start_end:
                        start_end = start_end.replace("&#946;","β")
                    elif "&#945;" in start_end:
                        start_end = start_end.replace("&#945;","α")
                    elif "&#947;" in start_end:
                        start_end = start_end.replace("&#947;","γ")
                    elif "&#948;" in start_end:
                        start_end = start_end.replace("&#948;","Δ")
                    else:
                        if "&#" in start_end:
                            start_end_f = start_end[start_end.find("&"):start_end.find(";")+1]
                            start_end = f"{html.unescape(start_end_f)}{start_end}"
                        else:
                            pass
                    all_metabolite.append(start_end.strip())
                else:
                    pass
        dict_pathways = {}
        name_pathway = get_pathway_name(smpdb_id)
        dict_pathways[name_pathway] = list(set(all_metabolite))

        return dict_pathways
                
    else:
        return False






#file_biopax, id_smp  = smpdb_id_to_file_metabolits("SMP0000007")
#print ( parse_BioPAX( file_biopax, id_smp  ) ) 