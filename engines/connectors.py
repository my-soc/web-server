import os
import yaml
import json
import shutil
import base64

from engines.constants import CONNECTORS_INDEX
from engines.constants import COMMANDS_INDEX
from engines.constants import INSTANCES_INDEX
from engines.constants import CONTENT_PATH

from engines.logging import log_debug, log_info, log_error


class Connectors:

    connectors = json.load(open(CONNECTORS_INDEX))
    commands = json.load(open(CONNECTORS_INDEX))
    instances = json.load(open(INSTANCES_INDEX))

    @classmethod
    def get_connectors(cls):
        log_debug("Request to get all connectors")
        result = {
            "status": 'success',
            "payload": {
                "Connectors": cls.connectors
            }
        }
        return result

    @classmethod
    def find_connector(cls, connector_id):
        log_debug(f"Request to find connector: {connector_id}")
        for i in range(len(cls.connectors)):
            if cls.connectors[i]["ID"] == connector_id:
                connector_path = cls.connectors[i].get("Path")
                try:
                    connector_file = open(connector_path, 'r')
                except FileNotFoundError as e:
                    log_error(e)
                    result = {
                        "status": 'fail',
                        "payload": {
                            'message': 'Error (C:2) Connector not found ..'
                        }
                    }
                    return result
                result = {
                    "status": 'success',
                    "payload": yaml.load(connector_file, Loader=yaml.FullLoader)
                }
                return result
        result = {
            "status": 'fail',
            "payload": {
                'message': 'Error (C:1) Connector not found ..'
            }
        }
        return result

    @classmethod
    def register_connector(cls, connector, received_content):
        log_info(f"Request to register connector:{connector}")
        temp_file = open(f'{CONTENT_PATH}/tmp/{connector.filename}', 'wb')
        temp_file.write(received_content)
        temp_file.close()
        file = open(f'{CONTENT_PATH}/tmp/{connector.filename}', 'r')
        path = f'{CONTENT_PATH}/tmp/{connector.filename}'
        try:
            connector = yaml.load(file, Loader=yaml.FullLoader)
            if connector.get('connector') and connector.get('id'):
                new_path = f'{CONTENT_PATH}/connectors/' + connector.get('id') + '/' + connector.get('id') + '.yml'
                try:
                    os.mkdir(f'{CONTENT_PATH}/connectors/' + connector.get('id'))
                except FileExistsError as e:
                    log_error(f'Connector already exists, error details: {e}')
                    file.close()
                    os.remove(path)
                    result = {
                        "status": 'fail',
                        "payload": {
                            "message": 'Error (C:3) Connector already exists ..'
                        }
                    }
                    return result
                file.close()
                shutil.move(path, new_path)
                try:
                    code = connector['connector']['code']
                    with open(f'{CONTENT_PATH}/connectors/' + connector.get('id') + '/' + 'Script.py', 'wt') \
                            as code_file:
                        code_file.write(code)

                    config = connector['parameters']
                    with open(f'{CONTENT_PATH}/connectors/' + connector.get('id') + '/' + 'Config.py', 'wt') \
                            as config_file:
                        config_file.write(json.dumps(config,indent=2))

                    commands = connector['connector']['commands']
                    with open(f'{CONTENT_PATH}/connectors/' + connector.get('id') + '/' + 'Commands.py', 'wt') \
                            as commands_file:
                        commands_file.write(json.dumps(commands, indent=2))

                    logo = base64.b64decode(connector.get('image'))
                    with open(f'{CONTENT_PATH}/connectors/' + connector.get('id') + '/' + 'Logo.png', 'wb') \
                            as logo_file:
                        logo_file.write(logo)

                    for command in connector['connector']['commands']:
                        command_entry = {
                            "Command": command.get('name'),
                            "ID": connector.get('id')
                        }
                        cls.commands.append(command_entry)
                        json.dump(cls.commands, open(COMMANDS_INDEX, 'r+'), indent=2)

                except Exception as e:
                    log_error(e)
                    result = {
                        "status": 'fail',
                        "payload": {
                            "message": 'Error (C:4) while registering the connector ..'
                        }
                    }
                    return result
                connector_entry = {
                    "ID": connector.get('id'),
                    "Name": connector.get('name'),
                    "DisplayName": connector.get('display'),
                    "Version": connector.get('version'),
                    "Description": connector.get('description'),
                    "Image": connector.get('image'),
                    "Path": new_path,
                    "Parameters": connector.get('parameters'),
                    "Instances": []
                }
                cls.connectors.append(connector_entry)
                json.dump(cls.connectors, open(CONNECTORS_INDEX, 'r+'), indent=2)
                result = {
                    "status": 'success',
                    "payload": {
                        "message": 'Connector successfully registered ..'
                    }
                }
                return result
            else:
                result = {
                    "status": 'fail',
                    "payload": {
                        "message": 'Error (C:5) while registering the connector ..'
                    }
                }
                return result
        except Exception as e:
            log_error(e)
            result = {
                "status": 'fail',
                "payload": {
                    "message": 'Error (C:6) while registering the connector ..'
                }
            }
            return result

    @classmethod
    def delete_connector(cls, connector_id):
        log_info(f"Request to delete connector: {connector_id}")

        def delete_commands(commands, connector):
            n = 0
            while n < len(commands):
                print (n,"->",len(commands))
                if commands[n]["ID"] == connector:
                    commands.pop(n)
                    with open(COMMANDS_INDEX, "w") as oldCommandsIndex:
                        json.dump(commands, oldCommandsIndex, indent=2)
                    n = 0
                n += 1

        for i in range(len(cls.connectors)):
            if cls.connectors[i]["ID"] == connector_id:
                connector_path = cls.connectors[i].get("Path")
                try:
                    shutil.rmtree(os.path.dirname(connector_path))
                except Exception as e:
                    log_error(e)
                    result = {
                        "status": 'fail',
                        "payload": {
                            "'message': 'Error (C:7) while deleting the connector ..'"
                        }
                    }
                    return result
                cls.connectors.pop(i)
                with open(CONNECTORS_INDEX, "w") as oldIndex:
                    json.dump(cls.connectors, oldIndex, indent=2)
                delete_commands(cls.commands, connector_id)
                result = {
                    "status": 'success',
                    "payload": {
                        "message": "Connector successfully deleted .."
                    }
                }
                return result
        result = {
            "status": 'fail',
            "payload": {
                "message": "Error (C:8) Connector not found .."
            }
        }
        return result

    @classmethod
    def add_instance(cls, connector_id, received_content):
        log_info(f"Request to add an instance to connector: {connector_id} , instance config: {received_content}")
        temp_connectors = cls.connectors
        for i in range(len(temp_connectors)):
            if temp_connectors[i]["ID"] == connector_id:
                temp_connectors[i]["Instances"].append(received_content.dict())
                with open(CONNECTORS_INDEX, "w") as oldIndex:
                    json.dump(temp_connectors, oldIndex, indent=2)
                result = {
                    "status": 'success',
                    "payload": {
                        'message': 'Config successfully saved ..'
                    }
                }
                return result
        result = {
            "status": 'fail',
            "payload": {
                'message': 'Error (C:9) Connector not found ..'
            }
        }
        return result

    @classmethod
    def delete_instance(cls, connector_id, instance_name):
        log_info(f"Request to delete an instance from connector: {connector_id} , instance name: {instance_name}")
        temp_connectors = cls.connectors
        for i in range(len(temp_connectors)):
            if temp_connectors[i]["ID"] == connector_id:
                for n in range(len(temp_connectors[i]['Instances'])):
                    if temp_connectors[i]['Instances'][n]['configName'] == instance_name:
                        temp_connectors[i]['Instances'].pop(n)
                        with open(CONNECTORS_INDEX, "w") as oldIndex:
                            json.dump(temp_connectors, oldIndex, indent=2)
                        result = {
                            "status": 'success',
                            "payload": {
                                'message': 'Instance successfully deleted ..'
                            }
                        }
                        return result
        result = {
            "status": 'fail',
            "payload": {
                'message': 'Error (C:10) Instance not found ..'
            }
        }
        return result

    @classmethod
    def update_instance(cls, connector_id, instance_name, received_content):
        log_info(f"Request to update an instance on connector: {connector_id} , instance name: {instance_name}, instance config: {received_content}")
        temp_connectors = cls.connectors
        for i in range(len(temp_connectors)):
            if temp_connectors[i]["ID"] == connector_id:
                for n in range(len(temp_connectors[i]['Instances'])):
                    if temp_connectors[i]['Instances'][n]['configName'] == instance_name:
                        temp_connectors[i]['Instances'][n].update(received_content)
                        with open(CONNECTORS_INDEX, "w") as oldIndex:
                            json.dump(temp_connectors, oldIndex, indent=2)
                        result = {
                            "status": 'success',
                            "payload": {
                                'message': 'Instance successfully updated ..'
                            }
                        }
                        return result
        result = {
            "status": 'fail',
            "payload": {
                'message': 'Error (C:11) Instance not found ..'
            }
        }
        return result
