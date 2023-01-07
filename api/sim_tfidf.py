CAREER_VILLAGE_PATH = '/mnt/azure/'


import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import re
import string
import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

questions =  pd.read_csv(CAREER_VILLAGE_PATH + "questions.csv")
answers = pd.read_csv(CAREER_VILLAGE_PATH + "answers.csv")
CONNECTION_STR = os.environ["CONN_STR"]
TOPIC_NAME = os.environ["TOPIC_NAME"]

def clean_text(text):
    '''Make text lowercase,remove punctuation
    .'''
    text = str(text).lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('%20', ' ', text)
    
    return text

def send_single_message(sender,df):
    # create a Service Bus message
    message = ServiceBusMessage(df)
    # send the message to the topic
    sender.send_messages(message)
    print("Sent a single message")

def get_top_n_answers(q_new):

    q_new1 = q_new
    q_new = [q_new]

    with open(CAREER_VILLAGE_PATH + 'tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    with open(CAREER_VILLAGE_PATH + 'q_tfidf.pkl', 'rb') as f:
        q_tfidf = pickle.load(f)

    q_new_tfidf = tfidf_vectorizer.transform(q_new)

    result = cosine_similarity(q_new_tfidf,q_tfidf)
    result_df = pd.DataFrame(result[0], columns = ['sim'])
    q = pd.concat([questions,result_df],axis = 1)
    q = q.sort_values(by="sim",ascending = False)
    q_10 = q[:10]
    ans_q_10 = pd.merge(answers, q, how = 'inner' ,
                      left_on = 'answers_question_id', right_on = 'questions_id')
    ans_q_10_sel = ans_q_10[["answers_author_id",
    "questions_id","questions_title","questions_body",
    "answers_body","sim"]].sort_values(by="sim",ascending = False)
    ans_q_10_sel["sim"]  = ans_q_10_sel["sim"].apply(lambda x:round(x,3))
    ans_q_10_sel = ans_q_10_sel.sort_values(by="sim",ascending = False)
    ans_q_10_sel = ans_q_10_sel[:10]

    ans_q_10_sel_msg = ans_q_10_sel
    ans_q_10_sel_msg["questions_query"] = q_new1
    
    ans_q_10_sel = ans_q_10_sel[["questions_title","questions_body","answers_body","sim"]]
    
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, 
    logging_enable=True)

    with servicebus_client:
        sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
        with sender:
            send_single_message(sender,ans_q_10_sel_msg.to_json())
    
    return(ans_q_10_sel)
