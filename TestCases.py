import pymongo
import unittest
import psycopg2
import pandas as pd
import TestingScript as test
from pandas.testing import assert_frame_equal

class mastertablecases(unittest.TestCase):
        
    def test_case_one(self):
        """
        Testing the data cleaning process 
        """
        DummyData = {'Name': ['Apple iPad Mini 2019 WiFi 256GB', 'Apple iPad Mini 2019'],
             'RAM': ['3GB RAM','3GB RAM'],
             'ROM': ['256GB Storage', '64GB Storage'],
             'Screen': ['7.9 inch Screen', '7.9 inch Screen'],
             'Battery': ['5124mAh', '5124mAh'],
             'Price': ['Rs. 41,590', 'Rs. 34,900'],
             'Specification': ['7.9 inch Screen, 3GB RAM, 256GB Storage, 5124mAh','7.9 inch Screen, 3GB RAM, 64GB Storage, 5124mAh']}

        DummyDataResult = {'Name': ['Apple iPad Mini 2019 WiFi 256GB','Apple iPad Mini 2019'],
                           'RAM': ['3GB','3GB'], 'ROM': ['256GB','64GB'], 'Screen': ['7.9','7.9'],
                           'Battery': [5124,5124], 'Price': [41590,34900],
                           'Specification': ['7.9 inch Screen, 3GB RAM, 256GB Storage, 5124mAh','7.9 inch Screen, 3GB RAM, 64GB Storage, 5124mAh'], 
                           'Brand': ['Apple','Apple'], 'OS': ['iOS','iOS']}
        
        DummyData = pd.DataFrame(DummyData)
        DummyDataResult = pd.DataFrame(DummyDataResult)

        DummyData = test.DataCleaning(DummyData)
        
        self.assertEqual(DummyData.shape, (2, 9), "Data Cleaning Module Check Failed")
        pd.testing.assert_frame_equal(DummyData.reset_index(drop=True), DummyDataResult.reset_index(drop=True), check_dtype=False)
    
    def test_case_two(self):
        """
        Testing the data type predication
        """
        
        DummyData = {'Name': ['Apple iPad Mini 2019'],'RAM': ['3GB'],'ROM': ['256GB'], 
                            'Screen': ['7.9'],'Battery': [5124], 'Price': [41590],
                           'Specification': ['7.9 inch Screen, 3GB RAM, 256GB Storage, 5124mAh'], 
                           'Brand': ['Apple'], 'OS': ['iOS']}
        
        DummyData = pd.DataFrame(DummyData)
        
        DummyData = test.DeviceType(DummyData)
        
        DeviceType = DummyData['Device Type'][0]

        self.assertEqual(DeviceType, "Medium Ended User", "Device Type predictor Module Check Failed")
    
    def test_case_three(self):
        """
        Testing highest frequency device sold and average sales cost for that device category
        """
        
        DummyData = {'Name': ['Apple iPad Mini 2019 WiFi 256GB', 'Apple iPad Mini 2019'],
             'RAM': ['3GB RAM','3GB RAM'],
             'ROM': ['256GB Storage', '64GB Storage'],
             'Screen': ['7.9 inch Screen', '7.9 inch Screen'],
             'Battery': ['5124mAh', '5124mAh'],
             'Price': ['Rs. 41,590', 'Rs. 34,900'],
             'Specification': ['7.9 inch Screen, 3GB RAM, 256GB Storage, 5124mAh','7.9 inch Screen, 3GB RAM, 64GB Storage, 5124mAh']}

        
        DummyData = pd.DataFrame(DummyData)

        DummyData = test.DataCleaning(DummyData)
        DummyData = test.DeviceType(DummyData)
        DeviceSold,Cost = test.InventorySummary(DummyData)
    
        self.assertEqual(DeviceSold, "Medium Ended User", "Module Identifying Highest Frequency Failed")
        self.assertEqual(Cost, 38245, "Module Identifying Average Cost Failed")
    
if __name__ == '__main__':
    unittest.main()