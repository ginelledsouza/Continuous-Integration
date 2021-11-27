# An Effortless Guide to Automation Testing using Python
Introducing unit and document testing with end-to-end continuous integration (CI) implementation via GitHub Actions

## Document Testing: TestingScript.py
- This script consists of two functions that use documentation testing. 
- DeviceType() and Main() methods have encapsulated docstring codes that test the function. 
- Before defining our test cases, it is essential to have a dummy dataset for testing. Therefore we define a dataframe - "Dummy".
- The Main() method generates a single output displaying the most frequent device type sold and the average cost. Therefore, we give the method a raw copy of the dataframe.
- The DeviceType() method only processes the dataframe to generate the type of device for each tablet phone. For this, we must perform one level of post-processing. Therefore, the post-processing is done by the DataCleaning() method.
- The test cases are within the docstring i.e """________""".  Here, we call the defined method as we would call it otherwise and provide the expected output for the same. 
- Kindly note, there must not be any additional line before or after the definition of the docstring.

## Unit Testing: TestCases.py
In unit testing, a developer tests a module to verify whether the module is error-free. An individual unit of the system is analyzed. If there are errors, the developer rectifies them before committing the module into production. We will use two methods used for to demonstrate unit testing.
- assertEqual(): assertEqual() is a unittest library function used to test the equality of two values. This function takes three parameters as input - value from a processed function, expected value, and an error message. It will return a boolean value depending upon the comparison of the two values. If both the values are equal, the method will return true else return false.
- pandas.testing.assert_frame_equal(): This function compares two DataFrames and provides an output that denotes any differences between the two. There are additional parameters that allow the developer to increase the testing difficulty.