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
    
    """
    >>> DeviceType(Dummy_test_one)
                         Name  RAM    ROM Screen  Battery  Price   Brand       OS        Device Type
    0            Lenovo Tab 7  2GB   16GB   6.98     3500   8299  Lenovo  Android  Medium Ended User
    1  Apple iPad Pro 11 2020  6GB  128GB     11     7538  66045   Apple      iOS    High Ended User
    2    Apple iPad Mini 2019  3GB   64GB    7.9     5124  34900   Apple      iOS  Medium Ended User
    """
    
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

    """ 
    >>> Main(Dummy_final_test)
    'Total sales were done for Medium Ended User and the average sales made are 21599'
    """
    Data = DataCleaning(Data)
    Data = DeviceType(Data)
    
    DeviceSold,Cost = InventorySummary(Data)
    
    Text = "Total sales were done for {} and the average sales made are {}".format(DeviceSold,Cost)
    
    return Text
    
Dummy = {'Name': ['Lenovo Tab 7', 'Apple iPad Pro 11 2020', 'Apple iPad Mini 2019'],
             'RAM': ['2GB RAM','6GB RAM','3GB RAM'],
             'ROM': ['16GB Storage', '128GB Storage', '64GB Storage'],
             'Screen': ['6.98 inch Screen', '11 inch Screen', '7.9 inch Screen'],
             'Battery': ['3500mAh', '7538mAh', '5124mAh'],
             'Price': ['Rs. 8,299', 'Rs. 66,045', 'Rs. 34,900']}
             
Dummy_final_test = pd.DataFrame(Dummy)
Dummy_test_one = DataCleaning(Dummy_final_test)

if __name__ == "__main__":
    import doctest
    doctest.testmod()