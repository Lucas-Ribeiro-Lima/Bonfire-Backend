def checkKeysInJson(data, keys_to_check):
    if isinstance(data, list):
        for item in data:
            if not all(key in item for key in keys_to_check):
                return False
        return True
    return False