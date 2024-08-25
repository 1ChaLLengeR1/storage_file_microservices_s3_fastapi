import uvicorn
from fastapi import FastAPI
from endpoints.api import api_router


app = FastAPI(title="storage_file_microservices_s3_fastapi", description="Is a simple microservice for files, catalogs, videos and another files. This project it serves to faster build my own applications. ")
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
