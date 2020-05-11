## SampSimu
Sampling and resampling techniques for simulation, random sample generation, estimation, and experiment design

---------

Author: Siavash Tabrizian - stabrizian@smu.edu

---------
## 1 - Sampling: 
There are different sampling techniques can be used in order to generate sample. This package helps 
the user to generate samples with three methods:

1 - Crude Monte Carlo sampling (Simple random sampling/SRS):

The unbiased sample mean estimator is as follwos: 

<a href="https://www.codecogs.com/eqnedit.php?latex=\overline{x}&space;=&space;\frac{\sum\limits_{i&space;=&space;1}^{n}&space;x_i}{n}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\overline{x}&space;=&space;\frac{\sum\limits_{i&space;=&space;1}^{n}&space;x_i}{n}" title="\overline{x} = \frac{\sum\limits_{i = 1}^{n} x_i}{n}" /></a> 

can be used in this case in order to estimate the mean <a href="https://www.codecogs.com/eqnedit.php?latex=\mu" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\mu" title="\mu" /></a>.
In this sampling technique, in order to obtain <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> observations, first <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> random numbers should be generated from <a href="https://www.codecogs.com/eqnedit.php?latex=\big[0,1\big]^R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\big[0,1\big]^R" title="\big[0,1\big]^R" /></a> where <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?R" title="R" /></a> is the number of random variables, and after that  using the CDF, the value can be taken from the distribution. 

Sampling steps for generating <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> observations:

~~~
For i <= n:
    For j <= R: 
		1. build the cumulative distribution of the random variable (CDF)
		2. draw a random number from [0,1] interval = r
		3. find the value of the random variable for r using the CDF of jth random variable
~~~

======================================

2 - Antithetic Sampling 

In this sampling technique, in order to obtain <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> observations, first <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{n}{2}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\frac{n}{2}" title="\frac{n}{2}" /></a> random numbers should be generated from <a href="https://www.codecogs.com/eqnedit.php?latex=r&space;=&space;\big[0,1\big]^R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?r&space;=&space;\big[0,1\big]^R" title="r = \big[0,1\big]^R" /></a> where <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?R" title="R" /></a> is the number of random variables, and after that  using the CDF, two values can be taken from the distribution using <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?r" title="r" /></a> and <a href="https://www.codecogs.com/eqnedit.php?latex=1&space;-&space;r" target="_blank"><img src="https://latex.codecogs.com/svg.latex?1&space;-&space;r" title="1 - r" /></a>. 


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

2 - Latin Hypercube Sampling (LHS) 

In this sampling technique, in order to obtain <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> observations, first each random variable should be stratified into <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> intervals. Thereafter, a permutation of intervals should be generated for each random variable, and they all together represent <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> hypercubes in the sample space, then a random observation can be taken from each hypercube randomely.


Sampling steps:

~~~
For i <= n:
    1. Generate $R$ random permutations of \{1,...,n\} = p^r_i
    For j <= R: 
		1. build the cumulative distribution of the random variable (CDF)
		2. draw a random number from p^r_i interval = r
		3. find the value of the random variable for r using the CDF of jth random variable
~~~

## 2 - Resampling: 
In this section of the code the description of the second class of sampling module is presented:

1 - Monte Carlo simulation:

There are <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?m" title="m" /></a> number of replications and in each replication a sample is going to be generated using one of the techniques from the previous section. The final estimation is the sample mean over the obtained estimations: 

<a href="https://www.codecogs.com/eqnedit.php?latex=\overline{x}&space;=&space;\frac{\sum\limits_{r&space;=&space;1}^{m}&space;\overline{x}_{r}}{m}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\overline{x}&space;=&space;\frac{\sum\limits_{r&space;=&space;1}^{m}&space;\overline{x}_{r}}{m}" title="\overline{x} = \frac{\sum\limits_{r = 1}^{m} \overline{x}_{r}}{m}" /></a>

2 - Bootstraping:

In this resmapling technique, <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?m" title="m" /></a> of smaller size samples are going to be generated from a given sample of the larger size. The estimation is can be done by using the sample mean estimator

3 - Jacknife:

It is another resampling technique for generating a set of samples of smaller size from a given sample of larger size. In this method <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a> number of samples are going to be generated from a sample of size <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n" title="n" /></a>. In each sample <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?i" title="i" /></a>, observation <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?i" title="i" /></a> is taken out from the sample, and this leads to <a href="https://www.codecogs.com/eqnedit.php?latex=R" target="_blank"><img src="https://latex.codecogs.com/svg.latex?i" title="i" /></a>  samples of size <a href="https://www.codecogs.com/eqnedit.php?latex=n-1" target="_blank"><img src="https://latex.codecogs.com/svg.latex?n-1" title="n-1" /></a>. The estimation is similar to bootstraping can be obtained using the sample mean estimator.
