from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from project.typesense_utils import search_in_typesense
from project.utils import conduct_matching, is_xml, parse_xml


app = FastAPI()

templates = Jinja2Templates(directory="project/templates")


@app.get("/homepage")
async def get_homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.get("/file_form")
async def get_file_form(request: Request):
    return templates.TemplateResponse("file_form.html", {"request": request})


@app.get("/search_form")
async def get_search_in_typesense(request: Request):
    return templates.TemplateResponse("search_form.html", {"request": request})


@app.post("/upload")
async def post_upload_file(file: UploadFile = File(...)):
    if not file:
        return JSONResponse(content={"message": "Please, upload a file!"})
    if not await is_xml(file):
        return JSONResponse(content={"message": "File is not xml!"})
    await file.seek(0)
    await parse_xml(file=file)
    return JSONResponse(content={"message": "File uploaded into typesense successfully!"})


@app.get("/typesense_search/{title}")
async def get_similar_products(title: str):
    content = await search_in_typesense(title)
    return JSONResponse(content=content)


@app.post("/conduct_matching")
async def post_conduct_matching():
    await conduct_matching()
    return JSONResponse(content={"message": "conducted"})
