
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import joblib
from pydanticbm import IrisData
import asyncio
from fastapi import BackgroundTasks, Depends, Request, Security
# from auth import get_api_key
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import JSONResponse


load_dotenv()

# Global dictionary to store models
models = {}

# API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "x-api-key"

# Default path where Docker mounts secrets
SECRET_FILE = "/run/secrets/api_key_secret"

def get_api_key():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as f:
            return f.read().strip()
    return None

API_KEY = get_api_key()


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_dir = os.getenv("MODEL_DIR", "models")  # fallback if env not set

    # Load the two classifier models
    models["logistic_regression"] = joblib.load(f"{model_dir}/logistic_regression.pkl")
    models["random_forest"] = joblib.load(f"{model_dir}/random_forest.pkl")

    print("Classifier models loaded successfully")

    yield

    models.clear()
    print("Models cleared on shutdown")




appls = FastAPI(lifespan=lifespan)


WHITELIST = ["/docs", "/openapi.json", "/models", "/health"]


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise JSONResponse(status_code=403, content={"detail": "Unauthorized"})


@appls.get("/secure-data")
async def secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "You have access!", "api_key": api_key}



@appls.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path not in WHITELIST:
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=403, content={"detail": "Unauthorized"})
    response = await call_next(request)
    return response


@appls.get("/models")
def list_models():
    return {"available_models": list(models.keys())}


@appls.post("/predict_async/{model_name}")
async def predict_async(model_name: str, data: IrisData):
    if model_name not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Simulate long-running task
    await asyncio.sleep(2)

    model = models[model_name]
    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(features).tolist()
    return {"model": model_name, "prediction": prediction}


def log_prediction(model_name: str, features: list, prediction: list):
    import time
    time.sleep(8)  # simulate logging delay
    print(f"Logged {model_name}: {features} -> {prediction}")

@appls.post("/predict_async_bg/{model_name}")
async def predict_async_bg(model_name: str, data: IrisData, background_tasks: BackgroundTasks, api_key: str = Depends(get_api_key)):
    features = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    prediction = models[model_name].predict(features).tolist()
    background_tasks.add_task(log_prediction, model_name, features, prediction)
    return {"model": model_name, "prediction": prediction}





