# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from pygan.noise_sampler import NoiseSampler


class GenerativeModel(metaclass=ABCMeta):
    '''
    Sampler which draws samples from the `fake` distribution.
    '''
    # is-a `NoiseSampler`.
    __noise_sampler = None

    def get_noise_sampler(self):
        ''' getter '''
        return self.__noise_sampler

    def set_noise_sampler(self, value):
        ''' setter '''
        if isinstance(value, NoiseSampler) is False:
            raise TypeError("The type of `__noise_sampler` must be `NoiseSampler`.")
        self.__noise_sampler = value

    noise_sampler = property(get_noise_sampler, set_noise_sampler)

    @abstractmethod
    def draw(self):
        '''
        Draws samples from the `fake` distribution.
        
        Returns:
            `np.ndarray` of samples.
        '''
        raise NotImplementedError()

    @abstractmethod
    def learn(self, grad_arr):
        '''
        Update this Generator by ascending its stochastic gradient.

        Args:
            grad_arr:   `np.ndarray` of gradients.

        Returns:
            `np.ndarray` of delta or gradients.

        '''
        raise NotImplementedError()

    @abstractmethod
    def switch_inferencing_mode(self, inferencing_mode=True):
        '''
        Set inferencing mode in relation to concrete regularizations.

        Args:
            inferencing_mode:       Inferencing mode or not.
        '''
        raise NotImplementedError()
