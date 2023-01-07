from typing import Union

from fastapi import FastAPI

import  readbus

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/questions/{questions}/")
def read_item(questions: Union[str, None] = None):
    return { "q": questions}

@app.post("/readbus")
def read_bus():
    readbus.readbus()