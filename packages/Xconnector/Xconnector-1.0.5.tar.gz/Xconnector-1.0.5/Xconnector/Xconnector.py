import tkinter.filedialog
from tkinter.ttk import Notebook
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as mb
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
import _thread as thread
from tkinter.ttk import Progressbar
from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText
import pandas 
from pandas import DataFrame
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
import matplotlib.ticker
import webbrowser
import os
#**********************************
### Run Function
#**********************************
pathh = os.path.realpath(__file__)
pathh = pathh.replace("Xconnector.py", "")
##### general function to save result in 
def save_result_in_function():
    global save_result_in
    save_result_in = filedialog.askdirectory()
    

### 1- HMDB_function
#####################################################
#####################################################
##### Functions for plots 

### disposition

def import_file_csv_HMDB():
    mpb_vis["value"] = 0
    global import_file_ids
    global IDs
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_HMDB"].tolist()
    mpb_vis["value"] = 100
    
def HMDB_plots():
    global transparent_
    global mpb_vis
    global IDs

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    try:
        if len (IDs) == 0:
            mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_HMDB)")
            return False  
    except:
        mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_HMDB)")
        return False



    mpb_vis["value"] = 0

    save_result_in_disposition = save_result_in

    labelVarhmdb.set("Loading")

    if transparent_.get() == 1:
        transparent = True
    else:
        transparent = False
    
    
    style_old = style_.get("1.0","end-1c")
    style = style_old
    if style  == "":
        style = "seaborn-pastel"
    else:
        style = style.strip()

    dpi_old = dpi_.get("1.0","end-1c")
    dpi = dpi_old
    if str( dpi ) == "":
        dpi = 600
    else:
        dpi = int(dpi)

    color_old = color_.get("1.0","end-1c")
    color = color_old
    if str( color  ) == "":
        color = "blue"
    else:
        color = color.strip()

############# Disposition

    if var_Disposition.get() == 1:
        labelVarhmdb.set("Loading")
        mpb_vis["value"] = 0
        from get_data_plot import Geninfo_HMDB, Route, Source, organC, subC, Cell, BioF
        from plotDB import all_plot
     


        mpb_vis["value"] = 10
        df_all = pandas.DataFrame()
        for data  in Geninfo_HMDB( IDs ,"Disposition"):
            mpb_vis["value"] = 30
            df_all = pandas.concat([df_all, data], axis=0,sort=False)
        

        # Route
        mpb_vis["value"] = 40
        plot_data_dict = Route(df_all["col2"].tolist())
        all_plot( plot_data_dict,  scales = "on_y", y_label = "Count", color = color,title = "Disposition",y_name = "Count", x_name = "Route of exposure" , style = style, dpi = dpi , transparent = transparent, kind= "bar"  ,save=True,  where_to_save = f"{save_result_in_disposition}/Route.png" )
        pyplot.close('all')
        # Source
        mpb_vis["value"] = 50
        plot_data_dict = Source(df_all["col2"].tolist())
        all_plot(plot_data_dict, scales = "on_y", y_label = "Count", color = color,title = "Disposition",x_name = "Source" ,  style = style, dpi = dpi ,transparent = transparent, kind= "bar" ,save=True, where_to_save = f"{save_result_in_disposition}/Source.png"  )
        pyplot.close('all') 
        # organC
        mpb_vis["value"] = 60
        plot_data_dict = organC(df_all["col2"].tolist())
        all_plot(plot_data_dict, scales = "on_y", y_label = "Count",color = color,title = "Disposition (Biological location)", x_name = "Organ and components" ,  style = style, dpi = dpi ,transparent = transparent, kind= "bar" , save=True, where_to_save = f"{save_result_in_disposition}/organC.png"  )
        pyplot.close('all') 
        # subC
        mpb_vis["value"] = 70
        plot_data_dict = subC(df_all["col2"].tolist())
        all_plot(plot_data_dict,W_and_H = (13,13), rot = 45 ,scales = "on_y", color = color,title = "Disposition (Biological location)",x_name = "Subcellular" ,  style = style, dpi = dpi ,transparent = transparent, kind= "bar" , save=True, where_to_save = f"{save_result_in_disposition}/subC.png"  )
        pyplot.close('all') 
        # Cell
        mpb_vis["value"] = 80
        plot_data_dict = Cell(df_all["col2"].tolist())
        all_plot(plot_data_dict, scales = "on_y", y_label = "Count",color = color,title = "Disposition (Biological location)", x_name = "Cell and elements" ,  style = style, dpi = dpi ,transparent = transparent, kind= "bar" ,save=True, where_to_save = f"{save_result_in_disposition}/Cell.png"  )
        pyplot.close('all') 
        # BioF
        mpb_vis["value"] = 90
        plot_data_dict = BioF(df_all["col2"].tolist())
        all_plot(plot_data_dict, scales = "on_y", y_label = "Count",color = color,title = "Disposition (Biological location)",y_name = "Count", x_name = "Biofluid and excreta" ,  style = style, dpi = dpi ,transparent = transparent, kind= "bar" , save=True, where_to_save = f"{save_result_in_disposition}/BioF.png"  )
        pyplot.close('all')

        labelVarhmdb.set("Done")
        mpb_vis["value"] = 100
        mb.showinfo(title="Result", message="All result have been saved")
############# Biological Properties

    if var_Biological.get() == 1:
        labelVarhmdb.set("Loading")
        mpb_vis["value"] = 0
        from get_data_plot import Geninfo_HMDB, BioSloc, Cellloc, Tissloc
        from plotDB import all_plot

        file_ids_csv = pandas.read_csv(import_file_ids)
        IDs  = file_ids_csv["IDs_HMDB"].tolist()
        mpb_vis["value"] = 10

        # BioSloc
        df_all = pandas.DataFrame()
        mpb_vis["value"] = 20
        for data  in Geninfo_HMDB( IDs ,"Biospecimen Locations"):
            mpb_vis["value"] = 30
            df_all = pandas.concat([df_all, data], axis=0,sort=False)


        mpb_vis["value"] = 40
        plot_data_dict = BioSloc(df_all["col2"].tolist())
        all_plot( plot_data_dict, title = "Biological Properties",y_label = "Count", x_name = "Biospecimen Locations" , style = style, dpi = dpi ,
                                 transparent = transparent, kind= "bar"  ,rot = 30, scales = "on_y"  , save=True, fontsize_text = 12, where_to_save = f"{save_result_in_disposition}/BioSloc.png",color = color  )
        
        pyplot.close('all')
        # Cellloc
        df_all = df_all.iloc[0:0]
        df_all = pandas.DataFrame()
        mpb_vis["value"] = 50
        for data  in Geninfo_HMDB( IDs ,"Cellular Locations"):
            mpb_vis["value"] = 60
            df_all = pandas.concat([df_all, data], axis=0,sort=False)

        mpb_vis["value"] = 70
        plot_data_dict = Cellloc(df_all["col2"].tolist())
        all_plot( plot_data_dict, title = "Biological Properties",y_label = "Cellular Locations", x_label = "Count", x_name = "Cellular Locations" , style = style, dpi = dpi , fontsize_text = 10,
                                 transparent = transparent, kind= "barh"  ,save=True,  where_to_save = f"{save_result_in_disposition}/Cellloc.png",color = color, W_and_H = (17,8), scales = "on_x"  )
        pyplot.close('all')

        # Tissloc
        df_all = df_all.iloc[0:0]
        df_all = pandas.DataFrame()
        mpb_vis["value"] = 80
        for data  in Geninfo_HMDB( IDs ,"Tissue Locations"):
            mpb_vis["value"] = 90
            df_all = pandas.concat([df_all, data], axis=0,sort=False)

        mpb_vis["value"] = 95
        plot_data_dict = Tissloc(df_all["col2"].tolist())
        all_plot( plot_data_dict, title = "Biological Properties",x_label = "Count", x_name = "Tissue Locations" , style = style, dpi = dpi ,
                                 transparent = transparent, kind= "barh"  , scales = "on_x"  ,save=True,  where_to_save = f"{save_result_in_disposition}/Tissloc.png",color = color, fontsize_text = 9, W_and_H = (17,8)  )
        pyplot.close('all')
        mpb_vis["value"] = 100
        labelVarhmdb.set("Done")
        mb.showinfo(title="Result", message="All result have been saved")
        return True
############# Predicted Properties

    if var_Predicted.get() == 1:
        labelVarhmdb.set("Loading")
        mpb_vis["value"] = 0

        from HMDB import PredProp
        import seaborn as sns
        from plotDB import lollplot


        # 1 water Solubility
        mpb_vis["value"] = 10
        water_all = {}
        pka_acid_dict = {}
        pka_basic_dict = {}
        for data  in PredProp(IDs):
            #water solubility
            try:
                water = data.loc[data['Property'] == "Water Solubility" , "Value"].values[0]
                water_all[list(data.index.values)[0]] = float( water.split()[0] )
            except:
                water_all[list(data.index.values)[0]] = "Not_found"


            #PKa
            try:
                pka_acid = data.loc[data['Property'] == "pKa (Strongest Acidic)" , "Value"].values[0]
                pka_acid_dict[list(data.index.values)[0]] =  float(pka_acid)
            except:
                pka_acid_dict[list(data.index.values)[0]] =  "Not_found"
            

            try:
                pka_basic = water = data.loc[data['Property'] == "pKa (Strongest Basic)" , "Value"].values[0]
                pka_basic_dict[list(data.index.values)[0]] =  float(pka_basic)
            except:
                pka_basic_dict[list(data.index.values)[0]] =  "Not_found"


        water_all = {k:v for k,v in water_all.items() if v != 'Not_found'}

        pka_acid_dict_ = {k:v for k,v in pka_acid_dict.items() if v != 'Not_found'}
        pka_basic_dict_ = {k:v for k,v in pka_basic_dict.items() if v != 'Not_found'}

        pka_acid_dict_ = {k:v for k,v in pka_acid_dict_.items() if k in pka_basic_dict_}
        pka_basic_dict_ = {k:v for k,v in pka_basic_dict_.items() if k in pka_acid_dict_}

        mpb_vis["value"] = 20
        
        # water
        mpb_vis["value"] = 30
        lollplot(water_all , title = "Predicted Propertie" , xlabel= "g/L", ylabel= "", 
                        transparent = transparent , dpi = dpi, color_plot = color,markersize_ = 8, legend_label = "Water Solubility",
                        save = True, where_to_save = f"{save_result_in_disposition}/Predicted_Propertie(Water_Solubility1).png")
        
        pyplot.close('all')

        
        mpb_vis["value"] = 50

        #pka_acid _ violine plot

        df_pka = pandas.DataFrame( {  "Strongest Acidic": list( pka_acid_dict_.values() ) ,
                                         "Strongest Basic": list( pka_basic_dict_.values() ) } 
                                            , index = list(pka_acid_dict_.keys())  )

        sns.violinplot(data=df_pka, palette="Pastel1" , inner = "box")
        fig = plt.gcf()
        fig.set_size_inches((13,8), forward=False)
        plt.title("Predicted Propertie")
        plt.ylabel("pKa")
        mpb_vis["value"] = 70
        plt.savefig(f"{save_result_in_disposition}/pKa.png", dpi= dpi , transparent = transparent )
        pyplot.close('all')

        #pKa acid_basic bipole bar plot
        from plotDB import new_bibarplot

        new_bibarplot(range(1,len(df_pka)+1) , df_pka["Strongest Acidic"].sort_values(ascending=False)  , IDs_label = list(df_pka.index.values) ,
                                x_label = "Metabolites count" ,transparent = transparent, title  = "Predicted Propertie (Strongest Acidic)",
                                dpi= dpi, save = True , styles = style , where_to_save = f"{save_result_in_disposition}/pKa_StrongestAcidic.png")



        new_bibarplot(range(1,len(df_pka) + 1) , df_pka["Strongest Basic"].sort_values(ascending=False)  ,  IDs_label = list(df_pka.index.values) ,
                                x_label = "Metabolites count" ,transparent = transparent, title  = "Predicted Propertie (Strongest Basic)",
                                    dpi= dpi, save = True , styles = style , where_to_save = f"{save_result_in_disposition}/pKa_StrongestBasic.png")


        labelVarhmdb.set("Done")
        mpb_vis["value"] = 100
        mb.showinfo(title="Result", message="All result have been saved")

