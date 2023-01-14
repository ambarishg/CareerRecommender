
import argparse
import os
import numpy as np
import pandas as pd
import glob
import gc
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import pickle

from azureml.core import Run
# from utils import load_data

parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
args = parser.parse_args()

def clean_text(text):
    '''Make text lowercase,remove punctuation
    .'''
    text = str(text).lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    return text


data_folder = os.path.join(args.data_folder, 'recodata')
print('Data folder:', data_folder)

questions  = pd.read_csv(os.path.join(data_folder, 'questions.csv'))
professionals = pd.read_csv(os.path.join(data_folder, 'professionals.csv'))
answers = pd.read_csv(os.path.join(data_folder, 'answers.csv'))

prof_ans_q = questions[(~questions["questions_title"].isna()) | (~questions["questions_body"].isna()) ]

q = prof_ans_q["questions_title"] + " " + prof_ans_q["questions_body"]
q  = q.apply(lambda x:clean_text(x))

N_FEATURES = 2000
MAX_DF     = 0.95
MIN_DF     = 2
LANGUAGE   = 'english'

tfidf_vectorizer = TfidfVectorizer(max_df=MAX_DF, 
                                   min_df=MIN_DF,
                                   stop_words=LANGUAGE)

q = q.dropna()
tfidf_vectorizer.fit(q)
q_tfidf = tfidf_vectorizer.transform((q))

# Get the experiment run context
run = Run.get_context()

run.log('MAX_DF', np.float(MAX_DF))
run.log('MIN_DF', np.float(MIN_DF))
run.log('N_FEATURES', np.float(N_FEATURES))


pickle.dump(tfidf_vectorizer,open('outputs/tfidf_vectorizer.pkl',"wb"))
pickle.dump(q_tfidf,open("outputs/q_tfidf.pkl","wb"))


run.complete()
