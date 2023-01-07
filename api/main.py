from typing import Union

from fastapi import FastAPI

import  sim_tfidf

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/questions/{questions}/")
def read_item(questions: Union[str, None] = None):
    return { "q": questions}

@app.post("/recotfidf")
def read_item_tfidf(questions: Union[str, None] = None):
    results = sim_tfidf.get_top_n_answers(questions)
    return results