import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import pandas as pd
import csv
import os
import calendar
from pandas.api.types import CategoricalDtype

#date range used in Tourplan report (update as needed)
startdate = "2016-01-01"
enddate = "2019-12-31"

#make filename from directory
inpath = "./tourplan-csv/"
outpath = "./plot-output/"
data_file = os.listdir(inpath)
for file in data_file:
    filename = inpath+file

    #read in the csv data
    df = pd.read_csv(filename)
    
    #set desired dataframe columns    
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
        idx = pd.period_range(start=startdate, end=enddate, freq='M')
        
        #reindex the dataframe using the period range above and fill in empty cells with 0
        df = df.reindex(idx, fill_value=0)        
        
        #Create multiindex of Month and Year
        gb = df.groupby([(df.index.month),(df.index.year)]).sum()

        #Reset index which turns month/year index into columns
        gb.reset_index(inplace=True)

        #Label Columns
        gb.columns = ['Month', 'Year', 'Sales']

        #Categories for ordering month abbreviation as cats rather than alphabetical
        cats = ['Jan','Feb','Mar','Apr','May','Jun',
        'Jul','Aug','Sep','Oct','Nov','Dec']
        cat_type = CategoricalDtype(categories=cats, ordered=True)
        
        #convert month integer into month abbreviation
        gb['Month'] = gb['Month'].apply(lambda x: calendar.month_abbr[x])

        #apply cat ordering
        gb['Month'] = gb['Month'].astype(cat_type)

        #pivot data to have new index of month, columns of year and value as sales
        gb_pivoted = gb.pivot(index='Month', columns = 'Year', values='Sales')
        
        gb_pivoted[gb_pivoted < 0] = 0

        #plot using supplier in the title and 14 x 10 inch size
        gb_pivoted.plot(kind='bar', rot=0, title='Monthly Sales for '+ mySupplier, figsize=(14,10), fontsize=12, color=['#E9D758', '#38618C', '#4E937A', '#EF3054'])
        plt.xlabel("Date", labelpad=16)
        plt.ylabel("Total Sales (NZD)", labelpad=20)

        #Save the plot figure with the Supplier filename
        mydir = outpath+mySupplier
        if not os.path.exists(mydir):
            os.mkdir(mydir)
        plt.savefig(mydir+'/'+mySupplier+'_yearly_sales_comparison2.svg', bbox_inches='tight', transparent=False)        
        plt.close()


        
    