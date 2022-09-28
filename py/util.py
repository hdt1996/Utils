


def kwargsReturnValues(kwargs:dict,var_names: list) -> tuple:
    var_list = []
    for variable in var_names:
        if kwargs.get(variable) == None:
            if variable == '':
                raise ValueError(f'Check GLOBALS:\n\nEmpty key passed in.\nCheck that there are no duplicate commas or ending commas in global string')
            raise ValueError(f'Missing {variable} in Kwargs. Fix logic for handling passed in/default kwargs to CLI')
        else:
            var_list.append(kwargs[variable])
    return var_list

def splitStringbyDelim(src_string:str,sp_delim:list, cl_delim:list = [],replace:str = '') -> list:
    arr = []
    for sp in sp_delim:
        for item in src_string.split(sp):
            for cl in cl_delim:
                item = item.replace(cl,replace)
            arr.append(item)
    return arr

def buildArrfromDict(data: dict = {}, item_type : type = str, item_delim: str = '', kv:bool = True):
    arr = []
    if not kv:
        for key in data:
            arr.append(data[key])
        return arr
    if item_type == str:
        for key in data:
            arr.append(f"{key}{item_delim}{data[key]} ;")
        return arr
    elif item_type == list:
        for key in data:
            arr.append([key,item_delim,data[key]])
        return arr

def buildDictBoolbyArr(arr: list):
    bool_dict = {}
    for item in arr:
        bool_dict[item] = True
    return bool_dict

def getDictDiffArr(dict_1:dict, dict_2:dict):
    diff_arr = []
    for key in dict_2:
        if key not in dict_1:
            diff_arr.append(key)
    return diff_arr

def getArrUniquesByDict(dict_1:dict) -> list:
    diff_arr = []
    new_dict = {}
    for key in dict_1:
        if new_dict.get(key) == None:
            new_dict[key] = True
            diff_arr.append(key)
    return diff_arr

def buildDictfromArrs(key_arr: list, value_arr: list):
    new_dict = {}
    for index, item in enumerate(key_arr):
        new_dict[item] = value_arr[index]
    return new_dict