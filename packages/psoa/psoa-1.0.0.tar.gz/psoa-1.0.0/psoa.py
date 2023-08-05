'''
An implementation of the Particle Swarm Optimization algorithm

Returns:
--------------------
parameters -- list of float
              a list of estimated parameters that optimize the objective function
best_objective_result -- float,
                         best result measured with the objective function

Examples:
--------------------
>>> s = swarm()
>>> obj1 = lambda x: -((x[0] - 10) ** 2 + (x[1] - 25) ** 2)
>>> s.maximize(obj1)
([10.0, 25.0], -0.0)
>>> # Rastrigin function
>>> obj2 = lambda x: 10 * len(x) + np.sum([xi ** 2 - 10 * np.cos(2 * np.pi * xi) for xi in x])
>>> s.minimize(obj2, dim=5, max_iteration=1e5, boundaries=((-5.12, -5.12, -5.12, -5.12, -5.12),
>>>                                                        (5.12, 5.12, 5.12, 5.12, 5.12)))
([-2.0902191353445784e-09,
  -6.659027711151939e-10,
  -4.9074379144973505e-09,
  1.1250520464439336e-09,
  -3.42855219094123e-10],
 0.0)

References:
--------------------
[1] "James McCaffrey: Swarm Intelligence Optimization using Python",
    Video from PyData Seattle 2015,
    available at https://www.youtube.com/watch?v=bVDX_UwthZI&t=1038s,
    accessed on 2020-07-04
'''


import numpy as np


class swarm(object):

    default_population = 100
    default_inertia_weight = 0.729
    default_cognitive_weight = 1.49445
    default_social_weight = 1.49445
    default_dim = 2
    default_max_iteration = 1e4

    def __init__(self, population=default_population,
                 inertia_weight=default_inertia_weight,
                 social_weight=default_social_weight,
                 cognitive_weight=default_cognitive_weight):
        self.population = population
        self.inertia_weight = inertia_weight
        self.cognitive_weight = cognitive_weight
        self.social_weight = social_weight

    def maximize(self, *args, **kwargs):
        self.extreme, self.arg_extreme = np.max, np.argmax
        self.better = np.greater
        return self.optimize(*args, **kwargs)

    def minimize(self, *args, **kwargs):
        self.extreme, self.arg_extreme = np.min, np.argmin
        self.better = np.less
        return self.optimize(*args, **kwargs)

    def optimize(self, objective_function, dim=default_dim,
                 initial_values=None, boundaries=None,
                 max_iteration=default_max_iteration):
        self.dim = dim
        self.obj = objective_function
        self.max_iteration = int(max_iteration)
        if boundaries is None:
            self.boundaries = None
            self.param_mins, self.param_maxs = None, None
        else:
            self.boundaries = np.array(boundaries)
            self.param_mins, self.param_maxs = self.boundaries
        self.boundaries = None if boundaries is None else np.array(boundaries)
        self.initialize_position_velocity(initial_values)
        for i in range(self.max_iteration):
            self.update()
        self.swarm_best_obj = self.obj(self.swarm_best_pos)
        return self.swarm_best_pos.tolist(), self.swarm_best_obj

    def update(self):
        self.s_c_rnds = np.random.random(size=(2 * self.population, self.dim))
        self.velocities = (self.inertia_weight * self.velocities +
                           self.s_c_rnds[:self.population] * self.cognitive_weight *
                           (self.particle_best_pos - self.positions) +
                           self.s_c_rnds[self.population:] * self.social_weight *
                           (self.swarm_best_pos - self.positions))
        self.positions = self.positions + self.velocities
        if self.boundaries is not None:
            self.positions_clipped = self.positions.clip(self.param_mins, self.param_maxs)
            self.velocities *= 1 - (self.positions != self.positions_clipped) * 2
            self.positions = self.positions_clipped
        self.curr_objs = np.apply_along_axis(self.obj, 1, self.positions)
        self.particle_best_pos = (self.positions * self.better(self.curr_objs, self.best_objs
                                                               ).reshape(-1, 1) +
                                  self.particle_best_pos * (~self.better(self.curr_objs, self.best_objs)
                                                            ).reshape(-1, 1))
        self.best_objs = self.extreme([self.best_objs, self.curr_objs], axis=0)
        self.swarm_best_pos = self.particle_best_pos[self.arg_extreme(self.best_objs)]

    def initialize_position_velocity(self, initial_values):
        if self.boundaries is not None:
            self.positions = np.random.uniform(self.param_mins, self.param_maxs,
                                               size=(self.population, self.dim))
        else:
            self.positions = np.random.random(size=(self.population, self.dim))
        if initial_values is not None:
            self.positions[0] = np.array(initial_values)
        self.velocities = np.random.random(size=(self.population, self.dim))
        self.particle_best_pos = self.positions
        self.best_objs = np.apply_along_axis(self.obj, 1, self.positions)
        self.swarm_best_pos = self.particle_best_pos[self.arg_extreme(self.best_objs)]
