from fastapi import FastAPI
from app.routes import auth, image_processing, users

app = FastAPI()

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(image_processing.router, prefix="/image", tags=["Image Processing"])
app.include_router(users.router, prefix="/user", tags=["User Management"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Maize Disease Detection API"}
