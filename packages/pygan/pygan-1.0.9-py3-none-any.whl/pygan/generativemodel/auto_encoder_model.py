# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from pygan.generative_model import GenerativeModel


class AutoEncoderModel(GenerativeModel):
    '''
    Auto-Encoder as a Generative model
    which draws samples from the `fake` distribution.
    '''

    @abstractmethod
    def pre_learn(self, true_sampler, epochs=1000):
        '''
        Pre learning.

        Args:
            true_sampler:       is-a `TrueSampler`.
            epochs:             Epochs.
        '''
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        '''
        Update the encoder and the decoder
        to minimize the reconstruction error of the inputs.

        Returns:
            `np.ndarray` of the reconstruction errors.
        '''
        raise NotImplementedError()
