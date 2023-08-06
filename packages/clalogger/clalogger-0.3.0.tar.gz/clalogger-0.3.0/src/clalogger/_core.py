"""Implementation of the clalogger main class"""

from ._factory import AbstractLoggerFactory

import abc
import logging
import typing


class ClaLogger(metaclass=abc.ABCMeta):
    """The ClaLogger parent class

    Classes have to inherit of this in order to support the ClaLogger features.
    Anyway, it can be used directly, in which case the logging class context
    will be ClaLogger itself.
    """

    _loggers: typing.Dict[type, logging.Logger] = {}

    @property
    @abc.abstractmethod
    def loggerFactoryClass(self) -> typing.Type[AbstractLoggerFactory]:
        """The logger factory class

        It is advised, for an application, to create a base class which
        inherits of classes implementing this method

        Returns
        -------
        AbstractLoggerFactory
            A concrete implementation
        """
        raise NotImplementedError

    @property
    def logger(self) -> logging.Logger:
        """The python logger

        It is created using the logger factory class

        Returns
        -------
        logging.Logger:
            The logger
        """
        # pylint: disable=protected-access
        # we use type(self)._loggers ... which looks like accessing a protected
        # member, but it is not not the case
        cls = type(self)
        if cls not in cls._loggers:
            cls._loggers[cls] = self.loggerFactoryClass(cls).logger
        return cls._loggers[cls]
