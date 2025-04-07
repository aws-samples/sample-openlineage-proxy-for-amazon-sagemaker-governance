def dict_get_key_values(dict_search, target_keys, find_set):
    """ Function to crawl a dict and get all distinct values for the target keys (array) into a set """
    if isinstance(dict_search, dict):
        for key, value in dict_search.items():
            if isinstance(value, dict):
                dict_get_key_values(value, target_keys, find_set)
            
            elif isinstance(value, list):
                for item in value: dict_get_key_values(item, target_keys, find_set)
            
            elif key in target_keys:
                complete_keys = True
                target_values = []
                for target_key in target_keys:
                    if target_key in dict_search: target_values.append(dict_search[target_key])
                    else: complete_keys = False
                    
                if complete_keys: find_set.add(tuple(target_values))

def dict_replace_key_values(dict_search: dict, update_map: dict):
    """ Function to crawl a dict and replace values in the update map. The update map maps all keys in the same dict to be updated with their corresponding value """
    if isinstance(dict_search, dict):
        for key, value in dict_search.items():
            if isinstance(value, dict):
                dict_replace_key_values(value, update_map)
            
            elif isinstance(value, list):
                for item in value: dict_replace_key_values(item, update_map)
            
            elif value in update_map.keys(): 
                new_values = update_map[value]
                if set(new_values.keys()) <= set(dict_search.keys()):
                    dict_search.update(new_values)