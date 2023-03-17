from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np

app = FastAPI()
data = pd.DataFrame()
@app.post('/uploadFile')
def upload_file(file:UploadFile = File(...,description = 'give heart.csv file')):
    tmp_data = pd.read_csv(file.file)
    app.state.df = tmp_data
    
    return tmp_data.to_json()


@app.get('/getDataLine/{number}')
def get_data(number:int):
    data = app.state.df
    app.state.df = pd.DataFrame(data)
    print(data)
    print(data.head(min(int(number),len(data))).to_json())
    return data.head(min(int(number),len(data))).to_json()

@app.get('/getColumns')
def get_columnns():
    data = app.state.df
    return {"data":data.columns}

@app.get('/getDataMM/{col_name}_{value}')
def get_Max_Min(col_name,value):    
    if (value == 'min'):
        data[data[col_name] == data[col_name].min()]
    else:
        data[data[col_name] == data[col_name].max()]



@app.get('/getDa/{col_name}_{value}')
def get_data(col_name,value):
    arr = np.array(df[col_name])
    if (value == "min") :
        return arr.min()
    elif (value == "max"):
        return arr.max()
    elif (value == "mean"):
        return arr.mean()
    return "None"

