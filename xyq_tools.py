import pandas as pd

def getEntity():
    df = pd.read_csv(r'D:\soft\other\project\report\data\df_character_fre.csv', index_col=0)
    df = df.T.iloc[::-1]  # transform and reverse rows (to get caps in right order for heat map)
    df = df.T
    return df

def generateTag():
    df = getEntity()
    value = [df.index[i] for i in range(8)]
    options=[{'label': i, 'value': i} for i in df.index]
    return value