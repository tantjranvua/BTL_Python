from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
app = FastAPI()

@app.post('/uploadfile')
def upload_file(file:UploadFile = File(...,description = 'give heart.csv file')):
    data = pd.read_csv(file.file)
    return data