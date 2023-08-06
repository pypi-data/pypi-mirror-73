import numpy as np
from scipy.sparse import lil_matrix, hstack, eye, vstack
from cobamp.core.linear_systems import GenericLinearSystem, VAR_CONTINUOUS, SteadyStateLinearSystem
from cobamp.core.optimization import LinearSystemOptimizer
from troppo.methods.base import ContextSpecificModelReconstructionAlgorithm, PropertiesReconstruction


# TODO make a generic LPProblem, then update with the necessary information for the LP7 and LP9 - this should improve
#  the performance of the algorithm

# TODO reformulate LP7/9 into a uniform structure and change bounds/objective functions

class FastcoreProperties(PropertiesReconstruction):

    def __init__(self, core, flux_threshold=1e-4, solver=None):
        new_mandatory = {'core': lambda x: isinstance(x, list) and len(x) > 0,
                         'core_idx': lambda x: isinstance(x, list) and len(x) > 0,
                         'solver': lambda x: isinstance(x, str)}
        new_optional = {}
        super().__init__()
        # self.base_mandatory['method'] = MethodsReconstruction.FASTCORE
        self.add_new_properties(new_mandatory, new_optional)
        self['flux_threshold'] = flux_threshold
        self['core'] = list(core)
        # TODO change this later, this is only for testing
        self['core_idx'] = list(core)
        self['solver'] = solver

    @staticmethod
    def from_integrated_scores(scores, **kwargs):
        # TODO change later, idk why core_idx is here
        return FastcoreProperties(core=scores,
                                  **dict({k: v for k, v in kwargs.items() if k not in ['core', 'core_idx']}))


