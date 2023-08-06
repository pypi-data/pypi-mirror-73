import pandas as pd 
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

################# bar plot


def all_plot( plot_data_dict, title, x_name , font_font = 14 , y_name = "Count", y_label = "" ,x_label = "" ,  color='blue', dpi=600 , transparent = False, style = "seaborn-pastel", legend=False, rot = 0 , save = False, where_to_save = "fig.png", W_and_H = (14,14) , kind= "bar", ha="center", va = "bottom", fontsize_text = 12, scales = "on"):
    """
    plot_data_dict = dict from the function genrates data to be ploted
    """
    fig, ax = plt.subplots()

    y_ax = plot_data_dict

    df_y = pd.DataFrame( {x_name: list(y_ax.keys()) ,  y_name: list(y_ax.values()) } )
    plt.style.use(style)

    df_y.plot(kind = kind , x = x_name, y = y_name,
                         rot = rot , legend = legend , fontsize = font_font,
                         ylim = (0, max(y_ax.values())+3) , color = color)

    plt.title(title , fontsize = font_font)

    if y_label != "":
        plt.ylabel(y_label , fontsize = font_font)
    else:
        plt.ylabel(y_name , fontsize = 14)

    if x_label != "":
        plt.xlabel(x_label , fontsize = font_font )
    else:
        plt.xlabel(x_name , fontsize = 14)
    
    
    for x, y in enumerate(y_ax.values()):
        if kind == "bar":
            if y != 0:
                text_write = float(y/sum( y_ax.values() ) *100)
                text_write = round(text_write,3)
                plt.text(x, y , s = str( text_write) + "%" , color='black', rotation=0, fontsize= fontsize_text, ha = ha, va= va)
        
            else:
                pass

            if scales == "on_x":
                if max ( list( y_ax.values() ) ) < 40:
                    plt.xticks( range (max ( list( y_ax.values() ) ) + 3   ) )
                
                else:
                    pass

            elif scales == "on_y":
                if max ( list( y_ax.values() ) ) < 40:
                    plt.yticks( range(max( list( y_ax.values() ) ) + 3  ) )
                else:
                    pass
                    
            else:
                pass
        elif kind == "barh":

            if y != 0:
                text_write = float(y/sum( y_ax.values() ) *100)
                text_write = round(text_write,3)
                plt.text(y , x , s = str( text_write) + "%" , color='black', rotation=0, fontsize= fontsize_text, va= "center")
                
            else:
                pass            
    
            if scales == "on_x":
                if max ( list( y_ax.values() ) ) < 40:
                    plt.xticks( range (max ( list( y_ax.values() ) ) + 3   ) )
                else:
                    pass

            elif scales == "on_y":
                if max ( list( y_ax.values() ) ) < 40:
                    plt.yticks( range(max( list( y_ax.values() ) ) + 3  ) )
                else:
                    pass
    

    plt.tick_params(axis="x", labelsize=font_font)
    plt.tick_params(axis="y", labelsize=font_font)

    plt.autoscale()
    if save and save == True:
        fig = plt.gcf()
        fig.set_size_inches(W_and_H, forward=False)
        plt.savefig(where_to_save, dpi= dpi , transparent = transparent)
    else:
        pass

    return plt


def bibarplot(x_num , y_num ,IDs_label , x_label , title ,fontsize_text = 8 ,fontsizey_label = 20 ,styles = "seaborn-pastel" , dpi = 600 , transparent = False, save= False, W_and_H = (20,13) , where_to_save = "fig.png" ):
    
    plt.style.use(styles)
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(1,1,1)
    ax.bar(x_num , y_num)
    plt.ylabel("pKa",fontsize =fontsizey_label)
    plt.xlim(0.5, max(x_num) + 1)
    plt.title(title, fontsize = 15, pad  = 0.9)
    #plt.xticks( range (max ( x_num ) + 1 ) )
    fig.text(0.48, 0.04, x_label, va='center', rotation=0 , fontsize = 15 )

    for x_index, y_value, z_label in zip(x_num, y_num, IDs_label) :
        

        if y_value >= 0:
            y_value_ = y_value + 0.1
            plt.text(x_index , y_value_ , s = str(z_label) , color='black', rotation=90, fontsize= "small", va= "bottom" , ha = "center")

        elif y_value < 0:
            y_value_ = y_value - 0.1
            plt.text(x_index , y_value_ , s = str(z_label) , color='black', rotation=90, fontsize= "small", va= "top",  ha = "center")

        

    ax.tick_params(axis="x", labelsize=15)
    ax.tick_params(axis="y", labelsize=20)

    ax.grid(b=False)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

    if len(x_num) <= 40:
        month = [""]
        month = month + [ str(i)  for i in range (1 , max ( x_num ) + 1 ) ]
        ax.set_xticks(range (max ( x_num ) + 1 ))  # ticks placed on [0, 1, ..., 11]
        ax.set_xticklabels(month)
    else:
        ax.xaxis.set_tick_params(labelsize="small")
        pass

    if save and save == True:
        fig = plt.gcf()
        fig.set_size_inches(W_and_H, forward=False)
        plt.savefig(where_to_save, dpi= dpi , transparent = transparent)
    else:
        pass

    return plt


