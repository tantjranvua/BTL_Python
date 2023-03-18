from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd
import schema
import numpy as np

app = FastAPI()
app.state.df = pd.DataFrame()

@app.post('/uploadFile', description ="Truyền vào dữ liệu dạng csv gồm dữ liệu về thông tin, chỉ số của bệnh nhân \n Endpoint sẽ upload file lên hệ thống và sử dụng thực hiện các endpoint khác")
def upload_file(file:UploadFile = File(...,description = 'give heart.csv file')):
    # print(app.state.df.shape)
    try:
        tmp_data = pd.read_csv(file.file)
        app.state.df = tmp_data
        return tmp_data.to_json()
    except:
        raise HTTPException(status_code = 404,detail="cannot read file")

@app.post('/addColumns/{name_row}', description ="Truyền vào dữ liệu dạng json gồm cột mới và dữ liệu cột thêm vào \n Endpoint sẽ trả về file dữ liệu dạng json mới \n")
def upload_columns(name_row:str,file:UploadFile = File(...,description = 'give columns.csv file')): 
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    try:
        tmp_data = pd.read_csv(file.file)
    except:
        raise HTTPException(status_code = 404,detail="cannot read file")
    if(tmp_data.shape[1]>1):
        raise HTTPException(status_code = 406,detail="data have more 1 column")
    app.state.df[name_row] = tmp_data
    return app.state.df.to_json()

@app.post('/addRow', description ="Truyền vào dữ liệu dạng json gồm dữ liệu dòng mới thêm mới \n Endpoint sẽ trả về file dữ liệu dạng json mới \n")
def upload_row(file:UploadFile = File(...,description = 'give row.csv file')):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    try:
        tmp_data = pd.read_csv(file.file)
        print(app.state.df.shape)
        app.state.df = app.state.df.append(tmp_data, ignore_index=True)
        print(app.state.df.shape)
        return app.state.df.to_json()
    except:
        raise HTTPException(status_code = 404,detail="cannot read file")
@app.get('/getDataLine/{number}',  description ="Truyền vào dữ liệu số dạng int \n Endpoint sẽ trả về giá trị của những cột")
def get_data(number:int):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    data = app.state.df
    # print(data.head(min(int(number),len(data))).to_json())
    return data.head(min(int(number),len(data))).to_json()

@app.get('/getColumns', description ="Endpoint sẽ trả về có những cột nào trong dữ liệu")
def get_columnns():
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    return {"Data ": pd.DataFrame(app.state.df.columns) }

@app.get('/getDataMM/{col_name}_{value}', description ="Truyền vào dữ liệu column. column.value dạng string \n Endpoint sẽ trả về giá trị trung bình, lớn nhất, nhỏ nhất của cột")
def get_Max_Min(col_name:str,value:str):  
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")  
    data = app.state.df
    if (col_name not in data.columns):
        raise HTTPException(status_code = 406,detail="column not exist")
    if (value == 'min'):
        return data[data[col_name] == data[col_name].min()].to_json()
    elif(value == 'max'):
        return data[data[col_name] == data[col_name].max()].to_json()
    else:
        raise HTTPException(status_code = 406,detail="value is not max or min") 

@app.get('/plot/{name}_{kind}')
def plot_Data(name:str,kind : str):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    try :
        fig = app.state.df[name].plot(kind=kind,  
        figsize=(20, 16), fontsize=26).get_figure()
        fig.savefig(name+"_"+kind+'.png')
        return FileResponse(name+"_"+kind+'.png',filename=name+"_"+kind+'.png')
    except:
        return "Error"
# --------------------------------
@app.post('/getmean_max_min', description="Truyền vào dữ liệu dạng json gồm tên cột dữ liệu và giá trị muốn trả về (mean/max/min) \n Endpoint sẽ trả về giá trị tương ứng của cột\n")
def get_data(column: schema.Columns_Value):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    if (column.name not in app.state.df.columns):
        raise HTTPException(status_code = 406,detail="column not exist")
    arr = np.array(app.state.df[column.name])
    if (column.value == "min") :
        return arr.min()
    elif (column.value == "max"):
        return arr.max()
    elif (column.value == "mean"):
        return arr.mean()
    else:
        raise HTTPException(status_code = 406,detail="value is not mean, max or min") 

@app.post('/smoking_dead', description ="Truyền dữ liệu số người hút thuốc \n Endpoint sẽ trả về số người tử vong vì hút thuốc")
def get_number_dead(data:schema.Smoking_Dead):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    if(data.people<1):
        raise HTTPException(status_code = 406,detail="number of people cannot small than 1")
    df = app.state.df
    df = df[df["smoking"]==1]
    pro = len(df[df["DEATH_EVENT"]==1])/len(df)
    A = np.random.binomial(1,pro,data.people)
    res = int(A.sum())
    return {"data": res}

@app.post('/get_number_smoking', description="Truyền dữ liệu về số người và tuổi \n Endpoint sẽ trả về dữ liệu số người hút thuốc trong độ tuổi theo phân phối chuẩn")
def get_number_smoking(data:schema.Number_Smoking):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    if(data.people<1 or data.age <1):
        raise HTTPException(status_code = 406,detail="number of people or age cannot small than 1")
    df = app.state.df
    df = df[df["smoking"]==1]
    arr = np.array(df["age"])
    A = np.random.normal(arr.mean(),arr.std(),data.people)
    A = np.round(A)
    res = int((A==data.age).sum())
    # print(type((A==data.age).sum()))
    return {"data": res}

@app.get('/benh/{name}', description="Truyền dữ liệu tên bệnh( anaemia hoặc diabetes) \n Endpoint sẽ trả về số lượng người mắc bệnh trong dữ liệu hiện tại")
def numberof(name:str):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    if((name!= "anaemia") and (name!="diabetes")):
        raise HTTPException(status_code = 406,detail="name is not anaemia or diabetes")
    df = app.state.df
    arr = np.array(df[name])
    res = int(arr.sum())
    return {"data": res}

@app.get('/change_platelets_to_{dv}', description="Truyền dữ liệu đơn vị của cột platelets \n Endpoint sẽ trả về cột theo đơn vị nào")
def change_platelets(dv:str):
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    arr = np.array(app.state.df['platelets'])
    if(dv == "gL"):
        arr =arr/1000
    elif(dv=="cellL"):
        arr = arr*1000
    else:
        raise HTTPException(status_code = 406,detail="unit is not gL or cellL")
    df = pd.DataFrame(arr) 
    return {"data":df}

@app.get('/randomOut', description="Endpoint sẽ trả về những thông tin của dòng dữ liệu ngẫu nhiên")
def random_print():
    if(app.state.df.shape[0]==0&app.state.df.shape[1]==0):
        raise HTTPException(status_code = 406,detail="data have not uploaded")
    pos_ = np.random.randint(len(app.state.df)-1, size=1)
    return {"Data" : app.state.df.iloc[pos_[0]]}
