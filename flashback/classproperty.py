class ClassPropertyMetaclass(type):
    """
    Defines a metaclass to ensure the property is settable, to use as `flashback.classproperty.meta`.
    """
    def __setattr__(cls, key, value):
        obj = cls.__dict__.get(key, None)
        if isinstance(obj, classproperty):
            return obj.__set__(cls, value)

        return super().__setattr__(key, value)


class classproperty:  # pylint: disable=invalid-name
    """
    Combines @classmethod and @property to define getters and setters on classes attributes.

    Any class that needs to use this @classproperty decorator must have classproperty.meta as
    metaclass to prevent attribute assignation via the class when no setter is defined.

    Adapted from https://stackoverflow.com/a/5191224.

    Examples:
        ```python
        from flashback import classproperty

        class Static(metaclass=classproperty.meta):
            _var = 1

            @classproperty
            def var(cls):
                return cls._var

            @var.setter
            def var(cls, value):
                cls._var = value

        static_1 = Static()
        assert static_1.var == 1

        static_2 = Static()
        assert static_2.var == 1

        # Handles static attribute assignation
        static_2.var = 2
        assert static_1.var == 2

        # Handles attribute assignation via the class
        Static.var = 3
        assert static_1.var == 3
        assert static_2.var == 3
        ```
    """
    meta = ClassPropertyMetaclass

    def __init__(self, func_get, func_set=None):
        """
        Params:
            func_get (Callable): the getter to decorate
            func_set (Callable): the setter to decorate
        """
        if not isinstance(func_get, (classmethod, staticmethod)):
            func_get = classmethod(func_get)

        # Explicitly checks against None to avoid converting it to a classmethod
        if func_set is not None and not isinstance(func_set, (classmethod, staticmethod)):
            func_set = classmethod(func_set)

        self.func_get = func_get
        self.func_set = func_set

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)

        return self.func_get.__get__(obj, cls)()

    def __set__(self, obj, value):
        if not self.func_set:
            raise AttributeError("can't set attribute")
        if not isinstance(obj, ClassPropertyMetaclass):
            cls = type(obj)
        else:
            cls = obj
            obj = None

        return self.func_set.__get__(obj, cls)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)

        self.func_set = func

        return self
