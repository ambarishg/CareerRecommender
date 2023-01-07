# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

sudo chmod 666 /var/run/docker.sock



#############################################################

# Change these four parameters as needed for your own environment
AKS_PERS_STORAGE_ACCOUNT_NAME=stgreco
AKS_PERS_RESOURCE_GROUP=recogroup
AKS_PERS_LOCATION=centralindia
AKS_PERS_SHARE_NAME=aksshare
AKS_BUS_NS=recobus
AKS_TOPIC=recotopic
AKS_SUBSCRIPTION=recosub

# Create a Resource Group          
az group create --location $AKS_PERS_LOCATION --resource-group $AKS_PERS_RESOURCE_GROUP 


######################################################################
#                 SERVICE BUS
######################################################################

az servicebus namespace create --resource-group $AKS_PERS_RESOURCE_GROUP --name $AKS_BUS_NS --location $AKS_PERS_LOCATION

az servicebus topic create --resource-group $AKS_PERS_RESOURCE_GROUP   --namespace-name $AKS_BUS_NS --name $AKS_TOPIC

az servicebus topic subscription create --resource-group $AKS_PERS_RESOURCE_GROUP --namespace-name $AKS_BUS_NS --topic-name $AKS_TOPIC --name $AKS_SUBSCRIPTION

#######################################################################

# Create a storage account
az storage account create -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -l $AKS_PERS_LOCATION --sku Standard_LRS

# Export the connection string as an environment variable, this is used when creating the Azure file share
export AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string -n $AKS_PERS_STORAGE_ACCOUNT_NAME -g $AKS_PERS_RESOURCE_GROUP -o tsv)

# Create the file share
az storage share create -n $AKS_PERS_SHARE_NAME --connection-string $AZURE_STORAGE_CONNECTION_STRING

# Get storage account key
STORAGE_KEY=$(az storage account keys list --resource-group $AKS_PERS_RESOURCE_GROUP --account-name $AKS_PERS_STORAGE_ACCOUNT_NAME --query "[0].value" -o tsv)

# Echo storage account name and key
echo Storage account name: $AKS_PERS_STORAGE_ACCOUNT_NAME
echo Storage account key: $STORAGE_KEY

##############################################################

# Put files in AZURE FILE SHARE 
# The files to be put are    

1. questions.csv            
2. answers.csv   
3. professionals.csv  
3. Recommender Model Files              

##################################################################

# Build the docker image        
docker build -t reco-tfidf .   

# Run Docker     
docker run -p 8000:8000 reco-tfidf

# Login into the Azure Container Registry    
docker tag reco-tfidf:latest recoacr.azurecr.io/reco:v5 

# Create a Resource Group          
az group create --location centralindia --resource-group recogroup 

# Create a Azure Container Registry    
az acr create --resource-group recogroup --name recoacr --sku Basic 

# Login into the Azure Container Registry     
az acr login -n recoacr   


# Push image into Azure Container Registry  
docker push recoacr.azurecr.io/reco:v5

# Update the  Azure Container Registry 
az acr update -n recoacr --admin-enabled true       

# Create AKS cluster
az aks create \
    --resource-group recogroup \
    --name recoCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr recoacr

# Get AKS cluster credentials
az aks get-credentials --resource-group recogroup --name recoCluster

kubectl create secret generic azure-secret --from-literal=azurestorageaccountname=$AKS_PERS_STORAGE_ACCOUNT_NAME --from-literal=azurestorageaccountkey=$STORAGE_KEY

# Secrets Containing the Service Bus endpoint             
kubectl apply -f secrets.yaml           

# Creating the Persistent Volume and Persistent Volume Claim   
kubectl apply -f pv.yaml

# Create pods and service 
kubectl apply -f reco-pv.yaml


# Cleanup ( Run in Console)   
az group delete --resource-group recogroup



