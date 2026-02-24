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
#? CONFIGURATION ERRORS
#? =========================

class DatabaseAliasNotRegisteredError(AppException):
    def __init__(self, alias: str):
        super().__init__(
            message=f"Database alias '{alias}' is not registered.",
            error_code="CONFIG_001",
            status_code=500,
            details={"alias": alias},
        )