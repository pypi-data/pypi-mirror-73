'''
Misc utils
'''
class InvalidParamsError(Exception):
    ''' Thrown if there is an error in params '''

def build_params(mappings: dict,
                 **kwargs,
                 ) -> dict:
    '''
    Build params from kwargs and return as dict

    Args:
      mappings::dict
        Dictionary of mappings { keyname: type }
    '''
    errors = []
    params = {}
    for keyName, t in mappings.items():
        val = kwargs.get(keyName, '')
        if keyName in kwargs and type(kwargs.get(keyName)) is not t:
            keyType = type(kwargs.get(keyName))
            err     = f'(key: {keyName}, type: {keyType.__name__}) '\
                      f'is not of type {t.__name__}'
            errors.append(err)
        
        if val:
            params[keyName] = val
    return params, errors
