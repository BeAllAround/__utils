from load import load

utils = load()

# using utils.deep_update

def main(*args):
    obj1 = { 'a': 1, 'foo': { 'bar': 1 } }
    obj2 = { 'b': 2, 'foo': { 'zoo': 2 } }
    result = { 'a': 1, 'foo': { 'bar': 1, 'zoo': 2 }, 'b': 2 }

    utils.deep_update(obj1, obj2)
    assert obj1 == result

    utils.export_json(obj1)


if __name__ == '__main__':
    main()
