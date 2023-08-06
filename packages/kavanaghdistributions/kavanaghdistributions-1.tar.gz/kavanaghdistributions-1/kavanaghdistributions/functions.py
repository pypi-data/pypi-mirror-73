import numpy as np

def random_draw(sample_shape, distribution, **kwargs):

    '''Function that takes in a given distribution (Normal, Poisson, or Binomial),
    and returns an array with specified sample amount and shape, with distribution
    specific keyword arguments.  
    
    --------------------------
    Required Keyword Arguments
    --------------------------
    samples =  Shape of samples required from specified distribution (int, or array like).

    distribution = Type of distribution required. Either: Normal, Poisson, or Binomial.

    ---------------------------------------
    Distribution specific keyword arguments
    ---------------------------------------

    OPTIONAL
    --------

    Normal: 
    Mean can be specified through the keyword argument 'mean'
        i.e mean = -0.5
    Standard Deviation can be specified (non-negative) through the keyword argument 'sd'
        i.e sd = 0.5

    Poisson: 
    Lambda can be specified (> 0) through keyword argument 'lam'
        ie. lam=10

    REQUIRED
    --------

    Binomial: 
    Number of experiments must be specified (> 0) through keyword argument 'num'
        ie. num = 10
    Probability of experiment can be specified (Between 0 and 1) through keyword argument 'prob'
        ie. prob = 0.2

    '''
        
    #Normal Distribution
    if distribution.lower() == 'normal':
        #Create empty draw dictionary
        draw = []
        #Set default parameters
        mean=0.0
        sd=1.0 
        
        #Check keywords and assign accordingly
        for keyword, argument in kwargs.items():
                if keyword == 'mean':
                    lam = argument
                elif keyword == 'sd':
                    sd = argument
                else: 
                    raise ValueError ("For Normal Distribution, you may only specify Mean (mean) or Standard Deviation (sd) as keyword arguments")
        
        #draw normal random samples            
        draw = np.random.normal(loc=mean, scale=sd, size=sample_shape)
        
    #Poisson Distibution
    elif distribution.lower() == 'poisson':
        #Create empty draw dictionary
        draw = []
        #Set default parameter
        lam = 1
        
        #Check keywords and assign accordingly
        for keyword, argument in kwargs.items():
            if keyword == 'lam':
                lam = argument
            else: 
                raise ValueError ("For Poisson Distribution, you may only specify Lambda (Lam) as a keyword argument")
        
        draw = np.random.poisson(lam=lam, size=sample_shape)
        
    #Binomial Distibution
    elif distribution.lower() == 'binomial':
        #Create empty draw dictionary
        draw = []
        #Create empty variables for validation later 
        num = None
        prob = None
        
        #Check keywords and assign accordingly
        for keyword, argument in kwargs.items():
                if keyword == 'num':
                    num = argument
                elif keyword == 'prob':
                    prob = argument
                else: 
                    raise ValueError ("For Binomial Distribution, you must only specify Number (num) and Probability (prob) as keyword arguments")
        
        #check that both kwargs were provided
        if not num or not prob:
            raise ValueError ("Please specify by Number (num) and Probability (prob) for Binomial Distribution")
    
        draw = np.random.binomial(n=num, p=prob, size=sample_shape)
      
    #If incorrect distribution specified, return ValueError
    else:
        raise ValueError ("Please specify a distribution of either Normal, Poisson, or Binomial")
                
    return draw