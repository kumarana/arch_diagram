from diagrams import Diagram, Cluster
from diagrams.azure.compute import FunctionApps
from diagrams.azure.network import ApplicationGateway
from diagrams.azure.database import SQLDatabases
from diagrams.azure.identity import ActiveDirectory
from diagrams.custom import Custom

with Diagram("githubtest_arch", show=True):
    # Substitute for Azure Active Directory
    auth = ActiveDirectory("Azure AD Auth")

    # NGINX Web Server - using Azure Application Gateway to represent it
    nginx = ApplicationGateway("NGINX Web Server")

    # Application Layer: TypeScript backend
    with Cluster("Application Layer"):
        typescript_server = FunctionApps("TypeScript Server")

    # Database Layer: MS SQL
    database = SQLDatabases("MS SQL Server")

    # Connections
    auth >> nginx               # Auth flows through web tier
    nginx >> typescript_server # Web to App
    typescript_server >> database  # App to DB
