import pandas as pd
'''this file for reading and saving the files'''



def Read_csv(path):
    file=pd.read_csv(path)
    return file
def Save_csv(file,path):
    file.to_csv(path,index=False)
    print('file saved successfully')


def Read_xlsx(path):
    file=pd.read_excel(path)
    return file
def Save_xlsx(file,path):
    file.to_excel(path,index=False)
    print('file saved successefully')


def Read_json(path):
    file=pd.read_json(path)
    return file
def Save_json(file,path):
    file.to_json(path,orient='records')

# def Read_db(path,conn):
    # file=pd.read_

