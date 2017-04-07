from copy import deepcopy

import numpy as np


class ActionRegressor(object):
    """
    This class is used to approximate the Q-function with a different
    approximator of the provided class for each action. It is often used in MDPs
    with discrete actions and cannot be used in MDPs with continuous actions.
    """
    def __init__(self, model, discrete_actions):
        """
        Constructor.

        # Arguments
            model (object): the model to approximate the Q-function of each
                action.
            discrete_actions (np.array): the values of the discrete actions.
        """
        self._discrete_actions = discrete_actions
        self._action_dim = self._discrete_actions.shape[1]
        self.models = list()

        for i in range(self._discrete_actions.shape[0]):
            self.models.append(deepcopy(model))

    def fit(self, x, y, **fit_params):
        """
        Fit the model.

        # Arguments
            x (np.array): input dataset containing states and actions.
            y (np.array): target.
            fit_params (dict): other parameters.
        """
        for i in range(len(self.models)):
            action = self._discrete_actions[i]
            idxs = np.argwhere(
                (x[:, -self._action_dim:] == action)[:, 0]).ravel()

            if idxs.size:
                self.models[i].fit(x[idxs, :-self._action_dim], y[idxs],
                                   **fit_params)

    def predict(self, x):
        """
        Predict.

        # Arguments
            x (np.array): input dataset containing states and actions.

        # Returns
            The predictions of the model.
        """
        predictions = np.zeros((x.shape[0]))
        for i in range(len(self.models)):
            action = self._discrete_actions[i]
            idxs = np.argwhere(
                (x[:, -self._action_dim:] == action)[:, 0]).ravel()

            if idxs.size:
                predictions[idxs] = self.models[i].predict(
                    x[idxs, :-self._action_dim])

        return predictions

    def __str__(self):
        return str(self.models[0]) + ' with action regression.'