# TearDrop

TearDrop project contains many useful various machine learning algorithms and models. You can
find there anything from Linear regression, KNN, SVMs up to deep learning and LSTMs. 

## Installation
Installing from pypi using `pip`:
```
pip install teardrop
# or you can do this
python3 -m pip install teardrop
```
You can also install it directly from our [repository](https://gitlab.com/dec0ded/teardrop):
```
pip install git+https://gitlab.com/dec0ded/teardrop
```

## Example code
Using TearDrop you can easily create many various neural nets, e.g. Dense neural network.
```python
from teardrop.layers.core import Dense
from teardrop.neural_models import Sequential

net = Sequential(loss='mse', optimizer='sgd')
net.add(Dense(10, activation='relu', input_shape=5))
net.add(Dense(1, activation='sigmoid'))
```
And voila! We've created a basic network which is able to take inputs with shape `(N, 5)`
and returns output with shape `(N, 1)`.

For more examples and better description, check our [documentation](https://dec0ded.gitlab.io/teardrop).