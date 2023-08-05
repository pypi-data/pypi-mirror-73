class __AddParams(object):
    def __init__(self, *args, **kwargs):
        pass 
                                                                                    
    def __add_attr__(self, name):                                                                                                         
        for k in name.keys():
            if k not in self.__dict__ and name[k] is not None:
                self.__dict__[k] = name[k]

class __ParseInitalize(__AddParams):
    
    def __init__(self, params, *args, **kwargs):
        self.__add_attr__(params)

a=__ParseInitalize({'test':'hl'})

