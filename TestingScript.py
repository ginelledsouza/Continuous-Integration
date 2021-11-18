import pandas as pd
import numpy as np

def DataCleaning(Data):
    
    Tablet = Data.copy()
    
    Tablet['Name'].fillna('', inplace=True)
    Tablet['Name'] = Tablet['Name'].apply(lambda x : x.replace("Price","").strip())
    Tablet['Brand'] = Tablet['Name'].apply(lambda x : x.split(" ")[0])
    
    Tablet['ROM'].fillna('', inplace=True)
    Tablet['ROM'] = Tablet['ROM'].apply(lambda x : x.split(",")[0].strip() if x != '' else '')
    Tablet['ROM'] = Tablet['ROM'].apply(lambda x : x.replace("Storage","").strip())
    
    Tablet['RAM'].fillna('', inplace=True)
    Tablet['RAM'] = Tablet['RAM'].apply(lambda x : x.replace("RAM","").strip())
    
    Tablet['Screen'].fillna('', inplace=True)
    Tablet['Screen'] = Tablet['Screen'].apply(lambda x : x.replace("inch Screen","").strip())
    
    Tablet['Battery'].fillna('', inplace=True)
    Tablet['Battery'] = Tablet['Battery'].apply(lambda x : x.replace("mAh","").strip())
    Tablet['Battery'] = Tablet['Battery'].apply(lambda x : np.nan if x == '' else int(x))
    
    Tablet['Price'].fillna('0', inplace=True)
    Tablet['Price'] = Tablet['Price'].apply(lambda x : int(x.replace(",","").replace("Rs.","")))
    
    Tablet['OS'] = Tablet['Brand'].apply(lambda x : 'iOS' if x == 'Apple' else ('Windows' if ((x == 'Microsoft')|(x == 'Notion')) else 'Android'))
    
    Tablet = Tablet[Tablet['Price'] != 0]
    
    Tablet = Tablet[Tablet['OS'] != '']
    Tablet.reset_index(drop=True,inplace=True)
        
    return Tablet
    
    
def DeviceType(Data):
    
    Tablet = Data.copy()
    
    RAMDatabase  = ['8GB','6GB', '4GB']
    ROMDatabase  = ['256GB', '128GB', '64GB', '16GB']

    Tablet['RAMDetails'] = Tablet['RAM'].apply(lambda x : 1 if x in RAMDatabase else 0)
    Tablet['ROMDetails'] = Tablet['ROM'].apply(lambda x : 1 if x in ROMDatabase else 0)
    Tablet['Battery'].fillna(0,inplace=True)
    Tablet['Battery'] = Tablet['Battery'].astype('int64') 
    Tablet['BatteryDetails'] = Tablet['Battery'].apply(lambda x : 1 if x >= 5000 else 0)
    Tablet['Score'] = Tablet['RAMDetails'] + Tablet['ROMDetails'] + Tablet['BatteryDetails'] 
    Tablet['Device Type'] = Tablet['Score'].apply(lambda x : 'Low Ended User' if x == 0 else ('High Ended User' if x == 3 else 'Medium Ended User'))

    Tablet.drop(['RAMDetails','ROMDetails','BatteryDetails','Score'], inplace=True, axis=1)

    Tablet.dropna(inplace=True)
    Tablet.reset_index(drop=True,inplace=True)
    
    return Tablet

def InventorySummary(Data):
    
    Summary = Data.copy()
    
    MaxDeviceSold = Summary['Device Type'].mode().values[0]
    Summary = Summary[Summary['Device Type'] == MaxDeviceSold]
    
    AvgCost = int(Summary['Price'].mean())
    
    
    return MaxDeviceSold,AvgCost
    
def Main(Data):
    
    Data = DataCleaning(Data)
    Data = DeviceType(Data)
    print("Tablet Inventory Data Processed")
    
    DeviceSold,Cost = InventorySummary(Data)
    
    print("Total sales were done for {} and the average sales made are {}".format(DeviceSold,Cost))
    
Data = pd.read_excel("../Testing_And_CICD_Demonstration/static/Tablet.xlsx")
Main(Data)