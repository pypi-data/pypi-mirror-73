        # water
        mpb_vis["value"] = 30
        df_water = pandas.DataFrame( {  "Water Solubility": list( water_all.values() ) } , index = list(water_all.keys())  )
        plt.style.use(style)
        df_water.sort_values(by = "Water Solubility" , inplace= True)
        df_water.plot.line(color = color, title = "Predicted Propertie" , fontsize = 8 , marker='o')
        plt.xticks(np.arange(len(df_water)), df_water.index.values , rotation=90 , fontsize=8)
        plt.ylabel("g/L" , fontsize=15)
        fig = plt.gcf()
        fig.set_size_inches((13,11), forward=False)
        plt.savefig(f"{save_result_in_disposition}/Predicted_Propertie(Water_Solubility).png", dpi= dpi , transparent = transparent)
        pyplot.close('all')

        ##################################

        #pka_acid _ line plot
        mpb_vis["value"] = 40
        df_pka = pandas.DataFrame( {  "Strongest Acidic": list( pka_acid_dict.values() ) ,
                                         "Strongest Basic": list( pka_basic_dict.values() ) } 
                                            , index = list(pka_acid_dict.keys())  )
        plt.style.use(style)
        df_pka["Strongest Acidic"].sort_values(ascending=True) .plot.line(color = color , title = "Predicted Propertie", marker='o' , legend=True)
        plt.xticks(np.arange(len(df_pka) ), df_pka.index.values ,  rotation=90 , fontsize=8 )
        fig = plt.gcf()
        fig.text(0.08, 0.55, 'pKa', va='center', rotation='vertical' , fontsize = 13)
        fig.set_size_inches((13,11), forward=False)
        mpb_vis["value"] = 50
        plt.savefig(f"{save_result_in_disposition}/line_StrongestAcidicpKa.png", dpi= dpi , transparent = transparent)
        pyplot.close('all')
        
        #pka_line _basic

        plt.style.use(style)
        #df_pka.sort_values(by = "Strongest Acidic" , inplace= True)
        df_pka["Strongest Basic"].sort_values(ascending=True) .plot.line(color = color ,title = "Predicted Propertie",  marker='o' , legend=True)
        plt.xticks(np.arange(len(df_pka) ), df_pka.index.values , rotation=90 , fontsize=8 )
        fig = plt.gcf()
        fig.text(0.08, 0.55, 'pKa', va='center', rotation='vertical' , fontsize = 13)
        fig.set_size_inches((13,13), forward=False)
        mpb_vis["value"] = 50
        plt.savefig(f"{save_result_in_disposition}/line_StrongestBasicpKa.png", dpi= dpi , transparent = transparent)
        pyplot.close('all')


++++++++++++++++++++++

    for x_index, y_value, z_label in zip(x_num, y_num, IDs_label) :
        

        y_value_ = ( y_value * (2/100) ) + y_value

        if y_value_ >= 0:
            plt.text(x_index , y_value_ , s = str(z_label) , color='black', rotation=90, fontsize= 13, va= "bottom")

        elif y_value_ < 0:
            plt.text(x_index , y_value_ , s = str(z_label) , color='black', rotation=90, fontsize= 13, va= "top")