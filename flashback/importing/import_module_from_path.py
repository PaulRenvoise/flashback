import inspect

from importlib import util, import_module

from ..debugging import get_frameinfo


def import_module_from_path(name, path):
    """
    Imports the contents of a module from a relative or absolute path and makes its content
    available for usage.

    Simulates `from module import *`.

    Examples:
        ```python
        from flashback.importing import import_module_from_path

        import_module_from_path("logging", "flashback")

        print(DEFAULT_CONSOLE_CONFIGURATION)
        ```

    Params:
        name (str): the name of the module to import
        path (str): the relative path in which to find the module to import

    Raises:
        ImportError: if a relative import beyond the top-level package is attempted
        ImportError: if the request module is not found
    """
    if path.startswith("."):
        caller_module = inspect.getmodule(get_frameinfo(1).frame)
        caller_package = caller_module.__package__

        module_path = util.resolve_name(path, caller_package)
    else:
        module_path = path

    imported_module = import_module(module_path + "." + name)
    if hasattr(imported_module, "__all__"):
        to_globalize = {name: getattr(imported_module, name) for name in imported_module.__all__}
    else:
        to_globalize = {name: attr for name, attr in imported_module.__dict__.items() if not name.startswith("_")}

    globals().update(to_globalize)
