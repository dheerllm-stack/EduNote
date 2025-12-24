from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from apps.calculator.route import router as calculator_router
from constants import SERVER_URL, PORT, ENV

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# CORS Middleware (किसी भी ओरिजिन से एक्सेस की अनुमति देता है)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Server is running"}

# हमने यहाँ prefix हटा दिया है ताकि route.py खुद अपना पाथ कंट्रोल कर सके
app.include_router(calculator_router, tags=["calculate"])

if __name__ == "__main__":
    # Ensure PORT is an integer
    uvicorn.run("main:app", host=SERVER_URL, port=int(PORT), reload=(ENV == "dev"))