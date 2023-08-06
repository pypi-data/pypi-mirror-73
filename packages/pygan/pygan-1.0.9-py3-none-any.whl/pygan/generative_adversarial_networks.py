# -*- coding: utf-8 -*-
from logging import getLogger
import numpy as np
from pygan.true_sampler import TrueSampler
from pygan.generative_model import GenerativeModel
from pygan.discriminative_model import DiscriminativeModel
from pygan.gans_value_function import GANsValueFunction
from pygan.gansvaluefunction.mini_max import MiniMax
from pygan.feature_matching import FeatureMatching


class GenerativeAdversarialNetworks(object):
    '''
    The controller for the Generative Adversarial Networks(GANs).
    '''

    def __init__(self, gans_value_function=None, feature_matching=False):
        '''
        Init.

        Args:
            gans_value_function:        is-a `GANsValueFunction`.

        '''
        if gans_value_function is None:
            gans_value_function = MiniMax()

        if feature_matching is False:
            feature_matching = FeatureMatching()

        if isinstance(gans_value_function, GANsValueFunction) is False:
            raise TypeError("The type of `gans_value_function` must be `GANsValueFunction`.")
        
        if isinstance(feature_matching, FeatureMatching) is False and feature_matching is not None:
            raise TypeError("The type of `feature_matching` must be `FeatureMatching`.")

        self.__gans_value_function = gans_value_function
        self.__feature_matching = feature_matching
        self.__logger = getLogger("pygan")

    def train(
        self,
        true_sampler,
        generative_model,
        discriminative_model,
        iter_n=100,
        k_step=10
    ):
        '''
        Train.

        Args:
            true_sampler:           Sampler which draws samples from the `true` distribution.
            generative_model:       Generator which draws samples from the `fake` distribution.
            discriminative_model:   Discriminator which discriminates `true` from `fake`.
            iter_n:                 The number of training iterations.
            k_step:                 The number of learning of the discriminative_model.
        
        Returns:
            Tuple data.
            - trained Generator which is-a `GenerativeModel`.
            - trained Discriminator which is-a `DiscriminativeModel`.
        '''
        if isinstance(true_sampler, TrueSampler) is False:
            raise TypeError("The type of `true_sampler` must be `TrueSampler`.")
        if isinstance(generative_model, GenerativeModel) is False:
            raise TypeError("The type of `generative_model` must be `GenerativeModel`.")
        if isinstance(discriminative_model, DiscriminativeModel) is False:
            raise TypeError("The type of `discriminative_model` must be `DiscriminativeModel`.")

        generative_model.switch_inferencing_mode(inferencing_mode=False)
        d_logs_list = []
        g_logs_list = []
        try:
            for n in range(iter_n):
                self.__logger.debug("-" * 100)
                self.__logger.debug("Iterations: (" + str(n+1) + "/" + str(iter_n) + ")")
                self.__logger.debug("-" * 100)
                self.__logger.debug(
                    "The `discriminator`'s turn."
                )
                self.__logger.debug("-" * 100)

                discriminative_model, d_logs_list = self.train_discriminator(
                    k_step,
                    true_sampler,
                    generative_model,
                    discriminative_model,
                    d_logs_list
                )

                self.__logger.debug("-" * 100)
                self.__logger.debug(
                    "The `generator`'s turn."
                )
                self.__logger.debug("-" * 100)

                generative_model, g_logs_list = self.train_generator(
                    true_sampler,
                    generative_model,
                    discriminative_model,
                    g_logs_list
                )

        except KeyboardInterrupt:
            print("Keyboard Interrupt.")

        self.__logs_tuple = (d_logs_list, g_logs_list)
        generative_model.switch_inferencing_mode(inferencing_mode=True)
        return generative_model, discriminative_model

    def train_discriminator(
        self,
        k_step,
        true_sampler,
        generative_model,
        discriminative_model,
        d_logs_list
    ):
        '''
        Train the discriminator.

        Args:
            k_step:                 The number of learning of the discriminative_model.
            true_sampler:           Sampler which draws samples from the `true` distribution.
            generative_model:       Generator which draws samples from the `fake` distribution.
            discriminative_model:   Discriminator which discriminates `true` from `fake`.
            d_logs_list:            `list` of probabilities inferenced by the `discriminator` (mean) in the `discriminator`'s update turn.

        Returns:
            Tuple data. The shape is...
            - Discriminator which discriminates `true` from `fake`.
            - `list` of probabilities inferenced by the `discriminator` (mean) in the `discriminator`'s update turn.

        '''
        for k in range(k_step):
            true_arr = true_sampler.draw()
            generated_arr = generative_model.draw()
            true_posterior_arr = discriminative_model.inference(true_arr)
            generated_posterior_arr = discriminative_model.inference(generated_arr)
            grad_arr = self.__gans_value_function.compute_discriminator_reward(
                true_posterior_arr,
                generated_posterior_arr
            )
            discriminative_model.learn(grad_arr)

            self.__logger.debug(
                "Inferenced by the `discriminator` (mean): " + str(generated_posterior_arr.mean())
            )
            self.__logger.debug(
                "Inferenced by the `discriminator` (MAE): " + str(np.abs(generated_posterior_arr).mean())
            )
            self.__logger.debug(
                "And update the `discriminator` by descending its stochastic gradient(means): " + str(grad_arr.mean())
            )

            d_logs_list.append(generated_posterior_arr.mean())

        return discriminative_model, d_logs_list

    def train_generator(
        self,
        true_sampler,
        generative_model,
        discriminative_model,
        g_logs_list
    ):
        '''
        Train the generator.

        Args:
            true_sampler:           Sampler which draws samples from the `true` distribution.
            generative_model:       Generator which draws samples from the `fake` distribution.
            discriminative_model:   Discriminator which discriminates `true` from `fake`.
            g_logs_list:            `list` of Probabilities inferenced by the `discriminator` (mean) in the `generator`'s update turn.

        Returns:
            Tuple data. The shape is...
            - Generator which draws samples from the `fake` distribution.
            - `list` of probabilities inferenced by the `discriminator` (mean) in the `generator`'s update turn.

        '''
        generated_arr = generative_model.draw()
        generated_posterior_arr = discriminative_model.inference(generated_arr)
        grad_arr = self.__gans_value_function.compute_generator_reward(
            generated_posterior_arr
        )
        grad_arr = discriminative_model.learn(grad_arr, fix_opt_flag=True)

        if self.__feature_matching is None:
            grad_arr = grad_arr.reshape(generated_arr.shape)
            generative_model.learn(grad_arr)
        else:
            grad_arr = self.__feature_matching.compute_delta(
                true_sampler=true_sampler, 
                discriminative_model=discriminative_model,
                generated_arr=generated_arr
            )
            grad_arr = grad_arr.reshape(generated_arr.shape)
            generative_model.learn(grad_arr)

            self.__logger.debug(
                "Loss of Feature matching: " + str(self.__feature_matching.loss_arr[-1])
            )

        self.__logger.debug(
            "Inferenced by the `discriminator` (mean): " + str(generated_posterior_arr.mean())
        )
        self.__logger.debug(
            "Inferenced by the `discriminator` (MAE): " + str(np.abs(generated_posterior_arr).mean())
        )
        self.__logger.debug(
            "And update the `generator` by descending its stochastic gradient(means): " + str(grad_arr.mean())
        )
        g_logs_list.append(generated_posterior_arr.mean())

        return generative_model, g_logs_list

    def extract_logs_tuple(self):
        '''
        Extract update logs data.

        Returns:
            The shape is:
            - `list` of probabilities inferenced by the `discriminator` (mean) in the `discriminator`'s update turn.
            - `list` of probabilities inferenced by the `discriminator` (mean) in the `generator`'s update turn.
        '''
        return self.__logs_tuple

    def get_feature_matching(self):
        ''' getter '''
        return self.__feature_matching
    
    def set_readonly(self, value):
        ''' setter '''
        raise TypeError("This property must be read-only.")
    
    feature_matching = property(get_feature_matching, set_readonly)
