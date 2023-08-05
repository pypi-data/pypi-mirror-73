from abc import ABC, abstractmethod


class AbstractTask(ABC):
    @abstractmethod
    def fnc(self, *args, **kwargs):
        """
        Task method for call parallel
        :param args:
        :param kwargs:
        :return:
        """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Method for calling self.fnc()
        :param args:
        :param kwargs:
        :return:
        """


class Task(AbstractTask):
    def fnc(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self.fnc(*args, **kwargs)
