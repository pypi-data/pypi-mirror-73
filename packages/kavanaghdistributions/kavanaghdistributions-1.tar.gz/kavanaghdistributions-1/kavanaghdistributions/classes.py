import numpy as np

#Parent Class
class ParentDistribution():
    'Parent Class for Distribution Classes'
    
    #initialise sample_output for error checking
    sample_output = []

    #initiliase class instance with sample shape
    def __init__(self, sample_shape):
        self.sample_shape = sample_shape

    #Summarise function for providing Min, Max, Mean and Standard Deviation
    def summarise(self):
        '''Provides a summary of the samples generated, included Min, Max, Mean, and Standard Deviation. '''
        
        #Error Check if a sample has been drawn
        if  len(self.sample_output) == 0:
            raise ValueError ("No samples available, please use the draw() method to draw a sample before summarising.")
        #Otherwise print the requested calculations
        else:
            print(f"Min: {np.min(self.sample_output)}\nMax: {np.max(self.sample_output)}\nMean: {np.mean(self.sample_output)}\nStandard Deviation: {np.std(self.sample_output)}")

#Normal Distribution Sub-Class
class NormalDistribution(ParentDistribution):
    '''
    Random Sample Generator for Normal Distribution
    -----------------------------------------------
    
    Required Arguments: 
    -------------------
    
        - sample_shape = Shape of required samples (int, or array-like)
        - mean = Mean of the required samples
        - sd = Standard Variation of required samples (non-negative)
    
    Methods:
    --------
    
        - draw() = Draws a random sample of specified shape, from a Normal Distribution, with specificed Mean and SD.
        - summarise() = Provides a summary of the samples generated, included Min, Max, Mean, and Standard Deviation.
    
    Attribute:
    ---------
    
        - sample_output = The random samples stored within the attribute of the class.
    
    '''
    #initiliase class instance with mean, standard deviation, and sample shape
    def __init__(self, mean, sd, sample_shape):
        
        #initialise parent class
        ParentDistribution.__init__(self, sample_shape)
        
        #initialise sub class
        self.mean = mean
        self.sd = sd
    
    #Function for drawing samples based on provided mean, standard deviation, and sample shape
    def draw(self):
        '''Draws a random sample of specified shape, from a Normal Distribution, with specificed Mean and SD. '''
        self.sample_output = np.random.normal(loc=self.mean, scale=self.sd, size=self.sample_shape)
        return self.sample_output

#Poisson Distribution Sub-Class
class PoissonDistribution(ParentDistribution):
    '''
    Random Sample Generator for Poisson Distribution
    ------------------------------------------------
    
    Required Arguments: 
    -------------------
    
        - sample_shape = Shape of required samples (int, or array-like)
        - lam = Lambda of the required samples (non-negative)
            
    Methods:
    --------
    
        - draw() = Draws a random sample of specified shape, from a Poisson Distribution, with specificed Lambda.
        - summarise() = Provides a summary of the samples generated, included Min, Max, Mean, and Standard Deviation.
       
    Attribute:
    ---------
    
        - sample_output = The random samples stored within the attribute of the class.
    
    '''
    
    #initiliase class instance with lambda and sample shape
    def __init__(self, lam, sample_shape):
          
        #initialise parent class
        ParentDistribution.__init__(self, sample_shape)
        
        #initialise sub class
        self.lam = lam
    
    #Function for drawing samples based on provided lambda and sample shape
    def draw(self):
        '''Draws a random sample of specified shape, from a Poisson Distribution, with specificed lambda. '''
        self.sample_output = np.random.poisson(lam=self.lam, size=self.sample_shape)
        return self.sample_output

#Binomail Distribution Sub-Class
class BinomialDistribution(ParentDistribution):
    '''
    Random Sample Generator for Binomial Distribution
    ------------------------------------------------
    
    Required Arguments: 
    -------------------
    
        - sample_shape = Shape of required samples (int, or array-like)
        - num = Number of experiments (must be greater than 0)
        - prob = Probability of experiments (must be > 0 and < 1)
        
    Methods:
    --------
    
        - draw() = Draws a random sample of specified shape, from a Binomial Distribution, with specificed num and prob.
        - summarise() = Provides a summary of the samples generated, included Min, Max, Mean, and Standard Deviation.
    
    Attribute:
    ---------
    
        - sample_output = The random samples stored within the attribute of the class.
    
    '''
    
    
    #initiliase class instance with lambd and sample shape
    def __init__(self, num, prob, sample_shape):
        
        #initialise parent class
        ParentDistribution.__init__(self, sample_shape)
        
        #initialise sub class
        self.num = num
        self.prob = prob
        
    #Function for drawing samples based on provided num, prob, and sample shape
    def draw(self):
        '''Draws a random sample of specified shape, from a Binomial Distribution, with specificed number of experiments and their probability. '''
        self.sample_output = np.random.binomial(n=self.num, p=self.prob, size=self.sample_shape)
        return self.sample_output