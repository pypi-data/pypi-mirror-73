#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import numpy.random as random


# In[2]:


def random_number_generator(n,distribution,*params):
    if len(params)>2:
        print('Too many parameters')
    else:
        print('Printing', n ,'random numbers')      
        if distribution == 'uniform':          
            print('Generating' ,n , 'from a uniform distribution')
            print (random.rand(n))          
        elif distribution =='Gaussian':
            print('generating',n , 'random numbers from a Gaussian distribution')
            print(random.randn(n))
        elif distribution == 'chisquare':
            p=params[0]
            print('Generating',n,'random numbers from a chisquare distribution')
            print(random.chisquare(p,n))
        elif distribution == 'weibull':
            print('Generating',n,'random numbers from a weibull distribution')
            print(random.weibull(size=n))
        elif distribution =='exponential':
            scale=params[0]
            print('Generating',n,'random numbers from a exponential distribution')
            print(random.exponential(scale,size=(n)))
        elif distribution == 'poisson':
            lam=params[0]
            print('Generating',n,'random numbers from a poisson distribution')
            print(np.random.poisson(lam,size=n))
        elif distribution =='binomial':
            p=params[0]
            t=params[1]
            print('Generating',n,'random numbers from a poisson distribution')
            print(random.binomial(n,p,t))
        elif distribution =='normal':
            mu=params[0]
            sigma=params[1]
            print('Generating',n,'random numbers from a log-normal distribution')
            print(random.normal(mu,sigma,n))
        elif distribution == 'gamma':
            scale=params[0]
            shape=params[1]
            print('Generating',n,'random numbers from a gamma distribution')
            print(random.gamma(shape,scale,size=n))
            
        else :
            print ('not a given distribution')
    return


# In[3]:


class uniform:
    
    def __init__(self,size):         
            self.size=size
            self.random_array=random.rand(self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from a uniform distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the Uniform distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[4]:


class gaussian:
    '''attributes'''
    def __init__(self,size):         
            self.size=size
            self.random_array=random.randn(self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from a gaussian distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the Gaussian distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[5]:


class binomial:
    
    def __init__(self,trials,probability,size):  
            self.trials=trials
            self.probability=probability
            self.size=size
            self.random_array=random.binomial(self.trials,self.probability,self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from a binomial distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the Binomial Distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[6]:


class chisquare:
    
    def __init__(self,df,size):  
            self.df=df
            self.size=size
            self.random_array=random.chisquare(self.df,self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from a chisquare distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the Chisquare Distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[7]:


class weibull:
    
    def __init__(self,size):  
            self.size=size
            self.random_array=random.weibull(self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from a weibull distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the weibull Distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[8]:


class exponential:
    
    def __init__(self,scale,size): 
            self.scale=scale
            self.size=size
            self.random_array=random.exponential(self.scale,self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from an exponential distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the Exponential Distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[9]:


class poisson:
    
    def __init__(self,lam,size): 
            self.lam=lam
            self.size=size
            self.random_array=random.poisson(self.lam,self.size) 
            
    def generator(self):
            
            print('Generating',self.size,'random numbers from a poisson distribution')
            print(self.random_array)
        
                  
    def summary(self):
            print('Summary of the Poisson Distribution')
            rand_array = self.random_array
            min_num = np.min(rand_array)
            max_num = np.max(rand_array)
            mean_num = np.mean(rand_array)
            median_num = np.median(rand_array)
            std_num = np.std(rand_array)
            print("\nMinimum: {}\nMaximum: {}\nMean: {}\nMedian: {}\nStandard Deviation: {} ". format(min_num , max_num, mean_num, median_num, std_num))
           


# In[ ]:




