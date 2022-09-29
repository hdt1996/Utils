import os
import pandas as pd
from .util import *
from .src.txt_encoding import ENCODINGS
import shutil
import re


class FileManager():
    def __init__(self):
        print('\n\n Init FileManager')

    def copyDir(self, src: os.PathLike, dst: os.PathLike):
        os.makedirs(name = dst, exist_ok=True)
        for pth in os.scandir(src):
            name = pth.name
            loc = pth.path
            if os.path.isfile(path = loc):
                shutil.copy(src = pth, dst = os.path.join(dst,name))
            elif os.path.isdir(s = loc):
                self.copyDir(src = loc, dst = os.path.join(dst,name))


    def findFilesbyExt(self,file_type:str = '', location: str = os.PathLike, dict_keys: bool = False, open_file: bool = False) -> list:
        if (not os.path.isdir(location)) and (not os.path.isfile(location)):
            if open_file == True:
                raise ValueError('File does not exist. Please review your --location CLI argument')
            return []
        file_list = []
        if os.path.isfile(path = location):
            if file_type == '':
                return [location]
            raise ValueError('File passed in to this method. File_type not necessary. Please remove file_type from CLI args to proceed.')
        for file in os.scandir(location):
            f_path = file.path
            if os.path.isfile(f_path) and f_path.endswith(file_type):
                file_list.append(f_path)
            elif os.path.isdir(f_path):
                file_list.extend(self.findFilesbyExt(file_type = file_type, location = f_path))
        if dict_keys:
            dict_obj = {}
            for f in file_list:
                dict_obj[f.upper()] = True
            file_list = dict_obj
        return file_list

    def extractText(self,file: os.PathLike, open_file: bool = False) -> str:
        if open_file == True:
            for index, encoder in enumerate(ENCODINGS):
                try:
                    with open(file = file, mode = 'r',encoding = encoder) as f:
                        txt = ''.join(f.readlines())
                        f.close()
                        return txt
                except:
                    pass
            raise ValueError(f'Unable to extract text from file. Add additional encoder.')
            
        else:
            return file
    def getDuplicNum(self, name: str, ext: str, num_prefix: str):
        num = 1
        while os.path.isfile(os.path.join(f"{name}{num_prefix}{num}.{ext}")):
            num+=1
        return num

    def removeLinesbyOrder(self, file: os.PathLike, num_list:list = None, overwrite: bool = False):
        if num_list == None:
            return
        num_map = {}
        for n in num_list:
            num_map[n] = True
        max_num = max(num_list)
        with open(file = file, mode = 'r') as f:
            modified_text = []
            lines = f.readlines()
            index = 1
            for line in lines:
                if line == '\n':
                    continue
                if index not in num_map:
                    modified_text.append(line)
                else:
                    pass
                if index == max_num:
                    index = 1
                    continue
                index += 1
            f.close()
        if overwrite:
            self.writeText(file = file, text= ''.join(modified_text),overwrite=True)
        else:
            self.writeText(file = file, text= ''.join(modified_text),overwrite=False)

    def getDatafromFile(self, file_loc: os.PathLike, return_type: type = dict, titles: int= None, col_to_index = None, srs_col_num = None):
        data = pd.read_csv(filepath_or_buffer = file_loc, header = titles)
        if return_type == dict:
            if col_to_index != None:
                data = data.set_index(col_to_index)
            data.index.name = 'Index'
            data = data.to_dict()['Index']
        elif return_type in [list, tuple, set, pd.Series]:
            data = data[srs_col_num]
            if return_type == pd.Series:
                return data[srs_col_num]
            data = data.to_list()
            if return_type == tuple:
                data = tuple(data)
            elif return_type == set:
                data = set(data)
        elif return_type == pd.DataFrame:
            pass
        else:
            raise TypeError('Return type you requested is not allowed in this method')
        return data
        
    def delimText(self,file: os.PathLike, overwrite: bool = False, num_prefix: str = '', delim: str = ';') -> str:
        for index, encoder in enumerate(ENCODINGS):
            try:
                if overwrite == False:
                    file_split = file.split('.')
                    ext = file_split.pop()
                    new_name = f"{''.join(file_split)}{num_prefix}{self.getDuplicNum(name = file_split[0], ext = ext, num_prefix = num_prefix)}.{ext}"
                    shutil.copy(src = file, dst = new_name)
                else:
                    new_name = file
                new_text = []
                with open(file = new_name, mode = 'r', encoding = encoder) as f:
                    for line in f.readlines():
                        for sp in line.split(delim):
                            new_text.append(f"{sp}\n")
                    f.close()
                cln_txt = []
                for i in new_text:
                    if i != '\n':
                        cln_txt.append(i)
                del new_text
                cln_txt.sort()
                cln_txt = ''.join(cln_txt)
                cln_txt = re.sub('[\n]{2}','\n',cln_txt)
                with open(file = new_name, mode = 'w', encoding = encoder) as f:
                    f.write(cln_txt)
                    f.close()
                return
            except:
                pass
        raise ValueError(f'Unable to read or write text file. Add additional encoder.')
        

    def writeText(self,file: os.PathLike, text:str = '', overwrite: bool = False, num_prefix: str = '_RESULTS_') -> str:
        for index, encoder in enumerate(ENCODINGS):
            try:
                if overwrite == False:
                    file_split = file.split('.')
                    ext = file_split.pop()
                    new_name = f"{''.join(file_split)}{num_prefix}{self.getDuplicNum(name = file_split[0], ext = ext, num_prefix = num_prefix)}.{ext}"
                    with open(file = new_name, mode = 'w', encoding = encoder) as f:
                        f.writelines(text)
                        f.close()
                        return (text, new_name)
                else:
                    with open(file = file, mode = 'w', encoding = encoder) as f:
                        f.writelines(text)
                        f.close()
                        return (text, file)
            except:
                pass
        raise ValueError(f'Unable to write text file. Add additional encoder.')

#FS = FileManager()
#FS.delimText(file = "C:\\Users\\hduon\\Documents\\Enzyme\\configurator\\apis\\Utilities\\src\\CSS_SRC.txt")