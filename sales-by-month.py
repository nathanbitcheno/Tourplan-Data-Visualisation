import matplotlib.pyplot as plt
import pandas as pd
import csv
import os

#make filename from directory
inpath = "./tourplan-csv/"
outpath = "./plot-output/"
data_file = os.listdir(inpath)
for file in data_file:
    filename = inpath+file

    #Extract the supplier Code 
    with open(filename) as csvDataFile:
        data = list(csv.reader(csvDataFile))
        supplier = data[1][1]
    
    #read in the csv data
    df = pd.read_csv(filename)

    #convert date to datetime and set date as the index for the dataframe
    df.index = pd.to_datetime(df['Date'])

    #set desired dataframe columns
    df = df[['Agent.1']]
    df.columns = ['Sales']

    #remove , from thousands number string
    df['Sales'] = df['Sales'].str.replace(',', '')

    #convert price string to float
    df['Sales'] = pd.to_numeric(df['Sales'], errors = 'raise')

    #group prices by year and month
    df = df.groupby([(df.index.year),(df.index.month)]).sum()
    print(df)
    #plot using supplier in the title and 14 x 10 inch size
    df.plot.bar(rot=0, title='Monthly Sales for '+ supplier, figsize=(14,10), fontsize=12)

    #Save the plot figure with the Supplier filename
    plt.savefig(outpath+supplier+'_sales.svg', bbox_inches='tight', transparent=False)

    #delete the csv file
    os.remove(filename)

