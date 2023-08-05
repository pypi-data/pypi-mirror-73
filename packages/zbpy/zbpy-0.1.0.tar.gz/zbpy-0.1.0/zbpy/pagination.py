import pandas as pd
import numpy as np
import json 
import pickle
from ast import literal_eval

class PaginationHandler():

    def __init__(self, f):
        """
        Initializes instance of PaginationHandler class.

        Parameters:
            f: paginationRequester - func (int) -> (dict[string][byte], bool) 
        """
        self.requester = f #paginationRequester func (int) -> (dict[string][]byte, bool)
        self.cur_data = None #dict[string][]byte
        self.cur_page = -1 #int
        self.has_next_page = True #bool
        self.cur_i = 0
        self.cur_keys = []
        self.return_dict = False 

    def __iter__(self):
        return self 

    def __next__(self):
        if self.cur_keys == []:
            self.cur_keys = self.keys()

        if self.cur_i >= len(self.cur_keys):
            if self.has_next_page:
                self.next()
                self.cur_keys = self.keys()
                self.cur_i = 0
            else:
                raise StopIteration()

        cur_key = self.cur_keys[self.cur_i]
        cur_item = self.cur_data[cur_key]
        self.cur_i += 1 


        try:
            if self.return_dict:
                return literal_eval(cur_item.decode())

            elif cur_item is not None:
                return cur_item
                
            else:
                return cur_key
        except AttributeError:
            #Comes to this if (return literal_eval(cur_item.decode())) fails because cur_item is None
            return cur_key
        except UnicodeDecodeError:
            #Comes to this if (return literal_eval(cur_item.decode())) fails because cur_item is np array
            return pickle.loads(cur_item)
        #{cur_key:literal_eval(cur_item.decode())}

    def return_pretty(self):
        """
        Will make items return as Python dictionaries or numpy arrays when PaginationHandler is iterated through. 
        """
        self.return_dict = True 

    def return_bytes(self):
        """
        Will make items return as bytes when PaginationHandler is iterated through. 
        """
        self.return_dict = False 
    
    def data(self):
        """
        Returns dict that maps strings to a list of bytes. 
        """
        return self.cur_data 

    def keys(self):
        """
        Returns a list of strings. 
        """
        keys = []
        for key in self.cur_data:
            keys.append(key)
        return keys 

    def data_all(self):
        """
        Returns a dict that maps strings to a list of bytes.
        """
        i = 1
        data = self.cur_data
        while(self.has_next_page):
            dat, nxt = self.requester(i)
            for key in dat:
                data[key] = dat[key]
            i += 1
            self.has_next_page = nxt 
            self.cur_page = i 
            if len(dat) == 0 or not nxt:
                break 
        
        self.has_next_page = False 
        self.cur_data = data  
        return self.cur_data

    def keys_all(self):
        """
        Returns a list of string.
        """
        ks = []
        for k in self.cur_data:
            ks.append(k)

        if not self.has_next_page:
            return ks 
        
        i = 1
        while(True):
            dat, nxt = self.requester(i)
            for k in dat:
                ks.append(k)
                self.cur_data[k] = None 
            i += 1 
            self.has_next_page = nxt 
            self.cur_page = i 
            if len(dat) == 0 or not nxt:
                break 
        
        self.has_next_page = False 
        return ks
    
    def next(self):
        """
        Changes the current data stored in the pagination handler to the next page if there is one. 
        """
        if not self.has_next_page:
            return 

        self.cur_page += 1 
        dat, nxt = self.requester(self.cur_page)
        
        self.cur_data = dat
        self.has_next_page = nxt  

    def to_dataframe(self):
        """
        Transforms all data in PaginationHandler into pandas.DataFrame.
        """
        indices = []
        df_data = {}

        all_data = self.data_all()
        for i in all_data:
            indices.append(i)

            #turn entry from bytes to python dictionary 
            to_dict = all_data[i].decode()
            entry = literal_eval(to_dict.replace('null', 'None'))
            for key in entry: 
                if key not in df_data:
                    df_data[key] = [entry[key]]
                else:
                    df_data[key].append(entry[key])

        return pd.DataFrame(df_data, index=indices)
            
        
def standard_pagination_handler(f):
    """
    Returns an object of class PaginationHandler.
    
    Parameters: 
        f: paginationRequester - func (int) -> (dict[string][byte], bool) 
    """
    ph = PaginationHandler(f)
    ph.next()
    return ph