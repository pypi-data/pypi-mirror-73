import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display




class MissingDataImputer_Numerical():
    '''
    Parameters:
    
    '''
    def __init__ (self, method, variables, value=None, random_state =1):
        self.method = method
        self.variables = variables
        self.value = value
        self.random_state = random_state
        
        
    def fit (self, df):
        
        if self.method =='mean':
            self.param_dict_ = df[self.variables].mean().to_dict()
        
        if self.method =='median':
            self.param_dict_ = df[self.variables].median().to_dict()
        
        if self.method =='mode':
            self.param_dict_ = df[self.variables].mode().to_dict()
        
        if self.method =='custom_value':
            if value==None:
                raise ValueError("for 'custom_value' method provide a valid value in the 'value' parameter")
            else:
                self.param_dict_ = {var:self.value for var in variables}
        
        if self.method =='random':
            None
            
        return self
    
    def transform(self, df):
        
        if self.method == 'random':
            df = self.__random_imputer__(df)
        
        else:
            for var in self.param_dict_:
                df[var].fillna(self.param_dict_[var] , inplace=True)
        
        return df
    
    def __random_imputer__(self, df):
        for var in self.variables:
            
            if df[var].isnull().sum()>0:
                
                # number of data point to extract at random
                n_samples = df[var].isnull().sum()

                #extract values
                random_sample = df[var].dropna().sample(n_samples, random_state=self.random_state)

                # re-index for pandas so that missing values are filled in the correct observations
                random_sample.index = df[df[var].isnull()].index

                # replace na
                df.loc[df[var].isnull(), var] = random_sample

        return df




class MissingDataImputer_Categorical():
    '''
    Parameters:
    
    '''
    def __init__ (self, strategy, variables, value='Missing', random_state =1):
        self.strategy = strategy
        self.variables = variables
        self.value = value
        self.random_state = random_state
        
        
    def fit (self, df):
        
        if self.strategy =='frequent':
            self.param_dict_ = df[self.variables].mode().to_dict()
        
        if self.strategy =='custom_value':
            if value==None:
                raise ValueError("for 'custom_value' method provide a valid value in the 'value' parameter")
            else:
                self.param_dict_ = {var:self.value for var in variables}
        
        if self.strategy =='random':
            None
            
        return self
    
    def transform(self, df):
        
        if self.strategy == 'random':
            df = self.__random_imputer__(df)
        
        else:
            for var in self.param_dict_:
                df[var].fillna(self.param_dict_[var] , inplace=True)
        
        return df
    
    def __random_imputer__(self, df):
        for var in self.variables:
            
            if df[var].isnull().sum()>0:
                
                # number of data point to extract at random
                n_samples = df[var].isnull().sum()

                #extract values
                random_sample = df[var].dropna().sample(n_samples, random_state=self.random_state)

                # re-index for pandas so that missing values are filled in the correct observations
                random_sample.index = df[df[var].isnull()].index

                # replace na
                df.loc[df[var].isnull(), var] = random_sample

        return df