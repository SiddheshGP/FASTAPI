from fastapi import FastAPI ,Path,HTTPException,Query
import json

app = FastAPI()

def data_load():
    try:
        with open('patients.json') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {"error": "File not found"}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON"}

@app.get("/")
def hello():
    return {'message': 'Patient Management System API'}

@app.get("/about")
def about():
    return {'message': 'A Fully Functional API to manage your patient record'}

@app.get("/view")
def view():
    data = data_load()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(...,description='Please provide patient id', example= 'P001')):
    data = data_load()

    if patient_id in data:
       return data[patient_id]
   
    #return {'message': 'patient not found'}
    raise HTTPException(status_code=404,detail='patient not found')


@app.get('/sort')

def sort_patient(sort_by: str = Query(...,description='sort on the basis of weight , height and bmi'), order: str = Query('asc',description='sort in ascendig or descendig order')):

    valid_field= ['weight','height','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail=f'invalid field, kindly enter the details like {valid_field}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'invalid order, either enter asc or desc')
    
    data=data_load()

    sort_order= True  if order == 'desc' else False  

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
