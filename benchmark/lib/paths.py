from pathlib import Path
from typing import Union

import lib.config as cfg
import lib.exceptions as ex

from pathlib import Path
from typing import Union, Optional
import os

class OutputPath:
    def __init__(self, output: Union[str, Path]):
        self._path = Path(output) if isinstance(output, str) else output
        self._validate_path()
    
    @property
    def path(self) -> Path:
        return self._path
    
    def _validate_path(self) -> None:
        if not self._path.parent.exists():
            raise ValueError(f"Parent directory does not exist: {self._path.parent}")
        if not self._path.parent.is_dir():
            raise ValueError(f"Parent path is not a directory: {self._path.parent}")
    
    def try_build_output_path(self, filename: str, suffix: str) -> Path:
        if self._path.is_dir():
            self._path = self._path / Path(filename).with_suffix(f".{suffix.lstrip('.')}")
        
        return self
    # Make it behave like a Path object
    def __getattr__(self, attr):
        """Delegate attribute access to the underlying Path object"""
        return getattr(self._path, attr)
    
    def __fspath__(self) -> str:
        """Support os.fspath() protocol"""
        return str(self._path)
    
    def __str__(self) -> str:
        return str(self._path)
    
    def __repr__(self) -> str:
        return f"OutputPath('{self._path}')"


class SourcePath:
    def __init__(self, source: Union[str, Path]):
        self._path = Path(source) if isinstance(source, str) else source
        self._validate_path()
    
    @property
    def path(self) -> Path:
        return self._path
    
    def _validate_path(self) -> None:
        if not self._path.exists():
            raise ex.FileValidationError(f"Source file does not exist.", self._path)
        
        if self._path.is_dir(): 
            return
        
        if self._path.suffix.lower() not in cfg.config['allowed_languages']:
            allowed = ', '.join(cfg.config['allowed_languages'])
            raise ValueError(
                f"File extension '{self._path.suffix}' not allowed. "
                f"Allowed extensions: {allowed}"
            )
    
    # Make it behave like a Path object
    def __getattr__(self, attr):
        """Delegate attribute access to the underlying Path object"""
        return getattr(self._path, attr)
    
    def __fspath__(self) -> str:
        """Support os.fspath() protocol"""
        return str(self._path)
    
    def __str__(self) -> str:
        return str(self._path)
    
    def __repr__(self) -> str:
        return f"SourcePath('{self._path}')"