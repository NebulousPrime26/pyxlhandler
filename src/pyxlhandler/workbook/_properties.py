from __future__ import annotations

import datetime as dt
import os
from collections import NamedTuple


class Properties(NamedTuple):
    """Class representing properties of an Excel file.

    Do not instantiate this class directly. Use the `from_file` class method to create an instance from a file.
    """

    last_modified: dt.datetime | None = None

    @classmethod
    def from_file(cls, file_path: str) -> Properties:
        """Load properties from a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            Properties: The loaded properties.
        """
        return cls(
            last_modified=dt.datetime.fromtimestamp(
                os.path.getmtime(file_path), tz=dt.UTC
            )
        )
