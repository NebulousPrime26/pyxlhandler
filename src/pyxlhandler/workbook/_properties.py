from __future__ import annotations

import datetime as dt
import os
from typing import Literal, NamedTuple


class Properties(NamedTuple):
    """Class representing properties of an Excel file.

    Do not instantiate this class directly. Use the `from_file` class method to create an instance from a file.
    """

    name: str | None = None

    # Timestamps
    created: dt.datetime | None = None
    last_modified: dt.datetime | None = None
    last_accessed: dt.datetime | None = None

    size: int | None = None

    @classmethod
    def from_file(cls, file_path: str) -> Properties:
        """Load properties from a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            Properties: The loaded properties.
        """
        return cls(
            name=os.path.basename(file_path),
            created=dt.datetime.fromtimestamp(os.path.getctime(file_path), tz=dt.UTC),
            last_modified=dt.datetime.fromtimestamp(os.path.getmtime(file_path), tz=dt.UTC),
            last_accessed=dt.datetime.fromtimestamp(os.path.getatime(file_path), tz=dt.UTC),
            size=os.path.getsize(file_path),
        )

    def get_size(self, unit: Literal["B", "KB", "MB", "GB"]) -> float:
        """Get the size of the file in the specified unit.

        Args:
            unit ({"B", "KB", "MB", "GB"}): The unit to return the size in.

        Returns:
            float: The size of the file in the specified unit.

        Raises:
            ValueError: If an unsupported unit is provided.
        """
        if unit not in {"B", "KB", "MB", "GB"}:
            raise ValueError(f"Unsupported unit '{unit}'. Supported units are 'B', 'KB', 'MB', 'GB'.")

        if self.size is None:
            return 0.0
        if unit == "B":
            return float(self.size)
        elif unit == "KB":
            return float(self.size) / 1024
        elif unit == "MB":
            return float(self.size) / (1024**2)

        return float(self.size) / (1024**3)
