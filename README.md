
Sampling techniques for simulation and generating new samples

Author: Siavash Tabrizian - stabrizian@smu.edu

---------
There are different sampling techniques can be used in order to generate samples. This package helps 
the user to generate samples with the three methods::

1 - Crude Monte Carlo sampling:

The unbiased sample mean estimator $\bar{x} = \frac{\sum x_i}{n}$ can be used in this case in order to estimate the mean $\mu$.

Sampling steps:

~~~
1. build the cumulative distribution of the random variable (CDF)
2. draw a random number from [0,1] interval = r
3. find the value of the random variable for r using the CDF
~~~