
# Random Number Package
---

### random number generator 

This module implement random number from the specified distribution.

### Real-valued distributions
---
The following functions generate specific real-valued distributions. Function parameters are named after the corresponding variables in the distribution’s equation.

1. uniform(size)

    Return the 'size random floating point numbers in the range [0.0, 1.0).
    
2. gaussian(size)

3. binomial(trials,probability,size)

   return samples from a binomial distribution, where each sample is equal to the number of successes over the n trials. 
   
4. chisquare(df,size)
    
    return samples from a chi-square distribution.
    Parameters:  
             a.  df : int or array_like of ints;Number of degrees of freedom.
              b.  size : int or tuple of ints, Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn. If size is                  None (default), a single value is returned if df is a scalar. Otherwise, np.array(df).size samples are drawn.
   
5. weibull(size)
    return  samples from a Weibull distribution.
    Parameters:
    a : float or array_like of floats
               Shape of the distribution. Should be greater than zero.
               size : int or tuple of ints, optional Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn. If size is None (default), a single value is returned if a is a scalar. Otherwise, np.array(a).size samples are drawn.
    
6. exponential(scale,size)
   return samples from an exponential distribution.
   Parameters:
   scale : float or array_like of floats
              The scale parameter, \beta = 1/\lambda.
   size : int or tuple of ints, optional Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn. If size is None (default), a single value is returned if scale is a scalar. Otherwise, np.array(scale).size samples are drawn.
              
7. poisson(lam,size)
   return samples from a poisson distribution.
   Parameters:
   lam : float or array_like of floats
              Expectation of interval, should be >= 0. A sequence of expectation intervals must be broadcastable over the requested size.
              size : int or tuple of ints, optional Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn. If size is None (default), a single value is returned if lam is a scalar. Otherwise, np.array(lam).size samples are drawn.
