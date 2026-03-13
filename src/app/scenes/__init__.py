import importlib
import pkgutil

# Dynamically import all modules in this package to register scenes.
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if not is_pkg:
        importlib.import_module(f".{module_name}", __package__)
