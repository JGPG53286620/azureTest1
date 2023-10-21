import azure.functions as func
import logging
import AccesList as access_list

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="SharePointAccessList")
def SharePointAccessList(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    function_result=access_list.connectSharepoint()

    return func.HttpResponse(function_result, status_code=200)
