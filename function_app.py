import azure.functions as func
import logging
import graph_connect
import pandas as pd

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="CreateGraphToken")
def CreateGraphToken(req: func.HttpRequest) -> func.HttpResponse:
    
    access_token = graph_connect.create_token()
    df=graph_connect.get_sharepointList_by_name(access_token=access_token, siteName="Data_lake", listName="ADCOT_CUENTAS_PLATAFORMAS", columnas_originales=["TIPO", "PROPIETARIO"])
    return func.HttpResponse(str(df))