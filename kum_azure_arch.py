from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import VM
from diagrams.azure.database import CosmosDb
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.integration import LogicApps
from diagrams.azure.network import VirtualNetworks, VirtualNetworkGateways, NetworkSecurityGroupsClassic
from diagrams.azure.security import KeyVaults
from diagrams.onprem.client import Users, Client
from diagrams.onprem.network import Internet
from diagrams.azure.web import AppServices

# Configure the diagram
with Diagram("Azure VM-Logic Apps Architecture with VPN", 
             show=False, 
             direction="TB",
             graph_attr={"rankdir": "TB", "splines": "ortho"}):
    
    # External components
    users = Users("End Users")
    internet = Internet("Internet")
    
    # Azure Active Directory (outside VNet for clarity)
    aad = ActiveDirectory("Azure Active\nDirectory")
    
    # VPN Gateway connection
    vpn_gateway = VirtualNetworkGateways("VPN Gateway")
    
    # Virtual Network
    with Cluster("Azure Virtual Network", graph_attr={"style": "dashed", "color": "blue"}):
        
        # Network Security Group
        nsg = NetworkSecurityGroupsClassic("Network Security\nGroup")
        
        # Frontend Subnet
        with Cluster("Frontend Subnet", graph_attr={"style": "dashed", "color": "green"}):
            frontend_vm = VM("Frontend VM\n(Web Server)")
        
        # Backend Subnet
        with Cluster("Backend Subnet", graph_attr={"style": "dashed", "color": "orange"}):
            logic_app = LogicApps("Logic Apps\n(Backend API)")
        
        # Data Subnet
        with Cluster("Data Subnet", graph_attr={"style": "dashed", "color": "purple"}):
            cosmos_db = CosmosDb("Cosmos DB\n(Database)")
    
    # Azure Services (outside VNet)
    key_vault = KeyVaults("Azure Key Vault\n(Secrets & Certificates)")
    
    # Connection flows
    # User authentication flow
    users >> Edge(label="1. Authentication", color="red") >> aad
    aad >> Edge(label="2. Auth Token", color="red") >> users
    
    # User to application flow through VPN
    users >> Edge(label="3. HTTPS Request", color="blue") >> internet
    internet >> Edge(label="4. VPN Tunnel", color="blue") >> vpn_gateway
    vpn_gateway >> Edge(label="5. Secure Connection", color="blue") >> nsg
    nsg >> Edge(label="6. Web Request", color="blue") >> frontend_vm
    
    # Internal application flow
    frontend_vm >> Edge(label="7. API Call", color="green") >> logic_app
    logic_app >> Edge(label="8. Database Query", color="orange") >> cosmos_db
    cosmos_db >> Edge(label="9. Data Response", color="orange") >> logic_app
    logic_app >> Edge(label="10. API Response", color="green") >> frontend_vm
    
    # Security and configuration
    frontend_vm >> Edge(label="Get Certificates", color="purple", style="dashed") >> key_vault
    logic_app >> Edge(label="Get Secrets", color="purple", style="dashed") >> key_vault
    
    # Authentication for services
    frontend_vm >> Edge(label="Service Auth", color="red", style="dashed") >> aad
    logic_app >> Edge(label="Service Auth", color="red", style="dashed") >> aad
    cosmos_db >> Edge(label="Access Control", color="red", style="dashed") >> aad