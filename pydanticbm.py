from pydantic import BaseModel, Field

# class IrisData(BaseModel):
#     sepal_length: float
#     sepal_width: float
#     petal_length: float
#     petal_width: float



class IrisData(BaseModel):
    sepal_length: float = Field(..., gt=0, le=10, description="Sepal length in cm, must be > 0 and ≤ 10")
    sepal_width: float  = Field(..., gt=0, le=10, description="Sepal width in cm, must be > 0 and ≤ 10")
    petal_length: float = Field(..., gt=0, le=10, description="Petal length in cm, must be > 0 and ≤ 10")
    petal_width: float  = Field(..., gt=0, le=10, description="Petal width in cm, must be > 0 and ≤ 10")