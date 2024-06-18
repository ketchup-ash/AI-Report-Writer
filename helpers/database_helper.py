import logging
from azure.cosmos import CosmosClient, PartitionKey

from helpers.file_system_helper import get_required_env

def get_persona_database_container():
    try:
        URL = get_required_env("DB_URL")
        KEY = get_required_env("DB_KEY")
        DATABASE_NAME = get_required_env("DB_NAME")
        CONTAINER_NAME = get_required_env("DB_CONTAINER_NAME")

        client = CosmosClient(URL, credential=KEY)
        
        database = client.create_database_if_not_exists(id=DATABASE_NAME)
        container = database.create_container_if_not_exists(
            id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/id"),
            offer_throughput=400
        )

        return container
    except Exception as e:
        logging.error(str(e))
        raise e

def update_persona_db(
        data: dict
):
    try:
        container = get_persona_database_container()
        
        final_obj = {
            "id": list(data.keys())[0],
            "section": list(data.keys())[0],
            "persona": list(data.values())[0]
        }

        container.upsert_item(final_obj)
    except Exception as e:
        logging.error(str(e))
        raise e

def select_persona_from_db():
    try:
        container = get_persona_database_container()
        query = "SELECT * FROM c"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        modified_items = {}
        for i in items:
            modified_items[i["section"]] = i["persona"]

        return modified_items
    except Exception as e:
        logging.error(str(e))
        raise e
