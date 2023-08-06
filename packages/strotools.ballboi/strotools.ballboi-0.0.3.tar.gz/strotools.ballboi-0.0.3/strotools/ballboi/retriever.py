'''
Base interface for retrieving stats.
'''
from abc import ABCMeta, abstractmethod


class RetrieverInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_schedule') and
               callable(subclass.get_schedule) or 
               NotImplemented)
    
    @abstractmethod
    def get_schedule(self,
                     **kwargs,
                     ):
        """ Get schedule from specified parameters """
        raise NotImplementedError