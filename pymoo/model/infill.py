import numpy as np


class InfillCriterion:

    def __init__(self,
                 repair=None,
                 eliminate_duplicates=None,
                 n_max_iterations=100,
                 **kwargs):

        super().__init__()
        self.n_max_iterations = n_max_iterations
        self.eliminate_duplicates = eliminate_duplicates
        self.repair = repair

    def do(self, problem, pop, n_offsprings, **kwargs):

        # the population object to be used
        off = pop.new()

        # infill counter - counts how often the mating needs to be done to fill up n_offsprings
        n_infills = 0

        # iterate until enough offsprings are created
        while len(off) < n_offsprings:

            # how many offsprings are remaining to be created
            n_remaining = n_offsprings - len(off)

            # do the mating
            _off = self._do(problem, pop, n_remaining, **kwargs)

            if self.eliminate_duplicates is not None:
                _off = self.eliminate_duplicates.do(_off, pop, off)

            # if more offsprings than necessary - truncate them randomly
            if len(off) + len(_off) > n_offsprings:
                n_remaining = n_offsprings - len(off)
                I = np.random.permutation(len(_off))[:n_remaining]
                _off = _off[I]

            # add to the offsprings and increase the mating counter
            off = off.merge(_off)
            n_infills += 1

            # if no new offsprings can be generated within a pre-specified number of generations
            if n_infills > self.n_max_iterations:
                break

        return off

    def _do(self, problem, pop, n_offsprings, **kwargs):
        pass
