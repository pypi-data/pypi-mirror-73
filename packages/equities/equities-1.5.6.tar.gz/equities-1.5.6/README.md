
# 🌟 equities 

## Overview: 

    equities allows for easy access to the SEC's XLBR Financial Statement Dataset
    Parsed data is stored locally and served to the user in pandas dataframes

###### The Dataset: 

https://www.sec.gov/dera/data/financial-statement-data-sets.html

## Install: 

    pip3 install equities

## TUTORIAL: 

The library consists of two central objects, Universe and Company. 

## Universe: 

A Universe should be thought of as a set of Companies. The universe object gives us the ability to download,
access and purge our data. 

    from equities.objects import Universe

    # Instantiation
    universe = Universe()

#### Downloading Data:

On first use the universe is empty. Before calling the download function we can optionally supply the 
universe with an array of quarter strings (and/or) an array of "CIK" or "Central Index Key" integers. A 
"CIK" number is a unique integer of 10 digits assigned to each company by the sec. 

    quarters = ["2016q1,"2017q1","2018q1","2019q1"] # quarters to be downloaded
    ciks = [1556593,1499200,1220754,917520,1040593,24741] # ciks to be parsed

If no optional arguments are supplied to "quarters" and "ciks" we proceed to either download all quarters and  
parse all companies, respectively. Lastly, passing an integer, say "x" in for the "ciks" array will limit 
the parsing of companies to the first "x" number of ciks in the universe.

To download data we call:

    universe.download(quarters=quarters,ciks=ciks)

The requested data will then be downloaded, parsed and saved locally. This means that anytime you reinstantiate 
the universe object, python remembers what you have already parsed. 

A small note on deleting data. To purge the universe and thereby delete all locally saved data, call:

    universe.purge()

#### Core Functionality:

To see the number of companies in the universe we can do: 

    print(len(universe))

Universe objects are indexable by "CIK" integers. To get a full list of the cik numbers in the universe one can do: 

    print(universe.ciks)

A dataframe summary of all companies in the universe is included in:

    print(universe.properties())

To access the first company in the above list you can do: 

    first_cik = universe.ciks[0]
    print(universe[first_cik])

This returns a Company Object.


## Company: 

A Company object should be thought of as an abstract representation of a real company. Every 
company must have an associated Universe of origin. 

    from equities.objects import Company

#### Accessing the Financial Statements

Consider the first Company in our universe, universe[first_cik]. It is a Company object. 

    company = universe[first_cik]

Dataframes of the company's financial statements over the universe in question is given by: 

    company.income()      # income statement dataframe

    company.balance()     # Balancesheet dataframe

    company.cash()        # Cash Flow Statement dataframe

    company.equity()      # Consolidatad Equity dataframe


#### Additional Company Methods

    company.name()        # Returns company name
    company.sic()         # Returns company sic group
    

#### Example 

I really want to demonstrate the beauty of this dataset as that is often difficult when looking
at thousands of numeric datatables. So let's take a very naive peek by plotting various statements 
as a kind of stacked timeseries. 

The following  is a start to finish example of how one might plot the first quarter income statements,
cashflow  statements and balance sheets of some  companies in the universe. We are interested in 
years  2015 to 2019.

To perform this experiment run: 

    universe.test()

Here is the code: 

    # Import modules
    import pandas as pd
    import matplotlib.pyplot as plt
    from equities.objects import Universe, Company

    # Instantiate universe Object
    u = Universe()

    # Download data
    quarters = ["2015q1","2016q1","2017q1","2018q1","2019q1"] # quarters to be downloaded
    ciks = [1556593,1499200,1220754,917520,1040593,24741] # ciks to be parsed

    # Matplotlib presets
    k,s,f = "bar",True,(20,10)

    for cik in u.ciks:

        # Observe that we wrap these plot statements in try blocks. This is 
        # because when a given sheet does not exist for a particular company
        # the universe will return the None type.

        # Plot income statement  
        try:    u[cik].income().plot(kind=k,stacked=s,figsize=f)
        except: pass

        # Plot cashflow statement 
        try:    u[cik].cash().plot(kind=k,stacked=s,figsize=f)
        except: pass

        # Plot balance sheet
        try:    u[cik].balance().plot(kind=k,stacked=s,figsize=f)
        except: pass

    plt.show()

    # Purge local data store
    u.purge()


###### Note 1:  
From the perspective of your computer, universes and companies are little shell classes that link to a particular 
location on your system. This location stores both the raw and parsed versions of the data.

###### Note 2:  
As of 8/23/19 entire dataset is approximately 16 GB in storage unzipped. Users should ensure at least 500 MB of 
free storage per quarter downloaded. Additionally, the parsing process reads all files into memory at the same time. 
In general for the average user, the amount of ram needed to parse "q" number of quarters is: (.5*q) * 1.2. This 
implies that you should have at least 19.2 GB of unused memory. Poor performance could be a result of memory swap issues. 

###### Note 3:  
Note that calling the download function automatically purges the current universe before data is downloaded. It is 
critically important that you purge universes after use as data on your system will be persistent even after 
you uninstall the package. If however, the use of pesistent data fits within the scope of what you're trying to do by 
all means use it. This was the intended design. 

###### Note 4: 
On a more personal note, one of my many qualms with open source 
financial data providers today is the limitations that come with having to GET requesting everything. Once parsed, 
data from the equities library is quickly and reliably accessed. 