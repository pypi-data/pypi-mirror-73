.. _proobzoo:


Probabilistic Model Zoo
===========================

In this section, we present the code for implementing some models in InferPy.


Bayesian Linear Regression
-----------------------------------

Graphically, a (Bayesian) linear regression can be defined as follows,

.. figure:: ../_static/img/linear_regression.png
   :alt: Bayesian Linear Regression
   :scale: 60 %
   :align: center

   Bayesian Linear Regression

The InferPy code for this model is shown below,


.. literalinclude:: ../../examples/probzoo/linear_regression.py
   :language: python3

--------------


Bayesian Logistic Regression
------------------------------------

Graphically, a (Bayesian) logistic regression can be defined as follows,

.. figure:: ../_static/img/logistic_regression.png
   :alt: Bayesian Logistic Regression
   :scale: 60 %
   :align: center

   Bayesian Linear Regression

The InferPy code for this model is shown below,



.. literalinclude:: ../../examples/probzoo/log_regression.py
   :language: python3
   :lines: 2-69


--------------


Linear Factor Model (PCA)
-------------------------


A linear factor model allows to perform principal component analysis (PCA). Graphically,
it can be defined as follows,


.. figure:: ../_static/img/pca.png
   :alt: Linear Factor Model (PCA)
   :scale: 100 %
   :align: center

   Linear Factor Model (PCA)

The InferPy code for this model is shown below,

.. literalinclude:: ../../examples/probzoo/pca.py
   :language: python3
   :lines: 8-57


--------------

Non-linear Factor Model (NLPCA)
--------------------------------------


Similarly to the previous model, the Non-linear PCA can be graphically defined as follows,

.. figure:: ../_static/img/nlpca.png
   :alt: Non-linear PCA
   :scale: 100 %
   :align: center

   Non-linear PCA

Its code in InferPy is shown below,

.. literalinclude:: ../../examples/probzoo/nlpca.py
   :language: python3
   :lines: 9-71




--------------

Variational auto-encoder (VAE)
--------------------------------------


Similarly to the PCA and NLPCA models, a variational auto-encoder allows to perform dimensionality
reduction. However a VAE will contain a neural network in the P model (decoder) and another
one in the Q (encoder). Its code in InferPy is shown below,

.. literalinclude:: ../../examples/probzoo/vae.py
   :language: python3
   :lines: 8-67



Note that in this example objects of class ``tf.layers`` are used, but
keras or tfp layers are compatible as well.




