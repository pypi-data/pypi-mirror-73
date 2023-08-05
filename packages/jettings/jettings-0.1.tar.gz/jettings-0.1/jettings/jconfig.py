#!/user/bin/env python3
import json
import sys
import os
from pathlib import Path

class Jettings:

    def __init__(self, config_filepath):
        self.config_filepath=config_filepath
        self.__init_jconfig_file(self.config_filepath)


    def __dic_nested_set(self,dic,list_pathkeys,a_value):
        #USAGE
        #Usage example: 
        #                   __dic_nested_set(my_dict,['key1','key2','key3'],a_value)
        # equivalent to     my_dict['key1']['key2']['key3']=a_value
        # .setdefault       if key does not exist, "my_dic.setdefault(key,value)"
        #                   inserts key with the specified value. 
        #                   value could be another empty dic, {}.

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(dic, dict) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
        if not isinstance(a_value, (dict,list,tuple,str,int,float,None)) == True : raise TypeError

        #IMPLEMENTATION
        for key in list_pathkeys[:-1]:
            dic = dic.setdefault(key,{})
        dic[list_pathkeys[-1]] = a_value

    def __dic_nested_get(self,dic,list_pathkeys):
        #WARNING:  
        #This method uses RECURSION, it recurses, calls itself, until it hits its exit
        #condition, when the forwarded pathkeys variable is chopped down to lenth zero.

        #USAGE:
        #Usage example:
        #                   __dic_nested_get(my_dict,['key1','key2','key3'])
        #equivalent to      my_dict['key1']['key2']['key3']

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(dic, (dict,str)) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
        
        #IMPLEMENTATION
        if len(list_pathkeys) == 0:
            return dic
        else:
            return self.__dic_nested_get(dic[list_pathkeys[0]], list_pathkeys[1:])

    def __dic_nested_del(self,dic,list_pathkeys):
        #USAGE
        #Usage example: 
        #                   __dic_nested_set(my_dict,['key1','key2','key3'],a_value)
        # equivalent to     my_dict['key1']['key2']['key3']=a_value
        # .setdefault       if key does not exist, "my_dic.setdefault(key,value)"
        #                   inserts key with the specified value. 
        #                   value could be another empty dic, {}.

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(dic, dict) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError

        #IMPLEMENTATION
        for key in list_pathkeys[:-1]:
            dic = dic.setdefault(key,{})
        del dic[list_pathkeys[-1]]

    def __json_nested_set(self,json_string, list_pathkeys, a_value):
        #USAGE
        #Usage example: 
        #                       __json_nested_set(json_string,['key1','key2','key3'],a_value)
        #python dict equivalent to     json_dict['key1']['key2']['key3']=a_value
        
        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(json_string, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
        if not isinstance(a_value, (dict,list,tuple,str,int,float,None)) == True : raise TypeError
        
    
        #IMPLEMENTATION
        try:
            dic=json.loads(json_string)
        except:
            raise RuntimeError ( "Could not parse JSON")

        self.__dic_nested_set(dic,list_pathkeys, a_value)

        #RETURN
        #Returns the modified json string
        return json.dumps(dic)


    def __json_nested_get(self,json_string, list_pathkeys):
        #USAGE:
        #Usage example:
        #                               __json_nested_get(my_dict,['key1','key2','key3'])
        #pyhton dict equivalent to      json_dict['key1']['key2']['key3']

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(json_string, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError

        #IMPLEMENTATION
        #convert json string to python dict
        dic=json.loads(json_string)

        #RETURN
        #Retuns the json value refenenced json keys
        return self.__dic_nested_get(dic,list_pathkeys)
        pass

    def __json_nested_del(self,json_string, list_pathkeys):
        #USAGE
        #Usage example: 
        #                       __json_nested_set(json_string,['key1','key2','key3'],a_value)
        #python dict equivalent to     json_dict['key1']['key2']['key3']=a_value
        
        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(json_string, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
     
        
    
        #IMPLEMENTATION
        try:
            dic=json.loads(json_string)
        except:
            raise RuntimeError ( "Could not parse JSON")

        self.__dic_nested_del(dic,list_pathkeys)

        #RETURN
        #Returns the modified json string
        return json.dumps(dic)

    def __json_write_file(self,filepath,json_string):
        #USAGE:
        #Usage example:
        #                   __json_write_file("/some/file/path",json_string)

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath , str) == True : raise TypeError
        if not isinstance(json_string, str) == True : raise TypeError

        #Just checking if json string is valid
        try:
            dic=json.loads(json_string)
        except:
            raise RuntimeError ( "Could not parse JSON")
            

        #write json to file while beautiful
        #json.dump always expects to be given a dict
        with open(filepath,'w') as outfile:
            json.dump(dic, outfile,indent=4)

        #RETURN
        #None


    def __json_read_file(self,filepath):
        #USAGE:
        #Usage example:
        #                   __json_read_file("/some/file/path")
        
        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath , str) == True : raise TypeError

        #Open and read in the json file
        with open(filepath) as infile:
            #json.load always reads in and converts direct to dict
            json_dict=json.load(infile)
        #lets convert json dict to a json str
        json_string=json.dumps(json_dict)

        #RETURN
        #Returns a string
        #A JSON string
        return json_string
        

    def __expand_filepath(self,filepath):
        #USAGE
        #Usage example:
        #               __expand_filepath(filepath)

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath , str) == True : raise TypeError


        #IMPLEMENTATION
        expanded_filepath = os.path.expanduser(filepath)
        expanded_filepath = os.path.abspath(expanded_filepath)
        
        #RETURN
        #Returns a fully formed absolute path for the host os.
        return expanded_filepath


    def __filepathchecks(self,filepath):
        #USAGE
        #Usage example:
        #               __filepathchecks('~/.mycfg.txt')                  HOME DIR SYMBOL
        #               __filepathchecks('/dir1/dir2/.mycfg.txt')         ABSOLUTE PATH
        #               __filepathchecks('mycfg.txt')                     RUNNING DIRECTORY

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath , str) == True : raise TypeError

        #EXPAND FILE PATH
        #Takes care of ~   ~user ./  ../..  and returns a fully formed absolute path. 
        expanded_filepath = self.__expand_filepath(filepath)


        #CHECK IF FILE EXISTS
        #Now we have a filepath for the system we are running on, lets check
        #if there is an actual file on that path.
        if not os.path.exists(expanded_filepath) == True : raise RuntimeError ( " Dave... I can't find your file: %s" % expanded_filepath )

        


        #CHECK IF FILE IS EMPTY
        #Ideally am empty file is size 0, but when manualy deliting chars
        #like \n can be left behind a size of less than or equal to 1 bit
        # is considered empty.
    
        if os.path.getsize(expanded_filepath) <= 1:
            #File is completely empty, not even initialised for json.
            #Lets initiate the file with an empty dict {}
            with open(expanded_filepath,'w') as outfile:
                json.dump({}, outfile)

        #CHECK IF FILE CONTAINS VALID JSON
        try:
            json_string=self.__json_read_file(expanded_filepath)
        except ValueError as e:
            raise ValueError( " \n\n Hey dude, \n\n YEA DUDE, YOU! \n\n Re: %s \n\n About your JSON based config file \"%s\". I found it, but either \n it  contains  invalid  JSON  or it isn't  totaly empty,  might have an \n invisible \\n or something."
                            "\n \n I didn't want to overwrite or delete  your data, so if you  could help \n me out and fix the JSON contents that would be great.\n \n Or you could  totaly delete the contents or leave  a single empty JSON \n object in there, you know, one of these mad lads {} " % (expanded_filepath,expanded_filepath)) from e 


        #RETURN
        #Return a valid filepath string.
        return expanded_filepath

    def __init_jconfig_file(self,filepath):
        #USAGE
        #Usage example
        #               init_jconfig_file('~/.config.txt')
        #
        #Creates an initialized config file if the one mentioned doesn't exist.

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath, str) == True : raise TypeError

        #EXPAND THAT FILE PATH
        expanded_filepath = self.__expand_filepath(filepath)

        #IMPLEMENTATION
        CONFIG_DIR_PATH=os.path.dirname(expanded_filepath)
        CONFIG_FILE_PATH=expanded_filepath

        if( not os.path.exists(CONFIG_DIR_PATH)):
            Path(CONFIG_DIR_PATH).mkdir(parents=True, exist_ok=True)

        if( not os.path.exists(CONFIG_FILE_PATH)):
            Path(CONFIG_FILE_PATH).touch()
            with open(CONFIG_FILE_PATH,'w') as json_file:
                json.dump({}, json_file)

        #OUTPUT
        #A fresh config file at filepath if it didn't already exist.

  


    def sets(self, list_pathkeys, a_value):
        filepath=self.config_filepath
        #USAGE:
        #Usage example:
        #                               jsets('filepath',['key1','key2','key3'],'a_value')
        #pyhton dict equivalent to      json_dict['key1']['key2']['key3']='a_value'

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
        if not isinstance(a_value, (dict,list,tuple,str,int,float,None)) == True : raise TypeError

        #FILE CHECKS
        checked_filepath=self.__filepathchecks(filepath)

        #IMPLEMENTATION
        json_string = self.__json_read_file(checked_filepath)
        json_string = self.__json_nested_set(json_string, list_pathkeys, a_value)
        
        #OUTPUT
        #Write to file
        self.__json_write_file(checked_filepath,json_string)

    def exists(self,list_pathkeys):
        filepath=self.config_filepath

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError

        #FILE CHECKS
        checked_filepath=self.__filepathchecks(filepath)

        #IMPLEMENTATION
        json_string = self.__json_read_file(checked_filepath)

        try:
            json_value = self.__json_nested_get(json_string, list_pathkeys)
            return True
        except KeyError as e:
            return False

    def gets(self,list_pathkeys):
        filepath=self.config_filepath
        #USAGE:
        #Usage example:
        #                               jgets('filepath',['key1','key2','key3'])
        #pyhton dict equivalent to      json_dict['key1']['key2']['key3']

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
        
        #FILE CHECKS
        checked_filepath=self.__filepathchecks(filepath)

        #IMPLEMENTATION
        json_string = self.__json_read_file(checked_filepath)

        try:
            json_value = self.__json_nested_get(json_string, list_pathkeys)
        except KeyError as e:
                raise ValueError( " \n\n Hey dude, \n\n YEA DUDE, YOU! \n\n Re: %s \n\n About your JSON based config file \"%s\". I found it, \n but you requested a missing key. \n\n Please check the first exception above for details. \n\n :)" % (filepath,filepath)) from e 


        
        #RETURN
        #Return jason value addressed by the list_pathkeys json path.
        return json_value

    def dels(self, list_pathkeys):
        filepath=self.config_filepath
        #USAGE:
        #Usage example:
        #                               jsets('filepath',['key1','key2','key3'],'a_value')
        #pyhton dict equivalent to      json_dict['key1']['key2']['key3']='a_value'

        #TYPE CHECKING
        #Let's do some argument type checking on json_string, list_pathkeys
        #Remember historicaly bool is subclass of int
        if not isinstance(filepath, str) == True : raise TypeError
        if not isinstance(list_pathkeys, list) == True : raise TypeError
        
        #FILE CHECKS
        checked_filepath=self.__filepathchecks(filepath)

        does_key_exist=self.exists(list_pathkeys)

        if(does_key_exist==False):
            pass
            #print(str(self.config_filepath) +" does not contain the key you want to delete" )
            return

        #IMPLEMENTATION
        json_string = self.__json_read_file(checked_filepath)
        json_string = self.__json_nested_del(json_string, list_pathkeys)
        
        #OUTPUT
        #Write to file
        self.__json_write_file(checked_filepath,json_string)
        

        


