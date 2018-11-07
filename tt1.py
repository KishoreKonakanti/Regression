# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 17:05:32 2018

@author: kkonakan
"""

# Atleast 2 letters can be surrounded by digits



def plot():
    country_list = list(gh.Country)
    total = list(gh.Total)
    r = np.arange(53)
    import matplotlib.pyplot as plt
    fig,ax = plt.subplots()
    plt.figure(figsize=(14,14))
    plt.xscale('symlog')
    plt.xlabel('Countries')
    plt.ylabel('Number of websites hosted')
    
    sz = list(gh.Total)
    sz = [x*30 for x in sz]
    
    for i,country in enumerate(country_list):
        x_coord = total[i] + xa
        y_coord = r[i] + ya
        fsize = 10 * (total[i]/100)
        if fsize < 10:
            fsize = 10
        print('Fontsizes:', fsize)
        plt.text(x_coord,y_coord,country, fontsize=fsize)
        #ax.annotate(country, [total[i], r[i]])
    #plt.annotate(
    plt.show()