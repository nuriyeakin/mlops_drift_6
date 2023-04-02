from fastapi import FastAPI, Request, Depends
from sqlmodel import Session
from models import Hepsiburada, HepsiburadaInput, HepsiburadaDriftInput
from scipy.stats import ks_2samp
import pandas as pd
import joblib
import models
from database import engine, get_db, create_db_and_tables

# Read models saved during train phase
estimator_hepsiburada_loaded = joblib.load("saved_models/randomforest_with_hepsiburada.pkl")

app = FastAPI()

# Creates all the tables defined in models module
create_db_and_tables()

def insert_hepsiburada(request, prediction, client_ip, db):
    new_hepsiburada = Hepsiburada(
        memory= request["memory"],
        ram= request["ram"],
        screen_size= request["screen_size"],
        power= request["power"],
        front_camera= request["front_camera"],
        rc1= request["rc1"],
        rc3= request["rc3"],
        rc5= request["rc5"],
        rc7= request["rc7"],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(new_hepsiburada)
        session.commit()
        session.refresh(new_hepsiburada)

    return new_hepsiburada



# hepsiburada prediction function
def make_hepsiburada_prediction(model, request):
    # parse input from request
    memory= request["memory"]
    ram= request["ram"]
    screen_size= request["screen_size"]
    power= request["power"]
    front_camera= request["front_camera"]
    rc1= request["rc1"]
    rc3= request["rc3"]
    rc5= request["rc5"]
    rc7= request["rc7"]

    # Make an input vector
    hepsiburada = [[memory, ram, screen_size, power, front_camera, rc1, rc3, rc5, rc7]]

    # Predict
    prediction = model.predict(hepsiburada)

    return prediction[0]


# Object agnostic drift detection function
def detect_drift(data1, data2):
    ks_result = ks_2samp(data1, data2)
    if ks_result.pvalue < 0.05:
        return "Drift exits"
    else:
        return "No drift"



# Hepsiburada Prediction endpoint
@app.post("/prediction/Hepsiburada")
async def predict_hepsiburada(request: HepsiburadaInput, fastapi_req: Request, db: Session = Depends(get_db)):
    prediction = make_hepsiburada_prediction(estimator_hepsiburada_loaded, request.dict())
    db_insert_record = insert_hepsiburada(request=request.dict(), prediction=prediction,
                                          client_ip=fastapi_req.client.host,
                                          db=db)
    return {"prediction": prediction, "db_record": db_insert_record}





# Hepsiburada drift detection endpoint
@app.post("/drift/hepsiburada")
async def detect(request: HepsiburadaDriftInput):
    # Select training data
    train_df = pd.read_sql("select * from hepsiburadatrain", engine)

    # Select predicted data last n days
    prediction_df = pd.read_sql(f"""select * from hepsiburada 
                                    where prediction_time >
                                    current_date - {request.n_days_before}""",
                                engine)

    memory_drift = detect_drift(train_df.memory, prediction_df.memory)
    ram_drift = detect_drift(train_df.ram, prediction_df.ram)
    screen_size_drift = detect_drift(train_df.screen_size, prediction_df.screen_size)
    power_drift = detect_drift(train_df.power, prediction_df.power)
    front_camera_drift = detect_drift(train_df.front_camera, prediction_df.front_camera)
    rc1_drift = detect_drift(train_df.rc1, prediction_df.rc1)
    rc3_drift = detect_drift(train_df.rc3, prediction_df.rc3)
    rc5_drift = detect_drift(train_df.rc5, prediction_df.rc5)
    rc7_drift = detect_drift(train_df.rc7, prediction_df.rc7)


    return {"memory_drift": memory_drift, "ram_drift": ram_drift, "screen_size_drift": screen_size_drift, "power_drift": power_drift, "front_camera_drift": front_camera_drift, "rc1_drift": rc1_drift, "rc3_drift": rc3_drift, "rc5_drift": rc5_drift, "rc7_drift": rc7_drift }


