def execute():

    ">>> Executing Test Statement Script"

    # Import modules
    import time 
    import pandas as pd
    import matplotlib.pyplot as plt
    from equities.objects import Universe, Company

    # Instantiate universe Object
    u = Universe()

    # Download data
    quarters = ["2015q1","2016q1","2017q1","2018q1","2019q1"]
    ciks = [1556593,1499200,1220754,917520,1040593,24741]
    u.download(quarters=quarters,ciks=ciks) #ciks=int("x") limits download to first "x" companies.

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
    time.sleep(50)

    # Purge local data store
    u.purge()

if __name__ == '__main__':

    execute()