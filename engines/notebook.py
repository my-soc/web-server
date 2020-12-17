import json

from engines.constants import ENTRIES_INDEX
from engines.logging import log_debug, log_info, log_error
from engines.wave import Wave


def parse_arguments(arguments: list):
    arguments_dict = {}
    for argument in arguments:
        arguments_dict[argument.split(":")[0]] = argument.split(":")[1].replace("\"", "")
    return arguments_dict


class Notebook:

    @staticmethod
    def get_entries():
        result = {}
        entries = Wave.get_notebook_entries()
        result["status"] = 'success'
        result["payload"] = entries
        return result

    @staticmethod
    def find_entry(entry_id):
        result = {}
        entries = json.load(open(ENTRIES_INDEX))
        for i in range(len(entries)):
            if entries[i]["ID"] == entry_id:
                result["status"] = 'success'
                result["payload"] = entries[i]["Content"]
                return result

        result["status"] = 'fail'
        result["payload"] = {
            "message": "Error (E:1) Entry not found .."
        }
        log_error(f"failed to find entry: {entry_id}")
        return result

    @staticmethod
    def post_entry(entry):
        result = {}
        output = None
        if entry.content.startswith('$'):
            try:
                command = (entry.content[1:].split(' '))
                output = Wave.execute_command(command[0], parse_arguments(command[1:]))
            except Exception as e:
                log_error("Error (E:2) while posting the entry .." + str(e))
            entry_record = {
                "command": entry.content,
                "content": output
            }
        else:
            entry_record = {
                "content": entry.content
            }
        try:
            entry = Wave.store_notebook_entry(entry_record)
            result["status"] = 'success'
            result["payload"] = entry
            return result
        except Exception as e:
            log_error(e)
            result["status"] = 'fail'
            result["payload"] = {
                "message": "Error (E:3) while posting the entry .."
            }
            return result

    @staticmethod
    def delete_entry(entry_id):
        result = {}
        try:
            res = Wave.delete_notebook_entry(entry_id)
            result["status"] = 'success'
            result["payload"] = res
            return result
        except Exception as e:
            log_error(e)
            result["status"] = 'fail'
            result["payload"] = {
                "message": "Error (E:4) Entry not found .."
            }
            return result
