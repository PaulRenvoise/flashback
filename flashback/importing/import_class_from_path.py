import inspect

from importlib import util, import_module

from ..debugging import get_frameinfo
from ..formatting import pascalize


def import_class_from_path(name, path):
    """
    Imports a class from a relative or absolute path, and returns it.

    Similar to `from module import Class` if this statement returned the imported class.

    Examples:
        ```python
        from flashback.importing import import_class_from_path

        borg_class = import_class_from_path("borg", "flashback")

        borg_class()
        ```

    Paramss:
        name (str): the name of the class to import
        path (str): the relative path in which to find the class to import

    Returns:
        Callable: the class from the imported module

    Raises:
        ImportError: if the requested module is not found
        ImportError: if a relative import beyond the top-level package is attempted
        AttributeError: if the class is not found in the imported module
    """
    if path.startswith("."):
        caller_module = inspect.getmodule(get_frameinfo(1).frame)
        caller_package = caller_module.__package__

        module_path = util.resolve_name(path, caller_package)
    else:
        module_path = path

    # Loads the module, will raise ImportError if module cannot be loaded
    # The module import is called with the complete absolute class path
    # (`import_module(absolute_path)`) rather than the relative class path for an absolute package
    # path (`import_module(relative_path, package=absolute_path)`) because it can happen that the
    # package is not yet loaded when it tries to import.
    imported_module = import_module(module_path + "." + name)

    # Gets the class, will raise AttributeError if class cannot be found
    return getattr(imported_module, pascalize(name))
