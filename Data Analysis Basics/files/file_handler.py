import pandas as pd
import psycopg2
import sqlalchemy

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


def Read_db(sql_stat,uhost,udatabase,user_u,upassword):
    conn=psycopg2.connect(
        host=uhost,
        database=udatabase,
        user=user_u,
        password=upassword
    )
    #will make data frame file don't forget
    file=pd.read_sql(sql_stat,conn)
    conn.close()
    return file
def Save_db(df, table_name, host, database, user, password):
    #! this code won't work if the table you try to replace in dependent on another table 
    #! or the opposite
    engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print('data updated successfully')