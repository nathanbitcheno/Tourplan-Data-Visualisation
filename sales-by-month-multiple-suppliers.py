import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import pandas as pd
import csv
import os

#make filename from directory
inpath = "./tourplan-csv/"
outpath = "./plot-output/"
data_file = os.listdir(inpath)
for file in data_file:
    filename = inpath+file

    #read in the csv data
    df = pd.read_csv(filename)

    #set desired dataframe columns    
    #df.index = pd.to_datetime(df['Date']).dt.to_period('M')
    
    df = df[['Date', 'Agent.1', 'Supplier']]
    df.columns = ['Date', 'Sales', 'Supplier']

    #remove , from thousands number string
    df['Sales'] = df['Sales'].str.replace(',', '')
    
    #convert price string to float
    df['Sales'] = pd.to_numeric(df['Sales'], errors = 'raise')
    
    #group the data by the supplier column
    grouped = df.groupby(['Supplier'])
    for supplier in grouped:
        
        #set the dataframe
        df = supplier[1]
        
        #set columns from data
        df = df[['Date', 'Sales', 'Supplier']]

        #assign supplier now to be used later in output (supplier column is lost during 
        # the next groupby sum as it is a string)
        mySupplier = df.iloc[0]['Supplier']
        
        #set the date column to datetime, use period format (yyyy-mm)
        df['Date'] = pd.to_datetime(df['Date']).dt.to_period('M')

        #now group by date (this makes date the index and sums the values in sales)
        df = df.groupby(df['Date']).sum()
        
        #sets the period range (this might need to be dynamic to accept date input from 
        # the user, or I could make a new script for each annual reporting period)
        idx = pd.period_range(start='2018-04-01', end='2019-03-31', freq='M')

        #reindex the dataframe using the period range above and fill in empty cells with 0
        df = df.reindex(idx, fill_value=0)        
        
        #plot using supplier in the title and 14 x 10 inch size
        df.plot.bar(rot=0, title='Monthly Sales for '+ mySupplier, figsize=(14,10), fontsize=12)
        

        #Save the plot figure with the Supplier filename
        plt.savefig(outpath+mySupplier+'_sales.svg', bbox_inches='tight', transparent=False)        
        plt.close()

   
        
    