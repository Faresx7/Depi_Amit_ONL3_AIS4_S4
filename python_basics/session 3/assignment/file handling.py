import os
def createfolders(path):
    '''
    
    '''
    for i in range(5):
        j=os.path.join(path,f"dir {i+1}")
        os.makedirs(j,exist_ok=True)
        print(os.listdir(j))
    lenth=len(os.listdir(path))
path="C:/Users/COMPUMARTS/Downloads/DEPI/Depi_Amit_BNS3_AIS4_S1/python_basics/session 3/test os"
createfolders(path)