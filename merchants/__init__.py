import importlib
import pkgutil
from pathlib import Path
import constants


__all__ = []

_current_dir = Path(__file__).parent

for module_info in pkgutil.iter_modules([str(_current_dir)]):
    module_name = module_info.name

    # Import the module dynamically
    module = importlib.import_module(f".{module_name}", package=__name__)

    # Check if the module has a 'parse_product' callable
    if hasattr(module, constants.PARSE_PRODUCT_FUNCTION_NAME) and callable(getattr(module, constants.PARSE_PRODUCT_FUNCTION_NAME)):
        # Add the module to the package namespace
        globals()[module_name] = module
        __all__.append(module_name)
