from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Form

from amazon_s3.bucket import AmazonBucket
from dropbox_st.storage import DropboxStorage


app = FastAPI()


@app.post("/api/dropbox")
async def upload_file_dropbox(
    request: Request,
    access_token: str = Form(...),
    text_file: UploadFile = File(),
):
    validate_type_file(text_file)
    text_url = DropboxStorage.upload_file(text_file, {"access_token": access_token})
    return {"text_url": text_url}


@app.post("/api/amazon")
async def upload_file_amazon(
    request: Request,
    aws_access_key_id: str = Form(...),
    aws_secret_access_key: str = Form(...),
    s3_bucket_name: str = Form(...),
    text_file: UploadFile = File(),
):
    validate_type_file(text_file)
    text_url = AmazonBucket.upload_file(
        text_file,
        {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "s3_bucket_name": s3_bucket_name,
        },
    )
    return {"text_url": text_url}


@app.get("/api/objects")
async def get_objects(request: Request):
    request_data = await request.json()

    objects = {}
    if request_data.get("amazon"):
        amazon_credentials = request_data["amazon"]
        objects["amazon"] = AmazonBucket.get_all_objects(amazon_credentials)
    if request_data.get("dropbox"):
        dropbox_credentials = request_data["dropbox"]
        objects["dropbox"] = DropboxStorage.get_all_objects(dropbox_credentials)

    return objects


def validate_type_file(file: UploadFile):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=422, detail="Wrong file type, use .txt")
