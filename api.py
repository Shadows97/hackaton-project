from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi.encoders import jsonable_encoder
from typing import Dict, Any
import random

app = FastAPI()


# Load parameters and model from checkpoint
# checkpoint = hf_hub_download(repo_id="chrisjay/mmtafrica", filename="mmt_translation.pt")
# device = 'gpu' if torch.cuda.is_available() else 'cpu'
# params = load_params({'checkpoint':checkpoint,'device':device})

# Chargement du DataFrame contenant les données
df_dendi = pd.read_csv("dendi_to_english_tested.csv")
df_fon = pd.read_csv("fondata.csv")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/translate")
# def get_translation(payload: Dict[Any, Any]):
#     '''
#     This takes a sentence and gets the translation.
#     '''



@app.post("/translate/dendi")
def get_translation( payload: Dict[Any, Any]):
    '''
    This takes a sentence and gets the translation.
    '''
    print(payload)
    correspondance = df_dendi[df_dendi['input_text'] == payload['source_sentence']]['new_anglais'].values
    
    if len(correspondance) > 0:
        return {'result': correspondance[0]}
    else:
        return {'result': "cheval"}