def new_bibarplot(x_num , y_num ,IDs_label , x_label , title ,fontsize_text = 8 ,fontsizey_label = 20 ,styles = "seaborn-pastel" , dpi = 600 , transparent = False, save= False, W_and_H = (20,15) , where_to_save = "fig.png" ):

    plt.style.use(styles)
    fig, ax = plt.subplots()

    plt.bar(x = x_num, height  = y_num , width= 0.4 )

    plt.ylabel("pKa",fontsize =fontsizey_label , labelpad = 10)
    plt.xlabel(x_label, fontsize =fontsizey_label , labelpad = 10 )
    plt.title(title, fontsize = 17, pad  = 10)

    bottom, top = min(y_num) , max(y_num)

    if bottom < 0:
        plt.ylim(bottom - 4  , top + 4 )
    elif bottom > 0 :
        plt.ylim(0 , top + 4 )
    elif bottom == 0 :
        plt.ylim(0 , top + 4 )
    
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    yticks[-1].label1.set_visible(False)

    #plt.xticks(x_num, list(bars_num))
    #bars_num = range(1, max(x_num) + 1 )
    plt.xlim(0,max(x_num)+1)
    xticks = ax.xaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)
    xticks[-1].label1.set_visible(False)
    plt.locator_params(axis="x", integer=True)

    #plt.margins(2)


    if len(x_num) <= 30:
        size_size = "large"
    else:
        size_size = "small"
    for x_index, y_value, z_label in zip(x_num, y_num, IDs_label) :

        if y_value >= 0:
            y_value_ = y_value + 0.08

            plt.text(x_index , y_value_ ,in_layout = True, s = str(z_label) , color='black', rotation=90, fontsize= size_size, va= "bottom" , ha = "center")

        elif y_value < 0:
            y_value_ = y_value - 0.08
            plt.text(x_index , y_value_ ,in_layout = True, s = str(z_label) , color='black', rotation=90, fontsize= size_size, va= "top",  ha = "center")



    #if len(x_num) <= 40:
    #    ax.set_xticks(range (max ( x_num ) + 1 ))  # ticks placed on [0, 1, ..., 11]
    #else:
    #    pass

    if min(y_num) < 0: 
        ax.axhline(0, color='k')
    else:
        pass

    if len(x_num) <= 10:
        ax.tick_params(labelsize = "x-large")
    elif len(x_num) <= 30:
        ax.tick_params(labelsize = "large")
    else:
        ax.tick_params(labelsize = "medium")
    #plt.autoscale()
    if save and save == True:
        fig = plt.gcf()
        fig.set_size_inches(W_and_H, forward=False)
        plt.savefig(where_to_save, dpi= dpi , transparent = transparent)
    else:
        pass

    return plt

