def ordir(any_object):
    for attr in sorted(any_object.__dir__()):
        print(attr)

