
Sampling techniques for simulation and generating new samples

Author: Siavash Tabrizian - stabrizian@smu.edu

---------
There are different sampling techniques can be used in order to generate samples. This package helps 
the user to generate samples with the three methods::

1 - Crude Monte Carlo sampling  

In this sampling technique, in order to obtain $$n$$ number of samples, first $$n$$ random numbers should 
be generated from the $$\big[0,1\big]^d$$ where $$d$$ is the number of random variables, and after that 
using the CDF of the values can be taken from the distribution. 

~~~
>>>monte
~~~