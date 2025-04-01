import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance configured for the MailerSend SDK.
    
    Args:
        name: Optional name for the logger, typically the module name.
              If not provided, it will use 'mailersend'.
    
    Returns:
        A configured logger instance
    """
    logger_name = f"mailersend.{name}" if name else "mailersend"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    # Don't add handlers if they've already been added
    # This prevents duplicate log messages
    if not logger.handlers and not logging.root.handlers:
        # Set up a default handler if none exists
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Default to WARNING level, users can override this
        logger.setLevel(logging.WARNING)
    
    return logger