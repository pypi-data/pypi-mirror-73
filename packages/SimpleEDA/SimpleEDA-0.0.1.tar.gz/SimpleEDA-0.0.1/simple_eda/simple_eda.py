#!/usr/bin/env python
# coding: utf-8

# In[95]:


import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler


# In[128]:



class SimpleEDA():
    '''This class contains all EDA operations you can perform using SimpleEDA.
    '''

    def __init__(self, df):
        self.df = df


    def summary(self):
        '''
        Summary function is the main function of SimpleEDA. DataFrame is the input and it does not return anything but prints the output.
        In output you get Statistical summary of DataFrame like mean, median etc. Then you will get DataFrame rows and columns, null value count,
        column types in numeric and categorical class, unique value count and duplicate rows information.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        Output
        ----------
        type : str
            prints a string,
        '''
        try:
            rows, cols =self.shape
            w = list(self.dtypes)
            column = list(self.columns)
            types = {}
            a = list(self.duplicated(subset=None, keep='first'))
            dup_count = a.count(True)
            dup_indices = []
            for i in range(len(a)):
                if a[i] == True:
                    dup_indices.append(i)
            duplicateRows = self[self.duplicated()]
            for i in range(len(w)):
                type_check = str(w[i])
                col = str(column[i])
                if 'int' in type_check or 'float' in type_check:
                    ty= 'numeric'
                else:
                    ty = 'Categorical'
                types[col] = ty
            types = pd.Series(types)
            summary = ("""
    \033[1m DataFrame Statistical Summary:\033[0m \n\n {}
    \033[1m DataFrame Summmary: \033[0m \n\n Number of Rows: {}\n Number of Columns: {}\n\n
    \033[1m Null value count \033[0m \n{}
    \033[1m Columns DataTypes:\033[0m \n\n {}\n
    \033[1m Unique values count:\033[0m \n\n {}
    \033[1m Total Duplicate rows found:\033[0m \n\n {}
    \033[1m Duplicate rows indices:\033[0m \n\n {}""".format(self.describe(),rows, cols,self.isnull().sum(),types,self.nunique(), dup_count, dup_indices))
            print(summary)

            if (duplicateRows.shape)[0] != 0:
                print("If you want to print Duplicate rows, Please write yes.")
                dup_a = input()
                if dup_a=='yes':
                    print(duplicateRows)
        except:
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame.")
    def gua_hist_num(self):
        '''
        Graphical univariate analysis function accepts a DataFrame as input and plots histograms of each numeric column. This may take time based
        on number of columns and rows. It accepts only numerical columns. Don't worry, we can get numeric columns from your DataFrame.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        Output
        ----------
        type : Plots
            plots histograms,
        '''
        try:
            new_self= self.select_dtypes(include=['int64', 'float64'])
            if len(list(new_self.columns)) < 5:
                new_self.hist(figsize=(10, 10), bins=50, xlabelsize=8, ylabelsize=8, )
            else:
                new_self.hist(figsize=(16, 20), bins=50, xlabelsize=8, ylabelsize=8)
        except:
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame and it contains atleast one numeric column")

    def gua_bar_cat(self):
        '''
        Graphical univariate analysis function accepts a DataFrame as input and plots bar charts of each categorical column. This may take time based
        on number of columns and rows. It accepts only categorical columns. Don't worry, we can get categorical columns from your DataFrame.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        Output
        ----------
        type : Plots
            plots bar charts,
        '''
        try:
            new_self= self.select_dtypes(include='object')
            if new_self.empty==False:
                column = list(new_self.columns)
                for c in column:
                    selfs = dict(new_self[c].value_counts())
                    self_vals = list(selfs.values())
                    if len(self_vals)<  30:
                        self_k= list(selfs.keys())
                        plt.figure(figsize=(6,4))
                        plt.bar(self_k, self_vals)
                        plt.title(c)
                        xlocs, xlabs = plt.xticks()
                        xlocs=[i for i in range(0,len(self_k))]
                        xlabs=[i for i in range(0,len(self_k))]
                        for i, v in enumerate(self_vals):
                            plt.text(xlocs[i], v, str(v))
                        plt.show()
                    else:
                        print("Too many values in the the graph makes ticks overlapping. We will set large figure size and horizontal Bar graph. Each graph may differ in looks due to difference data size and it may take some moments. If you want to proceed, write yes")
                        ans = input()
                        if ans=='yes':
                            self_k= list(selfs.keys())
                            bina = np.arange(len(self_k))
                            plt.figure(figsize=(10,150))
                            plt.barh(self_k, self_vals, height=0.8)
                            plt.ylim([0,bina.size])
                            plt.title(c)
                            plt.yticks(bina, self_k)
                            for index, value in enumerate(self_vals):
                                plt.text(value, index, str(value))
                            plt.show()
            else:
                print("No categorical Columns found")
        except:
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame and it contains atleast one categorical column")

    def corr_columns(self, thresh=0.90):
        '''
        Correlation columns accepts DataFrame and a threshhold. It returns a list of highly correlated columns based on your threshhold.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        thresh : float
            The thresh argument is used as input and accepts float. Default value is 0.90.

        Output
        ----------
        type : List
            returns a list of highly correlated columns,
        '''
        try:
            corr_matrix = self.corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
            to_drop = [column for column in upper.columns if any(upper[column] > thresh)]
            return to_drop
        except:
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame.")

    def find_outliers(self, method='z-score', thresh=3):
        '''
        Find outliers function accepts DataFrame, a string for method argument(default: z-score, accepts iqr also) and a int for thresh argument.
        if you have provided iqr, you don't need to pass thresh. Return 2 numpy arrays, first one gives you rows and second one gives you column.
        For example array([23]) array([3]) means 23rd row is outlier on basis of 3rd column value. e.g [23][3]

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        method : string
            The method argument is used as input and accepts string. Default value is z-score and it can accept iqr.

        thresh : float
            The thresh argument is used as input and accepts float. Default value is 3.

        Output
        ----------
        type : Numpy arrays
            returns 2 numpy array, first one gives rows numbers and second gives column number,
        '''
        try:
            new_self= self.select_dtypes(include=['int64', 'float64'])
            if method=='iqr':
                Q1 = new_self.quantile(0.25)
                Q3 = new_self.quantile(0.75)
                IQR = Q3 - Q1
                iqr_df = (new_self < (Q1 - 1.5 * IQR)) | (new_self > (Q3 + 1.5 * IQR))
                return np.where(iqr_df == True)
            else:
                z = np.abs(stats.zscore(new_self))
                return np.where(z > thresh)
        except :
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame.")

    def plot_boxplot(self):
        '''
        Plot Boxplot function accepts DataFrame and plot boxplot for each column. This may take time based
        on number of columns and rows. It accepts only numerical columns.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        Output
        ----------
        type : plots
            plot boxplot for each column,
        '''
        try:
            new_self= self.select_dtypes(include=['int64', 'float64'])
            column = list(new_self.columns)
            for c in column:
                fig, axs = plt.subplots(ncols=1)
                sns.boxplot(x=new_self[c])
        except :
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame.")

    def plot_scatterplots(self, target):
        '''
        Plot scatterplot function accepts DataFrame and plot scatterplot for each column. Accepts a string containing a target column name. This may take time based
        on number of columns and rows. It accepts only numerical columns.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        target: string
            Target column name

        Output
        ----------
        type : plots
            plot scatterplot for each column,
        '''
        try:
            new_self= self.select_dtypes(include=['int64', 'float64'])
            column = list(new_self.columns)
            for c in column:
                fig, axs = plt.subplots(ncols=1)
                sns.scatterplot(x=new_self[c], y=new_self[target])
        except :
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame and a valid target column.")

    def feature_selection(self, target):
        '''
        This function selected important features from input DataFrame. Accepts DataFrame and a target column. This may take time based
        on number of columns and rows. It accepts only numerical columns.

        Input
        ----------
        self : DataFrame
            The self argument is used as input and it accepts a DataFrame.

        target: string
            Target column name

        Output
        ----------
        type : list
            list of important features in the DataFrame,
        '''
        try:
            new_self= self.select_dtypes(include=['int64', 'float64'])
            scaler = StandardScaler()
            scaler.fit(new_self.fillna(0))
            sel_ = SelectFromModel(LogisticRegression(C=1, penalty='l2'))
            sel_.fit(scaler.transform(new_self.fillna(0)), new_self[target])
            selected_feat = new_self.columns[(sel_.get_support())]
            removed_feats = new_self.columns[(sel_.estimator_.coef_ == 0).ravel().tolist()]
            a = list(removed_feats)
            a.append(target)
            cols = new_self.columns
            imt_feats = [x for x in cols if x not in a]
            print("We have found these features to be important:")
            return imt_feats
        except :
            raise Exception("oops: Somthing bad happend. Make sure you are providing a DataFrame and a valid target column. This function can give erros.")


# In[129]:


# In[86]:





# In[ ]:
