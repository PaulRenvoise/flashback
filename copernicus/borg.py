# pylint: disable=access-member-before-definition

class Borg:
    """
    Implements a Borg pattern that is used to implement singleton behavior across multiple instances of a class.

    In the Borg design pattern, the focus is on sharing state instead of sharing instance identity.
    See: Python Cookbook, 5.22: <https://books.google.fr/books?id=yhfdQgq8JF4C&ots=-8okzwnM03&pg=PA208>

    Examples:
        ```
        from copernicus import Borg

        class Borged(Borg):
            pass

        borg_1 = Borged()
        borg_2 = Borged()

        # They're not the same instance
        assert borg_1 != borg_2
        assert id(borg_1) != id(borg_2)

        # But they share their attributes
        borg_1.assign_attribute('attr', 0)

        assert borg_2.attr == 0

        # And their attributes are not overridable
        borg_1.assign_attribute('attr', 'foo')

        assert borg_1.attr == 0
        ```
    """
    def __new__(cls, *_args, **_kwargs):
        if '_shared_state' not in cls.__dict__:
            cls._shared_state = {}

        obj = object.__new__(cls)
        obj.__dict__ = cls._shared_state

        return obj

    def assign_attribute(self, attribute, value, *args, **kwargs):
        """
        Assigns an attribute to the Borg if it's not already defined.
        `value` is checked for being a callable, and if so, is instantiated with the provided args and kwargs.

        Examples:
            ```
            self.assign_attribute('attr', 0)
            #=> assigns '0' to 'attr'

            self.assign_attribute('attr', dict, {'foo': 'bar'})
            #=> assigns 'dict({'foo': 'bar'})' to 'attr'

            self.assign_attribute('attr', func('foo'))
            #=> calls 'func('foo')' and assigns its return to 'attr'

            self.assign_attribute('attr', func, 'foo')
            #=> calls 'func('foo')' if attr is not set and assigns its return to 'attr'
            ```

        Params:
            - `attribute (str)` the name of the attribute to define
            - `value (Any)` the value to assign to the attribute
            - `args (list)` every additional positional arguments
            - `kwargs (dict)` every given keyword arguments

        Returns:
            - `None`
        """
        if hasattr(self, attribute):
            return

        if callable(value):
            setattr(self, attribute, value(*args, **kwargs))
        else:
            setattr(self, attribute, value)

    def assign_attributes(self, **kwargs):
        """
        Assigns multiple attributes to the Borg if they'rem not already defined.

        Only accepts keywords arguments, with the following structures: ATTRIBUTE_NAME=VALUE
        or ATTRIBUTE_NAME=(CALLABLE, ARGUMENTS) where the keywords arguments to forward to CALLABLE
        must be given as a dict as the last item of the tuple.

        Examples:
            ```
            self.assign_attributes(attr=0)
            #=> assigns '0' to 'attr'

            self.assign_attributes(attr=(dict({'foo': 'bar'}),))
            #=> calls 'dict({'foo': 'bar'})' and assigns its return to 'attr'

            self.assign_attributes(attr=(dict, {'foo': 'bar'}))
            #=> calls 'dict({'foo': 'bar'})' if 'attr' is not set and assigns its return to 'attr'

            self.assign_attributes(attr=('foo', 0))
            #=> assigns '('foo', 0)' to 'attr'

            self.assign_attributes(attr=(func, 0, 1)
            #=> calls 'func(0, 1)' if 'attr' is not set and assigns its return to 'attr'

            self.assign_attributes(attr=(func, {'foo': 'bar'}))
            #=> calls 'func(foo='bar')' if 'attr' is not set and assigns its return to 'attr'

            self.assign_attributes(attr=(func, 'foo', {'bar': 0})
            #=> calls 'func('foo', bar=0)' if 'attr' is not set and assigns its return to 'attr'
            ```

        Params:
            - `kwargs (dict)` every given keyword arguments

        Returns:
            - `None`
        """
        for attribute, value in kwargs.items():
            # Check for callable
            if isinstance(value, tuple) and callable(value[0]):
                # Check for kwargs
                if isinstance(value[-1], dict):
                    self.assign_attribute(attribute, value[0], *value[1:-1], **value[-1])
                else:
                    self.assign_attribute(attribute, value[0], *value[1:])
            else:
                self.assign_attribute(attribute, value)
