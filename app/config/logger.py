from app.factories.logger_factory import LoggerFactory


class Logger:
    @staticmethod
    def info(message: str):
        LoggerFactory.get_logger().info(message)

    @staticmethod
    def warning(message: str):
        LoggerFactory.get_logger().warning(message)

    @staticmethod
    def error(message: str):
        LoggerFactory.get_logger().error(message)

    @staticmethod
    def debug(message: str):
        LoggerFactory.get_logger().debug(message)
