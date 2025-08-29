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
        if file[col].dtype=='object' or file[col].dtype=='bool':
            #this will return the mode for specific column
            mode_v=file[col].mode()
            if not mode_v.empty:
                file[col]=file[col].fillna(mode_v[0])
        else:
            file[col]=file[col].fillna(file[col].mean())
    return file

def Drop_null(file,axis=0):
    '''this function for deleting all the rows or columns that have null values
    axis default is rows but u can choose column
    0 rows
    1 column
    '''
    #!this to delete any column have null value
    if axis==0:
        file=file.dropna(axis=0)
    else:
        file=file.dropna(axis=1)
    return file

def Numeric_summary(file):
    '''this function will return the mean and mode for numeric columns'''
    for col in file.select_dtypes(include=['int64', 'float64']).columns:
        print(f"{col}: mean={file[col].mean()}, median={file[col].median()}\n")
