# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

sudo chmod 666 /var/run/docker.sock

# Build the docker image        
docker build -t reco-servicebus .   

# Run Docker     
docker run -p 8000:8000 reco-servicebus

# Login into the Azure Container Registry    
docker tag reco-servicebus:latest recoacr.azurecr.io/reco-servicebus:v2 

# Create a Resource Group       
```
We do not need this since the Resource Group is already created     

```

az group create --location centralindia --resource-group recogroup 

# Create a Azure Container Registry    
```
We do not need this since the  Azure Container Registry  is already created     

```
az acr create --resource-group recogroup --name recoacr --sku Basic 

# Login into the Azure Container Registry     
az acr login -n recoacr   


# Push image into Azure Container Registry  
docker push recoacr.azurecr.io/reco-servicebus:v2

# Update the  Azure Container Registry 
az acr update -n recoacr --admin-enabled true       

# Create AKS cluster

```
We do not need this since the  AKS Cluster  is already created     

```
az aks create \
    --resource-group recogroup \
    --name recoCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr recoacr

# Get AKS cluster credentials
az aks get-credentials --resource-group recogroup --name recoCluster

kubectl apply -f secrets.yaml

# Create pods and service 
kubectl apply -f reco.yaml

# Cleanup ( Run in Console)  

```
We do not need cleanup  now     

```
az group delete --resource-group recogroup



