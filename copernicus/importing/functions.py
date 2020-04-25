import inspect

from importlib import util, import_module

from ..formatting import camelize


def import_class_from_path(name, path):
    """
    Imports a class from a relative or absolute path, and returns it.

    Similar to `from module import Class` if this statement returned the imported class.

    Examples:
        ```python
        from copernicus.importing import import_class_from_path

        borg_class = import_class_from_path('borg', 'copernicus')

        borg_class()
        ```

    Paramss:
        - `name (str)` the name of the class to import
        - `path (str)` the relative path in which to find the class to import

    Returns:
        - `Callable` the class from the imported module

    Raises:
        - `ImportError` if the requested module is not found
        - `ImportError` if a relative import beyond the top-level package is attempted
        - `AttributeError` if the class is not found in the imported module
    """
    if path.startswith('.'):
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        caller_package = caller_module.__package__

        module_path = util.resolve_name(path, caller_package)
    else:
        module_path = path

    # Loads the module, will raise ImportError if module cannot be loaded
    # The module import is called with the complete absolute class path (`import_module(absolute_path)`) rather
    # than the relative class path for an absolute package path (`import_module(relative_path, package=absolute_path)`)
    # because it can happen that the package is not yet loaded when we try to import.
    imported_module = import_module(module_path + '.' + name)

    # Gets the class, will raise AttributeError if class cannot be found
    return getattr(imported_module, camelize(name))


def import_module_from_path(name, path):
    """
    Imports the contents of a module from a relative or absolute path and makes its content available for usage.

    Simulates `from module import *`.

    Examples:
        ```python
        from copernicus.importing import import_module_from_path

        import_module_from_path('logging', 'copernicus')

        print(DEFAULT_CONSOLE_CONFIGURATION)
        ```

    Params:
        - `name (str)` the name of the module to import
        - `path (str)` the relative path in which to find the module to import

    Returns:
        - `None`

    Raises:
        - `ImportError` if a relative import beyond the top-level package is attempted
        - `ImportError` if the request module is not found
    """
    if path.startswith('.'):
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        caller_package = caller_module.__package__

        module_path = util.resolve_name(path, caller_package)
    else:
        module_path = path

    imported_module = import_module(module_path + '.' + name)
    print(imported_module)
    if hasattr(imported_module, '__all__'):
        to_globalize = {name: getattr(imported_module, name) for name in imported_module.__all__}
    else:
        to_globalize = {name: attr for name, attr in imported_module.__dict__.items() if not name.startswith('_')}

    globals().update(to_globalize)
