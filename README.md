# VanillaTensorflow 

The following repo consist of neural network models that are built purely on tensorflow without high level APIs. Feel free to use any of them to suit your needs.

## Dataset 

### Logistic Regression ###
The dataset consists of the multi-spectral values of pixels in 3x3 neighbourhoods in a satellite image, and the classification associated with the central pixel
in each neighbourhood. The aim is to predict this classification, given the multi-spectral values. In the sample dataset, the class of a pixel is coded as
a number.


**NUMBER OF EXAMPLES**
training set = 4435
test set = 2000

**NUMBER OF ATTRIBUTES**
36 (= 4 spectral bands x 9 pixels in neighbourhood )
The attributes are numerical, in the range 0 to 255.

**CLASS**

There are 6 decision classes: 1,2,3,4,5 and 7.
There are no examples with class 6 in this dataset and they have all been removed because of doubts about the validity of this class.


The number is a code for the following classes:
	Number Class
	1 red soil
	2 cotton crop
	3 grey soil
	4 damp grey soil
	5 soil with vegetation stubble
	6 mixture class (all types present)
	7 very damp grey soil

** Data Files **
Training data: sat_train.txt
Test data: sat_test.txt

More datasets with the respective neural network model will be placed in this repo.
 