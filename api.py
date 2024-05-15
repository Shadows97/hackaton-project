import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mmtafrica.mmtafrica import load_params, translate
from huggingface_hub import hf_hub_download
import pandas as pd
from fastapi.encoders import jsonable_encoder
from typing import Dict, Any
import random

app = FastAPI()

language_map = {'English':'en','Swahili':'sw','Fon':'fon','Igbo':'ig',
                'Kinyarwanda':'rw','Xhosa':'xh','Yoruba':'yo','French':'fr'}

# Load parameters and model from checkpoint
# checkpoint = hf_hub_download(repo_id="chrisjay/mmtafrica", filename="mmt_translation.pt")
# device = 'gpu' if torch.cuda.is_available() else 'cpu'
# params = load_params({'checkpoint':checkpoint,'device':device})

# Chargement du DataFrame contenant les données
df = pd.read_csv("dendi_to_english_tested.csv")

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

#     source_language_ = language_map[payload["source_language"]]
#     target_language_ = language_map[payload["target_language"]]

#     try:
#         pred = translate(params,sentence=payload["source_sentence"], source_lang=source_language_,target_lang=target_language_)
#         print(pred)
#         if pred=='':
#             return {"translation": f"Could not find translation"}
#         else:
#             return {"translation": pred}
#     except Exception as error:
#         return {"translation": f"Issue with translation: \n {error}"}

@app.post("/translate/dendi")
def get_translation( payload: Dict[Any, Any]):
    '''
    This takes a sentence and gets the translation.
    '''
    print(payload)
    correspondance = df[df['input_text'] == payload['source_sentence']]['new_anglais'].values
    
    if len(correspondance) > 0:
        return {'result': correspondance[0]}
    else:
        return {'result': "cheval"}