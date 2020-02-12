import requests
import json

### Set all the variables according to your requirements

PROTOCOL = "http"
OPENSTACK_IP = "OPENSTACK IP"
IP = PROTOCOL+"://"+OPENSTACK_IP

IDENTITY_PORT=""
COMPUTE_PORT = ""
NETWORK_PORT = ""

if(PROTOCOL == "http"):
    IDENTITY_PORT="5000"
    COMPUTE_PORT = "8774"
    NETWORK_PORT = "9696"

if(PROTOCOL == "https"):
    IDENTITY_PORT="13000"
    COMPUTE_PORT = "13774"
    NETWORK_PORT = "13696"


USER_NAME = "USER NAME"
USER_PASSWORD = "PASSWORD"

DOMAIN_ID = "DOMAIN"
PROJECT_ID = "PROJECT"

SECURITY_GROUP_NAME = "SECURITY GROUP NAME"

### End



try:
    unscoped_data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": USER_NAME,
                        "domain": {
                            "id": DOMAIN_ID
                        },
                        "password": USER_PASSWORD
                    }
                }
            }
        }
    }

    unscoped_headers = {
        "Content-Type":"application/json"
    }

    print("INITIATE LOGIN")

    login_initiate = requests.post(IP+":"+IDENTITY_PORT+"/v3/auth/tokens", data=json.dumps(unscoped_data), headers=unscoped_headers, verify=False)
    if(login_initiate.status_code != 201 and login_initiate.status_code != 200):
        raise Exception(login_initiate.text)

    unscoped_token = login_initiate.headers['X-Subject-Token']

    scoped_data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id":unscoped_token
                }
            },
            "scope": {
                "project": {
                    "id": PROJECT_ID
                }
            }
        }
    }

    scoped_headers = {
        "Content-Type":"application/json",
        "X-Auth-Token": unscoped_token
    }

    login_final = requests.post(IP+":"+IDENTITY_PORT+"/v3/auth/tokens",data=json.dumps(scoped_data), headers=scoped_headers, verify=False)
    if(login_final.status_code != 201 and login_final.status_code != 200):
        raise Exception(login_final.text)

    print("\nLOGIN SUCCESSFUL")

    token = login_final.headers['X-Subject-Token']
    service_headers = {
        "Content-Type":"application/json",
        "X-Auth-Token":token
    }
    print("\n\nFETCHING SERVERS\n")
    list_servers = requests.get(IP+":"+COMPUTE_PORT+"/v2.1/servers", headers = service_headers, verify=False)
    if(list_servers.status_code != 201 and list_servers.status_code != 200):
        raise Exception(list_servers.text)

    print(list_servers.content.decode("utf-8"))

    print("\n\nFETCHING NETWORKS\n")
    list_networks = requests.get(IP+":"+NETWORK_PORT+"/v2.0/networks/", headers = service_headers, verify=False)
    if(list_networks.status_code != 201 and list_networks.status_code != 200):
        raise Exception(list_networks.text)
        
    print(list_networks.content.decode("utf-8"))

    security_group_data={
        "security_group": {
            "name": SECURITY_GROUP_NAME,
            "description": "create security group from script"
        }
    }
    print("\n\nCREATING SECURITY GROUP\n")
    create_security_group = requests.post(IP+":"+NETWORK_PORT+"/v2.0/security-groups", data=json.dumps(security_group_data), headers = service_headers, verify=False)
    if(create_security_group.status_code != 201 and create_security_group.status_code !=200):
        raise Exception(create_security_group.text)
    print(create_security_group.text)

except Exception as e:
    print(e)