#####################################################
#####  the other Functions 
def SearchUsingID_HMDB(): 
    from HMDB import Geninfo, SynonymsData, ExpProp, PredProp, NConcsData, AConcsData, Pathways
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    labelVar.set("Loading")

    
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_HMDB"].tolist()
    mpb_all_hmdb["value"] = 3
    
    #### Geninfo
    df_all_Geninfo = pandas.DataFrame()
    for i_data in Geninfo(IDs):
        df_all_Geninfo = pandas.concat([df_all_Geninfo, i_data], axis=0,sort=False)


    mpb_all_hmdb["value"] = 5
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_Geninfo.to_csv(f"{save_result_in}/Geninfo_{save_file_name}")
    mpb_all_hmdb["value"] = 7

    ###############################################################
    ##############################################################

    mpb_all_hmdb["value"] = 10
    #### SynonymsData
    #
    df_all_SynonymsData = pandas.DataFrame()
    for i_data in SynonymsData(IDs):
        df_all_SynonymsData = pandas.concat([df_all_SynonymsData, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 20
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_SynonymsData.to_csv(f"{save_result_in}/SynonymsData_{save_file_name}")
    mpb_all_hmdb["value"] = 25

    ###############################################################
    ##############################################################
    
    mpb_all_hmdb["value"] = 30

    #### PredProp
    df_all_PredProp = pandas.DataFrame()
    for i_data in PredProp(IDs):
        df_all_PredProp = pandas.concat([df_all_PredProp, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 35

    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_PredProp.to_csv(f"{save_result_in}/PredProp_{save_file_name}")
    mpb_all_hmdb["value"] = 40


    ###############################################################
    ##############################################################
    labelVar.set("Loading.")
    mpb_all_hmdb["value"] = 45
    
    #### ExpProp

    df_all_ExpProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_ExpProp = pandas.concat([df_all_ExpProp, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 50
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_ExpProp.to_csv(f"{save_result_in}/ExpProp_{save_file_name}")

    mpb_all_hmdb["value"] = 55


    ###############################################################
    ##############################################################
    
    mpb_all_hmdb["value"] = 60
    #### AConcsData

    df_all_AConcsData = pandas.DataFrame()
    for i_data in AConcsData(IDs):
        df_all_AConcsData = pandas.concat([df_all_AConcsData, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 65
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_AConcsData.to_csv(f"{save_result_in}/AConcsData_{save_file_name}")
    mpb_all_hmdb["value"] = 70


    ###############################################################
    ##############################################################
    labelVar.set("Loading..")
    mpb_all_hmdb["value"] = 75
    #### NConcsData

    df_all_NConcsData = pandas.DataFrame()
    for i_data in NConcsData(IDs):
        df_all_NConcsData = pandas.concat([df_all_NConcsData, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 80
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_NConcsData.to_csv(f"{save_result_in}/NConcsData_{save_file_name}")
    mpb_all_hmdb["value"] = 85

    ###############################################################
    ##############################################################
    labelVar.set("Loading...")
    mpb_all_hmdb["value"] = 90
    #### Pathways
    df_all_Pathways = pandas.DataFrame()
    for i_data in Pathways(IDs):
        df_all_Pathways = pandas.concat([df_all_Pathways, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 95
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_Pathways.to_csv(f"{save_result_in}/Pathways_{save_file_name}")
    mpb_all_hmdb["value"] = 100

    labelVar.set("Done")
    
    mb.showinfo(title="Result", message="All result have been saved")
    
########################################################
#######################################################
def SearchUsingQuery_HMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    from HMDB import Geninfo , Search
    labelVar.set("Loading")

    # get searcher by
    if v_query.get() == 1:
        searcher = "metabolites"
    elif v_query.get() == 2:
        searcher = "diseases"
    elif v_query.get() == 3:
        searcher = "pathways"
    elif v_query.get() == 4:
        searcher = "proteins"
    elif v_query.get() == 5:
        searcher = "reactions"
    #get query
    mpb_all_hmdb["value"] = 10
    query_search_old = text_query.get("1.0","end-1c")
    query_search = query_search_old
    query_search = query_search.strip()
    HMDB_IDs = Search(query = query_search , searcher = searcher)
    mpb_all_hmdb["value"] = 40
    print (query_search)
    df_all_Search = pandas.DataFrame()
    for i_data in Geninfo(HMDB_IDs):
        df_all_Search = pandas.concat([df_all_Search, i_data], axis=0,sort=False)
    # save
    mpb_all_hmdb["value"] = 60
    df_all_Search.to_csv(f"{save_result_in}/Search.csv")
    mpb_all_hmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

########################################################
#######################################################
def ChemQuery_HMBB_run():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from HMDB import ChemQuery, Geninfo
    mpb_all_hmdb["value"] = 10

    # get data
    start_old = float(text1chm.get("1.0", "end-1c") )
    start = start_old
    end_old = float(text2chm.get("1.0", "end-1c") )
    end = end_old
    if vchem_hmdb.get() == 1:
        search_type = "molecular"
    elif vchem_hmdb.get() == 2:
        search_type = "monoisotopic"
    else:
        search_type = "molecular"

    filter_list = []
    if vchem_hmdb2.get() == 1:
        filter_list.append("quantified")
    elif vchem_hmdb2.get() == 2:
        filter_list.append("detected")
    elif vchem_hmdb2.get() == 3:
        filter_list.append("expected")
    else:
        filter_list.append("quantified")

    mpb_all_hmdb["value"] = 40

    df_all_ChemQuery = pandas.DataFrame()
    for i_data in ChemQuery(start=start , end=end,search_type=search_type ,filters=filter_list ):
        df_all_ChemQuery = pandas.concat([df_all_ChemQuery, i_data], axis=0,sort=False)

    mpb_all_hmdb["value"] = 60
    # save
    mpb_all_hmdb["value"] = 80
    df_all_ChemQuery.to_csv(f"{save_result_in}/ChemQuery.csv")
    mpb_all_hmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

########################################################
#######################################################

def LCMS_run_HMDB():
    # mases inserted seprated by ,
    # also adduct e.g ( M+H, M+H-H2O )
    # get data
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from HMDB import LCMS
    mpb_all_hmdb["value"] = 30

    def see_if_it_number(num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    old_masses = text_lcms1.get("1.0", "end-1c") 
    masess = old_masses
    masess = masess.split(",")
    masess = [ float(i) for i in masess if see_if_it_number(i)  ]

    adducts_old = text_lcms2.get("1.0", "end-1c") 
    adducts = adducts_old
    adducts = adducts.split(",")
    adducts = [ i for i in adducts if len(i) != 0 and not i.isdigit()  ]
    
    tolerance_old = float(text_lcms3.get("1.0", "end-1c"))
    tolerance = tolerance_old
    if vlcms.get() == 1:
        mode = "positive"
    elif vlcms.get() == 2:
        mode = "negative"
    elif vlcms.get() == 3:
        mode = "neutral"

    if vlcms1.get() == 1:
        unit = "Da"
    elif vlcms1.get() == 2:
        unit = "ppm"

    mpb_all_hmdb["value"] = 70
    df_lcms = LCMS(masses = masess ,mode = mode ,adducts = adducts
            ,tolerance = tolerance,tolerance_unit = unit)

    df_lcms.to_csv(f"{save_result_in}/LCMS.csv")
    mpb_all_hmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")
    
def LCMSMS_run_HMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from HMDB import LCMSMS
    from other_functions import make_it_correct
    mpb_all_hmdb["value"] = 30
    #get data 
    # peaks input as mass intens,mass intens,...
    peaks_old = text1_msms.get("1.0", "end-1c") 
    peaks = peaks_old
    peaks = peaks.split(",")
    peaks = [ i for i in peaks if len(i) != 0 and not i.isdigit()  ]
    
    PIM_old = float(text2_msms.get("1.0", "end-1c"))
    PIM = PIM_old
    PIMT_old = float(text3_msms.get("1.0", "end-1c"))
    PIMT = PIMT_old
    MCT_old = float(text4_msms.get("1.0", "end-1c"))
    MCT = MCT_old
    mpb_all_hmdb["value"] = 40

    if vlcmsms1.get() == 1:
        mode = "positive"
    elif vlcmsms1.get() == 2:
        mode = "negative"
    
    if vlcmsms2.get() == 1:
        unit = "Da"
    elif vlcmsms2.get() == 2:
        unit = "ppm"

    if vlcmsms3.get() == 1:
        cid = "low"
    elif vlcmsms3.get() == 2:
        cid = "med"
    elif vlcmsms3.get() == 3:
        cid = "high"

    if vlcmsms4.get() == 1:
        unit_mass = "Da"
    elif vlcmsms4.get() == 2:
        unit_mass = "ppm"

    if vlcmsms5.get() == 1:
        predicted1 = "True"
    else:
        predicted1 = "False"

    mpb_all_hmdb["value"] = 50

    df_lcmsms = LCMSMS( p_ion_mass = PIM,
                        p_ion_tolerance = PIMT,
                        parent_ion_mass_tolerance_units = unit,
                        ion_mode = mode,
                        cid = cid,
                        peaks = peaks,
                        mz_tolerance = MCT,
                        mz_tolerance_units = unit_mass,
                        predicted= predicted1)

    mpb_all_hmdb["value"] = 80

    df_lcmsms = make_it_correct(df_lcmsms)
    df_lcmsms.to_csv(f"{save_result_in}/LCMSMS.csv")
    mpb_all_hmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")
    
########################################################
#######################################################

def SMPDB_run_HMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False


    from SMPDB import find_smpdb_ids, get_pathway_name, smpdb_download_image
    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")
    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_HMDB"].tolist()
    mpb_all_hmdb["value"] = 10

    if filter_smpdb.get() == 1:
        filter_by1 = "Physiological"
    elif filter_smpdb.get() == 2:
        filter_by1 = "Metabolic"
    elif filter_smpdb.get() == 3:
        filter_by1 = "Signaling"
    elif filter_smpdb.get() == 4:
        filter_by1 = "Drug+Metabolism"
    elif filter_smpdb.get() == 5:
        filter_by1 = "Drug+Action"
    elif filter_smpdb.get() == 6:
        filter_by1 = "Disease"

    all_smpdb_list = []
    all_smpdb_dict = {}
    for i_ds in IDs:
        i_ds = i_ds.strip()
        smpdb_ids = find_smpdb_ids(i_ds ,filter_by=filter_by1  )
        all_smpdb_list.append(smpdb_ids)
        all_smpdb_dict[i_ds] = smpdb_ids
    mpb_all_hmdb["value"] = 40

    all_smpdb_list = [i for j in all_smpdb_list for i in j]

    pathway_dict = {}
    for i_smp in all_smpdb_list:
        pathway_dict[ i_smp ] = get_pathway_name(i_smp)
    mpb_all_hmdb["value"] = 60

    final_pathway_dict = {}
    HMDB_IDs = []
    for i_hmdb in all_smpdb_dict:
        for i_smp in all_smpdb_dict[i_hmdb]:
            final_pathway_dict[(i_smp,i_hmdb) ] = pathway_dict[i_smp]
    mpb_all_hmdb["value"] = 80

    df_pathway = pandas.DataFrame( { "SMPDB id": [i[0] for i in final_pathway_dict.keys()], 
                                        "HMDB id": [i[1] for i in final_pathway_dict.keys()],
                                        "Pathway": list(final_pathway_dict.values())  } )

    if image_smpdb.get() == 1:
        mpb_all_hmdb["value"] = mpb_all_hmdb["value"] + 10
        for i_smp in df_pathway["SMPDB id"].tolist():
            smpdb_download_image(i_smp , type_iamge = "simple_vector_image", save_as = f"{save_result_in}/{i_smp}.svg" )


    if pathway_smpdb.get() == 1:
        from SMPDB import smpdb_id_to_file_metabolits, parse_BioPAX
        mpb_all_hmdb["value"] = mpb_all_hmdb["value"] + 10
        all_infor_metabolites = {}
        for i_smp_id in all_smpdb_list:
            file_biopax, id_smp  = smpdb_id_to_file_metabolits(i_smp_id)
            all_infor_metabolites = dict(all_infor_metabolites , **parse_BioPAX( file_biopax, id_smp  ) )
        all_infor_metabolites_df = pandas.DataFrame({ key:pandas.Series(value) for key, value in all_infor_metabolites.items() })
        all_infor_metabolites_df =  all_infor_metabolites_df.apply(lambda x: x.sort_values().values)
        all_infor_metabolites_df.to_csv(f"{save_result_in}/SMPDB_HMDB_metabolites.csv")
    


    #change the col order and get the metabolite name
    #### Geninfo
    from HMDB import Geninfo
    names = []
    for i_data in Geninfo(df_pathway["HMDB id"].to_list()):
        names.append(i_data["Common Name"].tolist()[0])

    df_pathway["Common Name"] = names
    df_pathway.reset_index(drop=True , inplace = True)
    df_pathway_new = df_pathway[['HMDB id', 'Common Name', 'SMPDB id', 'Pathway']]
    df_pathway_new.to_csv(f"{save_result_in}/SMPDB_HMDB_pathway.csv")
    mpb_all_hmdb["value"] = 100
    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")
    







































#####################################################
#####################################################
### 2- LMDB_function
#####################################################
#####################################################
###plots

def import_file_csv_LMDB():
    mpb_all_lmdb["value"] = 0
    global import_file_ids
    global IDs
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_LMDB"].tolist()
    mpb_all_lmdb["value"] = 100
  
def LMDB_plots():
    global style
    global transparent_
    global dpi
    global color

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False


    try:
        if len (IDs) == 0:
            mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_LMDB)")
            return False  
    except:
        mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_LMDB)")
        return False

    mpb_all_lmdb["value"] = 10

    if transparent_.get() == 1:
        transparent = True
    else:
        transparent = False
    
    style_old = style_.get("1.0","end-1c")
    style = style_old
    if style  == "":
        style = "seaborn-pastel"
    else:
        style = style.strip()

    dpi_old = dpi_.get("1.0","end-1c")
    dpi = dpi_old
    if str( dpi ) == "":
        dpi = 600
    else:
        dpi = int(dpi)

    color_old = color_.get("1.0","end-1c")
    color = color_old
    if str( color  ) == "":
        color = "blue"
    else:
        color = color.strip()

    ###### Biofluid Locations and Tissue Locations
    from get_data_plot import Geninfo_LMDB, BioTissloc_LMDB
    from plotDB import all_plot
    labelVar.set("Loading")

    df_all = pandas.DataFrame()
    for data  in Geninfo_LMDB( IDs ,"Biofluid Locations and Tissue Locations"):
        mpb_all_lmdb["value"] = 30
        df_all = pandas.concat([df_all, data], axis=0,sort=False)
        
    # Biofluid
    mpb_all_lmdb["value"] = 40
    plot_data_dict = BioTissloc_LMDB(df_all["col2"].tolist())
    all_plot( plot_data_dict,color = color, title = "Biological Properties",
     x_name = "Biofluid Locations and Tissue Locations" , scales ="on_y" , 
     style = style, dpi = dpi , transparent = transparent, kind= "bar"  ,save=True, y_label = "Count", rot = 45, W_and_H = (13,13),
      where_to_save = f"{save_result_in}/BioTissloc.png" )
    pyplot.close('all')
    mpb_all_lmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def LMDB_plots_thread():
    thread.start_new_thread(LMDB_plots,())
########################################################
##########################################################
def SearchUsingID_LMDB(): 
    from LMDB import Geninfo, SynonymsData, ExpProp, PredProp, ConcsData
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_LMDB"].tolist()
    mpb_all_lmdb["value"] = 3

    #### Geninfo
    df_all_Geninfo = pandas.DataFrame()
    for i_data in Geninfo(IDs):
        df_all_Geninfo = pandas.concat([df_all_Geninfo, i_data], axis=0,sort=False)


    mpb_all_lmdb["value"] = 5
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_Geninfo.to_csv(f"{save_result_in}/Geninfo_{save_file_name}")
    mpb_all_lmdb["value"] = 7

    ###############################################################
    ##############################################################

    mpb_all_lmdb["value"] = 10
    #### SynonymsData
    #
    df_all_SynonymsData = pandas.DataFrame()
    for i_data in SynonymsData(IDs):
        df_all_SynonymsData = pandas.concat([df_all_SynonymsData, i_data], axis=0,sort=False)

    mpb_all_lmdb["value"] = 20
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_SynonymsData.to_csv(f"{save_result_in}/SynonymsData_{save_file_name}")
    mpb_all_lmdb["value"] = 25

    ###############################################################
    ##############################################################
    
    mpb_all_lmdb["value"] = 30
    #### ExpProp

    df_all_ExpProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_ExpProp = pandas.concat([df_all_ExpProp, i_data], axis=0,sort=False)


    mpb_all_lmdb["value"] = 35
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_ExpProp.to_csv(f"{save_result_in}/ExpProp_{save_file_name}")
    mpb_all_lmdb["value"] = 40


    ###############################################################
    ##############################################################
    labelVar.set("Loading.")
    mpb_all_lmdb["value"] = 45
    df_all_PredProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_PredProp = pandas.concat([df_all_PredProp, i_data], axis=0,sort=False)

    mpb_all_lmdb["value"] = 50
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_PredProp.to_csv(f"{save_result_in}/PredProp_{save_file_name}")
    mpb_all_lmdb["value"] = 55


    ###############################################################
    ##############################################################
    
    mpb_all_lmdb["value"] = 60
    #### ConcsData

    df_all_ConcsData = pandas.DataFrame()
    for i_data in ConcsData(IDs):
        df_all_ConcsData = pandas.concat([df_all_ConcsData, i_data], axis=0,sort=False)

    mpb_all_lmdb["value"] = 65
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_ConcsData.to_csv(f"{save_result_in}/ConcsData_{save_file_name}")
    mpb_all_lmdb["value"] = 70

    mpb_all_lmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

#####################################################
####################################################

def ChemQuery_LMBB_run():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from LMDB import ChemQuery, Geninfo
    mpb_all_lmdb["value"] = 10

    # get data
    start_old = float(text1chm.get("1.0", "end-1c") )
    start = start_old
    end_old = float(text2chm.get("1.0", "end-1c") )
    end = end_old
    if vchem_LMDB.get() == 1:
        search_type = "molecular"
    elif vchem_LMDB.get() == 2:
        search_type = "monoisotopic"
    else:
        search_type = "molecular"

    filter_list = []
    if vchem_LMDB2.get() == 1:
        filter_list.append("quantified")
    elif vchem_LMDB2.get() == 2:
        filter_list.append("detected")
    elif vchem_LMDB2.get() == 3:
        filter_list.append("expected")
    else:
        filter_list.append("quantified")

    mpb_all_lmdb["value"] = 40

    df_all_ChemQuery = pandas.DataFrame()
    for i_data in ChemQuery(start=start , end=end,search_type=search_type ,filters=filter_list ):
        df_all_ChemQuery = pandas.concat([df_all_ChemQuery, i_data], axis=0,sort=False)

    mpb_all_lmdb["value"] = 60
    # save
    mpb_all_lmdb["value"] = 80
    df_all_ChemQuery.to_csv(f"{save_result_in}/ChemQuery.csv")
    mpb_all_lmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

#######################################################
#######################################################

def SearchUsingQuery_LMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    from LMDB import Geninfo , txtsearch
    labelVar.set("Loading")
    #get query
    mpb_all_lmdb["value"] = 10
    query_search_old = text_query.get("1.0","end-1c")
    query_search = query_search_old
    query_search = query_search.strip()
    HMDB_IDs = txtsearch(query = query_search)
    mpb_all_lmdb["value"] = 40
    df_all_Search = pandas.DataFrame()
    for i_data in Geninfo(HMDB_IDs):
        df_all_Search = pandas.concat([df_all_Search, i_data], axis=0,sort=False)
    # save
    mpb_all_lmdb["value"] = 60
    df_all_Search.to_csv(f"{save_result_in}/txtsearch.csv")
    mpb_all_lmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

########################################################
#########################################################

def LCMS_run_LMDB():
    # mases inserted seprated by ,
    # also adduct e.g ( M+H, M+H-H2O )
    # get data
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from LMDB import LCMS
    mpb_all_lmdb["value"] = 30

    masess_old = text_lcms1.get("1.0", "end-1c") 
    masess = masess_old
    masess = masess.split(",")
    masess = [ float(i) for i in masess if i.isdigit ()  ]
    
    adducts_old = text_lcms2.get("1.0", "end-1c") 
    adducts = adducts_old
    adducts = adducts.split(",")
    adducts = [ i for i in adducts if len(i) != 0 and not i.isdigit()  ]
    
    tolerance_old = float(text_lcms3.get("1.0", "end-1c"))
    tolerance = tolerance_old
    if vlcms.get() == 1:
        mode = "positive"
    elif vlcms.get() == 2:
        mode = "negative"
    elif vlcms.get() == 3:
        mode = "neutral"

    if vlcms1.get() == 1:
        unit = "Da"
    elif vlcms1.get() == 2:
        unit = "ppm"

    mpb_all_lmdb["value"] = 70
    df_lcms = LCMS(masses = masess ,mode = mode ,adducts = adducts
            ,tolerance = tolerance,tolerance_unit = unit)

    df_lcms.to_csv(f"{save_result_in}/LCMS.csv")
    mpb_all_lmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

#########################################################
#########################################################
def LCMSMS_run_LMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from LMDB import LCMSMS
    from other_functions import make_it_correct

    mpb_all_lmdb["value"] = 30
    #get data 
    # peaks input as mass intens,mass intens,...
    peaks_old = text1_msms.get("1.0", "end-1c") 
    peaks = peaks_old
    peaks = peaks.split(",")
    peaks = [ i for i in peaks if len(i) != 0 and not i.isdigit()  ]
    
    PIM_old  = float(text2_msms.get("1.0", "end-1c"))
    PIM = PIM_old
    PIMT_old = float(text3_msms.get("1.0", "end-1c"))
    PIMT = PIMT_old
    MCT_old = float(text4_msms.get("1.0", "end-1c"))
    MCT = MCT_old
    mpb_all_lmdb["value"] = 40

    if vlcmsms1.get() == 1:
        mode = "positive"
    elif vlcmsms1.get() == 2:
        mode = "negative"
    
    if vlcmsms2.get() == 1:
        unit = "Da"
    elif vlcmsms2.get() == 2:
        unit = "ppm"

    if vlcmsms3.get() == 1:
        cid = "low"
    elif vlcmsms3.get() == 2:
        cid = "med"
    elif vlcmsms3.get() == 3:
        cid = "high"

    if vlcmsms4.get() == 1:
        unit_mass = "Da"
    elif vlcmsms4.get() == 2:
        unit_mass = "ppm"

    if vlcmsms5.get() == 1:
        predicted1 = "True"
    else:
        predicted1 = "False"

    mpb_all_lmdb["value"] = 50

    df_lcmsms = LCMSMS( p_ion_mass = PIM,
                        p_ion_tolerance = PIMT,
                        parent_ion_mass_tolerance_units = unit,
                        ion_mode = mode,
                        cid = cid,
                        peaks = peaks,
                        mz_tolerance = MCT,
                        mz_tolerance_units = unit_mass,
                        predicted= predicted1)

    mpb_all_lmdb["value"] = 80

    df_lcmsms = make_it_correct(df_lcmsms)
    df_lcmsms.to_csv(f"{save_result_in}/LCMSMS.csv")
    mpb_all_lmdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")
    

#########################################################
#########################################################

def Kegg_pathways_LMDB():

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    mpb_all_lmdb["value"] = 10
    labelVar.set("Loading")

    from get_data_plot import Geninfo_LMDB
    from KEGG import get_pathway_kegg

    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_LMDB"].tolist()


    df_all = pandas.DataFrame()
    for data  in Geninfo_LMDB( IDs ,"Kegg Compound ID"):
        mpb_all_lmdb["value"] = 30
        df_all = pandas.concat([df_all, data], axis=0,sort=False)
        
     
    mpb_all_lmdb["value"] = 40
    #kegg_ids = df_all["col2"].tolist()[0]

    df_result_kegg_all = pandas.DataFrame()
    for kegg_id , LMDB_id in zip( df_all["col2"], list(df_all.index) ) :
        mpb_all_lmdb["value"] = 60
        df_result = get_pathway_kegg(kegg_id ,LMDB_id )
        try:
            df_result_kegg_all = pandas.concat([df_result_kegg_all, df_result], axis=0,sort=False)
        except:
            continue 

    pyplot.close('all')
    mpb_all_lmdb["value"] = 100
    df_result_kegg_all.to_csv(f"{save_result_in}/Kegg_pathway.csv")

    mb.showinfo(title="Result", message="All result have been saved")

    labelVar.set("Done")

def Kegg_pathways_LMDB_thread():
    thread.start_new_thread(Kegg_pathways_LMDB,())








#########################################
### 3- YMDB
#########################################

def SearchUsingID_YMDB(): 
    from YMDB import Geninfo, ExpProp, PredProp
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_YMDB"].tolist()
    mpb_all_ymdb["value"] = 3

    #### Geninfo
    df_all_Geninfo = pandas.DataFrame()
    for i_data in Geninfo(IDs):
        df_all_Geninfo = pandas.concat([df_all_Geninfo, i_data], axis=0,sort=False)


    mpb_all_ymdb["value"] = 5
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_Geninfo.to_csv(f"{save_result_in}/Geninfo_{save_file_name}")
    mpb_all_ymdb["value"] = 7

    ###############################################################
    ##############################################################

    mpb_all_ymdb["value"] = 30
    #### ExpProp

    df_all_ExpProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_ExpProp = pandas.concat([df_all_ExpProp, i_data], axis=0,sort=False)


    mpb_all_ymdb["value"] = 35
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_ExpProp.to_csv(f"{save_result_in}/ExpProp_{save_file_name}")
    mpb_all_ymdb["value"] = 40


    ###############################################################
    ##############################################################
    labelVar.set("Loading.")
    mpb_all_ymdb["value"] = 45
    df_all_PredProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_PredProp = pandas.concat([df_all_PredProp, i_data], axis=0,sort=False)

    mpb_all_ymdb["value"] = 50
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_PredProp.to_csv(f"{save_result_in}/PredProp_{save_file_name}")
    mpb_all_ymdb["value"] = 55

    mpb_all_ymdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")


#####################################################
#####################################################
###plots

def import_file_csv_YMDB():
    mpb_all_ymdb["value"] = 0
    global import_file_ids
    global IDs
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_YMDB"].tolist()
    mpb_all_ymdb["value"] = 100
  
def YMDB_plots():
    global style
    global transparent_
    global dpi
    global color

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    try:
        if len (IDs) == 0:
            mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_YMDB)")
            return False  
    except:
        mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_YMDB)")
        return False

    mpb_all_ymdb["value"] = 10

    if transparent_.get() == 1:
        transparent = True
    else:
        transparent = False
    
    style_old = style_.get("1.0","end-1c")
    style = style_old
    if style  == "":
        style = "seaborn-pastel"
    else:
        style = style.strip()

    dpi_old = dpi_.get("1.0","end-1c")
    dpi = dpi_old
    if str( dpi ) == "":
        dpi = 600
    else:
        dpi = int(dpi)

    color_old = color_.get("1.0","end-1c")
    color = color_old
    if str( color  ) == "":
        color = "blue"
    else:
        color = color.strip()

    ###### Biofluid Locations and Tissue Locations
    from get_data_plot import Geninfo_YMDB, Cellloc_YMDB
    from plotDB import all_plot
    labelVar.set("Loading")
    df_all = pandas.DataFrame()
    for data  in Geninfo_YMDB( IDs ,"Cellular Locations"):
        mpb_all_ymdb["value"] = 30
        df_all = pandas.concat([df_all, data], axis=0,sort=False)
        
    # Biofluid
    mpb_all_ymdb["value"] = 40
    plot_data_dict = Cellloc_YMDB(df_all["col2"].tolist())
    all_plot( plot_data_dict,color = color, title = "Biological Properties", 
    x_name = "Cellular Locations" , style = style, dpi = dpi , x_label = "Count", scales = "on_x" ,
    transparent = transparent, kind= "barh"  ,save=True,  fontsize_text = 12,where_to_save = f"{save_result_in}/Cellloc.png" )
    pyplot.close('all')
    mpb_all_ymdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def YMDB_plots_thread():

    thread.start_new_thread(YMDB_plots,())

########################################
#######################################

def SearchUsingQuery_YMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    from YMDB import Geninfo , txtsearch
    labelVar.set("Loading")
    #get query
    mpb_all_ymdb["value"] = 10
    query_search_old = text_query.get("1.0","end-1c")
    query_search = query_search_old
    query_search = query_search.strip()
    HMDB_IDs = txtsearch(query = query_search)
    mpb_all_ymdb["value"] = 40
    df_all_Search = pandas.DataFrame()
    for i_data in Geninfo(HMDB_IDs):
        df_all_Search = pandas.concat([df_all_Search, i_data], axis=0,sort=False)
    # save
    mpb_all_ymdb["value"] = 60
    df_all_Search.to_csv(f"{save_result_in}/txtsearch.csv")
    mpb_all_ymdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")


########################################
########################################

def ChemQuery_YMDB_run():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from YMDB import ChemQuery, Geninfo
    mpb_all_ymdb["value"] = 10

    # get data
    start_old = float(text1chm.get("1.0", "end-1c") )
    start = start_old
    end_old = float(text2chm.get("1.0", "end-1c") )
    end = end_old

    if vchem_YMDB.get() == 1:
        search_type = "molecular"
    elif vchem_YMDB.get() == 2:
        search_type = "monoisotopic"
    else:
        search_type = "molecular"

    mpb_all_ymdb["value"] = 40

    df_all_ChemQuery = pandas.DataFrame()
    for i_data in ChemQuery(start=start , end=end,search_type=search_type ):
        df_all_ChemQuery = pandas.concat([df_all_ChemQuery, i_data], axis=0,sort=False)

    mpb_all_ymdb["value"] = 60
    # save
    mpb_all_ymdb["value"] = 80
    df_all_ChemQuery.to_csv(f"{save_result_in}/ChemQuery.csv")
    mpb_all_ymdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

########################################
#######################################

def LCMS_run_YMDB():
    # mases inserted seprated by ,
    # also adduct e.g ( M+H, M+H-H2O )
    # get data
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from YMDB import LCMS
    mpb_all_ymdb["value"] = 30

    masess_old = text_lcms1.get("1.0", "end-1c") 
    masess = masess_old
    masess = masess.split(",")
    masess = [ float(i) for i in masess if i.isdigit ()  ]
    
    adducts_old = text_lcms2.get("1.0", "end-1c") 
    adducts = adducts_old
    adducts = adducts.split(",")
    adducts = [ i for i in adducts if len(i) != 0 and not i.isdigit()  ]
    
    tolerance_old = float(text_lcms3.get("1.0", "end-1c"))
    tolerance = tolerance_old

    if vlcms.get() == 1:
        mode = "positive"
    elif vlcms.get() == 2:
        mode = "negative"
    elif vlcms.get() == 3:
        mode = "neutral"

    if vlcms1.get() == 1:
        unit = "Da"
    elif vlcms1.get() == 2:
        unit = "ppm"

    mpb_all_ymdb["value"] = 70
    df_lcms = LCMS(masses = masess ,mode = mode ,adducts = adducts
            ,tolerance = tolerance,tolerance_unit = unit)

    df_lcms.to_csv(f"{save_result_in}/LCMS.csv")
    mpb_all_ymdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

##########################################
##########################################

def LCMSMS_run_YMDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from YMDB import LCMSMS
    from other_functions import make_it_correct
    mpb_all_ymdb["value"] = 30
    #get data 
    # peaks input as mass intens,mass intens,...
    peaks_old = text1_msms.get("1.0", "end-1c") 
    peaks = peaks_old
    peaks = peaks.split(",")
    peaks = [ i for i in peaks if len(i) != 0 and not i.isdigit()  ]
    
    PIM_old = float(text2_msms.get("1.0", "end-1c"))
    PIM = PIM_old
    PIMT_old = float(text3_msms.get("1.0", "end-1c"))
    PIMT = PIMT_old
    MCT_old = float(text4_msms.get("1.0", "end-1c"))
    MCT = MCT_old
    mpb_all_ymdb["value"] = 40

    if vlcmsms1.get() == 1:
        mode = "positive"
    elif vlcmsms1.get() == 2:
        mode = "negative"
    
    if vlcmsms2.get() == 1:
        unit = "Da"
    elif vlcmsms2.get() == 2:
        unit = "ppm"

    if vlcmsms3.get() == 1:
        cid = "low"
    elif vlcmsms3.get() == 2:
        cid = "med"
    elif vlcmsms3.get() == 3:
        cid = "high"

    if vlcmsms4.get() == 1:
        unit_mass = "Da"
    elif vlcmsms4.get() == 2:
        unit_mass = "ppm"

    if vlcmsms5.get() == 1:
        predicted1 = "True"
    else:
        predicted1 = "False"

    mpb_all_ymdb["value"] = 50

    df_lcmsms = LCMSMS( p_ion_mass = PIM,
                        p_ion_tolerance = PIMT,
                        parent_ion_mass_tolerance_units = unit,
                        ion_mode = mode,
                        cid = cid,
                        peaks = peaks,
                        mz_tolerance = MCT,
                        mz_tolerance_units = unit_mass,
                        predicted= predicted1)

    mpb_all_ymdb["value"] = 80

    df_lcmsms = make_it_correct(df_lcmsms)
    df_lcmsms.to_csv(f"{save_result_in}/LCMSMS.csv")
    mpb_all_ymdb["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")


























#########################################
### 4- T3DB
#########################################
#### Plots

def import_file_csv_T3DB():
    mpb_all_t3db["value"] = 0
    global import_file_ids
    global IDs
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_T3DB"].tolist()
    mpb_all_t3db["value"] = 100
  
def T3DB_plots():
    global style
    global transparent_
    global dpi
    global color

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    try:
        if len (IDs) == 0:
            mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_T3DB)")
            return False  
    except:
        mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs with column name (IDs_T3DB)")
        return False

    mpb_all_t3db["value"] = 10

    if transparent_.get() == 1:
        transparent = True
    else:
        transparent = False
    
    style_old = style_.get("1.0","end-1c")
    style = style_old
    if style  == "":
        style = "seaborn-pastel"
    else:
        style = style.strip()

    dpi_old = dpi_.get("1.0","end-1c")
    dpi = dpi_old
    if str( dpi ) == "":
        dpi = 600
    else:
        dpi = int(dpi)

    color_old = color_.get("1.0","end-1c")
    color = color_old
    if str( color  ) == "":
        color = "blue"
    else:
        color = color.strip()

    ###### Biofluid Locations and Tissue Locations
    from get_data_plot import Geninfo_T3DB, Cellloc_T3DB, Tissloc_T3DB
    from plotDB import all_plot
    labelVar.set("Loading")

    df_all = pandas.DataFrame()
    for data  in Geninfo_T3DB( IDs ,"Cellular Locations"):
        mpb_all_t3db["value"] = 30
        df_all = pandas.concat([df_all, data], axis=0,sort=False)
        
    # Biofluid
    mpb_all_t3db["value"] = 40
    plot_data_dict = Cellloc_T3DB(df_all["col2"].tolist())
    all_plot( plot_data_dict,color = color, title = "Biological Properties", x_label = "Count" , scales = "on_x",
    x_name = "Cellular Locations" , style = style, dpi = dpi , transparent = transparent, kind= "barh" ,
    save=True, fontsize_text = 12, where_to_save = f"{save_result_in}/Cellloc.png" )
    pyplot.close('all')


    df_all = pandas.DataFrame()
    for data  in Geninfo_T3DB( IDs ,"Tissue Locations"):
        mpb_all_t3db["value"] = 30
        df_all = pandas.concat([df_all, data], axis=0,sort=False)
        

    mpb_all_t3db["value"] = 70
    plot_data_dict2 = Tissloc_T3DB(df_all["col2"].tolist())
    all_plot( plot_data_dict2,color = color, title = "Biological Properties", x_name = "Tissue Locations" , 
    style = style, dpi = dpi , transparent = transparent, kind= "barh", fontsize_text = 12, x_label = "Count" , scales = "on_x",
    save=True, where_to_save = f"{save_result_in}/Tissloc.png" )
    pyplot.close('all')

    mpb_all_t3db["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def T3DB_plots_thread():
    thread.start_new_thread(T3DB_plots,())

###############################################
def SearchUsingID_T3DB(): 
    from T3DP import Geninfo, ExpProp, PredProp
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_T3DB"].tolist()
    mpb_all_t3db["value"] = 3

    #### Geninfo
    df_all_Geninfo = pandas.DataFrame()
    for i_data in Geninfo(IDs):
        df_all_Geninfo = pandas.concat([df_all_Geninfo, i_data], axis=0,sort=False)


    mpb_all_t3db["value"] = 5
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_Geninfo.to_csv(f"{save_result_in}/Geninfo_{save_file_name}")
    mpb_all_t3db["value"] = 7

    ###############################################################
    ##############################################################

    mpb_all_t3db["value"] = 30
    #### ExpProp

    df_all_ExpProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_ExpProp = pandas.concat([df_all_ExpProp, i_data], axis=0,sort=False)


    mpb_all_t3db["value"] = 35
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_ExpProp.to_csv(f"{save_result_in}/ExpProp_{save_file_name}")
    mpb_all_t3db["value"] = 40


    ###############################################################
    ##############################################################
    labelVar.set("Loading.")
    mpb_all_t3db["value"] = 45
    df_all_PredProp = pandas.DataFrame()
    for i_data in ExpProp(IDs):
        df_all_PredProp = pandas.concat([df_all_PredProp, i_data], axis=0,sort=False)

    mpb_all_t3db["value"] = 50
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_PredProp.to_csv(f"{save_result_in}/PredProp_{save_file_name}")
    mpb_all_t3db["value"] = 55

    mpb_all_t3db["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

########################################
########################################
def SearchUsingQuery_T3DB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    from T3DP import Geninfo , txtsearch
    labelVar.set("Loading")
    #get query
    mpb_all_t3db["value"] = 10
    query_search_old = text_query.get("1.0","end-1c")
    query_search = query_search_old
    query_search = query_search.strip()
    HMDB_IDs = txtsearch(query = query_search)
    mpb_all_t3db["value"] = 40
    df_all_Search = pandas.DataFrame()
    for i_data in Geninfo(HMDB_IDs):
        df_all_Search = pandas.concat([df_all_Search, i_data], axis=0,sort=False)
    # save
    mpb_all_t3db["value"] = 60
    df_all_Search.to_csv(f"{save_result_in}/txtsearch.csv")
    mpb_all_t3db["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

#########################################
#########################################
def ChemQuery_T3DB_run():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from T3DP import ChemQuery, Geninfo
    mpb_all_t3db["value"] = 10

    # get data
    start_old = float(text1chm.get("1.0", "end-1c") )
    start = start_old
    end_old = float(text2chm.get("1.0", "end-1c") )
    end = end_old
    if vchem_T3DB.get() == 1:
        search_type = "molecular"
    elif vchem_T3DB.get() == 2:
        search_type = "monoisotopic"
    else:
        search_type = "molecular"

    mpb_all_t3db["value"] = 40

    df_all_ChemQuery = pandas.DataFrame()
    for i_data in ChemQuery(start=start , end=end,search_type=search_type ):
        df_all_ChemQuery = pandas.concat([df_all_ChemQuery, i_data], axis=0,sort=False)

    mpb_all_t3db["value"] = 60
    # save
    mpb_all_t3db["value"] = 80
    df_all_ChemQuery.to_csv(f"{save_result_in}/ChemQuery.csv")
    mpb_all_t3db["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

#########################################
########################################
def LCMS_run_T3DB():
    # mases inserted seprated by ,
    # also adduct e.g ( M+H, M+H-H2O )
    # get data
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from T3DP import LCMS
    mpb_all_t3db["value"] = 30

    masess_old = text_lcms1.get("1.0", "end-1c") 
    masess = masess_old
    masess = masess.split(",")
    masess = [ float(i) for i in masess if i.isdigit ()  ]
    
    adducts_old = text_lcms2.get("1.0", "end-1c") 
    adducts = adducts_old
    adducts = adducts.split(",")
    adducts = [ i for i in adducts if len(i) != 0 and not i.isdigit()  ]
    
    tolerance_old = float(text_lcms3.get("1.0", "end-1c"))
    tolerance = tolerance_old

    if vlcms.get() == 1:
        mode = "positive"
    elif vlcms.get() == 2:
        mode = "negative"
    elif vlcms.get() == 3:
        mode = "neutral"

    if vlcms1.get() == 1:
        unit = "Da"
    elif vlcms1.get() == 2:
        unit = "ppm"

    mpb_all_t3db["value"] = 70
    df_lcms = LCMS(masses = masess ,mode = mode ,adducts = adducts
            ,tolerance = tolerance,tolerance_unit = unit)

    df_lcms.to_csv(f"{save_result_in}/LCMS.csv")
    mpb_all_t3db["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

###########################################
##########################################
def LCMSMS_run_T3DB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    labelVar.set("Loading")

    from T3DP import LCMSMS
    from other_functions import make_it_correct
    mpb_all_t3db["value"] = 30
    #get data 
    # peaks input as mass intens,mass intens,...
    peaks_old = text1_msms.get("1.0", "end-1c") 
    peaks = peaks_old
    peaks = peaks.split(",")
    peaks = [ i for i in peaks if len(i) != 0 and not i.isdigit()  ]
    
    PIM_old = float(text2_msms.get("1.0", "end-1c"))
    PIM = PIM_old
    PIMT_old = float(text3_msms.get("1.0", "end-1c"))
    PIMT = PIMT_old
    MCT_old = float(text4_msms.get("1.0", "end-1c"))
    MCT = MCT_old
    mpb_all_t3db["value"] = 40

    if vlcmsms1.get() == 1:
        mode = "positive"
    elif vlcmsms1.get() == 2:
        mode = "negative"
    
    if vlcmsms2.get() == 1:
        unit = "Da"
    elif vlcmsms2.get() == 2:
        unit = "ppm"

    if vlcmsms3.get() == 1:
        cid = "low"
    elif vlcmsms3.get() == 2:
        cid = "med"
    elif vlcmsms3.get() == 3:
        cid = "high"

    if vlcmsms4.get() == 1:
        unit_mass = "Da"
    elif vlcmsms4.get() == 2:
        unit_mass = "ppm"

    if vlcmsms5.get() == 1:
        predicted1 = "True"
    else:
        predicted1 = "False"

    mpb_all_t3db["value"] = 50

    df_lcmsms = LCMSMS( p_ion_mass = PIM,
                        p_ion_tolerance = PIMT,
                        parent_ion_mass_tolerance_units = unit,
                        ion_mode = mode,
                        cid = cid,
                        peaks = peaks,
                        mz_tolerance = MCT,
                        mz_tolerance_units = unit_mass,
                        predicted= predicted1)

    mpb_all_t3db["value"] = 80

    df_lcmsms = make_it_correct(df_lcmsms)
    df_lcmsms.to_csv(f"{save_result_in}/LCMSMS.csv")
    mpb_all_t3db["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

###########################################
##########################################

def Kegg_pathways_T3DB():

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    mpb_all_t3db["value"] = 10
    labelVar.set("Loading")

    from get_data_plot import Geninfo_T3DB
    from KEGG import get_pathway_kegg

    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_T3DB"].tolist()


    df_all = pandas.DataFrame()
    for data  in Geninfo_T3DB( IDs ,"KEGG ID"):
        mpb_all_t3db["value"] = 30
        df_all = pandas.concat([df_all, data], axis=0,sort=False)
        
     
    mpb_all_t3db["value"] = 40
    #kegg_ids = df_all["col2"].tolist()[0]

    df_result_kegg_all = pandas.DataFrame()
    for kegg_id , T3DB_id in zip( df_all["col2"], list(df_all.index) ) :
        mpb_all_t3db["value"] = 60
        df_result = get_pathway_kegg(kegg_id ,T3DB_id )
        try:
            df_result_kegg_all = pandas.concat([df_result_kegg_all, df_result], axis=0,sort=False)
        except:
            continue 

    pyplot.close('all')
    mpb_all_t3db["value"] = 100
    df_result_kegg_all.to_csv(f"{save_result_in}/Kegg_pathway.csv")

    mb.showinfo(title="Result", message="All result have been saved")

    labelVar.set("Done")

def Kegg_pathways_T3DB_thread():
    thread.start_new_thread(Kegg_pathways_T3DB,())























###########################################
### all databases
###########################################
def SearchUsingID_all_database(): 
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")
    from All_in_DB import get_info_ids

    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs"].tolist()
    mpb_all_all_data_base["value"] = 10

    df_result = get_info_ids(IDs)
    mpb_all_all_data_base["value"] = 60

    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_result.to_csv(f"{save_result_in}/X_connector_{save_file_name}")

    mpb_all_all_data_base["value"] = 100
    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def SearchUsingQuery_all_database():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    from All_in_DB import get_id_all , get_info_ids

    labelVar.set("Loading")
    #get query
    mpb_all_all_data_base["value"] = 10
    query_search_old = text_query.get("1.0","end-1c")
    query_search = query_search_old
    query_search = query_search.strip()

    if query_search == "":
        mb.showerror(title="Error", message="Please insert a search query")
        return False
    else:
        pass
    ID_list = get_id_all(search_by = query_search)
    mpb_all_all_data_base["value"] = 40

    df_all_Search = get_info_ids(ID_list)
    # save
    mpb_all_all_data_base["value"] = 60
    df_all_Search.to_csv(f"{save_result_in}/txtsearch_Xconnector.csv")
    mpb_all_all_data_base["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")


############ plots
def import_file_csv_all_database():
    mpb_all_all_data_base["value"] = 0
    global import_file_ids
    global all_IDs
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    all_IDs  = file_ids_csv["IDs"].tolist()
    mpb_all_all_data_base["value"] = 100
    return True
def plot_xconnector1():
    
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    try:
        len (all_IDs)
    except:
        mb.showerror(title="Error", message="Please insert the CSV file that contains your IDs")
        return False

    labelVar.set("Loading")
    from All_in_DB import PredProp_all 
    import seaborn as sns
    from plotDB import lollplot

    
    global style
    global transparent_
    global dpi
    global color

    mpb_all_all_data_base["value"] = 10

    if transparent_.get() == 1:
        transparent = True
    else:
        transparent = False

    style_old = style_.get("1.0","end-1c")
    style = style_old
    if style  == "":
        style = "seaborn-pastel"
    else:
        style = style.strip()

    dpi_old = dpi_.get("1.0","end-1c")
    dpi = dpi_old
    if str( dpi ) == "":
        dpi = 600
    else:
        dpi = int(dpi)

    color_old = color_.get("1.0","end-1c")
    color = color_old
    if str( color  ) == "":
        color = "blue"
    else:
        color = color.strip()


    # 1 water Solubility
    mpb_all_all_data_base["value"] = 15
    water_all = {}
    pka_acid_dict = {}
    pka_basic_dict = {}

    for i_id in all_IDs:
        if "T3D" not in i_id:
            dp_type = i_id[:4]
        else:
            dp_type = i_id[:3]
        for data  in PredProp_all( [i_id] , db = dp_type):
            #water solubility
            try:
                water = data.loc[data['Property'] == "Water Solubility" , "Value"].values[0]
                water_all[list(data.index.values)[0]] = float( water.split()[0] )
            except:
                water_all[list(data.index.values)[0]] = "Not_found"

            #PKa
            try:
                pka_acid = data.loc[data['Property'] == "pKa (Strongest Acidic)" , "Value"].values[0]
                pka_acid_dict[list(data.index.values)[0]] =  float(pka_acid)
            except:
                pka_acid_dict[list(data.index.values)[0]] =  "Not_found"
            
            try:
                pka_basic = water = data.loc[data['Property'] == "pKa (Strongest Basic)" , "Value"].values[0]
                pka_basic_dict[list(data.index.values)[0]] =  float(pka_basic)
            except:
                pka_basic_dict[list(data.index.values)[0]] =  "Not_found"
    

        water_all = {k:v for k,v in water_all.items() if v != 'Not_found'}

        pka_acid_dict_ = {k:v for k,v in pka_acid_dict.items() if v != 'Not_found'}
        pka_basic_dict_ = {k:v for k,v in pka_basic_dict.items() if v != 'Not_found'}

        pka_acid_dict_ = {k:v for k,v in pka_acid_dict_.items() if k in pka_basic_dict_}
        pka_basic_dict_ = {k:v for k,v in pka_basic_dict_.items() if k in pka_acid_dict_}


    mpb_all_all_data_base["value"] = 20
    
    pyplot.close('all')
    # water
    lollplot(water_all , title = "Predicted Propertie" , xlabel= "g/L", ylabel= "", 
                        transparent = transparent , dpi = dpi, color_plot = color,markersize_ = 8, legend_label = "Water Solubility",
                        save = True, where_to_save = f"{save_result_in}/Predicted_Propertie(Water_Solubility1).png")
        
    pyplot.close('all')
    
    #pka_acid _ violine plot
    mpb_all_all_data_base["value"] = 40
    df_pka = pandas.DataFrame( {  "Strongest Acidic": list( pka_acid_dict_.values() ) ,
                                         "Strongest Basic": list( pka_basic_dict_.values() ) } 
                                            , index = list(pka_acid_dict_.keys())  )
    

    sns.violinplot(data=df_pka, palette="Pastel1" , inner = "box")
    fig = plt.gcf()
    fig.set_size_inches((13,8), forward=False)
    plt.title("Predicted Propertie(pKa)")
    plt.ylabel("pKa")
    mpb_all_all_data_base["value"] = 70
    plt.savefig(f"{save_result_in}/pKa.png", dpi= dpi , transparent = transparent)
    pyplot.close('all')

    #pKa acid_basic bipole bar plot
    from plotDB import bibarplot

    x_plot_x = bibarplot(range(1,len(df_pka)+1) , df_pka["Strongest Acidic"].sort_values(ascending=False)  , IDs_label = list(df_pka.index.values) ,
                                x_label = "Metabolites count" ,transparent = transparent, title  = "Predicted Propertie (Strongest Acidic)",
                                dpi= dpi, save = True , styles = style , where_to_save = f"{save_result_in}/pKa_StrongestAcidic.png")
    pyplot.close('all')
    y_plot_y = bibarplot(range(1,len(df_pka)+1) , df_pka["Strongest Basic"].sort_values(ascending=False)  ,  IDs_label = list(df_pka.index.values) ,
                                x_label = "Metabolites count" ,transparent = transparent, title  = "Predicted Propertie (Strongest Basic)",
                                    dpi= dpi, save = True , styles = style , where_to_save = f"{save_result_in}/pKa_StrongestBasic.png")
    pyplot.close('all')

    labelVar.set("Done")
    mpb_all_all_data_base["value"] = 100
    mb.showinfo(title="Result", message="All result have been saved")

    
    return True
def plot_xconnector1_thread():
    thread.start_new_thread(plot_xconnector1,())


























###########################################
### resDB
###########################################
#################
def SearchUsingID_respectDB(): 
    from respectDB import AccData
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_respectDB"].tolist()
    mpb_all_respectDB["value"] = 10

    #### Geninfo
    df_all_AccData = pandas.DataFrame()
    for i_data, _ in AccData(IDs):
        df_all_AccData = pandas.concat([df_all_AccData, i_data], axis=0,sort=False)


    mpb_all_respectDB["value"] = 50
    #save file 
    save_file_name = import_file_ids.split("/")[-1]
    df_all_AccData.to_csv(f"{save_result_in}/AccData_{save_file_name}")
    mpb_all_respectDB["value"] = 70

    mpb_all_respectDB["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def Draw_peak_respectDB():
    from respectDB import AccData, draw_peak
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    labelVar.set("Loading")
    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_respectDB"].tolist()
    mpb_all_respectDB["value"] = 10

    for i_id in IDs:
        draw_peak(str(i_id)).savefig(f"{save_result_in}/{i_id}.png", dpi=600)
        pyplot.close('all')
    mpb_all_respectDB["value"] = 60

    mpb_all_respectDB["value"] = 100
    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def Search_keyword_respectDB():

    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False

    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    from respectDB import AccData , Keyword
    mpb_all_respectDB["value"] = 10
    labelVar.set("Loading")

    CompName_old = text1_res.get("1.0","end-1c")
    CompName = CompName_old
    CompName = CompName.strip()

    CompFormuls_old = text2_res.get("1.0","end-1c")
    CompFormuls = CompFormuls_old
    CompFormuls = CompFormuls.strip()

    CompExactMass_old = text3_res.get("1.0","end-1c")
    CompExactMass = CompExactMass_old
    CompExactMass = CompExactMass.strip()

    CompTolerance_old = text4_res.get("1.0","end-1c")
    CompTolerance = CompTolerance_old
    CompTolerance = CompTolerance.strip()

    IDs = Keyword(name = CompName,
                    formula = CompFormuls,
                     exactmass= CompExactMass,
                     tolerance = CompTolerance)
    mpb_all_respectDB["value"] = 60

    df_all_Keyword = pandas.DataFrame()
    for i_data, _ in AccData(IDs):
        df_all_Keyword = pandas.concat([df_all_Keyword, i_data], axis=0,sort=False)


    mpb_all_respectDB["value"] = 90
    #save file 
    #save_file_name = import_file_ids.split("/")[-1]
    df_all_Keyword.to_csv(f"{save_result_in}/Keyword.csv")

    mpb_all_respectDB["value"] = 100

    labelVar.set("Done")
    mb.showinfo(title="Result", message="All result have been saved")

def Kegg_pathway_resDB():
    try:
        str(save_result_in)
    except:
        mb.showerror(title="Error", message="Please select a folder to save the result in")
        return False
    mb.showinfo(title="Note", message="This process will take time depending on the data size and the internet connection speed")

    mpb_all_respectDB["value"] = 10
    labelVar.set("Loading")

    from respectDB import AccData
    from KEGG import get_pathway_kegg

    ## get Ids
    import_file_ids = filedialog.askopenfilename()
    file_ids_csv = pandas.read_csv(import_file_ids)
    IDs  = file_ids_csv["IDs_respectDB"].tolist()

    df_all = {}
    for data , _ in AccData( IDs ):
        mpb_all_respectDB["value"] = 30
        try:
            df_all[list(data.index)[0]] = data["CH$ LINK_KEGG"][0]
        except:
            continue 
    mpb_all_respectDB["value"] = 40
    #kegg_ids = df_all["col2"].tolist()[0]

    df_result_kegg_all = pandas.DataFrame()
    for kegg_id in df_all:
        mpb_all_respectDB["value"] = 60
        df_result = get_pathway_kegg(df_all[kegg_id] ,kegg_id )
        print (df_result)
        try:
            df_result_kegg_all = pandas.concat([df_result_kegg_all, df_result], axis=0,sort=False)
        except:
            continue 

    pyplot.close('all')
    mpb_all_respectDB["value"] = 100
    df_result_kegg_all.to_csv(f"{save_result_in}/Kegg_pathway.csv")

    mb.showinfo(title="Result", message="All result have been saved")

    labelVar.set("Done")





#**********************************
### run threads 
#**********************************
# HMDB
def HMDB_plots_thread():
    thread.start_new_thread(HMDB_plots, ())

def SearchUsingID_HMDB_thread():
    thread.start_new_thread(SearchUsingID_HMDB, ())

def SearchUsingQuery_HMDB_thread():
    thread.start_new_thread(SearchUsingQuery_HMDB, ())

def ChemQuery_HMBB_run_thread():
    thread.start_new_thread(ChemQuery_HMBB_run, ())

def LCMS_run_HMDB_thread():
    thread.start_new_thread(LCMS_run_HMDB, ())

def LCMSMS_run_HMDB_thread():
    thread.start_new_thread(LCMSMS_run_HMDB,())

def SMPDB_run_HMDB_thread():
    thread.start_new_thread(SMPDB_run_HMDB,())
#LMDB

def SearchUsingID_LMDB_thread():
    thread.start_new_thread(SearchUsingID_LMDB,())

def ChemQuery_LMBB_run_thread():
    thread.start_new_thread(ChemQuery_LMBB_run, ())

def SearchUsingQuery_LMDB_thread():
    thread.start_new_thread(SearchUsingQuery_LMDB,())

def LCMS_run_LMDB_thread():
    thread.start_new_thread(LCMS_run_LMDB, ())

def LCMSMS_run_LMDB_thread():
    thread.start_new_thread(LCMSMS_run_LMDB,())

#YMSB

def SearchUsingID_YMDB_thread():
    thread.start_new_thread(SearchUsingID_YMDB,())

def SearchUsingQuery_YMDB_thread():
    thread.start_new_thread(SearchUsingQuery_YMDB,())

def ChemQuery_YMDB_run_thread():
    thread.start_new_thread(ChemQuery_YMDB_run,())

def LCMS_run_YMDB_thread():
    thread.start_new_thread(LCMS_run_YMDB,())

def LCMSMS_run_YMDB_thread():
    thread.start_new_thread(LCMSMS_run_YMDB,())

#T3DB
def SearchUsingID_T3DB_thread():
    thread.start_new_thread(SearchUsingID_T3DB,())

def SearchUsingQuery_T3DB_thread():
    thread.start_new_thread(SearchUsingQuery_T3DB,())

def ChemQuery_T3DB_run_thread():
    thread.start_new_thread(ChemQuery_T3DB_run,())

def LCMS_run_T3DB_thread():
    thread.start_new_thread(LCMS_run_T3DB,())

def LCMSMS_run_T3DB_thread():
    thread.start_new_thread(LCMSMS_run_T3DB,())

# alldatase
def SearchUsingID_all_database_thread():
    thread.start_new_thread(SearchUsingID_all_database,())

def SearchUsingQuery_all_database_thread():
    thread.start_new_thread(SearchUsingQuery_all_database,())

#resDB

def SearchUsingID_respectDB_thread():
    thread.start_new_thread(SearchUsingID_respectDB,())

def Draw_peak_respectDB_thread():
    thread.start_new_thread(Draw_peak_respectDB,())

def Search_keyword_respectDB_thread():
    thread.start_new_thread(Search_keyword_respectDB,())

def Kegg_pathway_resDB_thread():
    thread.start_new_thread(Kegg_pathway_resDB,())

#**********************************
### GUI Functions
#**********************************

 












### 0- x_connector_GUI
###################
def GUI_ALL():
    gui_all = tk.Toplevel(root)
    gui_all.iconbitmap(f'{pathh}logo\\logo.v1.ico')
    gui_all.title("Xconnector")

    global labelVar
    global mpb_all_all_data_base
    labelVar = StringVar()
    label = Label(gui_all, textvariable=labelVar).grid(row=2, column = 0, pady = 10, padx = 5 ,sticky=SE)

    # loading bar
    mpb_all_all_data_base = ttk.Progressbar(gui_all,orient ="horizontal",length = 170, mode ="determinate")
    mpb_all_all_data_base.grid(row=2, column = 1, pady = 10, padx = 10)
    mpb_all_all_data_base["maximum"] = 100

    ####################################################
    ### plots
    def visualize_toplevel_all_data_base():

        visualize_toplevel = tk.Toplevel(root)
        visualize_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        visualize_toplevel.title("Xconnector")
        global style_
        global transparent_
        global dpi_
        global color_
        #paramter

        tk.Label(visualize_toplevel, text="Style ").grid(row=0, column = 0,pady = 4, padx = 0, sticky=SE)
        style_ = Text(visualize_toplevel, width = 20, height= 1)
        style_.grid(row=0, column=1, pady = 4, padx = 0, sticky=SE )
        style_.insert(INSERT, "seaborn-pastel")

        transparent_ = IntVar()
        Checkbutton(visualize_toplevel, text="Transparent", variable=transparent_).grid(row=1, column = 2,  pady = 4 , sticky=SE)

        tk.Label(visualize_toplevel, text="dpi ").grid(row=1, column = 0, sticky=SE)
        dpi_ = Text(visualize_toplevel, width = 20, height= 1)
        dpi_.grid(row=1, column=1, pady = 4, padx = 0 , sticky=SE)
        dpi_.insert(INSERT, "600")


        tk.Label(visualize_toplevel, text="Color ").grid(row=2, column = 0, sticky=SE)
        color_ = Text(visualize_toplevel, width = 20, height= 1)
        color_.grid(row=2, column=1, pady = 4, padx = 0 , sticky=SE)
        color_.insert(INSERT, "blue")

        run_visualize = tk.Button(visualize_toplevel,
            text="Run", width = 10,
            command=plot_xconnector1_thread).grid(column= 3, row = 2, pady = 0, padx = 0,  sticky=SW ) 

        import_file = tk.Button(visualize_toplevel,
            text="Import IDs", width = 10,
            command=import_file_csv_all_database).grid(column= 3, row = 0, pady = 0, padx = 0,  sticky=SW ) 

    def thread_visualize_toplevel_all_data_base():
        thread.start_new_thread(visualize_toplevel_all_data_base, ())

    visualize = tk.Button(gui_all,
                text="Visualize", width = 30,
                command=thread_visualize_toplevel_all_data_base).grid(column= 0, row = 1, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for accessions functions

    search_using_acc_but = tk.Button(gui_all,
                text="Search using IDs", width = 30,
                command=SearchUsingID_all_database_thread).grid(column= 0, row = 0, pady = 10, padx = 10 )   

    #####################################################
    ##### GUI for text functions
    def tesxt_toplevel_all():

        gui_tesxt_toplevel_all = tk.Toplevel(root)
        gui_tesxt_toplevel_all.iconbitmap(f"{pathh}logo.v1.ico")
        gui_tesxt_toplevel_all.title("Xconnector")
        global text_query
        tk.Label(gui_tesxt_toplevel_all, text="Enter a search query").grid(row=0, column = 0)
        text_query = ScrolledText(gui_tesxt_toplevel_all, width = 60, height= 3)
        text_query.grid(row=0, column=1, pady = 10, padx = 10 )

        
        run_but = tk.Button(gui_tesxt_toplevel_all,
                    text="Search", width = 10,
                    command=SearchUsingQuery_all_database_thread).grid(row=1, column=1, pady = 10, padx = 10 )
        
    def thread_tesxt_toplevel_all_all():
        thread.start_new_thread(tesxt_toplevel_all, ())

    search_using_text_but = tk.Button(gui_all,
                text="Search using Metabolic Name", width = 30,
                command=thread_tesxt_toplevel_all_all).grid(column= 1, row = 0, pady = 10, padx = 10 )   

























### 1- HMDB_GUI
###################

def GUI_HMDB():
    gui_hmdb = tk.Toplevel(root)
    gui_hmdb.iconbitmap(f"{pathh}logo.v1.ico")
    gui_hmdb.title("HMDBconnector")
    global mpb_all_hmdb
    global labelVar

    labelVar = StringVar()
    label = Label(gui_hmdb, textvariable=labelVar).grid(row=2, column = 1, pady = 10, padx = 5 ,sticky=SE)

    # loading bar
    mpb_all_hmdb = ttk.Progressbar(gui_hmdb,orient ="horizontal",length = 200, mode ="determinate")
    mpb_all_hmdb.grid(row=2, column = 2, pady = 10, padx = 5 ,sticky=SE)
    mpb_all_hmdb["maximum"] = 100
    #####################################################
    ##### GUI for plots functions

    def visualize_toplevel_hmdb():
        global var_Disposition
        global var_Biological
        global style_
        global transparent_
        global dpi_
        global mpb_vis
        global color_
        global var_Predicted
        global labelVarhmdb
        visualize_toplevel = tk.Toplevel(root)
        visualize_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        visualize_toplevel.title("HMDBconnector")
        labelVarhmdb = StringVar()
        label = Label(visualize_toplevel, textvariable=labelVarhmdb).grid(row=4, column = 2, pady = 10, padx = 5 ,sticky=SE)

        # loading bar
        mpb_vis = ttk.Progressbar(visualize_toplevel,orient ="horizontal",length = 100, mode ="determinate")
        mpb_vis.grid(row=4, column = 3, pady = 4, padx = 4 ,sticky=SW)
        mpb_vis["maximum"] = 100
        #Disposition
        var_Disposition = IntVar()
        Checkbutton(visualize_toplevel, text="Disposition", variable=var_Disposition).grid(row=0, column = 0 , sticky=NW)

        #Process
        #var_Process = IntVar()
        #Checkbutton(visualize_toplevel, text="Process", variable=var_Process).grid(row=0, column = 1 , sticky=N)

        #Biological Properties
        var_Biological = IntVar()
        Checkbutton(visualize_toplevel, text="Biological Properties", variable=var_Biological).grid(row=0, column = 1 , sticky=NW)

        #Predicted Properties	
        var_Predicted = IntVar()
        Checkbutton(visualize_toplevel, text="Predicted Properties", variable=var_Predicted).grid(row=0, column = 2 , sticky=NW)


        #paramter


        tk.Label(visualize_toplevel, text="Style ").grid(row=2, column = 0,pady = 4, padx = 0, sticky=SE)
        style_ = Text(visualize_toplevel, width = 20, height= 1)
        style_.grid(row=2, column=1, pady = 4, padx = 0, sticky=SE )

        transparent_ = IntVar()
        Checkbutton(visualize_toplevel, text="Transparent", variable=transparent_).grid(row=2, column = 2,  pady = 4 , sticky=SE)

        tk.Label(visualize_toplevel, text="dpi ").grid(row=3, column = 0, sticky=SE)
        dpi_ = Text(visualize_toplevel, width = 20, height= 1)
        dpi_.grid(row=3, column=1, pady = 4, padx = 0 , sticky=SE)

        tk.Label(visualize_toplevel, text="Color ").grid(row=4, column = 0, sticky=SE)
        color_ = Text(visualize_toplevel, width = 20, height= 1)
        color_.grid(row=4, column=1, pady = 4, padx = 0 , sticky=SE)

        style_.insert(INSERT, "seaborn-pastel")
        dpi_.insert(INSERT, "600")
        color_.insert(INSERT, "blue")

        run_visualize = tk.Button(visualize_toplevel,
            text="Run", width = 10,
            command=HMDB_plots_thread).grid(column= 3, row = 2, pady = 10, padx = 10,  sticky=SW ) 

        import_file = tk.Button(visualize_toplevel,
            text="Import IDs", width = 10,
            command=import_file_csv_HMDB).grid(column= 3, row = 1, pady = 10, padx = 10,  sticky=SW ) 

    def thread_visualize_toplevel_hmdb():
        thread.start_new_thread(visualize_toplevel_hmdb, ())

    visualize = tk.Button(gui_hmdb,
                text="Visualize", width = 20,
                command=thread_visualize_toplevel_hmdb).grid(column= 0, row = 2, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for accessions functions

    search_using_acc_but = tk.Button(gui_hmdb,
                text="Search using IDs", width = 20,
                command=SearchUsingID_HMDB_thread).grid(column= 0, row = 0, pady = 10, padx = 10 )   

    #############################################
    #### SMPDB
    def smpdb_toplevel_hmdb():
        smpdb_toplevel = tk.Toplevel(root)
        smpdb_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        smpdb_toplevel.title("HMDBconnector")
        global filter_smpdb
        global image_smpdb
        global pathway_smpdb
        filter_smpdb = tk.IntVar()

        tk.Radiobutton(smpdb_toplevel, 
            text="Filter by: Physiological",
            variable=filter_smpdb, 
            value=1).grid(row=0, column=0, pady = 5, padx = 10, sticky = "NW"  )

        tk.Radiobutton(smpdb_toplevel, 
            text="Filter by: Metabolic",
            variable=filter_smpdb, 
            value=2).grid(row=0, column=1, pady = 5, padx = 10, sticky = "NW"  )

        tk.Radiobutton(smpdb_toplevel, 
            text="Filter by: Signaling",
            variable=filter_smpdb, 
            value=3).grid(row=0, column=2, pady = 5, padx = 10, sticky = "NW"  )

        tk.Radiobutton(smpdb_toplevel, 
            text="Filter by: Drug+Metabolism",
            variable=filter_smpdb, 
            value=4).grid(row=1, column=0, pady = 5, padx = 10, sticky = "NW"  )

        tk.Radiobutton(smpdb_toplevel, 
            text="Filter by: Drug+Action",
            variable=filter_smpdb, 
            value=5).grid(row=1, column=1, pady = 5, padx = 10, sticky = "NW"  )
        
        image_smpdb = IntVar()
        Checkbutton(smpdb_toplevel, text="Download pathways image", variable=image_smpdb).grid(row=6, column=0, pady = 5, padx = 5, sticky = "NW"  )

        pathway_smpdb = IntVar()
        Checkbutton(smpdb_toplevel, text="Get all metabolites involved", variable=pathway_smpdb).grid(row=6, column=1, pady = 5, padx = 5, sticky = "NW"  )



        tk.Radiobutton(smpdb_toplevel, 
            text="Filter by: Disease",
            variable=filter_smpdb, 
            value=6).grid(row=2, column=0, pady = 5, padx = 10, sticky = "NW"  )

        run_GUI_but = tk.Button(smpdb_toplevel,
                text="Run", width = 10,
                command=SMPDB_run_HMDB_thread).grid(row=2, column=2 , pady = 10, padx = 10 )  
       

    def smpdb_toplevel_hmdb_thread():
        thread.start_new_thread(smpdb_toplevel_hmdb,())


    search_using_acc_but_smpdb = tk.Button(gui_hmdb,
                text="Get SMPDB pathway", width = 20,
                command=smpdb_toplevel_hmdb_thread).grid(column= 0, row = 1, pady = 10, padx = 10 )  

    #####################################################
    ##### GUI for Search function

    def search_toplevel_hmdb():
        global text_query
        global v_query
        search_toplevel = tk.Toplevel(root)
        search_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        search_toplevel.title("HMDBconnector")
        tk.Label(search_toplevel, text="Enter a search query").grid(row=0, column = 0)
        text_query = ScrolledText(search_toplevel, width = 30, height= 10)
        text_query.grid(row=0, column=1, pady = 10, padx = 10 )

        v_query = tk.IntVar()

        tk.Radiobutton(search_toplevel, 
            text="Metabolites",
            variable=v_query, 
            value=1).grid(row=1, column=0, pady = 5, padx = 10, sticky = "NW"  )

        tk.Radiobutton(search_toplevel, 
            text="Diseases",
            variable=v_query, 
            value=2).grid(row=2, column=0, pady = 5, padx = 10, sticky = "NW" )

        tk.Radiobutton(search_toplevel, 
            text="pathways",
            variable=v_query, 
            value=3).grid(row=3, column=0, pady = 5, padx = 10, sticky = "NW" )

        tk.Radiobutton(search_toplevel, 
            text="Proteins",
            variable=v_query, 
            value=4).grid(row=1, column=1, pady = 5, padx = 10, sticky = "NW" )

        tk.Radiobutton(search_toplevel, 
            text="Reactions",
            variable=v_query, 
            value=5).grid(row=2, column=1, pady = 5, padx = 10, sticky = "NW" )

        run_GUI_but = tk.Button(search_toplevel,
                text="Run", width = 10,
                command=SearchUsingQuery_HMDB_thread).grid(row=3, column=1 , pady = 10, padx = 10 )  
       
    def thread_search_toplevel_hmdb():
        thread.start_new_thread(search_toplevel_hmdb, ())

    search_GUI_but = tk.Button(gui_hmdb,
                text="Searching by query", width = 20,
                command=thread_search_toplevel_hmdb).grid(column= 1, row = 0, pady = 10, padx = 10 )   

    #####################################################
    ##### GUI for ChemQuery function
    def ChemQuery_toplevel_hmdb():
        global text1chm
        global text2chm
        global vchem_hmdb
        global vchem_hmdb2
        ChemQuery_toplevel = tk.Toplevel(root) 
        ChemQuery_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        ChemQuery_toplevel.title("HMDBconnector")

        tk.Label(ChemQuery_toplevel, text="Start from").grid(row=0, column = 0)
        text1chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text1chm.grid(row=0, column=1,pady = 5, padx = 5, sticky = "NW"  )

        tk.Label(ChemQuery_toplevel, text="End at   ").grid(row=0, column = 2)
        text2chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text2chm.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  )

        vchem_hmdb = tk.IntVar()

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Molecular",
            variable=vchem_hmdb, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Monoisotopic",
            variable=vchem_hmdb, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )


        vchem_hmdb2 = tk.IntVar()
        
        tk.Radiobutton(ChemQuery_toplevel, 
            text="Quantified",
            variable=vchem_hmdb2, 
            value=1).grid(row=2, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Detected",
            variable=vchem_hmdb2, 
            value=2).grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="expected",
            variable=vchem_hmdb2, 
            value=3).grid(row=2, column=2, pady = 5, padx = 5, sticky = "NW"  )

        run_GUI_but = tk.Button(ChemQuery_toplevel,
                text="Run", width = 10,
                command=ChemQuery_HMBB_run_thread).grid(row=2, column=3, pady = 5, padx = 5, sticky = "NW"  )    

    def thread_ChemQuery_toplevel_hmdb():
        thread.start_new_thread(ChemQuery_toplevel_hmdb, ())

    ChemQuery_GUI_but = tk.Button(gui_hmdb,
                text="Search by MW", width = 20,
                command=thread_ChemQuery_toplevel_hmdb).grid(column= 1, row = 1, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for LCMS function
    def LCMS_toplevel_hmdb():

        global text_lcms1
        global text_lcms2
        global text_lcms3
        global vlcms
        global vlcms1

        LCMS_toplevel = tk.Toplevel(root) 
        LCMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMS_toplevel.title("HMDBconnector")

        tk.Label(LCMS_toplevel, text="Masses").grid(row=0, column = 0)
        text_lcms1 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms1.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMS_toplevel, text="Adducts").grid(row=0, column = 2)
        text_lcms2 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms2.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(LCMS_toplevel, text="Tolerance ±").grid(row=2, column = 0)
        text_lcms3 = Text(LCMS_toplevel, width = 8, height= 1)
        text_lcms3.grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        vlcms= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Positive",
            variable=vlcms, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Negative",
            variable=vlcms, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Neutral",
            variable=vlcms, 
            value=3).grid(row=1, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcms1= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Da",
            variable=vlcms1, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        
        tk.Radiobutton(LCMS_toplevel, 
            text="ppm",
            variable=vlcms1, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMS_toplevel,
                text="Run", width = 10,
                command=LCMS_run_HMDB_thread).grid(column= 3, row = 3, pady = 10, padx = 10 )   

    def thread_LCMS_toplevel_hmdb():
        thread.start_new_thread(LCMS_toplevel_hmdb, ())


    LCMS_GUI_but = tk.Button(gui_hmdb,
                text="MSS", width = 20,
                command=thread_LCMS_toplevel_hmdb).grid(column= 2, row = 0, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for LCMSMS function

    def LCMSMS_toplevel_hmdb():

        global text1_msms
        global text2_msms
        global text3_msms
        global text4_msms
        global vlcmsms1
        global vlcmsms2
        global vlcmsms3
        global vlcmsms4
        global vlcmsms5
        LCMSMS_toplevel = tk.Toplevel(root) 
        LCMSMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMSMS_toplevel.title("HMDBconnector")

        tk.Label(LCMSMS_toplevel, text="Peaks").grid(row=0, column = 0)
        text1_msms = ScrolledText(LCMSMS_toplevel, width = 25, height= 12)
        text1_msms.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass (Da)").grid(row=1, column = 0)
        text2_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text2_msms.grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass Tolerance ±").grid(row=1, column = 2)
        text3_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text3_msms.grid(row=1, column=3, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Mass/Charge (m/z) Tolerance ±").grid(row=2, column = 2)
        text4_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text4_msms.grid(row=2, column=3, pady = 5, padx = 5, sticky = "NW"  )  


        vlcmsms1= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Positive",
            variable=vlcmsms1, 
            value=1).grid(row=2, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Negative",
            variable=vlcmsms1, 
            value=2).grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms2= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Parent ion mass Da tolerance units",
            variable=vlcmsms2, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="parent ion mass ppm tolerance units",
            variable=vlcmsms2, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        vlcmsms3= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID low",
            variable=vlcmsms3, 
            value=1).grid(row=4, column=0, pady = 5, padx = 5, sticky = "NW"  )
        
        
        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID med",
            variable=vlcmsms3, 
            value=2).grid(row=4, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID high",
            variable=vlcmsms3, 
            value=3).grid(row=4, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms4= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit Da",
            variable=vlcmsms4, 
            value=1).grid(row=5, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit ppm",
            variable=vlcmsms4, 
            value=2).grid(row=5, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms5 = IntVar()
        Checkbutton(LCMSMS_toplevel, text="Include predicted spectra", variable=vlcmsms5).grid(row=6, column=0, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMSMS_toplevel,
                text="Run", width = 10,
                command=LCMSMS_run_HMDB_thread).grid(column= 3, row = 6, pady = 10, padx = 10 )


    def thread_LCMSMS_toplevel_hmdb():
        thread.start_new_thread(LCMSMS_toplevel_hmdb, ())


    ChemQuery_GUI_but = tk.Button(gui_hmdb,
                text="TMSS", width = 20,
                command=thread_LCMSMS_toplevel_hmdb).grid(column= 2, row = 1, pady = 10, padx = 10 )    




















































########################### 2- LMDB_GUI
###################

def GUI_LMDB():
    gui_lmdb = tk.Toplevel(root)
    gui_lmdb.iconbitmap(f"{pathh}logo.v1.ico")
    gui_lmdb.title("LMDBconnector")
    global labelVar
    global mpb_all_lmdb

    labelVar = StringVar()
    label = Label(gui_lmdb, textvariable=labelVar).grid(row=2, column = 1, pady = 10, padx = 5 ,sticky=SE)

    # loading bar
    mpb_all_lmdb = ttk.Progressbar(gui_lmdb,orient ="horizontal",length = 200, mode ="determinate")
    mpb_all_lmdb.grid(row=2, column = 2, pady = 10, padx = 5 ,sticky=SE)
    mpb_all_lmdb["maximum"] = 100

    #####################################################
    ## plot GUI
    def visualize_toplevel_lmdb():

        global style_
        global transparent_
        global dpi_
        global color_

        visualize_toplevel = tk.Toplevel(root)
        visualize_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        visualize_toplevel.title("LMDBconnector")
        #paramter

        tk.Label(visualize_toplevel, text="Style ").grid(row=0, column = 0,pady = 4, padx = 0, sticky=SE)
        style_ = Text(visualize_toplevel, width = 20, height= 1)
        style_.grid(row=0, column=1, pady = 4, padx = 0, sticky=SE )

        transparent_ = IntVar()
        Checkbutton(visualize_toplevel, text="Transparent", variable=transparent_).grid(row=1, column = 2,  pady = 4 , sticky=SE)

        tk.Label(visualize_toplevel, text="dpi ").grid(row=1, column = 0, sticky=SE)
        dpi_ = Text(visualize_toplevel, width = 20, height= 1)
        dpi_.grid(row=1, column=1, pady = 4, padx = 0 , sticky=SE)

        tk.Label(visualize_toplevel, text="Color ").grid(row=2, column = 0, sticky=SE)
        color_ = Text(visualize_toplevel, width = 20, height= 1)
        color_.grid(row=2, column=1, pady = 4, padx = 0 , sticky=SE)

        style_.insert(INSERT, "seaborn-pastel")
        dpi_.insert(INSERT, "600")
        color_.insert(INSERT, "blue")

        run_visualize = tk.Button(visualize_toplevel,
            text="Run", width = 10,
            command=LMDB_plots_thread).grid(column= 3, row = 2, pady = 0, padx = 0,  sticky=SW ) 

        import_file = tk.Button(visualize_toplevel,
            text="Import IDs", width = 10,
            command=import_file_csv_LMDB).grid(column= 3, row = 0, pady = 0, padx = 0,  sticky=SW ) 

    def thread_visualize_toplevel_lmdb():
        thread.start_new_thread(visualize_toplevel_lmdb, ())

    visualize = tk.Button(gui_lmdb,
                text="Visualize", width = 20,
                command=thread_visualize_toplevel_lmdb).grid(column= 0, row = 1, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for accessions functions

    accessions_GUI_but = tk.Button(gui_lmdb,
                text="Search using IDs", width = 20,
                command=SearchUsingID_LMDB_thread).grid(column= 0, row = 0, pady = 10, padx = 10 ) 


    #####################################################
    ##### GUI for ChemQuery functions

    def ChemQuery_toplevel_lmdb():
        ChemQuery_toplevel = tk.Toplevel(root)
        ChemQuery_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        ChemQuery_toplevel.title("LMDBconnector")
        global text1chm
        global text2chm
        global vchem_LMDB
        global vchem_LMDB2
        tk.Label(ChemQuery_toplevel, text="Start from").grid(row=0, column = 0)
        text1chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text1chm.grid(row=0, column=1,pady = 5, padx = 5, sticky = "NW"  )

        tk.Label(ChemQuery_toplevel, text="End at   ").grid(row=0, column = 2)
        text2chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text2chm.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  )

        vchem_LMDB = tk.IntVar()

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Molecular",
            variable=vchem_LMDB, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Monoisotopic",
            variable=vchem_LMDB, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )


        vchem_LMDB2 = tk.IntVar()
        
        tk.Radiobutton(ChemQuery_toplevel, 
            text="Quantified",value=1,
            variable=vchem_LMDB2) .grid(row=2, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Detected",value=2,
            variable=vchem_LMDB2).grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="expected",value=3,
            variable=vchem_LMDB2).grid(row=2, column=2, pady = 5, padx = 5, sticky = "NW"  )

        run_GUI_but = tk.Button(ChemQuery_toplevel,
                text="Run", width = 10,
                command=ChemQuery_LMBB_run_thread).grid(row=2, column=3, pady = 5, padx = 5, sticky = "NW"  )    

    def thread_ChemQuery_toplevel_lmdb():
        thread.start_new_thread(ChemQuery_toplevel_lmdb, ())

    ChemQuery_GUI_but = tk.Button(gui_lmdb,
                text="Search by MW", width = 20,
                command=thread_ChemQuery_toplevel_lmdb).grid(column= 1, row = 1, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for search function
    def search_toplevel_lmdb():
        search_toplevel = tk.Toplevel(root)
        search_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        search_toplevel.title("LMDBconnector")
        global text_query
        tk.Label(search_toplevel, text="Enter a search query").grid(row=0, column = 0)
        text_query = ScrolledText(search_toplevel, width = 60, height= 2)
        text_query.grid(row=0, column=1, pady = 10, padx = 10 )

        #text.get("1.0", "end-1c") 

        run_GUI_but = tk.Button(search_toplevel,
                text="Run", width = 10,
                command=SearchUsingQuery_LMDB_thread).grid(row=2, column=1 , pady = 10, padx = 10 )  

    def thread_search_toplevel_lmdb():
        thread.start_new_thread(search_toplevel_lmdb, ())

    search_GUI_but = tk.Button(gui_lmdb,
                text="Searching by query", width = 20,
                command=thread_search_toplevel_lmdb).grid(column= 1, row = 0, pady = 10, padx = 10 )

    #####################################################
    ##### GUI for LCMS function
    def LCMS_toplevel_lmdb():
        LCMS_toplevel = tk.Toplevel(root) 
        LCMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMS_toplevel.title("LMDBconnector")
        global text_lcms1
        global text_lcms2
        global text_lcms3
        global vlcms
        global vlcms1
        tk.Label(LCMS_toplevel, text="Masses").grid(row=0, column = 0)
        text_lcms1 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms1.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMS_toplevel, text="Adducts").grid(row=0, column = 2)
        text_lcms2 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms2.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(LCMS_toplevel, text="Tolerance ±").grid(row=2, column = 0)
        text_lcms3 = Text(LCMS_toplevel, width = 8, height= 1)
        text_lcms3.grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        vlcms= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Positive",
            variable=vlcms, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Negative",
            variable=vlcms, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Neutral",
            variable=vlcms, 
            value=3).grid(row=1, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcms1= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Da",
            variable=vlcms1, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        
        tk.Radiobutton(LCMS_toplevel, 
            text="ppm",
            variable=vlcms1, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMS_toplevel,
                text="Run", width = 10,
                command=LCMS_run_LMDB_thread).grid(column= 3, row = 3, pady = 10, padx = 10 )   

    def thread_LCMS_toplevel_lmdb():
        thread.start_new_thread(LCMS_toplevel_lmdb, ())


    LCMS_GUI_but = tk.Button(gui_lmdb,
                text="MSS", width = 20,
                command=thread_LCMS_toplevel_lmdb).grid(column= 2, row = 0, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for LCMSMS function

    def LCMSMS_toplevel_lmdb():
        LCMSMS_toplevel = tk.Toplevel(root) 
        LCMSMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMSMS_toplevel.title("LMDBconnector")
        global text1_msms
        global text2_msms
        global text3_msms
        global text4_msms
        global vlcmsms1
        global vlcmsms2
        global vlcmsms3
        global vlcmsms4
        global vlcmsms5
        tk.Label(LCMSMS_toplevel, text="Peaks").grid(row=0, column = 0)
        text1_msms = ScrolledText(LCMSMS_toplevel, width = 25, height= 12)
        text1_msms.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass (Da)").grid(row=1, column = 0)
        text2_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text2_msms.grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass Tolerance ±").grid(row=1, column = 2)
        text3_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text3_msms.grid(row=1, column=3, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Mass/Charge (m/z) Tolerance ±").grid(row=2, column = 2)
        text4_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text4_msms.grid(row=2, column=3, pady = 5, padx = 5, sticky = "NW"  ) 

        vlcmsms1= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Positive",
            variable=vlcmsms1, 
            value=1).grid(row=2, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Negative",
            variable=vlcmsms1, 
            value=2).grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms2= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Parent ion mass Da tolerance units",
            variable=vlcmsms2, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="parent ion mass ppm tolerance units",
            variable=vlcmsms2, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        vlcmsms3= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID low",
            variable=vlcmsms3, 
            value=1).grid(row=4, column=0, pady = 5, padx = 5, sticky = "NW"  )
        
        
        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID med",
            variable=vlcmsms3, 
            value=2).grid(row=4, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID high",
            variable=vlcmsms3, 
            value=3).grid(row=4, column=2, pady = 5, padx = 5, sticky = "NW"  ) 

        vlcmsms4= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit Da",
            variable=vlcmsms4, 
            value=1).grid(row=5, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit ppm",
            variable=vlcmsms4, 
            value=2).grid(row=5, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms5 = IntVar()
        Checkbutton(LCMSMS_toplevel, text="Include predicted spectra", variable=vlcmsms5).grid(row=6, column=0, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMSMS_toplevel,
                text="Run", width = 10,
                command= LCMSMS_run_LMDB_thread).grid(column= 3, row = 6, pady = 10, padx = 10 )


    def thread_LCMSMS_toplevel_lmdb():
        thread.start_new_thread(LCMSMS_toplevel_lmdb, ())


    ChemQuery_GUI_but = tk.Button(gui_lmdb,
                text="TMSS", width = 20,
                command=thread_LCMSMS_toplevel_lmdb).grid(column= 2, row = 1, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for KEgg function

    accessions_GUI_Kegg = tk.Button(gui_lmdb,
                text="KEGG pathways", width = 20,
                command=Kegg_pathways_LMDB_thread).grid(column= 0, row = 2, pady = 10, padx = 10 ) 






















































########################### 4- YMDB_GUI
###################
def GUI_YMDB():
    gui_ymdb = tk.Toplevel(root)
    gui_ymdb.iconbitmap(f"{pathh}logo.v1.ico")
    gui_ymdb.title("YMDBconnector")
    global labelVar
    global mpb_all_ymdb
    labelVar = StringVar()
    label = Label(gui_ymdb, textvariable=labelVar).grid(row=2, column = 1, pady = 10, padx = 5 ,sticky=SE)

    # loading bar
    mpb_all_ymdb = ttk.Progressbar(gui_ymdb,orient ="horizontal",length = 200, mode ="determinate")
    mpb_all_ymdb.grid(row=2, column = 2, pady = 10, padx = 5 ,sticky=SE)
    mpb_all_ymdb["maximum"] = 100

    #####################################################
    ### plots

    def visualize_toplevel_ymdb():

        visualize_toplevel = tk.Toplevel(root)
        visualize_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        visualize_toplevel.title("YMDBconnector")
        global style_
        global transparent_
        global dpi_
        global color_
        #paramter

        tk.Label(visualize_toplevel, text="Style ").grid(row=0, column = 0,pady = 4, padx = 0, sticky=SE)
        style_ = Text(visualize_toplevel, width = 20, height= 1)
        style_.grid(row=0, column=1, pady = 4, padx = 0, sticky=SE )

        transparent_ = IntVar()
        Checkbutton(visualize_toplevel, text="Transparent", variable=transparent_).grid(row=1, column = 2,  pady = 4 , sticky=SE)

        tk.Label(visualize_toplevel, text="dpi ").grid(row=1, column = 0, sticky=SE)
        dpi_ = Text(visualize_toplevel, width = 20, height= 1)
        dpi_.grid(row=1, column=1, pady = 4, padx = 0 , sticky=SE)

        tk.Label(visualize_toplevel, text="Color ").grid(row=2, column = 0, sticky=SE)
        color_ = Text(visualize_toplevel, width = 20, height= 1)
        color_.grid(row=2, column=1, pady = 4, padx = 0 , sticky=SE)

        style_.insert(INSERT, "seaborn-pastel")
        dpi_.insert(INSERT, "600")
        color_.insert(INSERT, "blue")

        run_visualize = tk.Button(visualize_toplevel,
            text="Run", width = 10,
            command=YMDB_plots_thread).grid(column= 3, row = 2, pady = 0, padx = 0,  sticky=SW ) 

        import_file = tk.Button(visualize_toplevel,
            text="Import IDs", width = 10,
            command=import_file_csv_YMDB).grid(column= 3, row = 0, pady = 0, padx = 0,  sticky=SW ) 

    def thread_visualize_toplevel_ymdb():
        thread.start_new_thread(visualize_toplevel_ymdb, ())

    visualize = tk.Button(gui_ymdb,
                text="Visualize", width = 20,
                command=thread_visualize_toplevel_ymdb).grid(column= 0, row = 1, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for accessions functions

    accessions_GUI_but = tk.Button(gui_ymdb,
                text="Search using IDs", width = 20,
                command=SearchUsingID_YMDB_thread).grid(column= 0, row = 0, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for ChemQuery functions

    def ChemQuery_toplevel_ymdb():
        ChemQuery_toplevel = tk.Toplevel(root) 
        ChemQuery_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        ChemQuery_toplevel.title("YMDBconnector")
        global text1chm
        global text2chm
        global vchem_YMDB

        tk.Label(ChemQuery_toplevel, text="Start from").grid(row=0, column = 0)
        text1chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text1chm.grid(row=0, column=1,pady = 5, padx = 5, sticky = "NW"  )

        tk.Label(ChemQuery_toplevel, text="End at   ").grid(row=0, column = 2)
        text2chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text2chm.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  )

        vchem_YMDB = tk.IntVar()

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Molecular",
            variable=vchem_YMDB, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Monoisotopic",
            variable=vchem_YMDB, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )

        run_GUI_but = tk.Button(ChemQuery_toplevel,
                text="Run", width = 10,
                command=ChemQuery_YMDB_run_thread).grid(row=1, column=3, pady = 5, padx = 5, sticky = "NW"  )    

    def thread_ChemQuery_toplevel_ymdb():
        thread.start_new_thread(ChemQuery_toplevel_ymdb, ())

    ChemQuery_GUI_but = tk.Button(gui_ymdb,
                text="Search by MW", width = 20,
                command=thread_ChemQuery_toplevel_ymdb).grid(column= 1, row = 0, pady = 10, padx = 10 )    

    ####################################################
    #### text search
    def search_toplevel_ymdb():
        search_toplevel = tk.Toplevel(root)
        search_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        search_toplevel.title("YMDBconnector")
        global text_query
        tk.Label(search_toplevel, text="Enter a search query").grid(row=0, column = 0)
        text_query = ScrolledText(search_toplevel, width = 60, height= 2)
        text_query.grid(row=0, column=1, pady = 10, padx = 10 )

        #text.get("1.0", "end-1c") 

        run_GUI_but = tk.Button(search_toplevel,
                    text="Run", width = 10,
                    command=SearchUsingQuery_YMDB_thread).grid(row=2, column=1 , pady = 10, padx = 10 )  
        
    def thread_search_toplevel_ymdb():
        thread.start_new_thread(search_toplevel_ymdb, ())

    search_GUI_but = tk.Button(gui_ymdb,
                text="Searching by query", width = 20,
                command=thread_search_toplevel_ymdb).grid(column= 1, row = 1, pady = 10, padx = 10 )

    #####################################################
    ##### GUI for LCMS function
    def LCMS_toplevel_ymdb():
        LCMS_toplevel = tk.Toplevel(root) 
        LCMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMS_toplevel.title("YMDBconnector")
        global text_lcms1
        global text_lcms2
        global text_lcms3
        global vlcms
        global vlcms1
        tk.Label(LCMS_toplevel, text="Masses").grid(row=0, column = 0)
        text_lcms1 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms1.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMS_toplevel, text="Adducts").grid(row=0, column = 2)
        text_lcms2 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms2.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(LCMS_toplevel, text="Tolerance ±").grid(row=2, column = 0)
        text_lcms3 = Text(LCMS_toplevel, width = 8, height= 1)
        text_lcms3.grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        vlcms= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Positive",
            variable=vlcms, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Negative",
            variable=vlcms, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Neutral",
            variable=vlcms, 
            value=3).grid(row=1, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcms1= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Da",
            variable=vlcms1, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        
        tk.Radiobutton(LCMS_toplevel, 
            text="ppm",
            variable=vlcms1, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMS_toplevel,
                text="Run", width = 10,
                command=LCMS_run_YMDB_thread).grid(column= 3, row = 3, pady = 10, padx = 10 )   

    def thread_LCMS_toplevel_ymdb():
        thread.start_new_thread(LCMS_toplevel_ymdb, ())


    LCMS_GUI_but = tk.Button(gui_ymdb,
                text="MSS", width = 20,
                command=thread_LCMS_toplevel_ymdb).grid(column= 2, row = 0, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for LCMSMS function

    def LCMSMS_toplevel_ymdb():
        LCMSMS_toplevel = tk.Toplevel(root) 
        LCMSMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMSMS_toplevel.title("YMDBconnector")
        global text1_msms
        global text2_msms
        global text3_msms
        global text4_msms
        global vlcmsms1
        global vlcmsms2
        global vlcmsms3
        global vlcmsms4
        global vlcmsms5
        tk.Label(LCMSMS_toplevel, text="Peaks").grid(row=0, column = 0)
        text1_msms = ScrolledText(LCMSMS_toplevel, width = 25, height= 12)
        text1_msms.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass (Da)").grid(row=1, column = 0)
        text2_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text2_msms.grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass Tolerance ±").grid(row=1, column = 2)
        text3_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text3_msms.grid(row=1, column=3, pady = 5, padx = 5, sticky = "NW"  )  


        tk.Label(LCMSMS_toplevel, text="Mass/Charge (m/z) Tolerance ±").grid(row=2, column = 2)
        text4_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text4_msms.grid(row=2, column=3, pady = 5, padx = 5, sticky = "NW"  ) 


        vlcmsms1= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Positive",
            variable=vlcmsms1, 
            value=1).grid(row=2, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Negative",
            variable=vlcmsms1, 
            value=2).grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms2= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Parent ion mass Da tolerance units",
            variable=vlcmsms2, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="parent ion mass ppm tolerance units",
            variable=vlcmsms2, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        vlcmsms3= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID low",
            variable=vlcmsms3, 
            value=1).grid(row=4, column=0, pady = 5, padx = 5, sticky = "NW"  )
        
        
        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID med",
            variable=vlcmsms3, 
            value=2).grid(row=4, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID high",
            variable=vlcmsms3, 
            value=3).grid(row=4, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms4= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit Da",
            variable=vlcmsms4, 
            value=1).grid(row=5, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit ppm",
            variable=vlcmsms4, 
            value=2).grid(row=5, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms5 = IntVar()
        Checkbutton(LCMSMS_toplevel, text="Include predicted spectra", variable=vlcmsms5).grid(row=6, column=0, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMSMS_toplevel,
                text="Run", width = 10,
                command=LCMSMS_run_YMDB_thread).grid(column= 3, row = 6, pady = 10, padx = 10 )


    def thread_LCMSMS_toplevel_ymdb():
        thread.start_new_thread(LCMSMS_toplevel_ymdb, ())


    ChemQuery_GUI_but = tk.Button(gui_ymdb,
                text="TMSS", width = 20,
                command=thread_LCMSMS_toplevel_ymdb).grid(column= 2, row = 1, pady = 10, padx = 10 )    




























































########################### 4- T3DB_GUI
###################

def GUI_T3DB():
    gui_t3db = tk.Toplevel(root)
    gui_t3db.iconbitmap(f"{pathh}logo.v1.ico")
    gui_t3db.title("T3DBconnector")
    global labelVar
    global mpb_all_t3db
    labelVar = StringVar()
    label = Label(gui_t3db, textvariable=labelVar).grid(row=2, column = 1, pady = 10, padx = 5 ,sticky=SE)

    # loading bar
    mpb_all_t3db = ttk.Progressbar(gui_t3db,orient ="horizontal",length = 200, mode ="determinate")
    mpb_all_t3db.grid(row=2, column = 2, pady = 10, padx = 5 ,sticky=SE)
    mpb_all_t3db["maximum"] = 100

    ####################################################
    ### plots
    def visualize_toplevel_t3db():

        visualize_toplevel = tk.Toplevel(root)
        visualize_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        visualize_toplevel.title("T3DBconnector")
        global style_
        global transparent_
        global dpi_
        global color_
        #paramter

        tk.Label(visualize_toplevel, text="Style ").grid(row=0, column = 0,pady = 4, padx = 0, sticky=SE)
        style_ = Text(visualize_toplevel, width = 20, height= 1)
        style_.grid(row=0, column=1, pady = 4, padx = 0, sticky=SE )

        transparent_ = IntVar()
        Checkbutton(visualize_toplevel, text="Transparent", variable=transparent_).grid(row=1, column = 2,  pady = 4 , sticky=SE)

        tk.Label(visualize_toplevel, text="dpi ").grid(row=1, column = 0, sticky=SE)
        dpi_ = Text(visualize_toplevel, width = 20, height= 1)
        dpi_.grid(row=1, column=1, pady = 4, padx = 0 , sticky=SE)

        tk.Label(visualize_toplevel, text="Color ").grid(row=2, column = 0, sticky=SE)
        color_ = Text(visualize_toplevel, width = 20, height= 1)
        color_.grid(row=2, column=1, pady = 4, padx = 0 , sticky=SE)

        style_.insert(INSERT, "seaborn-pastel")
        dpi_.insert(INSERT, "600")
        color_.insert(INSERT, "blue")

        run_visualize = tk.Button(visualize_toplevel,
            text="Run", width = 10,
            command=T3DB_plots_thread).grid(column= 3, row = 2, pady = 0, padx = 0,  sticky=SW ) 

        import_file = tk.Button(visualize_toplevel,
            text="Import IDs", width = 10,
            command=import_file_csv_T3DB).grid(column= 3, row = 0, pady = 0, padx = 0,  sticky=SW ) 

    def thread_visualize_toplevel_ymdb():
        thread.start_new_thread(visualize_toplevel_t3db, ())

    visualize = tk.Button(gui_t3db,
                text="Visualize", width = 20,
                command=thread_visualize_toplevel_ymdb).grid(column= 0, row = 1, pady = 10, padx = 10 ) 


    #####################################################
    ##### GUI for accessions functions

    accessions_GUI_but = tk.Button(gui_t3db,
                text="Search using IDs", width = 20,
                command=SearchUsingID_T3DB_thread).grid(column= 0, row = 0, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for Search function

    def search_toplevel_t3db():
        search_toplevel = tk.Toplevel(root)
        search_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        search_toplevel.title("T3DBconnector")
        global text_query
        tk.Label(search_toplevel, text="Enter a search query").grid(row=0, column = 0)
        text_query = ScrolledText(search_toplevel, width = 60, height= 3)
        text_query.grid(row=0, column=1, pady = 10, padx = 10 )

        #text.get("1.0", "end-1c") 

        run_GUI_but = tk.Button(search_toplevel,
                text="Run", width = 10,
                command=SearchUsingQuery_T3DB_thread).grid(row=3, column=1 , pady = 10, padx = 10 )  
       
    def thread_search_toplevel_t3db():
        thread.start_new_thread(search_toplevel_t3db, ())

    search_GUI_but = tk.Button(gui_t3db,
                text="Searching by query", width = 20,
                command=thread_search_toplevel_t3db).grid(column= 1, row = 1, pady = 10, padx = 10 )   

    #####################################################
    ##### GUI for ChemQuery functions

    def ChemQuery_toplevel_t3db():
        ChemQuery_toplevel = tk.Toplevel(root) 
        ChemQuery_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        ChemQuery_toplevel.title("T3DBconnector")
        global text1chm
        global text2chm
        global vchem_T3DB

        tk.Label(ChemQuery_toplevel, text="Start from").grid(row=0, column = 0)
        text1chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text1chm.grid(row=0, column=1,pady = 5, padx = 5, sticky = "NW"  )

        tk.Label(ChemQuery_toplevel, text="End at   ").grid(row=0, column = 2)
        text2chm = Text(ChemQuery_toplevel, width = 8, height= 1)
        text2chm.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  )

        vchem_T3DB = tk.IntVar()

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Molecular",
            variable=vchem_T3DB, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(ChemQuery_toplevel, 
            text="Monoisotopic",
            variable=vchem_T3DB, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )

        run_GUI_but = tk.Button(ChemQuery_toplevel,
                text="Run", width = 10,
                command=ChemQuery_T3DB_run_thread).grid(row=1, column=3, pady = 5, padx = 5, sticky = "NW"  )    

    def thread_ChemQuery_toplevel_t3db():
        thread.start_new_thread(ChemQuery_toplevel_t3db, ())

    ChemQuery_GUI_but = tk.Button(gui_t3db,
                text="Search by MW", width = 20,
                command=thread_ChemQuery_toplevel_t3db).grid(column= 1, row = 0, pady = 10, padx = 10 )    


    #####################################################
    ##### GUI for LCMS function
    def LCMS_toplevel_t3db():
        LCMS_toplevel = tk.Toplevel(root) 
        LCMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMS_toplevel.title("T3DBconnector")
        global text_lcms1
        global text_lcms2
        global text_lcms3
        global vlcms
        global vlcms1

        tk.Label(LCMS_toplevel, text="Masses").grid(row=0, column = 0)
        text_lcms1 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms1.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMS_toplevel, text="Adducts").grid(row=0, column = 2)
        text_lcms2 = ScrolledText(LCMS_toplevel, width = 10, height= 12)
        text_lcms2.grid(row=0, column=3, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(LCMS_toplevel, text="Tolerance ±").grid(row=2, column = 0)
        text_lcms3 = Text(LCMS_toplevel, width = 8, height= 1)
        text_lcms3.grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        vlcms= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Positive",
            variable=vlcms, 
            value=1).grid(row=1, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Negative",
            variable=vlcms, 
            value=2).grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMS_toplevel, 
            text="Neutral",
            variable=vlcms, 
            value=3).grid(row=1, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcms1= tk.IntVar()

        tk.Radiobutton(LCMS_toplevel, 
            text="Da",
            variable=vlcms1, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        
        tk.Radiobutton(LCMS_toplevel, 
            text="ppm",
            variable=vlcms1, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMS_toplevel,
                text="Run", width = 10,
                command=LCMS_run_T3DB_thread).grid(column= 3, row = 3, pady = 10, padx = 10 )   

    def thread_LCMS_toplevel_t3db():
        thread.start_new_thread(LCMS_toplevel_t3db, ())


    LCMS_GUI_but = tk.Button(gui_t3db,
                text="MSS", width = 20,
                command=thread_LCMS_toplevel_t3db).grid(column= 2, row = 0, pady = 10, padx = 10 )    

    #####################################################
    ##### GUI for LCMSMS function

    def LCMSMS_toplevel_t3db():
        LCMSMS_toplevel = tk.Toplevel(root) 
        LCMSMS_toplevel.iconbitmap(f"{pathh}logo.v1.ico")
        LCMSMS_toplevel.title("T3DBconnector")
        global text1_msms
        global text2_msms
        global text3_msms
        global text4_msms
        global vlcmsms1
        global vlcmsms2
        global vlcmsms3
        global vlcmsms4
        global vlcmsms5

        tk.Label(LCMSMS_toplevel, text="Peaks").grid(row=0, column = 0)
        text1_msms = ScrolledText(LCMSMS_toplevel, width = 25, height= 12)
        text1_msms.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass (Da)").grid(row=1, column = 0)
        text2_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text2_msms.grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Parent Ion Mass Tolerance ±").grid(row=1, column = 2)
        text3_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text3_msms.grid(row=1, column=3, pady = 5, padx = 5, sticky = "NW"  )  

        tk.Label(LCMSMS_toplevel, text="Mass/Charge (m/z) Tolerance ±").grid(row=2, column = 2)
        text4_msms = Text(LCMSMS_toplevel, width = 8, height= 1)
        text4_msms.grid(row=2, column=3, pady = 5, padx = 5, sticky = "NW"  ) 


        vlcmsms1= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Positive",
            variable=vlcmsms1, 
            value=1).grid(row=2, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Negative",
            variable=vlcmsms1, 
            value=2).grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms2= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Parent ion mass Da tolerance units",
            variable=vlcmsms2, 
            value=1).grid(row=3, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="parent ion mass ppm tolerance units",
            variable=vlcmsms2, 
            value=2).grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  )


        vlcmsms3= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID low",
            variable=vlcmsms3, 
            value=1).grid(row=4, column=0, pady = 5, padx = 5, sticky = "NW"  )
        
        
        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID med",
            variable=vlcmsms3, 
            value=2).grid(row=4, column=1, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="CID high",
            variable=vlcmsms3, 
            value=3).grid(row=4, column=2, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms4= tk.IntVar()

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit Da",
            variable=vlcmsms4, 
            value=1).grid(row=5, column=0, pady = 5, padx = 5, sticky = "NW"  )

        tk.Radiobutton(LCMSMS_toplevel, 
            text="Mass/Charge (m/z) Tolerance unit ppm",
            variable=vlcmsms4, 
            value=2).grid(row=5, column=1, pady = 5, padx = 5, sticky = "NW"  )

        vlcmsms5 = IntVar()
        Checkbutton(LCMSMS_toplevel, text="Include predicted spectra", variable=vlcmsms5).grid(row=6, column=0, pady = 5, padx = 5, sticky = "NW"  )


        run_GUI_but = tk.Button(LCMSMS_toplevel,
                text="Run", width = 10,
                command=LCMSMS_run_T3DB_thread).grid(column= 3, row = 6, pady = 10, padx = 10 )


    def thread_LCMSMS_toplevel_t3db():
        thread.start_new_thread(LCMSMS_toplevel_t3db, ())


    LCMSMS_GUI_but = tk.Button(gui_t3db,
                text="TMSS", width = 20,
                command=thread_LCMSMS_toplevel_t3db).grid(column= 2, row = 1, pady = 10, padx = 10 )    


    ######################################################
    ############## KEGG
    accessions_GUI_Kegg = tk.Button(gui_t3db,
                text="KEGG pathways", width = 20,
                command=Kegg_pathways_T3DB_thread).grid(column= 0, row = 2, pady = 10, padx = 10 ) 



































########################### 5- Res_GUI
###################
def GUI_Res():
    gui_res = tk.Toplevel(root)
    gui_res.iconbitmap(f"{pathh}logo.v1.ico")
    gui_res.title("ResDBconnector")
    global labelVar
    global mpb_all_respectDB
    labelVar = StringVar()
    label = Label(gui_res, textvariable=labelVar).grid(row=2, column = 1, pady = 10, padx = 5 ,sticky=SE)

    # loading bar
    mpb_all_respectDB = ttk.Progressbar(gui_res,orient ="horizontal",length = 200, mode ="determinate")
    mpb_all_respectDB.grid(row=2, column = 2, pady = 10, padx = 5 ,sticky=SE)
    mpb_all_respectDB["maximum"] = 100
    #####################################################
    ##### GUI for accessions functions


    accessions_GUI_but = tk.Button(gui_res,
                text="Search using IDs", width = 20,
                command=SearchUsingID_respectDB_thread).grid(column= 0, row = 0, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for draw peaks functions

    draw_GUI_but = tk.Button(gui_res,
                text="Draw peaks", width = 20,
                command=Draw_peak_respectDB_thread).grid(column= 2, row = 0, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for draw peaks functions

    def Keyword_toplevel_res():
        gui__res_Keyword = tk.Toplevel(root)
        gui__res_Keyword.iconbitmap(f"{pathh}logo.v1.ico")
        gui__res_Keyword.title("ResDBconnector")
        global text1_res
        global text2_res
        global text3_res
        global text4_res

        tk.Label(gui__res_Keyword, text="Compound name").grid(row=0, column = 0, sticky = "NW")
        text1_res = Text(gui__res_Keyword, width = 60, height= 1.2)
        text1_res.grid(row=0, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(gui__res_Keyword, text="Compound formula").grid(row=1, column = 0, sticky = "NW")
        text2_res = Text(gui__res_Keyword, width = 60, height= 1.2)
        text2_res.grid(row=1, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(gui__res_Keyword, text="Compound exact mass").grid(row=2, column = 0, sticky = "NW")
        text3_res = Text(gui__res_Keyword, width = 60, height= 1.2)
        text3_res.grid(row=2, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        tk.Label(gui__res_Keyword, text="Compound tolerance").grid(row=3, column = 0, sticky = "NW")
        text4_res = Text(gui__res_Keyword, width = 60, height= 1.2)
        text4_res.grid(row=3, column=1, pady = 5, padx = 5, sticky = "NW"  ) 

        search_GUI_but = tk.Button(gui__res_Keyword,
                text="Search", width = 10,
                command=Search_keyword_respectDB_thread).grid(row=4, column=3, pady = 5, padx = 5, sticky = "NW"  ) 

    def thread_Keyword_toplevel_res():
        thread.start_new_thread(Keyword_toplevel_res, ())

    Keyword_GUI_but = tk.Button(gui_res,
                text="Searching by Keywords", width = 20,
                command=thread_Keyword_toplevel_res).grid(column= 1, row = 0, pady = 10, padx = 10 ) 

    #####################################################
    ##### GUI for KEgg function

    accessions_GUI_Kegg = tk.Button(gui_res,
                text="KEGG pathways", width = 20,
                command=Kegg_pathway_resDB_thread).grid(column= 0, row = 1, pady = 10, padx = 10 ) 






#**********************************
### Thread and functions for GUI
#**********************************


def thread_hmdb():
    thread.start_new_thread(GUI_HMDB , ())

def thread_lmdb():
    thread.start_new_thread(GUI_LMDB , ())

def thread_ymdb():
    thread.start_new_thread(GUI_YMDB , ())

def thread_t3db():
    thread.start_new_thread(GUI_T3DB , ())

def thread_res():
    thread.start_new_thread(GUI_Res , ())

def thread_all():
    thread.start_new_thread(GUI_ALL , ())

































################################
### Main GUI
################################

root = tk.Tk()
root.title("Xconnector (V: 1.0.0)")
root.resizable(False, False)
root.geometry("1000x600")
root.iconbitmap(f'{pathh}logo.v1.ico')


##############################
#### menu


def OpenFile():
    name = askopenfilename()
def About():
    url_to_open = "https://github.com/Proteomicslab57357/Xconnector"
    webbrowser.open(url_to_open)

def Documentation():
    os.startfile("Documentation.pdf")


menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Save Result In...", command=save_result_in_function)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
helpmenu.add_separator()
helpmenu.add_command(label="Documentation", command= Documentation)


##############################
#### database Button

photo1 = PhotoImage(file = f"{pathh}\logo\\HMDB.png") 

HMDB = tk.Button(root,
                text="",
                command=thread_hmdb, 
                image = photo1,
                bd=0,
                ).place(x=100, y=0)

photo2 = PhotoImage(file = f"{pathh}\logo\\LMDB.png") 

LMDB = tk.Button(root,
                text="",
                command=thread_lmdb, 
                image = photo2,
                bd=0,
                ).place(x=700, y=0)  


photo3 = PhotoImage(file = f"{pathh}\logo\\YMDB.png") 

YMDB = tk.Button(root,
                text="",
                command=thread_ymdb, 
                image = photo3,
                bd=0,
                ).place(x=100, y=200)

photo4 = PhotoImage(file = f"{pathh}\logo\\T3DB.png") 

T3DB = tk.Button(root,
                text="",
                command=thread_t3db, 
                image = photo4,
                bd=0,
                ).place(x=700, y=200)           

photo5 = PhotoImage(file = f"{pathh}\logo\\ReSpect.png") 

T3DB = tk.Button(root,
                text="",
                command=thread_res, 
                image = photo5,
                bd=0,
                ).place(x=390, y=300)       

photo6 = PhotoImage(file = f"{pathh}\logo\logo.v1.png") 

All = tk.Button(root,
                text="",
                command=thread_all, 
                image = photo6,
                bd=0,
                ).place(x=390, y=80) 
##############################
##### main logos

#main_logo = PhotoImage(file = f"{pathh}\logo\logo.v1.png") 
#imglabel = Label(root, image=main_logo, bd=0).place(x=390, y=80)


##############################
##### logos
tk.Label(root, text="Powered and supported by:").place(x=10, y=470)

photo11 = PhotoImage(file = f"{pathh}\logo\\IM1.png") 
photo12 = PhotoImage(file = f"{pathh}\logo\\IM2.png") 
photo13 = PhotoImage(file = f"{pathh}\logo\\IM4.png") 
photo14 = PhotoImage(file = f"{pathh}\logo\\IM3.png") 


imglabel = Label(root, image=photo11).place(x=150, y=500)
imglabel = Label(root, image=photo12).place(x=400, y=510)
imglabel = Label(root, image=photo13).place(x=600, y=510)
imglabel = Label(root, image=photo14).place(x=760, y=510)

root.mainloop()
