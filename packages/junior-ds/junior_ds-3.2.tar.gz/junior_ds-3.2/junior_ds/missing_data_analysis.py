import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display


class MissingDataAnalysis:
    def __init__ (self, train, test = None, target = None, model = None):
        self.__train__ = train
        self.__test__ = test
        self.__target__ = target
        self.__model__ = model
        
    # ------------------------------------------------------#
    # Numerical Variable Imputation #
    # ------------------------------------------------------#
    
    def explore_numerical_imputation (self, variable):
        
    
    # ------------------------------------------------------#
    # Categorical Variable Imputation #
    # ------------------------------------------------------#
    
    def categorical_imputation(self, variable, strategy='frequent'):
        """
        Parameters:
            strategy: 'frequent' for imputing the missing values with most frequent value
                      'missing' create a category called Missing for all missing values
                      'random' for arbitrary value imputation
        """
        c = variable
        
        self.__printmd__ ('**<u>Missing Values :</u>**')

        print ('  Number :', self.__train__[c].isnull().sum())
        print ('  Percentage :', self.__train__[c].isnull().mean()*100, '%')


        if strategy == 'frequent':
            df = self.__frequent_category_imputation__(c)
        
        if strategy == 'missing':
            df = self.__missing_category_imputation__(c)
            
        if strategy == 'random':
            df = self.__random_category_imputation__(c)
        
        return df
        
    def explore_categorical_imputation (self, variable):
        """
        Compares the results from various imputation methods so that you can choose the best suited one

        
        # 1st chart => existing categories and avg target value
        # 2nd chart => missing value replaced by frequent category ; then plot a chart with target value
        # 3rd chart => missing value replaced by 'Missing' category ; then plot a chart with target value
        # 4th chart => missing value replaced by random distribution ; then plot a chart with target value
        
        """
        df = self.__train__
        c = variable
        
        self.__printmd__ ('**<u>Missing Values :</u>**')

        print ('  Number :', self.__train__[c].isnull().sum())
        print ('  Percentage :', self.__train__[c].isnull().mean()*100, '%')
        print ()
        
        self.__printmd__(f'**<u>We have following options for Imputing the Missing Value for Categorical Variable, {c} :</u>**')
        print ('  1. Imputing missing values by Frequent Category' )
        print ('  2. Imputing missing values by Missing Label' )
        print ('  3. Imputing missing values by Randomly selected value' )
        
        print ()
        print ("Let's visualize the impact of each imputation and compare it with original distribution")
        print ()
        
        print ("1. Original Distribution of all Categories")
        self.__plot_categories_with_target__(df, c)
        
        print ("2. All Categories after Frequent Category Imputation")
        temp = self.__frequent_category_imputation__(c)
        fig = plt.figure(figsize = (8,4))
        ax = fig.add_subplot(111)
        
        # Frequent value
        print ('Look at the Distibution of Frequent Category and Missing Data. Are there some major differences')
        value = df[c].mode().item()
        df[df[c] == value][self.__target__].plot(kind = 'kde', ax = ax, color = 'blue')
        
        # NA Value
        df[df[c].isnull()][self.__target__].plot(kind = 'kde', ax = ax, color = 'red')
        
        # Add the legend
        labels = ['Most Frequent category', 'with NA']
        ax.legend(labels, loc = 'best')
        plt.show()
        
        
        self.__plot_categories_with_target__(temp, c+'_freq')
        
        
        print ("3. All Categories after Missing Label Imputation")
        temp = self.__missing_category_imputation__(c)
        self.__plot_categories_with_target__(temp, c+'_miss')
        
        
        print ("4. All Categories after Randomly Selected Value Imputation")
        temp = self.__random_category_imputation__(c)
        self.__plot_categories_with_target__(temp, c+'_random')
        
        
        

    
    def __frequent_category_imputation__(self, c):
        
        df = self.__train__
        value = df[c].mode().item()
        
        print ('\n\nMost Frequent Category: ', value)
        
        df[c+'_freq'] = df[c].fillna(value)
        
        return df
        
    def __missing_category_imputation__(self, c):
        value = 'Missing'
        
        self.__train__[c+'_miss'] = self.__train__[c].fillna(value)
        
        return self.__train__  
    
    def __random_category_imputation__(self, c):
        
        # Get the number of null values for variable
        number_nulls = self.__train__[c].isnull().sum()
        # Get that many number of values from dataset chosen at random
        random_sample = self.__train__[c].dropna().sample(number_nulls, random_state = 0)
        # Set the index of random sample to that of null values
        random_sample.index = self.__train__[self.__train__[c].isnull()].index
        # make a copy of dataset including NA 
        self.__train__[c+'_random'] = self.__train__[c].copy()
        # replace the NA in newly created variable
        self.__train__.loc[self.__train__[c].isnull(), c+'_random'] = random_sample
        
        return self.__train__  
    
        
    def __plot_categories_with_target__(self, temp, col):
        df = temp
        target = self.__target__
        plot_df = self.__calculate_mean_target_per_category__(df, col, target)
        plot_df.reset_index(drop = True, inplace=True)


        fig, ax = plt.subplots(figsize=(12,4))
        plt.xticks(plot_df.index, plot_df[col], rotation = 90)

        ax.bar(plot_df.index, plot_df['perc'], align = 'center', color = 'lightgrey')

        ax2 = ax.twinx()
        ax2.plot(plot_df.index, plot_df[target], color = 'green')

        ax.axhline(y=0.05, color = 'red')

        ax.set_xlabel(col)
        ax.set_ylabel('Percentage Distribution')
        ax2.set_ylabel('Mean Target Value')


        plt.show()    
        
    def __calculate_mean_target_per_category__(self, df, col, target):
        
        length_df = len(df)
        temp = pd.DataFrame(df[col].value_counts()/length_df)
        temp = pd.concat([temp, pd.DataFrame(df.groupby(col)[target].mean())], axis=1)
        temp.reset_index(inplace=True)
        temp.columns = [col, 'perc', target]
        temp.sort_values(by='perc', ascending = False, inplace=True)
        return temp
    
    # ------------------------------------------------------#
    # Utility Function
    # ------------------------------------------------------#
    def __printmd__(self, string):
        display(Markdown(string))