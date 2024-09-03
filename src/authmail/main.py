from fastapi import FastAPI

from authmail.schema import EmailDto, ChallengeDto, ResponseDto, MessageDto
from authmail.api import SourceEndpoint, ApiEndpoint

_src: SourceEndpoint = None
_api: ApiEndpoint = ApiEndpoint(_src)

app = FastAPI()

@app.post(f"{_api.base_path}/challenge/", response_model=ChallengeDto)
async def create_challenge(dto: EmailDto) -> ChallengeDto:
    return _api.submit_email(dto)

@app.post(f"{_api.base_path}/response/")
async def submit_response(dto: ResponseDto) -> None:
    return _api.submit_response(dto)

@app.post(f"{_api.base_path}/msg/")
async def send_email(dto: EmailDto) -> None:
    return _api.send_email(dto)