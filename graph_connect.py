import requests
import json
from msal import ConfidentialClientApplication

def create_token(scopes:list=[]):
    """
    create an access token for the current client(aplication instance)
    ----------------------------
    scopes: scopes for the token, related to the desired operation. default obligatory: https://graph.microsoft.com/.default
    """
    client_id="e097ba8b-8279-499a-a77b-261dde85bfa0"
    client_secret="wrP8Q~SepAZOGNCzciUb0qwmIRCh7UDs1mUq5aPj"
    tenant_id="7266cf60-2a18-461e-9a40-171f83b02de5"

    autority=f"https://login.microsoftonline.com/{tenant_id}"

    #handle scopes
    scopes.append("https://graph.microsoft.com/.default")
    msal_scopes=scopes

    msal_app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=autority,
    )

    result=msal_app.acquire_token_silent(
        scopes=msal_scopes,
        account=None,
    )

    if not result:
        result=msal_app.acquire_token_for_client(scopes=msal_scopes)

    if "access_token" in result:
        access_token=result["access_token"]
    else:
        raise Exception("error creando un token"+ str(result))

    return access_token

def get_GraphAPI(endpoint:str, access_token, extra_headers:dict={}):
    """
    uses the Get request onto the graph API and resturn the response in json format
    https://graph.microsoft.com/v1.0/+endpoint

    default header is Authorization: Bearer {access_token}
    """
    graph_endpoint="https://graph.microsoft.com/v1.0/"
    final_endpoint=graph_endpoint+endpoint

    headers={"Authorization": f"Bearer {access_token}"}
    
    #add the extra headers to the request
    for key in extra_headers.keys():
        headers[key] = extra_headers[key]

    #make the get request
    response=requests.get(url=final_endpoint, headers=headers)
    return json.dumps(response.json(), indent=4)