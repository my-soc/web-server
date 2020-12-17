import importlib
from engines.constants import VERSION
from engines.database import Database
from engines.connectors import Connectors


class Wave:
    # Constructor
    def __init__(self):
        pass

    @staticmethod
    def get_version():
        return {
            "status": "success",
            "payload": {
                "Version": VERSION
            }
        }

    # Database Static Methods
    @staticmethod
    def load_sample_data(data_type: str):
        if Database.load_sample_data(data_type):
            return {"message": f"Sample {data_type} data is loaded .."}
        else:
            return {"message": f"Failed to load sample {data_type} data .."}

    @staticmethod
    def delete_sample_data(data_type: str):
        if Database.delete_sample_data(data_type):
            return {"message": f"Sample {data_type} data is deleted .."}
        else:
            return {"message": f"Failed to delete sample {data_type} data .."}

    @staticmethod
    def execute_command(command, args):
        for command_object in Connectors.commands:
            if command_object['Command'] == command:
                module = "content.connectors." + command_object['ID'] + "." + command_object['ID']
                connector = importlib.import_module(module, ".")
                instance = connector.Connector()
                return instance.execute(command, args)
        return "Command Not Found"

    @staticmethod
    def get_notebook_entries():
        return Database.get_docs(index="notebook")

    @staticmethod
    def store_notebook_entry(entry_content):
        return Database.store_doc(index="notebook", data=entry_content)

    @staticmethod
    def delete_notebook_entry(entry_id):
        return Database.delete_doc(index="notebook", doc_id=entry_id)
