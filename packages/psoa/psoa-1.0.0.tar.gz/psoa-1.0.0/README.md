# psoa

An implementation of the Particle Swarm Optimization algorithm

## Methodology  
To be added

## Installation:  
```
pip install psoa
```  
or

```
conda install -c wangxiangwen psoa
```

## Example Usage:  
```python
>>> import psoa
>>> s = psoa.swarm()
>>> obj = lambda x: -((x[0] - 10) ** 2 + (x[1] - 25) ** 2)
>>> s.maximize(obj, dim=2)
([10.0, 25.0], -0.0)
>>> obj2 = lambda x: np.sum([xi ** 2 - 10 * np.cos(2 * np.pi * xi)
>>>                          for xi in x]) + 10 * len(x)
>>> s.minimize(obj2, dim=5, max_iteration=1e5,
>>>            boundaries=((-5.12, -5.12, -5.12, -5.12, -5.12),
>>>                        (5.12, 5.12, 5.12, 5.12, 5.12)))
([-2.0902191353445784e-09,
  -6.659027711151939e-10,
  -4.9074379144973505e-09,
  1.1250520464439336e-09,
  -3.42855219094123e-10],
 0.0)
```
