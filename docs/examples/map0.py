from load import load

utils = load()

# using utils.Map

def main(*args):
    map0 = utils.Map({ 
                        'a': 1, 
                    })
    assert map0.a == 1
    assert map0.b == None
    print(map0)



if __name__ == '__main__':
    main()
