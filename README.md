We will build a **Career Recommendation Engine** using `Text Data and Azure Kubernetes Service`. To demonstrate this, we would use a case study approach and build a recommendation engine for a non-profit organization **Career Village**.               

CareerVillage.org is a **non-profit** that crowdsources career advice for underserved youth.         

We will use the following
*	Questions asked by the students               
*	Answers provided by the professionals and the professionals details                            
When a student asks a question, we would find similar questions which have been answered. Then we would connect the student question with the professional so that the professional can answer the question. In the user interface, we would also display the top ten questions and answers which have the highest similarity with the question asked.                   

The main components are as follows:

* `Azure ML model` for building the Recommender Models      
* `UI`         
* `Recommendation Microservice` using the Models              
* `Professionals Microservice` connecting the Recommendations with the Professionals        


<hr/>

**Deployment Steps**            

<hr />

1. Create the Models in Azure ML
2. Deploy the Recommendation Microservice. The deployment steps are in `api\deployment_steps.md`           
3. Deploy the Professionals Microservice. The deployment steps are in `servicebusapi\deployment_steps.md`           
4. Deploy the UI Microservice. The deployment steps are in `ui\deployment_steps.md`       

<hr/>

**Recommender Models**            

<hr />             

|  FileName  |  Description |
|---|---|
| recodata folder   |   Contains the files Questions / Professionals / Answers         |       
| AzureML_recommender-tfidf.ipynb  |     Azure ML model creation in Jupyter Notebook        |        



<hr/>

**Recommenders Service**            

<hr />             

|  FileName  |  Description |
|---|---|
| Dockerfile |   Docker file for the Container Image        |       
| requirements.txt |   Has the dependencies required for the Container Image        |        
|  main.py | Has the code for running the *FastAPI* implementation |    
| pv.yaml |   Yaml for the  **Persistent Volume and the Persistent Volume Claim**        |        
|  secrets.yaml | Yaml for the secrets for the **Service Bus** used by the API   |          
|  reco-pv.yaml | Yaml for the **Deployments** and the **Services** for the `Recommendation Service`   |      
|  sim_tfidf.py | Has the code for Recommendation microservice      |                 


<hr/>

**Professionals Service**            

<hr />             

|  FileName  |  Description |
|---|---|
| Dockerfile |   Docker file for the Container Image        |       
| requirements.txt |   Has the dependencies required for the Container Image         |        
|  main.py | Has the code for running the *FastAPI* implementation for the `Professionals` microservice     |    
|  secrets.yaml | Yaml for the secrets for the **Service Bus** and the **Azure SQL** used by the API    |          
|  reco.yaml | Yaml for the **Deployments** and the **Services** for the `Recommendation Service`    |      
|  readbus.py | Has the code for Professionals Microservice       |     
|  sqlqueries.sql | Script for creating the tables in **Azure SQL**        |     

<hr/>

**UI Service**            

<hr />             


|  FileName  |  Description |
|---|---|
| Dockerfile |   Docker file for the Container Image        |       
| requirements.txt |   Has the dependencies required for the Container Image        |        
|  app.py | Has the code for running the Flask app |    
|  flaskr / __init__.py | Has the code for initialization for the **Flask** App |      
|  flaskr / templates / reco.py | Code for calling the Recommender Service       |        
|  flaskr / static folder | Folder containing the CSS file   |           


