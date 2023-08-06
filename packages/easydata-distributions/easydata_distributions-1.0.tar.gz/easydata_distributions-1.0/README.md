# easydata_distributions
This package can help the users to calculate mean, standard deviation and probability density function for Gaussian and Binomial data distributions.

# Supported Functions
* Calculate the mean of the data.
* Calculate the standard devidation of the data.
* Calculate the probability density function of the data.
* Plot Histogram of PDF.
* Addition of 2 distributions.

# Usage
***import***
`from easydata_distributions import Gaussain` 
`gaussain=Gaussian(25,2)` --parameters: Mean and sigma

OR 
`from easydata_distributions import Binomial`
`gaussain=Gaussian(0.5,25)` --parameters: Probability and Number of times.

***Mean***
`gaussain.mean`

***Standard deviation***
`gaussian.stdev`

***Plot Histogram***
`gaussian.plot_histogram()`
