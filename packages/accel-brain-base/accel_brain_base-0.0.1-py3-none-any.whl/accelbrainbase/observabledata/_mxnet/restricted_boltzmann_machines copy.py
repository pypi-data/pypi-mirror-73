# -*- coding: utf-8 -*-
import numpy as np
import mxnet.ndarray as nd
import mxnet as mx
import warnings
from accelbrainbase.observable_data import ObservableData
from accelbrainbase.activatabledata._mxnet.activatable_data import ActivatableData
from accelbrainbase.activatabledata._mxnet.activatabledata.logistic_function import LogisticFunction
from accelbrainbase.computable_delta import ComputableDelta
from accelbrainbase.computabledelta._mxnet.mean_squared_error import MeanSquaredError
from accelbrainbase.optimizabledata._mxnet.optimizable_data import OptimizableData
from accelbrainbase.optimizabledata._mxnet.optimizabledata.sgd import SGD
from accelbrainbase.iteratable_data import IteratableData
from logging import getLogger


class RestrictedBoltzmannMachines(ObservableData):
    '''
    Restricted Boltzmann Machines(RBM).
    
    According to graph theory, the structure of RBM corresponds to 
    a complete bipartite graph which is a special kind of bipartite 
    graph where every node in the visible layer is connected to every 
    node in the hidden layer. Based on statistical mechanics and 
    thermodynamics(Ackley, D. H., Hinton, G. E., & Sejnowski, T. J. 1985), 
    the state of this structure can be reflected by the energy function.

    In relation to RBM, the Contrastive Divergence(CD) is a method for 
    approximation of the gradients of the log-likelihood(Hinton, G. E. 2002).
    This algorithm draws a distinction between a positive phase and a 
    negative phase. Conceptually, the positive phase is to the negative 
    phase what waking is to sleeping.

    The procedure of this method is similar to Markov Chain Monte Carlo method(MCMC).
    However, unlike MCMC, the visbile variables to be set first in visible layer is 
    not randomly initialized but the observed data points in training dataset are set 
    to the first visbile variables. And, like Gibbs sampler, drawing samples from hidden 
    variables and visible variables is repeated k times. Empirically (and surprisingly), 
    `k` is considered to be `1`.

    References:
        - Ackley, D. H., Hinton, G. E., & Sejnowski, T. J. (1985). A learning algorithm for Boltzmann machines. Cognitive science, 9(1), 147-169.
        - Hinton, G. E. (2002). Training products of experts by minimizing contrastive divergence. Neural computation, 14(8), 1771-1800.
        - Le Roux, N., & Bengio, Y. (2008). Representational power of restricted Boltzmann machines and deep belief networks. Neural computation, 20(6), 1631-1649.
    '''

    # The list of losses.
    __loss_arr = []
    # Learning rate.
    __learning_rate = 0.5
    # Batch size in learning.
    __batch_size = 0
    # Batch size in inference(recursive learning or not).
    __r_batch_size = 0

    def __init__(
        self,
        visible_activatable_data,
        hidden_activatable_data,
        hidden_dim=100,
        weights_arr=None,
        computable_delta=None,
        optimizable_data=None,
        learning_rate=0.005,
        learning_attenuate_rate=1.0,
        attenuate_epoch=50,
        scale=None
    ):
        '''
        Init.
        
        Args:
            computable_delta:                Loss function.
            optimizable_data:                Optimization function.
        '''
        if isinstance(visible_activatable_data, ActivatableData) is False:
            raise TypeError("The type of `visible_activatable_data` must be `ActivatableData`.")
        if isinstance(hidden_activatable_data, ActivatableData) is False:
            raise TypeError("The type of `hidden_activatable_data` must be `ActivatableData`.")

        self.__visible_activatable_data = visible_activatable_data
        self.__hidden_activatable_data = hidden_activatable_data

        if computable_delta is None:
            computable_delta = MeanSquaredError(weight=1/hidden_dim)
        elif isinstance(computable_delta, ComputableDelta) is False:
            raise TypeError("The type of `computable_delta` must be `ComputableDelta`.")

        if optimizable_data is None:
            optimizable_data = SGD(momentum=0.0)
        elif isinstance(optimizable_data, OptimizableData) is False:
            raise TypeError("The type of `optimizable_data` must be `OptimizableData`.")

        self.__computable_delta = computable_delta
        self.__optimizable_data = optimizable_data

        self.__hidden_dim = hidden_dim
        self.__weights_arr = weights_arr
        self.__visible_bias_arr = None
        self.__hidden_bias_arr = None

        self.__diff_weights_arr = None
        self.__visible_diff_bias_arr = None
        self.__hidden_diff_bias_arr = None

        self.__learning_rate = learning_rate
        self.__learning_attenuate_rate = learning_attenuate_rate
        self.__attenuate_epoch = attenuate_epoch

        self.__loss_arr = np.array([])

        self.__scale = scale

        logger = getLogger("accelbrainbase")
        self.__logger = logger

        self.__loss_list = []
        self.__test_loss_list = []

    def learn(self, iteratable_data):
        '''
        Learn samples drawn by `IteratableData.generate_learned_samples()`.

        Args:
            iteratable_data:     is-a `IteratableData`.

        '''
        if isinstance(iteratable_data, IteratableData) is False:
            raise TypeError("The type of `iteratable_data` must be `IteratableData`.")

        self.__loss_list = []
        self.__test_loss_list = []

        try:
            epoch = 0
            for observed_arr, label_arr, test_observed_arr, test_label_arr in iteratable_data.generate_learned_samples():
                if ((epoch + 1) % self.__attenuate_epoch == 0):
                    self.__learning_rate = self.__learning_rate * self.__learning_attenuate_rate

                self.wake_sleep(observed_arr)
                """
                self.sleep_wake(
                    feature_points_arr=self.__hidden_activity_arr
                )
                """
                self.wake_sleep(test_observed_arr, inferencing_mode=True)
                self.sleep_wake(
                    feature_points_arr=self.__hidden_activity_arr,
                    inferencing_mode=True
                )

                if (epoch + 1) % 100 == 0:
                    self.__logger.debug("Epoch: " + str(epoch + 1) + " Train loss: " + str(self.__loss_list[-1]) + " Test loss: " + str(self.__test_loss_list[-1]))

                epoch = epoch + 1
        except KeyboardInterrupt:
            self.__logger.debug("Interrupt.")

        self.__logger.debug("end. ")

        self.__loss_arr = np.c_[
            np.array(self.__loss_list[:len(self.__test_loss_list)]),
            np.array(self.__test_loss_list)
        ]

    def inference(self, observed_arr):
        '''
        Inference samples drawn by `IteratableData.generate_inferenced_samples()`.

        Args:
            observed_arr:   rank-2 Array like or sparse matrix as the observed data points.
                            The shape is: (batch size, feature points)

        Returns:
            `mxnet.ndarray` of inferenced feature points.
        '''
        self.wake_sleep(observed_arr, inferencing_mode=True)
        self.sleep_wake(self.__hidden_activity_arr, inferencing_mode=True)
        return self.__visible_activity_arr

    def __initialize(self):
        if self.__scale is None:
            self.__scale = np.sqrt(1 / ((self.__visible_activity_arr.shape[1])))

        if self.__weights_arr is None:
            self.__weights_arr = nd.random.normal(
                shape=(
                    self.__visible_activity_arr.shape[1],
                    self.__hidden_dim
                ),
                ctx=self.__visible_activity_arr.context,
                loc=0, 
                scale=1
            ) * self.__scale

        if self.__visible_bias_arr is None:
            self.__visible_bias_arr = nd.zeros(
                (self.__visible_activity_arr.shape[1]),
                ctx=self.__visible_activity_arr.context
            )

        if self.__hidden_bias_arr is None:
            self.__hidden_bias_arr = nd.zeros(
                (self.__hidden_dim),
                ctx=self.__visible_activity_arr.context
            )

        if self.__diff_weights_arr is None:
            self.__diff_weights_arr = nd.zeros_like(self.__weights_arr)
        
        if self.__visible_diff_bias_arr is None:
            self.__visible_diff_bias_arr = nd.zeros_like(self.__visible_bias_arr)

        if self.__hidden_diff_bias_arr is None:
            self.__hidden_diff_bias_arr = nd.zeros_like(self.__hidden_bias_arr)

    def wake_sleep(self, observed_arr, inferencing_mode=False):
        '''
        Waking, sleeping, and learning.

        Standing on the premise that the settings of
        the activation function and weights operation are common.

        Args:
            observed_arr:       Observed data points.
            inferencing_mode:   Inferencing mode or learning mode.
        '''
        self.__observed_arr = observed_arr
        # Waking.
        self.__visible_activity_arr = observed_arr.copy()
        # Dynamic initialization.
        self.__initialize()

        self.__hidden_activity_arr = self.__hidden_activatable_data.activate(
            nd.dot(
                self.__visible_activity_arr,
                self.__weights_arr
            ) + self.__hidden_bias_arr
        )

        # Dropout.
        self.__hidden_activatable_data.inferencing_mode = inferencing_mode
        self.__hidden_activity_arr = self.__hidden_activatable_data.dropout(
            self.__hidden_activity_arr
        )

        if inferencing_mode is False:
            self.__diff_weights_arr += nd.dot(
                self.__visible_activity_arr.T,
                self.__hidden_activity_arr
            )

            self.__visible_diff_bias_arr += nd.nansum(self.__visible_activity_arr, axis=0)
            self.__hidden_diff_bias_arr += nd.nansum(self.__hidden_activity_arr, axis=0)

        # Sleeping.
        self.__visible_activity_arr = self.__visible_activatable_data.activate(
            nd.dot(
                self.__hidden_activity_arr,
                self.__weights_arr.T
            ) + self.__visible_bias_arr
        )

        self.__hidden_activity_arr = self.__hidden_activatable_data.activate(
            nd.dot(
                self.__visible_activity_arr, 
                self.__weights_arr
            ) + self.__hidden_bias_arr
        )

        # Dropout.
        self.__hidden_activity_arr = self.__hidden_activatable_data.de_dropout(
            self.__hidden_activity_arr
        )

        # Validation.
        if inferencing_mode is False:
            print("-")
            arr = self.__observed_arr.asnumpy()
            print((arr.min(), arr.mean(), arr.max()))
            arr = self.__visible_activity_arr.asnumpy()
            print((arr.min(), arr.mean(), arr.max()))

            loss = self.__computable_delta.compute_loss(
                self.__observed_arr, 
                self.__visible_activity_arr
            ).mean()
            loss += self.__optimizable_data.compute_weight_decay(
                self.__weights_arr
            )
            self.__loss_list.append(loss.asnumpy()[0])

        if inferencing_mode is False:
            self.__diff_weights_arr -= nd.dot(
                self.__visible_activity_arr.T,
                self.__hidden_activity_arr
            )
            self.__visible_diff_bias_arr -= nd.nansum(self.__visible_activity_arr, axis=0)
            self.__hidden_diff_bias_arr -= nd.nansum(self.__hidden_activity_arr, axis=0)
            self.__diff_weights_arr += self.__optimizable_data.compute_weight_decay_delta(
                self.__weights_arr
            )

        if inferencing_mode is False:
            # Learning.
            params_list= [
                self.__visible_bias_arr,
                self.__hidden_bias_arr,
                self.__weights_arr
            ]
            grads_list = [
                self.__visible_diff_bias_arr / self.__observed_arr.shape[0],
                self.__hidden_diff_bias_arr / self.__observed_arr.shape[0],
                self.__diff_weights_arr / self.__observed_arr.shape[0]
            ]

            if self.__visible_activatable_data.batch_norm is not None:
                params_list.append(
                    self.__visible_activatable_data.batch_norm.beta_arr
                )
                params_list.append(
                    self.__visible_activatable_data.batch_norm.gamma_arr
                )
                grads_list.append(
                    self.__visible_activatable_data.batch_norm.delta_beta_arr
                )
                grads_list.append(
                    self.__visible_activatable_data.batch_norm.delta_gamma_arr
                )

            if self.__hidden_activatable_data.batch_norm is not None:
                params_list.append(
                    self.__hidden_activatable_data.batch_norm.beta_arr
                )
                params_list.append(
                    self.__hidden_activatable_data.batch_norm.gamma_arr
                )
                grads_list.append(
                    self.__hidden_activatable_data.batch_norm.delta_beta_arr
                )
                grads_list.append(
                    self.__hidden_activatable_data.batch_norm.delta_gamma_arr
                )

            params_list = self.__optimizable_data.optimize(
                params_list=params_list,
                grads_list=grads_list,
                learning_rate=self.__learning_rate
            )
            self.__visible_bias_arr = params_list.pop(0)
            self.__hidden_bias_arr = params_list.pop(0)
            self.__weights_arr = params_list.pop(0)
            arr = self.__visible_bias_arr.asnumpy()

            if self.__visible_activatable_data.batch_norm is not None:
                self.__visible_activatable_data.batch_norm.beta_arr = params_list.pop(0)
                self.__visible_activatable_data.batch_norm.gamma_arr = params_list.pop(0)

            if self.__hidden_activatable_data.batch_norm is not None:
                self.__hidden_activatable_data.batch_norm.beta_arr = params_list.pop(0)
                self.__hidden_activatable_data.batch_norm.gamma_arr = params_list.pop(0)

        self.__visible_diff_bias_arr = nd.zeros_like(self.__visible_bias_arr)
        self.__hidden_diff_bias_arr = nd.zeros_like(self.__hidden_bias_arr)
        self.__diff_weights_arr = nd.zeros_like(self.__weights_arr, dtype=np.float64)

    def sleep_wake(self, feature_points_arr=None, inferencing_mode=False):
        '''
        Sleeping, waking, and learning.

        Args:
            feature_points_arr: Feature points.
            inferencing_mode:   Inferencing mode or learning mode.
        '''
        # Sleeping.
        if feature_points_arr is not None:
            self.__hidden_activity_arr = feature_points_arr

        self.__visible_activity_arr = self.__visible_activatable_data.activate(
            nd.dot(
                self.__hidden_activity_arr, 
                self.__weights_arr.T
            ) + self.__visible_bias_arr
        )

        self.__hidden_activity_arr = self.__hidden_activatable_data.activate(
            nd.dot(
                self.__visible_activity_arr, 
                self.__weights_arr
            ) + self.__hidden_bias_arr
        )

        if inferencing_mode is False:
            self.__diff_weights_arr -= nd.dot(
                self.__visible_activity_arr.T,
                self.__hidden_activity_arr
            )

            self.__visible_diff_bias_arr -= nd.nansum(self.__visible_activity_arr, axis=0)
            self.__hidden_diff_bias_arr -= nd.nansum(self.__hidden_activity_arr, axis=0)

        # Waking.
        self.__hidden_activity_arr = self.__hidden_activatable_data.activate(
            nd.dot(
                self.__visible_activity_arr, 
                self.__weights_arr
            ) + self.__hidden_bias_arr
        )

        # Validation.
        if inferencing_mode is True:
            loss = self.__computable_delta.compute_loss(
                self.__observed_arr, 
                self.__visible_activity_arr
            ).mean()
            loss += self.__optimizable_data.compute_weight_decay(
                self.__weights_arr
            )
            self.__test_loss_list.append(loss.asnumpy()[0])

        if inferencing_mode is False:
            self.__diff_weights_arr += nd.dot(
                self.__visible_activity_arr.T,
                self.__hidden_activity_arr
            )

            self.__visible_diff_bias_arr += nd.nansum(self.__visible_activity_arr, axis=0)
            self.__hidden_diff_bias_arr += nd.nansum(self.__hidden_activity_arr, axis=0)

            self.__diff_weights_arr += self.__optimizable_data.compute_weight_decay_delta(
                self.__weights_arr
            )

        if inferencing_mode is False:
            # Learning.
            params_list = [
                self.__visible_bias_arr,
                self.__hidden_bias_arr,
                self.__weights_arr
            ]
            grads_list = [
                self.__visible_diff_bias_arr / self.__observed_arr.shape[0],
                self.__hidden_diff_bias_arr / self.__observed_arr.shape[0],
                self.__diff_weights_arr / self.__observed_arr.shape[0]
            ]

            if self.__visible_activatable_data.batch_norm is not None:
                params_list.append(
                    self.__visible_activatable_data.batch_norm.beta_arr
                )
                params_list.append(
                    self.__visible_activatable_data.batch_norm.gamma_arr
                )
                grads_list.append(
                    self.__visible_activatable_data.batch_norm.delta_beta_arr
                )
                grads_list.append(
                    self.__visible_activatable_data.batch_norm.delta_gamma_arr
                )

            if self.__hidden_activatable_data.batch_norm is not None:
                params_list.append(
                    self.__hidden_activatable_data.batch_norm.beta_arr
                )
                params_list.append(
                    self.__hidden_activatable_data.batch_norm.gamma_arr
                )
                grads_list.append(
                    self.__hidden_activatable_data.batch_norm.delta_beta_arr
                )
                grads_list.append(
                    self.__hidden_activatable_data.batch_norm.delta_gamma_arr
                )

            params_list = self.__optimizable_data.optimize(
                params_list=params_list,
                grads_list=grads_list,
                learning_rate=self.__learning_rate
            )
            self.__visible_bias_arr = params_list.pop(0)
            self.__hidden_bias_arr = params_list.pop(0)
            self.__weights_arr = params_list.pop(0)

            if self.__visible_activatable_data.batch_norm is not None:
                self.__visible_activatable_data.batch_norm.beta_arr = params_list.pop(0)
                self.__visible_activatable_data.batch_norm.gamma_arr = params_list.pop(0)

            if self.__hidden_activatable_data.batch_norm is not None:
                self.__hidden_activatable_data.batch_norm.beta_arr = params_list.pop(0)
                self.__hidden_activatable_data.batch_norm.gamma_arr = params_list.pop(0)

        self.__visible_diff_bias_arr = nd.zeros_like(self.__visible_bias_arr)
        self.__hidden_diff_bias_arr = nd.zeros_like(self.__hidden_bias_arr)
        self.__diff_weights_arr = nd.zeros_like(self.__weights_arr, dtype=np.float64)

    def extract_learned_dict(self):
        '''
        Extract (pre-) learned parameters.

        Returns:
            `dict` of the parameters.
        '''
        params_arr_dict = {
            "weights_arr": self.weights_arr,
            "visible_bias_arr": self.visible_bias_arr,
            "hidden_bias_arr": self.hidden_bias_arr
        }
        
        return params_arr_dict

    def save_parameters(self, filename):
        '''
        Save parameters to files.

        Args:
            filename:       File name.
        '''
        params_arr_dict = self.extract_learned_dict()
        mx.nd.save(filename, params_arr_dict)

    def load_parameters(self, filename):
        '''
        Load parameters to files.

        Args:
            filename:       File name.
        '''
        params_arr_dict = mx.nd.load(filename)
        self.__weights_arr = params_arr_dict["weights_arr"]
        self.__visible_bias_arr = params_arr_dict["visible_bias_arr"]
        self.__hidden_bias_arr = params_arr_dict["hidden_bias_arr"]

    def set_readonly(self, value):
        ''' setter '''
        raise TypeError("This is read-only.")

    def get_loss_list(self):
        ''' getter for `list` of losses in training. '''
        return self.__loss_list

    loss_list = property(get_loss_list, set_readonly)

    def get_test_loss_arr(self):
        ''' getter for `list` of losses in test. '''
        return self.__test_loss_list

    test_loss_list = property(get_test_loss_arr, set_readonly)

    def get_loss_arr(self):
        ''' getter for losses. '''
        return self.__loss_arr

    loss_arr = property(get_loss_arr, set_readonly)

    def get_feature_points_arr(self):
        ''' getter for `mxnet.narray` of feature points in middle hidden layer. '''
        return self.__hidden_activity_arr

    feature_points_arr = property(get_feature_points_arr, set_readonly)

    def get_weights_arr(self):
        ''' getter for `mxnet.ndarray` of weights matrics. '''
        return self.__weights_arr

    def set_weights_arr(self, value):
        ''' setter for `mxnet.ndarray` of weights matrics.'''
        self.__weights_arr = value
    
    weights_arr = property(get_weights_arr, set_weights_arr)

    def get_visible_bias_arr(self):
        ''' getter for `mxnet.ndarray` of biases in visible layer.'''
        return self.__visible_bias_arr
    
    def set_visible_bias_arr(self, value):
        ''' setter for `mxnet.ndarray` of biases in visible layer.'''
        self.__visible_bias_arr = value
    
    visible_bias_arr = property(get_visible_bias_arr, set_visible_bias_arr)

    def get_hidden_bias_arr(self):
        ''' getter for `mxnet.ndarray` of biases in hidden layer.'''
        return self.__hidden_bias_arr
    
    def set_hidden_bias_arr(self, value):
        ''' setter for `mxnet.ndarray` of biases in hidden layer.'''
        self.__hidden_bias_arr = value
    
    hidden_bias_arr = property(get_hidden_bias_arr, set_hidden_bias_arr)

    def get_visible_activity_arr(self):
        ''' getter for `mxnet.ndarray` of activities in visible layer.'''
        return self.__visible_activity_arr

    def set_visible_activity_arr(self, value):
        ''' setter for `mxnet.ndarray` of activities in visible layer.'''
        self.__visible_activity_arr = value

    visible_activity_arr = property(get_visible_activity_arr, set_visible_activity_arr)

    def get_hidden_activity_arr(self):
        ''' getter for `mxnet.ndarray` of activities in hidden layer.'''
        return self.__hidden_activity_arr

    def set_hidden_activity_arr(self, value):
        ''' setter for `mxnet.ndarray` of activities in hidden layer.'''
        self.__hidden_activity_arr = value

    hidden_activity_arr = property(get_hidden_activity_arr, set_hidden_activity_arr)
