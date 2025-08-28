import pandas as pd
from files import *
file=pd.read_csv("C:/Users/COMPUMARTS/Downloads/saved.csv")
# print(file)
# print(Data_type(file))
i=Fill_null(file)
print(Null_values(file))