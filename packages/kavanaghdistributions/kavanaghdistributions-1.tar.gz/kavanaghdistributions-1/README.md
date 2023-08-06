# kavanaghdistributions

kavanaghdistributions is a python package for generating samples from Normal, Poisson and Binomial Distributions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install kavanaghdistributions.

```bash
pip install kavanaghdistributions
```

## Usage

```python
from kavanaghdistributions.functions import random_draw
from kavanaghdistributions.classes import NormalDistribution, PoissonDistribution, BinomialDistribution

#random_draw function 

random_draw(sample_shape=5, distribution='normal', mean=1, sd=2)
# generates: array([1.82261281, 0.81926903, 3.06892213, 1.62636623, 2.05127246])

random_draw(sample_shape=5, distribution='poisson', lam=10)
# generates: array([12,  8,  7, 14,  8])

random_draw(sample_shape=(2,2), distribution='binomial', num=2, prob=0.3)
#generates: array([[0, 0],
#                  [1, 0]])


#NormalDistribution

nd = NormalDistribution(mean=3, sd=1, sample_shape=5)
nd.draw()
#generates array([3.59149631, 3.13146966, 3.98872244, 3.59125381, 4.36412151])
nd.summarise()
#generates:
#Min: 3.1314696620512454
#Max: 4.3641215077437945
#Mean: 3.733412745193425
#Standard Deviation: 0.41609169604466906

#PoissonDistribution

pd = PoissonDistribution(lam=(2,3,2), sample_shape=[2,2,3])
pd.draw()
#generates:
#array([[[0, 0, 2],
#        [2, 1, 1]],
#
#       [[3, 3, 1],
#       [2, 1, 3]]])
pd.summarise()
#generates:
#Min: 0
#Max: 3
#Mean: 1.5833333333333333
#Standard Deviation: 1.0374916331657276

#BinomialDistribution

bd = BinomialDistribution(num=4, prob=0.5, sample_shape=6)
bd.draw()
#generates: array([2, 3, 2, 1, 1, 1])
bd.summarise()
#generates: 
#Min: 1
#Max: 3
#Mean: 1.6666666666666667
#Standard Deviation: 0.74535599249993

```



## License
[MIT](https://choosealicense.com/licenses/mit/)