# -*- coding: utf-8 -*-
import numpy as np
from logging import getLogger

from pygan.generativemodel.auto_encoder_model import AutoEncoderModel
from pygan.true_sampler import TrueSampler

from pydbm.cnn.convolutionalneuralnetwork.convolutional_auto_encoder import ConvolutionalAutoEncoder as CAE
from pydbm.cnn.layerablecnn.convolution_layer import ConvolutionLayer as ConvolutionLayer1
from pydbm.cnn.layerablecnn.convolution_layer import ConvolutionLayer as ConvolutionLayer2
from pydbm.cnn.layerablecnn.convolutionlayer.deconvolution_layer import DeconvolutionLayer
from pydbm.synapse.cnn_graph import CNNGraph as DeCNNGraph

from pydbm.synapse.cnn_graph import CNNGraph as ConvGraph1
from pydbm.synapse.cnn_graph import CNNGraph as ConvGraph2
from pydbm.activation.tanh_function import TanhFunction
from pydbm.activation.logistic_function import LogisticFunction
from pydbm.loss.mean_squared_error import MeanSquaredError
from pydbm.optimization.optparams.adam import Adam
from pydbm.optimization.opt_params import OptParams
from pydbm.verification.verificate_function_approximation import VerificateFunctionApproximation


class ConvolutionalAutoEncoder(AutoEncoderModel):
    '''
    Convolutional Auto-Encoder(CAE) as a `AutoEncoderModel`.

    A stack of Convolutional Auto-Encoder (Masci, J., et al., 2011) 
    forms a convolutional neural network(CNN), which are among the most successful models 
    for supervised image classification.  Each Convolutional Auto-Encoder is trained 
    using conventional on-line gradient descent without additional regularization terms.
    
    In this library, Convolutional Auto-Encoder is also based on Encoder/Decoder scheme.
    The encoder is to the decoder what the Convolution is to the Deconvolution.
    The Deconvolution also called transposed convolutions 
    "work by swapping the forward and backward passes of a convolution." (Dumoulin, V., & Visin, F. 2016, p20.)

    References:
        - Dumoulin, V., & V,kisin, F. (2016). A guide to convolution arithmetic for deep learning. arXiv preprint arXiv:1603.07285.
        - Masci, J., Meier, U., Cireşan, D., & Schmidhuber, J. (2011, June). Stacked convolutional auto-encoders for hierarchical feature extraction. In International Conference on Artificial Neural Networks (pp. 52-59). Springer, Berlin, Heidelberg.

    '''

    def __init__(
        self,
        batch_size=20,
        learning_rate=1e-10,
        learning_attenuate_rate=0.1,
        attenuate_epoch=50,
        opt_params=None,
        convolutional_auto_encoder=None,
        deconvolution_layer_list=None,
        gray_scale_flag=True,
        channel=None
    ):
        '''
        Init.

        Args:
            batch_size:                     Batch size in mini-batch.
            learning_rate:                  Learning rate.
            learning_attenuate_rate:        Attenuate the `learning_rate` by a factor of this value every `attenuate_epoch`.
            attenuate_epoch:                Attenuate the `learning_rate` by a factor of `learning_attenuate_rate` every `attenuate_epoch`.
                                            Additionally, in relation to regularization,
                                            this class constrains weight matrixes every `attenuate_epoch`.

            convolutional_auto_encoder:     is-a `pydbm.cnn.convolutionalneuralnetwork.convolutional_auto_encoder.ConvolutionalAutoEncoder`.
            deconvolution_layer_list:       `list` of `DeconvolutionLayer`.
            gray_scale_flag:                Gray scale or not.
                                            This parameter will be refered when `channel` is None.
                                            If `True`, the channel will be `1`. If `False`, the channel will be `3`.

            channel:                        Channel.
        '''
        if channel is None:
            if gray_scale_flag is True:
                channel = 1
            else:
                channel = 3

        if opt_params is None:
            opt_params = Adam()
            opt_params.weight_limit = 1e+10
            opt_params.dropout_rate = 0.0

        if isinstance(opt_params, OptParams) is False:
            raise TypeError()

        scale = 0.01
        if convolutional_auto_encoder is None:
            conv1 = ConvolutionLayer1(
                ConvGraph1(
                    activation_function=TanhFunction(),
                    filter_num=batch_size,
                    channel=channel,
                    kernel_size=3,
                    scale=scale,
                    stride=1,
                    pad=1
                )
            )

            conv2 = ConvolutionLayer2(
                ConvGraph2(
                    activation_function=TanhFunction(),
                    filter_num=batch_size,
                    channel=batch_size,
                    kernel_size=3,
                    scale=scale,
                    stride=1,
                    pad=1
                )
            )

            convolutional_auto_encoder = CAE(
                layerable_cnn_list=[
                    conv1, 
                    conv2
                ],
                epochs=100,
                batch_size=batch_size,
                learning_rate=learning_rate,
                learning_attenuate_rate=learning_attenuate_rate,
                attenuate_epoch=attenuate_epoch,
                computable_loss=MeanSquaredError(),
                opt_params=opt_params,
                verificatable_result=VerificateFunctionApproximation(),
                test_size_rate=0.3,
                tol=1e-15,
                save_flag=False
            )

        if deconvolution_layer_list is None:
            deconvolution_layer_list = [DeconvolutionLayer(
                DeCNNGraph(
                    activation_function=TanhFunction(),
                    filter_num=batch_size,
                    channel=channel,
                    kernel_size=3,
                    scale=scale,
                    stride=1,
                    pad=1
                )
            )]

        self.__convolutional_auto_encoder = convolutional_auto_encoder
        self.__deconvolution_layer_list = deconvolution_layer_list
        self.__opt_params = opt_params

        self.__learning_rate = learning_rate
        self.__attenuate_epoch = attenuate_epoch
        self.__learning_attenuate_rate = learning_attenuate_rate

        self.__batch_size = batch_size
        self.__saved_img_n = 0
        self.__attenuate_epoch = 50

        self.__epoch_counter = 0

        logger = getLogger("pygan")
        self.__logger = logger

    def pre_learn(self, true_sampler, epochs=1000):
        '''
        Pre learning.

        Args:
            true_sampler:       is-a `TrueSampler`.
            epochs:             Epochs.
        '''
        if isinstance(true_sampler, TrueSampler) is False:
            raise TypeError("The type of `true_sampler` must be `TrueSampler`.")
        
        learning_rate = self.__learning_rate

        pre_loss_list = []
        for epoch in range(epochs):
            if (epoch + 1) % self.__attenuate_epoch == 0:
                learning_rate = learning_rate * self.__learning_attenuate_rate

            try:
                observed_arr = true_sampler.draw()
                inferenced_arr = self.inference(observed_arr)
                if observed_arr.size != inferenced_arr.size:
                    raise ValueError("In pre-learning, the rank or shape of observed data points and feature points in last layer must be equivalent.")
                grad_arr = self.__convolutional_auto_encoder.computable_loss.compute_delta(observed_arr, inferenced_arr)
                loss = self.__convolutional_auto_encoder.computable_loss.compute_loss(observed_arr, inferenced_arr)
                pre_loss_list.append(loss)
                self.__logger.debug("Epoch: " + str(epoch) + " loss: " + str(loss))
                _ = self.__convolutional_auto_encoder.back_propagation(grad_arr)
                self.__convolutional_auto_encoder.optimize(learning_rate, epoch)
            except KeyboardInterrupt:
                self.__logger.debug("Interrupt.")
                break

        self.__pre_loss_arr = np.array(pre_loss_list)

    def draw(self):
        '''
        Draws samples from the `fake` distribution.

        Returns:
            `np.ndarray` of samples.
        '''
        observed_arr = self.noise_sampler.generate()
        _ = self.inference(observed_arr)
        feature_arr = self.__convolutional_auto_encoder.extract_feature_points_arr()
        for i in range(len(self.__deconvolution_layer_list)):
            try:
                feature_arr = self.__deconvolution_layer_list[i].forward_propagate(feature_arr)
            except:
                self.__logger.debug("Error raised in Deconvolution layer " + str(i + 1))
                raise

        return feature_arr

    def inference(self, observed_arr):
        '''
        Draws samples from the `fake` distribution.

        Args:
            observed_arr:     `np.ndarray` of observed data points.
        
        Returns:
            `np.ndarray` of inferenced.
        '''
        return self.__convolutional_auto_encoder.inference(observed_arr)

    def learn(self, grad_arr):
        '''
        Update this Discriminator by ascending its stochastic gradient.

        Args:
            grad_arr:   `np.ndarray` of gradients.

        Returns:
            `np.ndarray` of delta or gradients.

        '''
        if ((self.__epoch_counter + 1) % self.__attenuate_epoch == 0):
            self.__learning_rate = self.__learning_rate * self.__learning_attenuate_rate

        deconvolution_layer_list = self.__deconvolution_layer_list[::-1]
        for i in range(len(deconvolution_layer_list)):
            try:
                grad_arr = deconvolution_layer_list[i].back_propagate(grad_arr)
            except:
                self.__logger.debug("Error raised in Convolution layer " + str(i + 1))
                raise

        self.__optimize_deconvolution_layer(self.__learning_rate, self.__epoch_counter)

        layerable_cnn_list = self.__convolutional_auto_encoder.layerable_cnn_list[::-1]
        for i in range(len(layerable_cnn_list)):
            try:
                grad_arr = layerable_cnn_list[i].back_propagate(grad_arr)
            except:
                self.__logger.debug(
                    "Delta computation raised an error in CNN layer " + str(len(layerable_cnn_list) - i)
                )
                raise

        self.__convolutional_auto_encoder.optimize(self.__learning_rate, self.__epoch_counter)

        self.__epoch_counter += 1
        return grad_arr

    def __optimize_deconvolution_layer(self, learning_rate, epoch):
        '''
        Back propagation for Deconvolution layer.
        
        Args:
            learning_rate:  Learning rate.
            epoch:          Now epoch.
            
        '''
        params_list = []
        grads_list = []

        for i in range(len(self.__deconvolution_layer_list)):
            if self.__deconvolution_layer_list[i].delta_weight_arr.shape[0] > 0:
                params_list.append(self.__deconvolution_layer_list[i].graph.weight_arr)
                grads_list.append(self.__deconvolution_layer_list[i].delta_weight_arr)

        for i in range(len(self.__deconvolution_layer_list)):
            if self.__deconvolution_layer_list[i].delta_bias_arr.shape[0] > 0:
                params_list.append(self.__deconvolution_layer_list[i].graph.bias_arr)
                grads_list.append(self.__deconvolution_layer_list[i].delta_bias_arr)

        params_list = self.__opt_params.optimize(
            params_list,
            grads_list,
            learning_rate
        )

        i = 0
        for i in range(len(self.__deconvolution_layer_list)):
            if self.__deconvolution_layer_list[i].delta_weight_arr.shape[0] > 0:
                self.__deconvolution_layer_list[i].graph.weight_arr = params_list.pop(0)
                if ((epoch + 1) % self.__attenuate_epoch == 0):
                    self.__deconvolution_layer_list[i].graph.weight_arr = self.__opt_params.constrain_weight(
                        self.__deconvolution_layer_list[i].graph.weight_arr
                    )

        for i in range(len(self.__deconvolution_layer_list)):
            if self.__deconvolution_layer_list[i].delta_bias_arr.shape[0] > 0:
                self.__deconvolution_layer_list[i].graph.bias_arr = params_list.pop(0)

        for i in range(len(self.__deconvolution_layer_list)):
            if self.__deconvolution_layer_list[i].delta_weight_arr.shape[0] > 0:
                if self.__deconvolution_layer_list[i].delta_bias_arr.shape[0] > 0:
                    self.__deconvolution_layer_list[i].reset_delta()

    def update(self):
        '''
        Update the encoder and the decoder
        to minimize the reconstruction error of the inputs.

        Returns:
            `np.ndarray` of the reconstruction errors.
        '''
        if ((self.__epoch_counter + 1) % self.__attenuate_epoch == 0):
            self.__learning_rate = self.__learning_rate * self.__learning_attenuate_rate

        observed_arr = self.noise_sampler.generate()
        inferenced_arr = self.inference(observed_arr)

        error_arr = self.__convolutional_auto_encoder.computable_loss.compute_loss(
            observed_arr,
            inferenced_arr
        )

        delta_arr = self.__convolutional_auto_encoder.computable_loss.compute_delta(
            observed_arr,
            inferenced_arr
        )

        delta_arr = self.__convolutional_auto_encoder.back_propagation(delta_arr)
        self.__convolutional_auto_encoder.optimize(self.__learning_rate, self.__epoch_counter)

        self.__epoch_counter += 1
        return error_arr

    def switch_inferencing_mode(self, inferencing_mode=True):
        '''
        Set inferencing mode in relation to concrete regularizations.

        Args:
            inferencing_mode:       Inferencing mode or not.
        '''
        self.__opt_params.inferencing_mode = inferencing_mode
        self.__convolutional_auto_encoder.opt_params.inferencing_mode = inferencing_mode

    def get_convolutional_auto_encoder(self):
        ''' getter '''
        return self.__convolutional_auto_encoder
    
    def set_convolutional_auto_encoder(self, value):
        ''' setter '''
        raise TypeError("This property must be read-only.")
    
    convolutional_auto_encoder = property(get_convolutional_auto_encoder, set_convolutional_auto_encoder)

    def get_deconvolution_layer_list(self):
        ''' getter '''
        return self.__deconvolution_layer_list
    
    def set_deconvolution_layer_list(self, value):
        ''' setter '''
        self.__deconvolution_layer_list = value
    
    deconvolution_layer_list = property(get_deconvolution_layer_list, set_deconvolution_layer_list)

    def set_readonly(self, value):
        ''' setter '''
        raise TypeError("This property must be read-only.")
    
    def get_pre_loss_arr(self):
        ''' getter '''
        return self.__pre_loss_arr

    pre_loss_arr = property(get_pre_loss_arr, set_readonly)
