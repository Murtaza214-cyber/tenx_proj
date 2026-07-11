# app/main.py
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.config.database import engine, Base
from app.features.users.user_routes import router as user_router
from app.features.products.product_routes import router as product_router
from app.features.orders.order_routes import router as order_router
from app.features.categories.category_routes import router as category_router

# Initialize structural database tables directly on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Production Mini E-Commerce System",
    version="1.0.0"
)





# Connect Separated Route Concerns
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(category_router)
@app.get("/")
def root_check():
    return {"Root": "Welcome to the Mini E-Commerce System!"}

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    cleaned_errors =[]
    for error in exc.errors():
        safe_error = {
            "msg": error.get("msg", "Invalid input"),
            "type": error.get("type", "validation_error")
        }
        

        cleaned_errors.append(safe_error)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": cleaned_errors
            }
            
        )