# pylint: disable=access-member-before-definition

class Borg:
    """
    Implements the Borg design pattern, used to implement singleton behavior across multiple
    instances of a class.

    In the Borg design pattern, the focus is on sharing instance state instead of instance
    identity.

    Examples:
        ```python
        from flashback import Borg

        class Borged(Borg):
            pass

        borg_1 = Borged()
        borg_2 = Borged()

        # They're not the same instance
        assert borg_1 != borg_2
        assert id(borg_1) != id(borg_2)

        # But they share their attributes
        borg_1.assign_attribute("attr", 0)

        assert borg_1.attr == 0
        assert borg_2.attr == 0

        # And their attributes are not overridable
        borg_1.assign_attribute("attr", "foo")

        assert borg_1.attr == 0
        assert borg_2.attr == 0
        ```
    """
    def __new__(cls, *_args, **_kwargs):
        if "_shared_state" not in cls.__dict__:
            cls._shared_state = {}

        obj = object.__new__(cls)
        obj.__dict__ = cls._shared_state

        return obj

    def assign_attribute(self, attribute, value, *args, **kwargs):
        """
        Assigns a `value` to the `attribute` of the Borg, if it's not already defined.

        The `value` is checked for being a callable, and if so, is instantiated with the provided
        `args` and `kwargs`. This allows to call `value` with `args` and `kwargs` only if
        `attribute` is not already set, reducing useless computation.

        Examples:
            ```python
            from flashback import Borg

            class Borged(Borg):
                pass

            borg = Borged()

            borg.assign_attribute("attr_1", 0)
            assert borg.attr_1 == 0

            borg.assign_attribute("attr_1", 1)
            assert borg.attr_1 == 0

            borg.assign_attribute("attr_2", dict, {"foo": "bar"})
            assert borg.attr_2 == {"foo": "bar"}

            borg.assign_attribute("attr_3", str(1))
            # calls 'str(1)', then assigns its return to 'attr_3' if it is not set
            assert borg.attr_3 == "1"

            borg.assign_attribute("attr_4", str, 2)
            # calls 'str(2)' if 'attr_4' is not set, then assigns its return to 'attr_3'
            assert borg.attr_4 == "2"
            ```

        Params:
            attribute (str): the name of the attribute to define
            value (Any): the value to assign to the attribute
            args (tuple): every additional positional arguments
            kwargs (dict): every given keyword arguments
        """
        if hasattr(self, attribute):
            return

        if callable(value):
            setattr(self, attribute, value(*args, **kwargs))
        else:
            setattr(self, attribute, value)

    def assign_attributes(self, **kwargs):
        """
        Assigns multiple values to their respective attributes of the Borg if they're not already
        defined.

        Only accepts keywords arguments, with the following accepted structures:
        ATTRIBUTE_NAME=VALUE or ATTRIBUTE_NAME=(CALLABLE, ARGUMENTS),
        where the keywords arguments to forward to CALLABLE must be given as a dict as the last
        item of the tuple.

        Examples:
            ```python
            from flashback import Borg

            class Borged(Borg):
                pass

            borg = Borged()

            borg.assign_attributes(attr_1=0)
            assert borg.attr_1 == 0

            borg.assign_attributes(attr_4=("foo", 0))
            assert borg.attr_4 == ("foo", 0)

            borg.assign_attributes(attr_2=(dict({"foo": "bar"}),))
            # calls 'dict({"foo": "bar"})', then assigns its return to 'attr_2' if it is not set
            assert borg.attr_2 == {"foo": "bar"}

            borg.assign_attributes(attr_3=(dict, {"foo": "bar"}))
            # calls 'dict({"foo": 1})' if 'attr_3' is not set, then assigns its return to 'attr_3'
            assert borg.attr_3 == {"foo": "bar"}

            borg.assign_attributes(attr_5=(str, 0)
            # calls 'str(0)' if 'attr_5' is not set, then assigns its return to 'attr_5'
            assert borg.attr_5 == "0"
            ```

        Params:
            kwargs (dict): every given keyword arguments
        """
        for attribute, value in kwargs.items():
            if isinstance(value, tuple) and callable(value[0]):
                if isinstance(value[-1], dict):
                    self.assign_attribute(attribute, value[0], *value[1:-1], **value[-1])
                else:
                    self.assign_attribute(attribute, value[0], *value[1:])
            else:
                self.assign_attribute(attribute, value)
