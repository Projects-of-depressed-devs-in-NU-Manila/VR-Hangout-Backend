# makes a singleton class. Just initialize the class and it will not create a new class.
instances = {}

def singleton(cls):
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance