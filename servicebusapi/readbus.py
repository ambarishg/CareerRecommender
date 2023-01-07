
from azure.servicebus import ServiceBusClient

import os
import pandas as pd
import pyodbc

# connstr = "Endpoint=sb://recobus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=uoNVKi9pm6DBR+2OGMB3Bp9tyFcdAjpjwWHduzM9mJ4="
# topic_name = "recotopic"
# subscription_name = "recosub"

# ##################################
# server = 'tcp:recoserver.database.windows.net'
# database = 'recodb' 
# username = 'ambarish' 
# password = 'Blog@123456' 

###############################################

CAREER_VILLAGE_PATH = '/mnt/azure/'

connstr = os.environ["CONN_STR"]
topic_name = os.environ["TOPIC_NAME"]
subscription_name = os.environ["SUBSCRIPTION_NAME"]

##################################
server = os.environ["SERVER"]
database = os.environ["DATABASE"]
username = os.environ["USERNAME"] 
password = os.environ["PASSWORD"]
driver= '{ODBC Driver 17 for SQL Server}'

###################################

CONN_DB_STR = 'DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password


INSERT_QRY = "INSERT INTO dbo.Reco (QuestionsQuery,\
    QuestionsID,QuestionsTitle, \
    QuestionsBody, AnswersBody,Similarity) values(?,?,?,?,?,?)"

INSERT_QRY_PROFESSIONAL_WF = "INSERT INTO dbo.ProfessionalsWF (QuestionsQuery,\
    ProfessionalsID) values(?,?)"



############################################################

def convert_to_dataframe(jsonStr):
    results = pd.read_json(str(jsonStr))
    return (results)

def insert_rows(df):
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
    for index, row in df.iterrows():
        cursor.execute(INSERT_QRY, 
        row.questions_query,
        row.questions_id,
        row.questions_title, 
        row.questions_body, 
        row.answers_body,
        row.sim,
        )
    cnxn.commit()
    cursor.close()

def insert_rows_professional(df):
    cnxn = pyodbc.connect(CONN_DB_STR)
    cursor = cnxn.cursor()
   # Insert Dataframe into SQL Server:
    for index, row in df.iterrows():
        cursor.execute(INSERT_QRY_PROFESSIONAL_WF, 
        row.questions_query,
        row.professionals_id
        )
    cnxn.commit()
    cursor.close()

def readbus():
    with ServiceBusClient.from_connection_string(connstr) as client:
        with client.get_subscription_receiver(topic_name, subscription_name) as receiver:
            for msg in receiver:
                data_transformed = convert_to_dataframe(msg)
                
                print(data_transformed)
                receiver.complete_message(msg)
                insert_rows(data_transformed)

                professionals = pd.read_csv(CAREER_VILLAGE_PATH + "professionals.csv")
                df_professionals = pd.merge(data_transformed,professionals,how = 'left' ,
                        left_on = 'answers_author_id', right_on = 'professionals_id')
                print("#####################################################")
                print(df_professionals)
                insert_rows_professional(df_professionals)
