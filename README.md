
Sampling techniques for simulation and generating random sample

Author: Siavash Tabrizian - stabrizian@smu.edu

---------
There are different sampling techniques can be used in order to generate sample. This package helps 
the user to generate samples with three methods:

1 - Crude Monte Carlo sampling:

The unbiased sample mean estimator $\bar{x} = \frac{\sum x_i}{n}$ can be used in this case in order to estimate the mean $\mu$.
In this sampling technique, in order to obtain $n$ observations, first $n$ random numbers should be generated from $\big[0,1\big]^R$ where $R$ is the number of random variables, and after that  using the CDF, the value can be taken from the distribution. 

Sampling steps for generating $n$ samples:

~~~
For i <= n:
    For j <= R: 
		1. build the cumulative distribution of the random variable (CDF)
		2. draw a random number from [0,1] interval = r
		3. find the value of the random variable for r using the CDF of jth random variable
~~~

======================================

2 - Antithetic Sampling 

In this sampling technique, in order to obtain $n$ observations, first $n/2$ random numbers should be generated from $r = \big[0,1\big]^R$ where $R$ is the number of random variables, and after that  using the CDF, two values can be taken from the distribution using $r$ and $1-r$. 


Sampling steps:

~~~
For i <= n/2:
    For j <= R: 
		1. build the cumulative distribution of the random variable (CDF)
		2. draw a random number from [0,1] interval = r
		3. find the value of the random variable for r using the CDF of jth random variable
		3. find the value of the random variable for 1-r using the CDF of jth random variable
~~~

======================================

2 - Latin Hypercube Sampling 

In this sampling technique, in order to obtain $n$ observations, first each random variable should be stratified into $n$ intervals. Thereafter, a permutation of intervals should be generated for each random variable, and they all together represent $n$ hypercubes in the sample space, then a random observation can be taken from each hypercube randomely.


Sampling steps:

~~~
For i <= n:
    1. Generate $R$ random permutations of \{1,...,n\} = p^r_i
    For j <= R: 
		1. build the cumulative distribution of the random variable (CDF)
		2. draw a random number from p^r_i interval = r
		3. find the value of the random variable for r using the CDF of jth random variable
~~~



