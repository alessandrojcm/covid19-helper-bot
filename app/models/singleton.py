# From: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Singleton(object):
    _instances = {}

    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_)
        return class_._instances[class_]
