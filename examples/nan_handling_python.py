"""
Author: Michael Roth
Date: 10 Oct 2025
Description: Example code to handle NaN values in Python when writing to and reading from JSON files.
"""

import numpy as np
import codecs, json

a = np.arange(10, dtype=float).reshape(2, 5)
a[1, 1] = np.nan
b = a.tolist()
file_path = "path.json"  ## your path variable
json.dump(
    b,
    codecs.open(file_path, "w", encoding="utf-8"),
    separators=(",", ":"),
    sort_keys=True,
    indent=4,
)


with open(file_path) as f:
    d = json.load(f)
    print(d)