class FASTcore(ContextSpecificModelReconstructionAlgorithm):
    properties_class = FastcoreProperties

    def __init__(self, S, lb, ub, properties):
        super().__init__(S, lb, ub, properties)
        self.S = np.array(S)
        self.model_lb, self.model_ub = np.array(lb), np.array(ub)
        self.lb, self.ub = np.array(lb), np.array(ub)
        self.properties = properties
        self.n_metabolites, self.n_reactions = self.S.shape
        self.metabolites, self.reactions = np.array([i for i in range(self.n_metabolites)]), np.array(
            [i for i in range(self.n_reactions)])
        self.counter = 0
        self.LPproblem, self.lsoLP3, self.lsoLP7, self.lsoLP9 = None, None, None, None

    def reverse_irreversible_reactions_in_reverse_direction(self, irrev_reverse_idx):
        '''
        Identifies the irreversible reactions in the reverse direction and returns the S matrix with the signals for the
        metabolites reversed, a vector with the upper bounds as reversed form the lower bounds and a vector with the lower
        bounds as the reverse of the upper ones.
        Returns: S, ub, lb after modifications

        '''
        if irrev_reverse_idx.size > 0:  # if they exist
            self.S[:, irrev_reverse_idx] = -self.S[:, irrev_reverse_idx]
            temp = self.ub[irrev_reverse_idx]
            self.ub[irrev_reverse_idx] = -self.lb[irrev_reverse_idx]
            self.lb[irrev_reverse_idx] = -temp
        return

    def generate_LP3_problem(self):
        self.LP3problem = SteadyStateLinearSystem(self.S, self.lb, self.ub,
                                                  ['V' + str(i) for i in range(self.S.shape[1])],
                                                  solver=self.properties['solver'])
        self.lsoLP3 = LinearSystemOptimizer(self.LP3problem)

    def LP3(self, J, basis=None):
        # objective function
        f = np.zeros(self.n_reactions)
        f[J] = -1

        self.LP3problem.set_objective(f, minimize=True)
        self.LP3problem.model.configuration.presolve = False
        solution = self.lsoLP3.optimize()

        return {i: k[1] for i, k in enumerate(solution.var_values().items()) if i <= self.n_reactions - 1}

    def LP7(self, J, basis=None):
        # TODO implement basis (from CPLEX) to improve the speed of the algorithm
        print('LP7')
        nJ = J.size  # number of irreversible reactions
        # m,n and m2,n2 are the same since the matrix S does not change throughout the algorithm, so we'll be using
        # self.n_metabolites and self.n_reactions

        # objective function
        f = -np.concatenate([np.zeros((self.n_reactions)), np.ones((nJ))])

        # equalities
        Aeq = hstack([self.S, lil_matrix((self.n_metabolites, nJ))])
        beq = np.zeros(self.n_metabolites)

        # inequalities
        Ij = lil_matrix((nJ, self.n_reactions))
        # nJ x n_reactions
        Ij[tuple([list(range(nJ)), J])] = -1  # Ij(sub2ind(size(Ij),(1:nj)',J(:))) = -1; from the original code
        Aineq = hstack([Ij, eye(nJ)])
        bineq = np.zeros((nJ,))

        # bounds
        lb = np.concatenate([self.lb, -np.inf * np.ones((nJ,))])
        ub = np.concatenate([self.ub, np.ones((nJ,)) * self.properties['flux_threshold']])

        A = vstack([Aeq, Aineq])
        b_lb, b_ub = np.concatenate([beq, [None] * nJ]), np.concatenate([beq, bineq])
        # b_lb, b_ub = np.concatenate([beq, -np.inf * np.ones((nJ, ))]), np.concatenate([beq, bineq])

        problem = GenericLinearSystem(A.toarray(), VAR_CONTINUOUS, lb, ub, b_lb, b_ub,
                                      ['V' + str(i) for i in range(A.shape[1])], solver=self.properties['solver'])

        lso = LinearSystemOptimizer(problem)
        problem.set_objective(f, True)
        problem.model.configuration.presolve = False
        # problem.model.configuration.lpmethod = 'dual'
        solution = lso.optimize()
        solution.x().sum()

        print(solution.objective_value())

        if solution.status() != 'optimal':
            print('Warning, Solution is not optimal')

        if solution:
            return {i: k[1] for i, k in enumerate(solution.var_values().items()) if i <= self.n_reactions - 1}
        else:
            return [np.nan] * self.n_reactions

    def LP9(self, K, P):
        print('LP9')
        scalingFactor = 1e5

        V = []
        if K.size == 0 or P.size == 0:
            return np.array([])

        nP = P.size
        nK = K.size

        # objective
        f = np.concatenate([np.zeros((self.n_reactions)), np.ones((nP))])

        # equalities
        Aeq = hstack([self.S, lil_matrix((self.n_metabolites, nP))])
        beq = np.zeros(self.n_metabolites)
        # inequalities
        Ip = lil_matrix((nP, self.n_reactions))
        Ip[tuple([list(range(nP)), P])] = 1
        Ik = lil_matrix((nK, self.n_reactions))
        Ik[tuple([list(range(nK)), K])] = 1

        Aineq = vstack([hstack([Ip, -eye(nP)]), hstack([-Ip, -eye(nP)]), hstack([-Ik, lil_matrix((nK, nP))])])
        bineq = np.concatenate(
            [np.zeros((2 * nP,)), -np.ones((nK,)) * self.properties['flux_threshold'] * scalingFactor])
        # bounds
        lb = np.concatenate([self.lb, np.zeros((nP,))]) * scalingFactor
        ub = np.concatenate([self.ub, np.array(
            list(map(max, zip(np.abs(self.model_lb[P]), np.abs(self.model_ub[P])))))]) * scalingFactor

        A = vstack([Aeq, Aineq])
        b_lb, b_ub = np.concatenate([beq, [None] * (2 * nP + nK)]), np.concatenate([beq, bineq])

        problem = GenericLinearSystem(A.toarray(), VAR_CONTINUOUS, lb, ub, b_lb, b_ub,
                                      ['V' + str(i) for i in range(A.shape[1])], solver=self.properties['solver'])

        lso = LinearSystemOptimizer(problem)
        problem.set_objective(f, True)
        solution = lso.optimize()
        print(solution.objective_value())

        if solution.status() != 'optimal':
            print('Warning, Solution is not optimal')

        if solution:
            return {i: k[1] for i, k in enumerate(solution.var_values().items()) if i <= self.n_reactions - 1}
        else:
            return [np.nan] * self.n_reactions

    def findSparseMode(self, J, P, singleton, basis=None):
        if J.size == 0:
            return np.array([], dtype=int)

        supp = []

        if basis is None:
            basis = []
        print('before LP7')
        if singleton:
            V = self.LP7(J[0], basis)
        else:
            # V, basis = self.LP7(J, basis)
            V = self.LP7(J, basis)

        K = np.array([rJ for rJ in J if V[rJ] >= 0.99 * self.properties['flux_threshold']])

        print('done LP7')
        if K.size > 0:
            V = self.LP9(K, P)
            Supp = np.array([i for i, k in V.items() if
                             (np.abs(k) >= 0.99 * self.properties['flux_threshold']) and i <= self.n_reactions - 1])
            print('done LP9')
            return Supp
        else:
            return np.array([])

    def preprocessing(self):
        irreversible_reactions_idx_to_change = np.where(self.model_ub <= 0)[0]
        self.reverse_irreversible_reactions_in_reverse_direction(irreversible_reactions_idx_to_change)
        irreversible_reactions_idx = np.where(self.model_lb >= 0)[0]

        singleton = False

        J = np.intersect1d(self.properties['core_idx'], irreversible_reactions_idx)  # irreversible reactions in core

        print('J size' + str(len(J)))
        print(J)

        P = np.setdiff1d(self.reactions, self.properties['core_idx'])  # non-core reactions

        supp = self.findSparseMode(J, P, singleton)

        if np.setdiff1d(J, supp).size > 0:
            raise Exception('Inconsistent irreversible core reactions \n\tImpossible to build model')

        return np.setdiff1d(self.properties['core_idx'], supp), supp, P, irreversible_reactions_idx

    def fastcore(self):
        flipped = False
        singleton = False
        J, A, P, irreversible_reactions_idx = self.preprocessing()
        print(J.size, A.size)
        while J.size > 0:
            P = np.setdiff1d(P, A)

            supp = self.findSparseMode(J, P, singleton)

            # print(A, supp)

            A = np.union1d(A, supp).astype(int)
            print(J.size, A.size)

            if np.intersect1d(J, A) != np.array([]):
                J = np.setdiff1d(J, A)
                flipped = False
            else:
                if singleton:
                    JiRev = np.setdiff1d(J[0], irreversible_reactions_idx)
                else:
                    JiRev = np.setdiff1d(J, irreversible_reactions_idx)
                if flipped or JiRev == np.array([]):
                    if singleton:
                        print('Error: Global network is not consistent')
                        print(J)
                        return sorted(np.union1d(A, J))
                    else:
                        flipped = False
                        singleton = True
                else:
                    self.reverse_irreversible_reactions_in_reverse_direction(JiRev)
                    flipped = True
                    print('Flipped')

        print(J.size, A.size)
        return sorted(A)

    def run(self):
        return self.fastcore()
