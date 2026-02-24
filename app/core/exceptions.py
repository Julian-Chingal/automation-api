from typing import Any, Dict, Optional


class AppException(Exception):
    """
    Base exception for the application.
    All custom exceptions should inherit from this class.
    """
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}

        super().__init__(message)


#? =========================
#? TRANSFORMATION ERRORS
#? =========================

class TransformationError(AppException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="TRANSFORM_001",
            status_code=400,
            details=details,
        )


class MissingSourceColumnsError(AppException):
    def __init__(self, missing_columns: list[str]):
        super().__init__(
            message="Missing source columns for mapping.",
            error_code="TRANSFORM_002",
            status_code=400,
            details={"missing_columns": missing_columns},
        )


class MissingRequiredColumnsError(AppException):
    def __init__(self, missing_columns: list[str]):
        super().__init__(
            message="Missing required columns after transformation.",
            error_code="TRANSFORM_003",
            status_code=400,
            details={"missing_columns": missing_columns},
        )


class InvalidHeadersError(AppException):
    def __init__(self, missing_columns: list[str], file_columns: list[str]):
        super().__init__(
            message="Invalid file headers. The first row must contain the expected column names.",
            error_code="TRANSFORM_005",
            status_code=400,
            details={
                "expected_columns": missing_columns,
                "file_columns": file_columns,
                "help": "Make sure the headers are in the first row of your file."
            },
        )


class EmptyFileError(AppException):
    def __init__(self):
        super().__init__(
            message="The uploaded file contains no valid rows.",
            error_code="TRANSFORM_004",
            status_code=400,
        )


#? =========================
#? DATABASE ERRORS
#? =========================

class DatabaseConnectionError(AppException):
    def __init__(self):
        super().__init__(
            message="Could not connect to the database.",
            error_code="DB_001",
            status_code=500,
        )


class DatabaseInsertError(AppException):
    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message="An error occurred while inserting data into the database.",
            error_code="DB_002",
            status_code=500,
            details=details,
        )


class DuplicateKeyError(AppException):
    def __init__(self):
        super().__init__(
            message="Duplicate key detected.",
            error_code="DB_003",
            status_code=409,
        )


#? =========================
#? FILE HANDLING ERRORS
#? =========================

class UnsupportedFileFormatError(AppException):
    def __init__(self, extension: str, supported_formats: list[str]):
        super().__init__(
            message=f"Unsupported file format: '.{extension}'.",
            error_code="FILE_001",
            status_code=400,
            details={"extension": extension, "supported_formats": supported_formats},
        )


class FileReadError(AppException):
    def __init__(self, filename: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Error reading file '{filename}'.",
            error_code="FILE_002",
            status_code=400,
            details=details or {"filename": filename},
        )


#? =========================
#? CONFIGURATION ERRORS
#? =========================

class ConfigurationError(AppException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFIG_001",
            status_code=500,
            details=details,
        )


class DatabaseAliasNotRegisteredError(AppException):
    def __init__(self, alias: str):
        super().__init__(
            message=f"Database alias '{alias}' is not registered.",
            error_code="CONFIG_002",
            status_code=500,
            details={"alias": alias},
        )