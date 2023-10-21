import requests
import json
from msal import ConfidentialClientApplication
import pandas as pd

#Desarrollado con Microsoft Graph v1.0
#Sujeto a errores dependiendo de los cambios de Graph en versiones futuras

def create_token(scopes:list=[]):
    """
    create an access token for the current client(aplication instance)
    ----------------------------
    scopes: scopes for the token, related to the desired operation. default obligatory: https://graph.microsoft.com/.default
    -------------------------------
    example scopes: ['Mail.Send', 'Mail.ReadWrite']
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
    return response.json()

def transform_json_Dataframe(original_json, columnas_originales:list):
    """
    transforma el objeto JSON obtenido desde Graph y lo transforma en el dataframe correspondiente
    OJO:tener en cuenta que las columnas id y titulo ya vinen pór defecto [id, Title, ....los demas nombres].
    """
    #filtrar para mantener las columnas originales
    columnas=["id", "Title"]
    for nombre in columnas_originales:
        columnas.append("field_"+nombre)

    new_nombres={}
    for old_name in columnas:
        new_nombres[old_name] = old_name.replace("field_", "")

    df = pd.DataFrame([item['fields'] for item in original_json['value']])
    df = df[columnas]
    df = df.rename(columns=new_nombres)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    #["id", "Title", "field_TIPO", "field_PROPIETARIO"]
    return df

def get_sharepointList_by_id(access_token, siteId:str, listId:str, columnas_originales:list):
    """
    Obtener una lista de sharepoint teniendo en cuenta el id de la pagina, y el id de la lista deseada.
    columnas originales: una lista con los nombres de las columnas que estaban originalemente en el dataframe
    --------------------------------------------
    retorna: df: lista de sharepoint
    --------------------------------------------
    ejemplos: (ver hasta abajo)
    *siteId: glouphi.sharepoint.com,ac20f787-60ac-4d06-b24c-e79f3c8df836,78daa70c-32c5-4ee5-bb96-2dd7d5644dea\n
    *listId: e6f28343-c325-49d5-a4dd-1152b2d07bbd\n
    *columnas originales: ["TIPO", "PROPIETARIO"]
    """

    sharepointSite=get_GraphAPI(endpoint=f"sites/{siteId}/lists/{listId}/items?expand=fields", access_token=access_token)
    df=transform_json_Dataframe(sharepointSite, columnas_originales)
    return df

def get_siteId(name:str, access_token):
    """
    Obetener el id de una lista dado su nombre
    --------------------
    retorna: str: site_id
    """
    response_json=get_GraphAPI(endpoint=f"sites?search={name}", access_token=access_token)
    if "id" in response_json["value"][0]:
        site_id=response_json["value"][0]["id"]
        return site_id
    else:
        raise Exception(f"La pagina con nombre {name} no se ha encontrado, verifique que este escrito correctamente o que exista dicho recurso.")

def get_listId_with_site_id(siteId:str, name:str, access_token):
    """
    Obtener el id de una lista (con el id del sitio)
    -----------------------
    retorna: str: list_id
    """
    response_json=get_GraphAPI(endpoint=f"sites/{siteId}/lists?search={name}", access_token=access_token)
    if "id" in response_json["value"][0] and (response_json["value"][0]["name"]==name or response_json["value"][0]["displayName"]==name):
        list_id=response_json["value"][0]["id"]
        return list_id
    else:
        raise Exception(f"La lista con nombre {name} no se ha encontrado, verifique que este escrito correctamente o que exista dicho recurso.")

def get_listId_whit_siteName(siteName:str, name:str, access_token):
    """
    Obtener el id de una lista (con el nombre del sitio)
    ------------------
    retorna: list: [site_id, list_id]
    """
    #obtener el id del sitio
    siteId = get_siteId(siteName, access_token=access_token)
    
    #obtener el id de la lista
    response_json=get_GraphAPI(endpoint=f"sites/{siteId}/lists?search={name}", access_token=access_token)
    if "id" in response_json["value"][0] and (response_json["value"][0]["name"]==name or response_json["value"][0]["displayName"]==name):
        list_id=response_json["value"][0]["id"]
        return siteId,list_id
    else:
        raise Exception(f"La lista con nombre {name} no se ha encontrado, verifique que este escrito correctamente o que exista dicho recurso.")

def get_sharepointList_by_name(access_token, siteName:str, listName:str, columnas_originales:list):
    """
    Obtener una lista de sharepoint teniendo en cuenta el nombre de la pagina, y el nombre de la lista deseada.
    columnas originales: una lista con los nombres de las columnas que estaban originalemente en el dataframe
    --------------------------------------------
    retorna: df: lista de sharepoint
    ----------------------------------------
    ejemplos: (ver hasta abajo)
    *siteName: Data_lake\n
    *listName: ADCOT_CUENTAS_PLATAFORMAS\n
    *columnas originales: ["TIPO", "PROPIETARIO"]
    """
    siteId, listId= get_listId_whit_siteName(siteName=siteName, name=listName, access_token=access_token)
    sharepointSite=get_GraphAPI(endpoint=f"sites/{siteId}/lists/{listId}/items?expand=fields", access_token=access_token)
    df=transform_json_Dataframe(sharepointSite, columnas_originales)
    return df