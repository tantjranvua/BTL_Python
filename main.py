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


@app.post('/addRow')
def upload_row(file:UploadFile = File(...,description = 'give row.csv file')):
    tmp_data = pd.read_csv(file.file)
    app.state.df = app.state.df.append(tmp_data, ignore_index=True)
    
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

@app.post('/get_number_smoking')
def get_number_smoking(data:schema.Number_Smoking):
    df = app.state.df
    df = df[df["smoking"]==1]
    arr = np.array(df["age"])
    A = np.random.normal(arr.mean(),arr.std(),data.people)
    A = np.round(A)
    res = int((A==data.age).sum())
    # print(type((A==data.age).sum()))
    return {"data": res}

@app.get('/smoking_dead')
def get_number_dead(data:schema.Smoking_Dead):
    df = app.state.df
    df = df[df["smoking"]==1]
    pro = len(df[df["DEATH_EVENT"]==1])/len(df)
    A = np.random.binomial(1,pro,data.people)
    res = int(A.sum())
    return {"data": res}

@app.get('/randomOut')
def random_print():
    pos_ = np.random.randint(len(app.state.df)-1, size=1)
    return {"Data" : app.state.df.iloc[pos_[0]]}

@app.get('/plot/{name}_{kind}')
def plot_Data(name:str,kind : str):
    try :
        fig = app.state.df[name].plot(kind=kind,  
        figsize=(20, 16), fontsize=26).get_figure()
        fig.savefig(name+"_"+kind+'.png')
        return FileResponse(name+"_"+kind+'.png',filename=name+"_"+kind+'.png')
    except:
        return "Error"
