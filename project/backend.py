from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="project/templates")


@app.get("/homepage")
async def homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.get("/form")
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    return JSONResponse(content={"message": "File uploaded successfully!"})
