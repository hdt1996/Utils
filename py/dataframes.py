import pandas as pd
from .util import buildDictBoolbyArr
import numpy as np

class DataFrames():
    #TODO allow multiple dataframes to be pulled and concated per arguments
    def __init__(self, df_col_names = [], df_index = ''):
        self.df = pd.DataFrame()
        self.col_dict = {}
        self.df_index = df_index
        if self.df_index != '':
            if not self.df_index in df_col_names:
                raise ValueError('Make sure self.df_index is one of the column names.')
        for col in df_col_names:
            self.col_dict[col] = []
        if len(df_col_names) != len(self.col_dict):
            raise ValueError('Column_Name list error. One of them are duplicates. Please make each unique.')

    def combine(self, col_to_join: str, main_df: pd.DataFrame, new_df: pd.DateOffset, join_type: str = 'outer'):
        main_df = main_df.merge(right = new_df, how = join_type, on = col_to_join)
        return main_df

    def getDatabyURL(self,url):
        if url == None:
            return pd.DataFrame()
        return pd.read_csv(url)

    def buildSeriesList(self, nested_list:list, col_names: list):
        result_list = []
        for s_list in nested_list:
            result_list.append(pd.Series(data = s_list, index = col_names))
        return result_list

    def addColumn(self, df: pd.DataFrame, data: list, col_name: str):
        # Data parameter must be list and must match length of dataframe
        df[col_name] = data
        return df

    def removeColumns(self, df: pd.DataFrame, col_to_remove: list):
        df_uniques = buildDictBoolbyArr(df.columns)
        for ctr in col_to_remove:
            if ctr in df_uniques:
                df = df.drop(columns = ctr)
        return df

    def changeColDtype(self, df: pd.DataFrame, types: list|str = 'string'):
        if isinstance(types, str):
            for col in df.columns:
                df[col]=df[col].astype(dtype = types)
        elif isinstance(types, list):
            for index, col in enumerate(df.columns):
                df[col]=df[col].astype(dtype = types[index])
        return df

    def removeTextByCol(self,df: pd.DataFrame, texts: list|str):
        if isinstance(texts, str):
            for col in df.columns:
                df[col] = df[col].str.replace(texts,'')
        elif isinstance(texts, list):
           for index, col in enumerate(df.columns):
                df[col] = df[col].str.replace(texts[index],'')
        return df

    def addRow(self, data: list):
        self.df.loc[len(self.df.index)] = data

    def buildDFbyNumpy(self, data: list = [], index: list = None, to_shape: tuple = ()):
        if isinstance(data, np.ndarray):
            def recurse(d_item: np.ndarray, index: int, mult_index: list = [], n: int = 0):
                # Recursion method that uses local variable mult_index to reduce heap_memory stacking
                # For function to work properly, mult_index = [] CANNOT be passed to function call
                mult_index.append(index)
                for it_index, item in enumerate(d_item):
                    if isinstance(item,np.ndarray):
                        recurse(d_item = item, index = it_index, n = n + 1)
                    else:
                        col_dict[it_index].append(item)
                indices.append(str(mult_index))
                mult_index.pop()
            def recurse2(value: int, index: int, mult_index: list = [], n: int = 0, to_shape: tuple = ()):
                mult_index.append(index)
                curr_shape = to_shape[n]
                for i in range(curr_shape):
                    mult_index.append(i)
                    if n < len(to_shape) - 1:
                        recurse2(value = value, index = i, n = n + 1, to_shape = to_shape)
                    else:
                        col_dict[0].append(value)
                        indices.append(str(mult_index)) 
                    mult_index.pop()
                mult_index.pop()
            indices = []
            col_dict = {}
            if len(data.shape) == 1:
                col_dict[0] = []

                if len(to_shape) > 2:
                    for index in range(data.shape[0]):
                        recurse2(value = data[index], index = index, to_shape = list(to_shape[1:-1]), mult_index = [])
                        #indices.pop()
                else:
                    col_dict[0] = list(data)
                    indices = None
            else:
                for i in range(data.shape[len(data.shape)-1]):
                    col_dict[i] = []
                for index in range(data.shape[0]):
                    recurse(d_item = data[index], index = index)
                    indices.pop()
                    
            self.df = pd.DataFrame(data = col_dict, index = indices)
            del col_dict
            del indices
            return self.df

    def buildDFbyList(self, data:list = [], columns: list= None, index:list = None):
        if isinstance(data, np.ndarray):
            raise TypeError('Please use buildDFbyNumpy method for numpy objects instead.')
        if columns and len(columns) != len(data.columns):
            raise ValueError('Column names list must match number of columns in dataframe.')
        if index and len(index) != len(data):
            raise ValueError('Index list must match number of rows')
        self.df = pd.DataFrame(data = data, columns = columns,index = index)
        return self.df


    def stats(self, df: pd.DataFrame):
        return  df.describe()

    def buildDFbyDict(self):
        max_length = None
        for file in self.col_dict:
            arr =  self.col_dict[file]
            if max_length == None:
                max_length = len(arr)
                continue
            if len(arr) != max_length:
                raise ValueError(f'Array length -- {len(arr)} -- within {file} does not match current len -- {max_length} --.\nCheck that CLI arg check_multiple = False')
        if self.df_index == '':
            self.df = pd.DataFrame(data =  self.col_dict)
        else:
            self.df = pd.DataFrame(data =  self.col_dict).set_index(self.df_index)
        return self.df

    def allIntColumns(self, df: pd.DataFrame):
        for col in df.columns:
            if not isinstance(col, int):
                return False
        return True


