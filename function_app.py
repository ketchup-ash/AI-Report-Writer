import json
import azure.functions as func
import logging

from helpers.database_helper import select_persona_from_db, update_persona_db
from workers.main_worker import download_worker, upload_worker

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="download_file", methods=["POST"])
def download_file(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        response = download_worker(
            file_content=req_body
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
        try:
            item_id = req.params.get('item_id')
            items = select_persona_from_db(item_id=item_id)
        except:
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

@app.route(route="update_sections", methods=["POST"])
def update_sections(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        update_persona_db(req_body)

        return func.HttpResponse(
            body=json.dumps(req_body),
            status_code=200
        )
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            body=e,
            status_code=400
        )


@app.route(route="upload_file", methods=["POST"])
def upload_file(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_data = req.get_json()
        try:
            base64_file = req_data["file"]
        except:
            raise Exception("base64 not found")

        response = upload_worker(base64_file)

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
