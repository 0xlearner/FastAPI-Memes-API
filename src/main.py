from typing import List
import fastapi as _fastapi
import fastapi.responses as _responses
from fastapi.responses import HTMLResponse
import services as _service

app = _fastapi.FastAPI()

@app.get('/')
def index():
    content = """
<body>
<form method="post" action="/upload-meme/memes" enctype="multipart/form-data">
<input name="images" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.get('/download-memes/{subreddit_name}')
def download_memes(subreddit_name: str):
    return _service.zip_files(subreddit_name)

@app.post('/upload-meme/{subreddit_name}')
def post_meme(subreddit_name: str, images: List[_fastapi.UploadFile] = _fastapi.File(...)):       
    file_name = {"files": [_service.upload_image(subreddit_name, image) for image in images]}
    if file_name is None:
        return _fastapi.HTTPException(status_code=409, detail="Invalid File Type!")
    return file_name

@app.get('/meme-of-the-day/{subreddit_name}')
def random_meme(subreddit_name: str):
    image_path = _service.get_random_meme(subreddit_name)
    return _responses.FileResponse(image_path)