def lollplot(plot_data_dict, title ,xlabel , ylabel, where_to_save = "fig.png", style = "seaborn-pastel", color_plot = "skyblue", markersize_ = 4 ,fontsize_ = 15 , legend_label = "", save = False, transparent = False, dpi = 600  ,W_and_H = (13,11)  ):

    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib.patches as mpatches

    for i_remove , _ikey in zip ( list(plot_data_dict.values()) , list(plot_data_dict.keys()) ):
        if i_remove <= 0.0009:
            del plot_data_dict[_ikey]
	#data
    df_data = pd.DataFrame( data = { "IDs" : list(plot_data_dict.keys()),  "values": list(plot_data_dict.values()) } )

    ordered_df = df_data.sort_values(by='values').reset_index(drop=True)

    my_range = range(1, len(df_data.index) + 1)

    plt.style.use(style)

    f, (ax, ax2 , ax3, ax4, ax5 , ax6) = plt.subplots(1,6, sharex=False , sharey = True)


    # plot the same data on both axes

    ax.hlines(y=my_range, xmin=0, xmax=ordered_df['values'],
           color= color_plot)
    ax2.hlines(y=my_range, xmin=0, xmax=ordered_df['values'],
        color= color_plot)
    ax3.hlines(y=my_range, xmin=0, xmax=ordered_df['values'],
        color= color_plot)
    ax4.hlines(y=my_range, xmin=0, xmax=ordered_df['values'],
        color= color_plot)
    ax5.hlines(y=my_range, xmin=0, xmax=ordered_df['values'],
        color= color_plot)
    ax6.hlines(y=my_range, xmin=0, xmax=ordered_df['values'],
        color= color_plot)

    if len (df_data.index) > 30:
        markersize_ = 3
    for i_x , i_y in zip(ordered_df['values'],my_range) :

        if 0 <= i_x <= 0.09:

            ax.plot(i_x, i_y, 'o', markersize = markersize_ , color = "black" )

        elif 0.1 <= i_x <= 1:
            ax2.plot(i_x, i_y, 'o', markersize = markersize_ , color = "black" )

        elif 1.1 <= i_x <= 10:
            ax3.plot(i_x, i_y, 'o', markersize = markersize_ , color = "black" )

        elif 10.1 <= i_x <= 33:
            ax4.plot(i_x, i_y, 'o', markersize = markersize_ , color = "black" )

        elif 33.1 <= i_x <= 100:
            ax5.plot(i_x, i_y, 'o', markersize = markersize_ , color = "black" )

        elif 100.1 <= i_x <= 1000:
             ax6.plot(i_x, i_y, 'o', markersize = markersize_ , color = "black" )
                                    
	
	
    if len (df_data.index + 1) <= 15:
        plt.yticks(ordered_df.index+1, ordered_df['IDs']  , va = "center" )
        ax.tick_params(axis = 'y', which = 'major', labelsize = "large")

    elif  15 < len (df_data.index + 1) <= 40:
        plt.yticks(ordered_df.index+1, ordered_df['IDs']  , va = "center" )
        ax.tick_params(axis = 'y', which = 'major', labelsize = "medium")

    else:
        plt.yticks(ordered_df.index+1, ordered_df['IDs']  , va = "center")
        ax.tick_params(axis = 'y', which = 'major', labelsize = 4 )



    #plt.title(title)
    f.text(0.5, 0.015, xlabel, ha='center', va='center', fontsize = fontsize_)
    f.text(0.5, 0.04, ylabel, ha='center', va='center' , fontsize = fontsize_)
    f.suptitle(title, fontsize=fontsize_)


    f.text(0.128, 0.038, "Partially insoluble", va='center', fontsize = 11)
    f.text(0.26, 0.038, "Very slightly Soluble", va='center', fontsize = 11)
    f.text(0.44, 0.038, "Slightly Soluble", ha='center', va='center', fontsize = 11)
    f.text(0.573, 0.038, "Sparingly Soluble", ha='center', va='center', fontsize = 11)
    f.text(0.71, 0.038, "Soluble", ha='center', va='center', fontsize = 11)
    f.text(0.845, 0.038, "Freely Soluble", ha='center', va='center', fontsize = 11)



    patch = mpatches.Patch(color=color_plot, label= legend_label)
    plt.legend(handles=[patch])

    # zoom-in / limit the view to different portions of the data"""
    ax6.set_xlim(100.05, 1500) 
    ax5.set_xlim(32.8, 106.5)  
    ax4.set_xlim(9.8, 34.5)
    ax3.set_xlim(1.01, 12)
    ax2.set_xlim(0.091, 1.2)
    ax.set_xlim(0, 0.13)


    # hide the spines between ax , ax2, ....
    ax6.spines["left"].set_visible(False)

    ax5.spines['right'].set_visible(False)
    ax5.spines['left'].set_visible(False)

    ax4.spines['right'].set_visible(False)
    ax4.spines['left'].set_visible(False)

    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_visible(False)

    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)

    ax.spines['right'].set_visible(False)

    # to remove the tick line

    ax.tick_params("y",which='major', length=0) 
    ax2.tick_params("y",which='major', length=0) 
    ax3.tick_params("y",which='major', length=0) 
    ax4.tick_params("y",which='major', length=0) 
    ax5.tick_params("y",which='major', length=0) 
    ax6.tick_params("y",which='major', length=0) 



    ax6.xaxis.set_ticks([100.1,500,1000,1500])
    ax5.xaxis.set_ticks([33.1,66.5,100])
    ax4.xaxis.set_ticks([10.1,21.5,33])
    ax3.xaxis.set_ticks([1.1,5.5,10])
    ax2.xaxis.set_ticks([0.1,0.5,1])
    ax.xaxis.set_ticks([0,0.045,0.09])



    f.subplots_adjust(wspace=0.1)
    ax.tick_params("x",labelrotation=90)
    ax2.tick_params("x",labelrotation=90)
    ax3.tick_params("x",labelrotation=90)
    ax4.tick_params("x",labelrotation=90)
    ax5.tick_params("x",labelrotation=90)
    ax6.tick_params("x",labelrotation=90)


    if save and save == True:
        fig = plt.gcf()
        if len(df_data.index + 1) <= 30:
            W_and_H = (13,16)
        else:
            pass
        fig.set_size_inches(W_and_H, forward=False)
        plt.savefig(where_to_save, dpi= dpi , transparent = transparent)
    else:
        pass

    return plt