from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
import schema
import numpy as np

app = FastAPI()
app.state.df = pd.DataFrame()

@app.post('/uploadFile')
def upload_file(file:UploadFile = File(...,description = 'give heart.csv file')):
    tmp_data = pd.read_csv(file.file)
    app.state.df = tmp_data
    
    return tmp_data.to_json()

@app.post('/addColumns/{name_row}')
def upload_columns(name_row:str,file:UploadFile = File(...,description = 'give columns.csv file')):
    tmp_data = pd.read_csv(file.file)
    app.state.df[name_row] = tmp_data
    
    return app.state.df.to_json()

@app.post('/getmean_max_min')
def get_data(column: schema.Columns_Value):
    arr = np.array(app.state.df[column.name])
    if (column.value == "min") :
        return arr.min()
    elif (column.value == "max"):
        return arr.max()
    elif (column.value == "mean"):
        return arr.mean()
    return "None"

@app.get('/getDataLine/{number}')
def get_data(number:int):
    data = app.state.df
    # print(data.head(min(int(number),len(data))).to_json())
    return data.head(min(int(number),len(data))).to_json()

@app.get('/getColumns')
def get_columnns():
    return {"Data ": pd.DataFrame(app.state.df.columns) }

@app.get('/getDataMM/{col_name}_{value}')
def get_Max_Min(col_name:str,value:str):    
    data = app.state.df
    if (value == 'min'):
        return data[data[col_name] == data[col_name].min()].to_json()
    else:
        return data[data[col_name] == data[col_name].max()].to_json()


@app.get('/benh/{name}')
def numberof(name:str):
    data = app.state.df
    res = int((data[data[name] == 1].count()[name]))
    # print(type(int(res)))
    return {"data": res}
    # return 0

