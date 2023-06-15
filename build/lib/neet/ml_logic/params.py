"""
neet model package params
load and validate the environment variables in the `.env`

"""
# Example below #

import os
import numpy as np

DATASET_SIZE = os.environ.get("DATASET_SIZE")
VALIDATION_DATASET_SIZE = os.environ.get("VALIDATION_DATASET_SIZE")
