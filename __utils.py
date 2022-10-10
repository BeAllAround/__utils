import sys;
from time import time;

'''
    d = {"_list": []}
    d1 = {}
    d1["_list"] = d["_list"]
    d1["_list"].append(1);

    assert d["_list"] == d1["_list"]
'''

def estimate(f, log = False, *args):
    start = time();

    if log:
        sys.stdout.write('Testing [' + str(f) + ']...');
        sys.stdout.write('\n');

    f(*args);

    sys.stdout.write(str(time() - start));
    sys.stdout.write('\n');

def log(chunk):
    sys.stdout.write(str(chunk));

def logObject(obj):
    if type(obj) == str:
        log('"')
    log(obj)
    if type(obj) == str:
        log('"')

def isEmpty(arr):
    return not bool(len(arr))

def _export_json(obj, source, t = 1):
    if type(obj) == dict:
        keys = obj.keys()
        log('{')
        if not isEmpty(keys):
            log('\n')
        for i, key in enumerate(keys):
            log('    ' * t)
            logObject(key)
            log(': ')

            if type(obj[key]) == dict and obj[key] == source:
                log('{...}')
            else:
                _export_json(obj[key], source, t+1)
            if len(keys) - i - 1:
                log(',')
            log('\n')

        if not isEmpty(keys):
            log('    ' * (t-1))
        log('}')

    elif type(obj) == list:
        log('[')
        if not isEmpty(obj):
            log('\n')
        for i, item in enumerate(obj):
            log('    ' * t)
            if type(item) == dict and item == source:
                log('{...}')
            else:
                _export_json(item, source, t+1)
            if len(obj) - i - 1:
                log(',')
            log('\n')
        if not isEmpty(obj):
            log('    ' * (t-1))
        log(']')

    else:
        logObject(obj)

def export_json(obj):
    _export_json(obj, obj)
    log('\n')


def __deep_update(obj, _obj, typing = True):
    for key, value in _obj.items():
        if key in obj.keys():
            if(typing and (type(obj[key]) != type(value))): # and (type(obj[key]) != dict and type(value) != dict)):
                raise TypeError(); # TYPE RESTRICTION
            if type(value) != dict and type(obj[key]) != dict: # overwrite values but NOT OBJECTS(DICTS)!
                obj[key] = value;
            if type(obj[key]) == dict and type(value) == dict:
                __deep_update(obj[key], value);
        else:
            obj[key] = value;
        '''
        # python-native solution
        try:
            obj[key];
            if type(value) != dict and type(obj[key]) != dict:
                obj[key] = value;
            if type(obj[key]) == dict and type(value) == dict:
                __deep_update(obj[key], value);
        except KeyError:
            obj[key] = value;
        '''

def __update(obj, _obj):
    obj.update(_obj);
    return obj;

def __deep_update_and_copy(source, target, typing = True):
    obj = __update({}, source);
    _obj = target;
    for key, value in _obj.items():
        if key in obj.keys():
            if(typing and (type(obj[key]) != type(value))): # and (type(obj[key]) != dict and type(value) != dict)):
                raise TypeError(); # TYPE RESTRICTION
            if type(value) != dict and type(obj[key]) != dict: # overwrite values but NOT OBJECTS(DICTS)!
                obj[key] = value;
            if type(obj[key]) == dict and type(value) == dict:
                # __update(obj, {key: __deep_update_and_copy(obj[key], value)}); # or:
                obj[key] = __deep_update_and_copy(obj[key], value);
        else:
            # __update(obj, {key: value}); # or:
            obj[key] = value;
    return obj;

def ___deep_copy(source):
    if type(source) == list: # TODO: is_iter?
        arr = [] # list()
        for item in source:
            arr.append(___deep_copy(item))
        return arr
    elif type(source) == dict:
        obj = {} # dict()
        for key in source: # for key in source.keys(): # 
            obj.update({key: ___deep_copy(source[key])})
        return obj
    elif type(source) == tuple:
        # TypeError: 'tuple' object does not support item assignment
        # TypeError: 'tuple' object doesn't support item deletion
        tup = tuple()
        for item in source:
            tup += tuple([___deep_copy(item)]) # __add__
        return tup
    else:
        return source

def __deep_copy(source):
    iter(source); # will raise an exception as it's built-in
    return ___deep_copy(source)

class Map:
    def __init__(self, obj: dict = {}):
        __deep_copy = globals()['__deep_copy']

        self.__dict__.update(obj)

    def __getattr__(self, key):
        try:
            return self.__dict__[key];
        except KeyError:
            return None

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        try:
            return self.__dict__[item]
        except KeyError:
            return None

    def __repr__(self):
        return str(self.__dict__) # TODO: customize

def __globals():
    return Map(globals())


def __test__():
    foo = 'foo';
    a1 = {foo: {1: '2', 4: 4, 5: 5, 6: {7: {9: 9}}}, 'a': 5};
    a2 = {foo: {1: '1', 2: '2', 6: {7: {8: {}}}}, 'a': int(6)};
    # __deep_update(a1, a2); # not overwriting all the objects
    # a1.update(a2); # overwriting all the objects

    a3 = __deep_update_and_copy(a1, a2);
    print(a1);
    print(a3);

    l1 = [1, 3]; # one - dimensional
    l2 = __deep_copy(l1);
    l2[0] = 2;
    print(l1);
    print(l2);

    l1 = [[1, 2], [3, 4]]; # two or more - dimensional
    l2 = __deep_copy(l1);
    l2[0][1] = 99;
    print(l1);

    # testing nested objects in a list
    obj1 = [{0: {1: 2}}, 10, ([1], [2])];
    obj2 = __deep_copy(obj1);
    obj1[0][0][1] = 3;
    obj1[1] = 9;
    obj1[2][0][0] = 3;

    print(obj1, obj2);
    assert obj1 != obj2


    # testing nested objects in an obj
    obj1 = {0: {1: 2}};
    obj2 = __deep_copy(obj1);

    obj1[0][1] = 3;
    print(obj1, obj2);
    assert obj1 != obj2

    obj1 = 1;
    try: # testing "iter(source)"
        __deep_copy(obj1);
        assert False;
    except TypeError:
        assert True;


    m = Map({'vFlag': True});
    assert m.vFlag == True;
    assert m['vFlag'] == True
    print('m: ', m)

    m.vFlag = False
    assert m.vFlag == False
    assert m['vFlag'] == False
    assert m.dFlag == None
    assert m['dFlag'] == None

    assert __globals().__deep_copy == __deep_copy

    export_json({'a': 1, 'func': lambda x: x+1, 'uu':[1,40,[],[1,2]],
        'b': {'c': 10, 'd': 11 , 'f': {}, 'string': 'laaa'}
    })

    # issue - 7
    obj = {'a': 1,}
    obj['b'] = obj # also - test with nested arrays [obj] and [[obj]]
    export_json(obj)
    # print(obj)


if __name__ == '__main__': # false when import-ed
    __test__();
