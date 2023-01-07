# Build the docker image        
docker build -t recoui .   

# Run Docker     
docker run -p 5000:5000 recoui

# Login into the Azure Container Registry    
docker tag recoui:latest recoacr.azurecr.io/recoui:v1  

# Create a Resource Group          
```
We do not need this since the Resource Group is already created       

```
az group create --location centralindia --resource-group recogroup 

# Create a Azure Container Registry    
```
We do not need this since the Azure Container Registry  is already created     

```
az acr create --resource-group recogroup --name recoacr --sku Basic 

# Login into the Azure Container Registry     
az acr login -n recoacr   


# Push image into Azure Container Registry  
docker push recoacr.azurecr.io/recoui:v1

# Update the  Azure Container Registry 
az acr update -n recoacr --admin-enabled true       

# Create AKS cluster
```
We do not need this since the AKS cluster  is already created     

```
az aks create \
    --resource-group recogroup \
    --name recoCluster \
    --node-count 1 \
    --generate-ssh-keys \
    --attach-acr recoacr

# Get AKS cluster credentials
az aks get-credentials --resource-group recogroup --name recoCluster

#######################################################

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz


##########################################################
# Create pods and service 
kubectl apply -f reco.yaml

# Cleanup ( Run in Console)   
az group delete --resource-group recogroup