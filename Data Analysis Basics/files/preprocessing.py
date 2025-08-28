import pandas as pd

def Data_type(file):
    return file.dtypes

def Change_data_type(file,column_name,new_type):
    file[column_name]=file[column_name].astype(new_type)
    print('data type successfully changed')

def Null_values(file):
    return file.isnull().sum()

def Fill_null(file):
    for col in file.columns:
        if file[col].dtype=='object' or file[col].dtype=='boolean' or file[col].dtype=='bool':
            file[col]=file[col].fillna(False)
        else:
            file[col]=file[col].fillna(file[col].mean())
    return file


