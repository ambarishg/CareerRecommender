from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

import requests
import pandas as pd
import os 

bp = Blueprint('reco', __name__)

url = os.environ["KUBERNETES_RECO_URL"]

@bp.route('/', methods=('GET', 'POST'))
def predict():
     if request.method == 'POST':
        q_new =  request.form.get("question")
          
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {'questions':q_new}
        
        r = requests.post(url,params= PARAMS)
        # Convert JSON to DataFrame Using read_json()
        results = pd.read_json(r.text)
            
        return render_template('recommendations/index.html',
        allitems = list(results.values.tolist()),
        recos = True,
        question_new = q_new)

     return render_template('recommendations/index.html',
     allitems = None,recos = False)

