import logging

def config_logger():
    """Configures logging system for recording and tracking errors.
    
    Args:
        None
        
    Returns:
        None
    """
    
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Creating file handler - writes messages to log file on system
    file_handler = logging.FileHandler('air_quality_monitoring.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Create console handler - streams messages to main console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Adding handlers to logger
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)