from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
app = FastAPI()

data = 0

@app.post('/uploadfile')
def upload_file(file:UploadFile = File(...,description = 'give heart.csv file')):
    data = pd.read_csv(file.file)
    return data.to_html()

@app.post('/mean_max_min')
def get_mean_max_min(columns:str):
    print(data)
    col_name = columns
    arr = np.array(data[col_name])
    arr.max()
    arr.min()
    arr.mean()
    return columns