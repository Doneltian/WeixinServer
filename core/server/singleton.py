class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'__instance'):
            cls.__instance = super().__new__(cls,*args, **kwargs)
        return cls.__instance