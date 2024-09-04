import json
from typing import Any

from fastapi import FastAPI

from schema import EmailDto, ChallengeDto, ResponseDto, MessageDto
from api import SourceEndpoint, ApiEndpoint

import config as cfg

_src: SourceEndpoint = SourceEndpoint(cfg.challenge_handler, cfg.mail_handler)
_api: ApiEndpoint = ApiEndpoint(_src)

with open("config/config.json", "r") as fp:
    config: dict[str, Any] = json.load(fp)

if config.get('generate_docs', False):
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

@app.post(f"{_api.base_path}/challenge/", response_model=ChallengeDto)
async def create_challenge(dto: EmailDto) -> ChallengeDto:
    return _api.submit_email(dto)

@app.post(f"{_api.base_path}/response/")
async def submit_response(dto: ResponseDto) -> None:
    return _api.submit_response(dto)

@app.post(f"{_api.base_path}/msg/")
async def send_email(dto: MessageDto) -> None:
    return _api.send_email(dto)