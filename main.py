from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np

app = FastAPI()

data 

@app.post('/uploadFile')
def upload_file(file:UploadFile = File(...,description = 'give heart.csv file')):
    data = pd.read_csv(file.file)
    return data


@app.get('/getDataLine/{number}')
def get_data(number):
    return data.head(min(number,len(data)))

@app.get('/getColumns')
def get_columnns():
    return data.columns

@app.get('/getDataLine/{col_name}_{value}')
def get_data(col_name,value):
    arr = np.array(df[col_name])
    if (value == "min") :
        return arr.min()
    elif (value == "max"):
        return arr.max()
    elif (value == "mean"):
        return arr.mean()
    return "None"

# col_name ="age"
# arr = np.array(df[col_name])
# arr.max()
# arr.min()
# arr.mean()