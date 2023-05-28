from typing import Optional
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Body, UploadFile
from pydantic import BaseModel
from typing import List
import json
import campingShopper

# from models.api import (
#     DeleteRequest,
#     DeleteResponse,
#     QueryRequest,
#     QueryResponse,
#     UpsertRequest,
#     UpsertResponse,
# )
# from datastore.factory import get_datastore
# from services.file import get_document_from_file

from starlette.responses import FileResponse

# from models.models import DocumentMetadata, Source
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

PORT = 8080

origins = [
    f"http://localhost:{PORT}",
    "https://chat.openai.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BuildRequirements(BaseModel):
    requirements: str
    budget: int

class BuildResponse(BaseModel):
    response: str
    links: List[str]

@app.post("/get_gear_recommendations")
async def start_build(build_req: BuildRequirements):
    # print("The requirements are is: " + build_req.requirements)
    # print(f"The budget is: {build_req.budget}")
    
    items = campingShopper.get_camping_itemlist(build_req.requirements)
    print('items are: ' + items)

    budget = campingShopper.create_budget(build_req.requirements, build_req.budget, items)
    print('bugdet is: ' + budget)

    amazon_links = campingShopper.get_amazon_links(json.loads(budget))
    print('amazon links are: ' + str(amazon_links))

    purchase_list = campingShopper.create_purchase_list(amazon_links)
    

    return json.dumps(purchase_list, indent=4,default=str)

@app.route("/logo.png")
async def get_logo(request):
    file_path = "./logo.png"
    return FileResponse(file_path, media_type="image/png")

@app.route("/.well-known/ai-plugin.json")
async def get_logo(request):
    file_path = "./.well-known/ai-plugin.json"
    return FileResponse(file_path, media_type="text/json")

@app.route("/openapi.yaml")
async def get_openapi(request):
    file_path = "./openapi.yaml"
    return FileResponse(file_path, media_type="text/json")

if __name__ == "__main__":
  uvicorn.run(app, host="localhost", port=PORT)