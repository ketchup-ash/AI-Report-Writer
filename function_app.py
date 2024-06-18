import json
import azure.functions as func
import logging

from helpers.database_helper import select_persona_from_db, update_persona_db
from workers.main_worker import download_worker

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="download_file", methods=["POST"])
def download_file(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        file_content = req_body.get('file_content', [])

        response = download_worker(
            file_content=file_content
        )

        return func.HttpResponse(
            body=json.dumps(response),
            status_code=200
        )
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            body=e,
            status_code=400
        )

@app.route(route="get_sections", methods=["GET"])
def get_sections(req: func.HttpRequest) -> func.HttpResponse:
    try:
        items = select_persona_from_db()

        return func.HttpResponse(
            body=json.dumps(items),
            status_code=200
        )
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            body=e,
            status_code=400
        )

@app.route(route="update_sections", auth_level=func.AuthLevel.ANONYMOUS)
def update_sections(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        update_persona_db(req_body)

        return func.HttpResponse(
            body="Data successfully updated or inserted.",
            status_code=200
        )
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            body=e,
            status_code=400
        )
