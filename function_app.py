import azure.functions as func
import logging
import graph_connect

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="CreateGraphToken")
def CreateGraphToken(req: func.HttpRequest) -> func.HttpResponse:
    
    access_token = graph_connect.create_token()

    sharepointSite=graph_connect.get_GraphAPI(endpoint="sites?search=Data_lake", access_token=access_token)

    return func.HttpResponse(str(sharepointSite))