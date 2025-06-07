from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import KubernetesServices, ContainerRegistries
from diagrams.azure.database import SQLDatabases, CosmosDb
from diagrams.azure.devops import Pipelines
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.monitor import Monitor
from diagrams.azure.network import LoadBalancers, VirtualNetworks
from diagrams.azure.security import KeyVaults
from diagrams.azure.storage import BlobStorage
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.onprem.client import Users, Client
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Prometheus
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.vcs import Git

# Configure the diagram
with Diagram("Azure Kubernetes Service (AKS) Architecture", 
             show=False, 
             direction="LR",
             graph_attr={"rankdir": "LR", "splines": "ortho"}):
    
    # External clients
    client_apps = Client("Client apps")
    devops = Users("Dev/Ops")
    
    # CI/CD Pipeline
    cicd = Pipelines("Azure\nPipelines")
    
    # Load Balancer
    load_balancer = LoadBalancers("Azure Load\nBalancer")
    
    # Container Registry
    container_registry = ContainerRegistries("Azure\nContainer\nRegistry")
    
    # External Data Stores
    with Cluster("External\ndata stores"):
        sql_db = SQLDatabases("SQL Database")
        cosmos_db = CosmosDb("Azure\nCosmos DB")
    
    # AKS Cluster
    with Cluster("Azure Kubernetes Service (AKS)", graph_attr={"style": "dashed"}):
        
        # Frontend namespace
        with Cluster("Front end", graph_attr={"style": "dashed"}):
            ingress = Ingress("Ingress")
        
        # Backend services namespace  
        with Cluster("Back-end services", graph_attr={"style": "dashed"}):
            backend_pod1 = Pod("Pod")
            backend_pod2 = Pod("Pod")
            autoscaling_pod = Pod("Pod\nautoscaling")
        
        # Utility services namespace
        with Cluster("Utility services", graph_attr={"style": "dashed"}):
            elasticsearch = Elasticsearch("Elasticsearch")
            prometheus = Prometheus("Prometheus")
    
    # Virtual Network
    vnet = VirtualNetworks("Virtual network")
    
    # Azure Services
    active_directory = ActiveDirectory("Azure Active\nDirectory")
    monitor = Monitor("Azure\nMonitor")
    key_vault = KeyVaults("Azure\nKey Vault")
    
    # Connections
    client_apps >> load_balancer >> ingress
    
    ingress >> [backend_pod1, backend_pod2]
    backend_pod1 >> autoscaling_pod
    backend_pod2 >> autoscaling_pod
    
    autoscaling_pod >> sql_db
    autoscaling_pod >> cosmos_db
    
    # CI/CD flow
    devops >> cicd
    cicd >> Edge(style="dashed") >> container_registry
    container_registry >> Edge(style="dashed") >> ingress
    
    # Docker operations
    docker_push = Docker("Docker\npush")
    docker_pull = Docker("Docker\npull")
    cicd >> docker_push >> container_registry
    container_registry >> docker_pull >> ingress
    
    # Role-based access control
    devops >> Edge(label="Role-based\naccess control") >> active_directory
    
    # Monitoring and security
    [backend_pod1, backend_pod2, autoscaling_pod] >> monitor
    [backend_pod1, backend_pod2, autoscaling_pod] >> key_vault