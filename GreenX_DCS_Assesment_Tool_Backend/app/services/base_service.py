import re

class BaseService:
    def __init__(self, repository) -> None:
        self._repository = repository

    def get_list(self, schema):
        return self._repository.read_by_options(schema)

    def get_by_id(self, id: int):
        return self._repository.read_by_id(id)

    def add(self, schema):
        return self._repository.create(schema)

    def patch(self, id: int, schema):
        return self._repository.update(id, schema)

    def patch_attr(self, id: int, attr: str, value):
        return self._repository.update_attr(id, attr, value)

    def put_update(self, id: int, schema):
        return self._repository.whole_update(id, schema)

    def remove_by_id(self, id):
        return self._repository.delete_by_id(id)




def is_valid_name(name: str) -> bool:
    
    if name == "" or name.lower() == "string":
        return False

    # Define a regex pattern that disallows any special characters
    # and checks the conditions mentioned
    regex = r"^[a-zA-Z0-9][a-zA-Z0-9 '-]+$"

    if re.match(regex, name) and not any(char in name for char in "!@#$%^&*()_+=[]{}|;:'\",.<>/?\\`~"):
        return True
    else:
        return False
    

def is_valid_description(description: str) -> bool:
    if description == "" or description.lower() == "string":
        return False

    # Define a regex pattern that allows the specified characters
    regex = r"^[a-zA-Z0-9][a-zA-Z0-9 '.,;():-]+$"

    if re.match(regex, description):
        return True
    else:
        return False
