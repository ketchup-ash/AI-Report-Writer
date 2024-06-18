import base64
import logging
from helpers.document_helper import create_document, doc_to_base64

def download_worker(
        file_content: list
):
    try:
        buffer = create_document(
            file_content=file_content
        )

        base64file = doc_to_base64(
            buffer=buffer
        )

        #############################################
        # file_bytes = base64.b64decode(base64file)

        # with open('output.docx', 'wb') as f:
        #     f.write(file_bytes)
        #############################################

        return {
            "file": base64file
        }
    except Exception as e:
        logging.error(str(e))
        raise Exception(f"Error in download_workder: {e}") from e
