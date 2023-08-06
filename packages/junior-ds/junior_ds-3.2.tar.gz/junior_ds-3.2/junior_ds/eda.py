import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display

class eda:
    """
    Does the EDA for numerical variable
    
    Optional Arguments:
    target: define the target variable
    model : regression / classification 
    """
    def __init__ (self, df, target = None, model = None):
        self.__df__ = df
        self.__target__ = target
        self.__model__ = model
        self.__length_df__= len(df)
    
    def eda_numerical_variable(self, variable):
        
        c = variable
        s = self.__df__[variable]

        
        # 1. Basic Statistics

        print ('Total Number of observations : ', len(s))
        print ()

        print ('Datatype :', (s.dtype))
        print ()

        self.__printmd__ ('**<u>5 Point Summary :</u>**')

        print ('  Minimum  :\t\t', s.min(), '\n  25th Percentile :\t', s.quantile(0.25), 
               '\n  Median :\t\t', s.median(), '\n  75th Percentile :\t', s.quantile(0.75), 
               '\n  Maximum  :\t\t', s.max())

        print ()

        # 2. Missing values

        self.__printmd__ ('**<u>Missing Values :</u>**')

        print ('  Number :', s.isnull().sum())
        print ('  Percentage :', s.isnull().mean()*100, '%')

        # 3. Histogram

        sns.distplot(s.dropna(), hist = True, fit = norm, kde = True)
        plt.show()

        # 4. Spread Statistics

        print ('Skewness :' , s.skew())
        print ('Kurtosis :', s.kurt())
        print ()

        # 5. Q-Q plot
        res = stats.probplot(s.dropna(), dist = 'norm', plot = plt)
        plt.show()

        # 6. Box plot to check the spread outliers
        print ()
        sns.boxplot(s.dropna(), orient = 'v')
        plt.show()

        # 7. Get outliers. Here distance could be a user defined parameter which defaults to 1.5

        print ()
        self.__printmd__ ('**<u>Outliers :</u>**')

        IQR = np.quantile(s, .75) - np.quantile(s, .25)
        upper_boundary = np.quantile(s, .75) + 1.5 * IQR
        lower_boundary = np.quantile(s, .25) - 1.5 * IQR

        print ('  Right end outliers :', np.sum(s>upper_boundary))
        print ('  Left end outliers :', np.sum(s < lower_boundary))

        # 8. Various Variable Transformations

        print ()
        self.__printmd__ (f'**<u>Explore various transformations for {c}</u>**')
        print ()

        print ('1. Logarithmic Transformation')
        s_log = np.log(s)
        self.__normality_diagnostic__(s_log)

        print ('2. Exponential Transformation')
        s_exp = np.exp(s)
        self.__normality_diagnostic__(s_exp)

        print ('3. Square Transformation')
        s_sqr = np.square(s)
        self.__normality_diagnostic__(s_sqr)

        print ('4. Square-root Transformation')
        s_sqrt = np.sqrt(s)
        self.__normality_diagnostic__(s_sqrt)

        print ('5. Box-Cox Transformation')
        s_boxcox, lambda_param = stats.boxcox(s)
        self.__normality_diagnostic__(s_boxcox)
        print ('Optimal Lambda for Box-Cox transformation is :', lambda_param )
        print ()

        print ('6. Yeo Johnson Transformation')
        s = s.astype('float')
        s_yeojohnson, lambda_param = stats.yeojohnson(s)
        self.__normality_diagnostic__(s_yeojohnson)
        print ('Optimal Lambda for Yeo Johnson transformation is :', lambda_param )
        print ()
    
    
    
    
    def __printmd__(self, string):
        display(Markdown(string))

    def __normality_diagnostic__ (self, s):
        plt.figure(figsize = (16, 4))

        plt.subplot(1,2,1)
        sns.distplot(s, hist = True, fit = norm, kde = True)
        plt.title('Histogram')

        plt.subplot(1,2,2)
        stats.probplot(s, dist="norm", plot=plt)
        plt.ylabel('RM Quantiles')

        plt.show()
        
        
    #### -------- Categorical Variables ------- #####
    
    def eda_categorical_variable(self, variable, add_missing=False, add_rare=False, tol=0.05):
        """
        """
        c = variable
        s = self.__df__[variable]
        target = self.__target__
        model = self.__model__
        
        # 1. Basic Statistics
        print ('Total Number of observations : ', len(s))
        print ()
        
        # 2. Cardinality
        print ('Number of Distinct Categories (Cardinality): ', len(s.unique()))
        print ('Distinct Values : ', s.unique())
        print ()
        
        
        # 3. Missing Values

        self.__printmd__ ('**<u>Missing Values :</u>**')
        
        nmiss = s.isnull().sum()
        print ('  Number :', s.isnull().sum())
        print ('  Percentage :', s.isnull().mean()*100, '%')

        # 4. Plot Categories
        
        self.__printmd__ ('**<u>Category Plots :</u>**')
        self.__plot_categories__(c)

        # 5. Plot Categories by including Missing Values
        
        if nmiss:
            print ('Category plot by including Missing Values')
            self.__plot_categories__(c, add_missing = True)
            
        # 6. Plot categories by combining Rare label
        
        print ('Category plot by including missing (if any) and Rare labels')
        print (f'Categories less than {tol} value are clubbed in RARE label')
        self.__plot_categories__(c, add_missing = True, add_rare = True)
        
        #7. Plot categories with target
        
        if target:
            self.__printmd__ ('**<u>Category Plot and Mean Target value:</u>**')
            self.__plot_categories_with_target__(c)
               

       #8. Plot distribution of target variable for each categories
    
        if target:
            self.__printmd__ ('**<u>Distribution of Target variable for all categories:</u>**')
            self.__plot_target_with_categories__(c)
               
    def __plot_categories__(self, c,  add_missing = False, add_rare = False, tol=0.05):

        df = self.__df__
        length_df = len(df)
        if add_missing:
            df[c] = df[c].fillna('Missing')


        s = pd.Series(df[c].value_counts() / length_df)
        s.sort_values(ascending = False, inplace = True)

        if add_rare:
            non_rare_label = [ix for ix, perc in s.items() if perc>tol]
            df[c] = np.where(df[c].isin(non_rare_label), df[c], 'rare')
            plot_df = pd.Series(df[c].value_counts() / length_df)
            plot_df.sort_values(ascending = False, inplace = True)

        else :
            plot_df = s


        fig = plt.figure(figsize=(12,4))
        ax = plot_df.plot.bar(color = 'royalblue')
        ax.set_xlabel(c)
        ax.set_ylabel('Percentage')
        ax.axhline(y=0.05, color = 'red')
        plt.show()

    def __plot_categories_with_target__(self, c):
        df = self.__df__
        target = self.__target__
        plot_df = self.__calculate_mean_target_per_category__(df, c, target)
        plot_df.reset_index(drop = True, inplace=True)


        fig, ax = plt.subplots(figsize=(12,4))
        plt.xticks(plot_df.index, plot_df[c], rotation = 90)

        ax.bar(plot_df.index, plot_df['perc'], align = 'center', color = 'lightgrey')

        ax2 = ax.twinx()
        ax2.plot(plot_df.index, plot_df[target], color = 'green')

        ax.axhline(y=0.05, color = 'red')

        ax.set_xlabel(c)
        ax.set_ylabel('Percentage Distribution')
        ax2.set_ylabel('Mean Target Value')


        plt.show()

    def __calculate_mean_target_per_category__(self, df, c, target):
        
        length_df = len(df)
        temp = pd.DataFrame(df[c].value_counts()/length_df)
        temp = pd.concat([temp, pd.DataFrame(df.groupby(c)[target].mean())], axis=1)
        temp.reset_index(inplace=True)
        temp.columns = [c, 'perc', target]
        temp.sort_values(by='perc', ascending = False, inplace=True)
        return temp
    
    def __plot_target_with_categories__(self, c):
        df = self.__df__
        target = self.__target__
        
        fig = plt.figure(figsize=(12,6))
        for cat in df[c].unique():
            df[df[c]==cat][target].plot(kind = 'kde', label = cat)

        plt.xlabel(f'Distribution of {target}')
        plt.legend(loc='best')
        plt.show()
        
    