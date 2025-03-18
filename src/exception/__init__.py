import sys  # Used to get error details like file name and line number
import logging  # Used to log error messages

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    This function gives detailed error messages with file name, line number, and error message.
                 _	Ignore Exception Type
                 _	Ignore Exception Message
                exc_tb	-->Store detailed error location
                exc_tb.tb_lineno	-->Line Number
                exc_tb.tb_frame.f_code.co_filename	-->File Name

    """
    _, _, exc_tb = error_detail.exc_info()  # Get traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get file name where error occurred
    line_number = exc_tb.tb_lineno  # Get line number where error occurred
    
    error_message = f"Error occurred in script: [{file_name}] at line [{line_number}]: {str(error)}"
    logging.error(error_message)  # Log error message
    return error_message

class MyException(Exception):
    """
    Custom exception class to generate detailed error messages.
    """
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)  # Call parent class Exception
        self.error_message = error_message_detail(error_message, error_detail)  # Store detailed message

    def __str__(self) -> str:
        return self.error_message  # Return error message when printed


"""
-----------------------------------What This Code Does:
----Provides file name
----Gives line number
----Logs detailed error message
----Exception Class

"""