#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import copy


class KernelExpr(ABC):
    r"""Base class for any kernel expressions."""
    @abstractmethod
    def __call__(self, X, Y=None, eval_gradient=False, **options):
        """Evaluates the pairwise kernel matrix (i.e. the Gramian matrix)
        between feature vectors in X and Y.

        Parameters
        ----------
        X: list or ndarray
            Collection of feature objects/vectors.
        Y: list or ndarray
            Another collection of feature objects/vectors.
        eval_gradient: Boolean
            If True, computes the gradient of the kernel matrix with respect
            to hyperparameters and return it alongside the kernel matrix.
        options: keyword arguments
            Additional kernel-specific arguments.

        Returns
        -------
        Returns
        -------
        kernel_matrix: ndarray
            if Y is None, return a square matrix containing pairwise
            kernel evaluations between the feature objects in X; otherwise,
            returns a matrix containing kernel evaluations across graphs in X
            and Y.
        gradient: ndarray
            The gradient of the kernel matrix with respect to kernel
            hyperparameters. Only returned if eval_gradient is True.
        """
        pass

    @abstractmethod
    def diag(self, X, **options):
        """Evaluates only the diagonal of the pairwise kernel matrix.

        Parameters
        ----------
        X: list or ndarray
            List of feature objects/vectors
        eval_gradient: Boolean
            If True, computes the gradient of the kernel matrix with respect
            to hyperparameters and return it alongside the kernel matrix.

        Returns
        -------
        diagonal: numpy.array or list of np.array(s)
            Returns a vector containing the kernel evaluation between each
            feature objects in X with itself.
        gradient: ndarray
            The gradient of the kernel matrix diagonal with respect to kernel
            hyperparameters. Only returned if eval_gradient is True.
        """
        pass

    @property
    @abstractmethod
    def theta(self):
        pass

    @theta.setter
    @abstractmethod
    def theta(self, value):
        pass

    @property
    @abstractmethod
    def bounds(self):
        pass

    # @property
    # def hyperparameters(self):
    #     return self.graph_kernel.hyperparameters

    # @property
    # def hyperparameter_bounds(self):
    #     return self.graph_kernel.hyperparameter_bounds

    def clone_with_theta(self, theta):
        clone = copy.deepcopy(self)
        clone.theta = theta
        return clone

    def __add__(self, other):
        pass


class BinaryKernelExpr(KernelExpr):
    r"""Base class for any kernel expressions."""
    @property
    @abstractmethod
    def leaf(self):
        


    @abstractmethod
    def __call__(self, X, Y=None, eval_gradient=False, **options):
        """Evaluates the pairwise kernel matrix (i.e. the Gramian matrix)
        between feature vectors in X and Y.

        Parameters
        ----------
        X: list or ndarray
            Collection of feature objects/vectors.
        Y: list or ndarray
            Another collection of feature objects/vectors.
        eval_gradient: Boolean
            If True, computes the gradient of the kernel matrix with respect
            to hyperparameters and return it alongside the kernel matrix.
        options: keyword arguments
            Additional kernel-specific arguments.

        Returns
        -------
        Returns
        -------
        kernel_matrix: ndarray
            if Y is None, return a square matrix containing pairwise
            kernel evaluations between the feature objects in X; otherwise,
            returns a matrix containing kernel evaluations across graphs in X
            and Y.
        gradient: ndarray
            The gradient of the kernel matrix with respect to kernel
            hyperparameters. Only returned if eval_gradient is True.
        """
        pass

    @abstractmethod
    def diag(self, X, **options):
        """Evaluates only the diagonal of the pairwise kernel matrix.

        Parameters
        ----------
        X: list or ndarray
            List of feature objects/vectors
        eval_gradient: Boolean
            If True, computes the gradient of the kernel matrix with respect
            to hyperparameters and return it alongside the kernel matrix.

        Returns
        -------
        diagonal: numpy.array or list of np.array(s)
            Returns a vector containing the kernel evaluation between each
            feature objects in X with itself.
        gradient: ndarray
            The gradient of the kernel matrix diagonal with respect to kernel
            hyperparameters. Only returned if eval_gradient is True.
        """
        pass

    @property
    @abstractmethod
    def theta(self):
        pass

    @theta.setter
    @abstractmethod
    def theta(self, value):
        pass

    @property
    @abstractmethod
    def bounds(self):
        pass

    # @property
    # def hyperparameters(self):
    #     return self.graph_kernel.hyperparameters

    # @property
    # def hyperparameter_bounds(self):
    #     return self.graph_kernel.hyperparameter_bounds

    def clone_with_theta(self, theta):
        clone = copy.deepcopy(self)
        clone.theta = theta
        return clone

    def __add__(self, other):
        pass
