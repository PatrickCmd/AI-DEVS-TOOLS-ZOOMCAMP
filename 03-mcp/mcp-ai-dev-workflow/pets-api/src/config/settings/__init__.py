"""
Django settings module.

Automatically loads the appropriate settings based on the ENVIRONMENT variable.
"""

import os

# Determine which settings module to use
environment = os.environ.get("ENVIRONMENT", "development").lower()

if environment == "production":
    from .production import *  # noqa: F403, F401
elif environment == "test":
    from .test import *  # noqa: F403, F401
else:
    from .development import *  # noqa: F403, F401
