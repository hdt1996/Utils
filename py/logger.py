import os
from datetime import datetime
from .file_manager import FileManager
from .dev import Development
from .directory import *
from datetime import datetime
FS = FileManager()
DEV = Development()

class Logger():
    def __init__(self, proj_name: str = 'General'):
        self.debug_dict = {}
        self.proj_name = proj_name
        os.makedirs(name = os.path.join(LOG_DIR,proj_name), exist_ok=True)

    def recurseLogDict(self,debug:bool = True, custom:str = '',isolate: list = [], db_dict :dict = None) -> str:
        """
        Should be called to build large string of nested HTML elements
        """
        var_log = []
        if db_dict == None:
            db_dict = self.debug_dict

        db_dict_length = len(db_dict)
        for index, var in enumerate(db_dict):
            if var == f"File {index}" :
                per_file_arr = []
                per_file_arr.append(f"----------------------------File {index}------------------------------\n\n")
                per_file_arr.append('\n'.join(self.recurseLogDict(debug = debug, custom = custom,  isolate = isolate, db_dict = db_dict[var])))
                var_log.append('\n')
                var_log.append('\n'.join(per_file_arr))
                continue
            if len(isolate) >=1 and not var in isolate:
                continue
            if index == db_dict_length - 1:
                var_log.append(f"\r{var} ------------- Type: {type(db_dict[var])} ---------------------- Value:----------------\n{db_dict[var]}")
                break
            var_log.append(f"\r{var} ------------- Type: {type(db_dict[var])} ---------------------- Value:----------------\n{db_dict[var]}")

        #should be string only if it reaches here

        #print('Recursion Count: ', COUNT,'\n','build:\n',build)
        return var_log

    def saveLog(self, log: str, title: str = None):
        log_file_name = f"{datetime.now().strftime('%Y_%m_%d')}{f'_{title}' if title != None else ''}.txt"
        FS.writeText(file = os.path.join(LOG_DIR, self.proj_name, log_file_name), text = log, overwrite= False, num_prefix='_LOG_')

    def logVars(self,debug:bool = True, custom:str = '',isolate: list = [], db_dict :dict = None, save:bool = False, to_terminal:bool = True, title: str = None) -> None:
        if not debug:
            return
        var_log = []
        if db_dict == None:
            db_dict == self.debug_dict

        var_log.append(''.join(self.recurseLogDict(debug = debug, custom = custom, isolate = isolate, db_dict = db_dict)))
        var_log = '\n'.join(var_log)
        log = \
        f"""
        \r\n------------DEBUG LOGS-------------Time: {datetime.now()}\n
        {var_log}
        {custom}

        """
        if to_terminal:
            print(log)
        if save:
            self.saveLog(log = log, title = title)
    def addKeyDBVars(self, var_list:list, var_values):
        if len(var_values) > 0:
            for item in var_values:
                if not isinstance(item, str):
                    raise TypeError ('You passed in an array with nested Dictionaries. Please use addArrDBVars method instead.')
        if len(var_list) != len(var_values):
            raise ValueError("List arguments passed in must match. Variable Names --> Variable Values")
        for index, name in enumerate(var_list):
            self.debug_dict[name]=var_values[index]

    def addArrDBVars(self, arr: list):
        if not isinstance(arr, list):
            raise TypeError('Array is not passed into argument for arr.')
        for num, d in enumerate(arr):
            self.debug_dict[f"File {num}"] = d

    def traceRelevantErrors(self,error_log:list,script_loc:os.PathLike,latest = False):
        new_error_log = []
        proj_files_dict = FS.findFilesbyExt(file_type = '.py',location = script_loc.replace('main.py',''), dict_keys=True)
        error_length = len(error_log)
        for index, error_file in enumerate(error_log):
            file_name = os.path.join(error_file.split(", line")[0].replace(' ','').replace('"',''))
            if file_name.upper() in proj_files_dict and index < error_length:
                new_error_log.append(error_file)
            else:
                pass
        new_error_log.append(error_log[error_length - 1])
        if latest:
            print('\nMy Error\n')
            print(new_error_log.pop())
        else:
            print('\nMy Error\n')
            print('\n'.join(new_error_log))


