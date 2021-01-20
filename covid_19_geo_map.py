#!/usr/bin/env python
# coding: utf-8

# # Load EDA (Loading the suitable environment for GeoPandas)


#conda activate geo_env
 #(cenv)$ conda install ipykernel
 #(cenv)$ conda deactivate


# Importing Required Libraries

import pandas as pd 
import geopandas as gpd
import descartes
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# Loading the data from Github Depositoriy and saving it


confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
death_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"



# load Our dataset 
df_confirmed = pd.read_csv(confirmed_url)
df_confirmed.head()

# Exploring the data 


df_confirmed.shape




df_confirmed.columns

# Shaping  and data wrangling 

confirmed_df = df_confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])



confirmed_df.rename(columns={"Variable":"Date","value":"Confirmed"},inplace= True)





confirmed_df.head()





confirmed_df.tail()



# Function to Fetch and reshape
def get_n_melt_data(data_url,case_type):
    df= pd.read_csv(data_url)
    melted_df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
    melted_df.rename(columns={"Variable":"Date","value":case_type},inplace= True)
    return melted_df
    



# fetch Death or Recovered
recovered_df = get_n_melt_data(recovered_url,"Recovered")
death_df = get_n_melt_data(death_url,"Deaths")
recovered_df.head()



print(confirmed_df.shape)
print(recovered_df.shape)
print(death_df.shape)





# joining All 3 datasets
final_df = confirmed_df.join(recovered_df['Recovered']).join(death_df['Deaths'])
final_df.tail(7)





# save Data as csv
final_df.to_csv("Corina_Updates.csv")




gdf01 = gpd.GeoDataFrame(final_df,geometry= gpd.points_from_xy(final_df['Long'],final_df['Lat']))
gdf01.plot(figsize=(20,10))

# visiolazing data on the global map

#overlapping with world map
world= gpd.read_file(gpd.datasets.get_path ('naturalearth_lowres'))
ax= world.plot(figsize=(20,10))
ax.axis('off')




# Overlap with Data
fig,ax= plt.subplots(figsize=(20,10))
gdf01.plot(cmap ='Reds',ax=ax)
world.geometry.boundary.plot(color=None,edgecolor= 'k',linewidth =2,ax=ax)






