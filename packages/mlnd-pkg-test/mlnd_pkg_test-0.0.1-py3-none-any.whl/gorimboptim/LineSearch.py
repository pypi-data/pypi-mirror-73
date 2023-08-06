from autograd         import grad
import autograd.numpy as np

#from LineSearch import LineSearch
from .BaseOptimizer import Optimizer

class DichotomousLineSearch(Optimizer):
    """Dichotomous search class for line optimization."""
    def __init__(self, cost_function, interval, ftol=1e-8, max_iterations=1e3):
        """
        Class constructor.
        Args:
            cost_function: One dimensional function to optimize.
            
            interval: Optimization interval defined for the input variable. Must
            be an iterator containing two floats or integers.
            
            ftol: Cost function tolerance. Default value is 10^-8.
            
            max_iterations: Optimizer iteration limit. Default value is 10^3 .
            iterations.
        """
        super().__init__(cost_function, ftol)
        self.max_iterations = max_iterations
        self.epsilon = self.ftol/4
        self.test_interval(interval)
        
        
    def test_interval(self, candidate_interval):
        """
        Tests the interval argument for two conditions:
            - Contains exactly two elements;
            - Both elements are numbers;
        """
        assert hasattr(candidate_interval, '__len__'), "Interval argument must be a\
        container"
        assert len(candidate_interval) == 2, "Interval argument must have \
        exactly two elements"

        try:
            _ = float(candidate_interval[0])
            _ = float(candidate_interval[1])
            self.interval = candidate_interval
        except ValueError as error:
            print("Interval argument must be a container and contain exactly \
            two numbers.")
            exit(ValueError)
            
    
    def get_test_points(self):
        """Calculate test points based on current search interval."""
        self.intervalCenter = np.mean(self.interval)
        self.xA = self.intervalCenter - self.epsilon/2
        self.xB = self.intervalCenter + self.epsilon/2

        self.fA = self.evaluate(self.xA)
        self.fB = self.evaluate(self.xB)
        return self.xA, self.xB

        
    def iteration(self):
        """Run new iteration and return updated search interval."""
        # Compute xA, xB and f(xA), f(xB)
        self.get_test_points()

        if self.fA <= self.fB:
            self.interval = [self.interval[0], self.xB]
        elif self.fA > self.fB:
            self.interval = [self.xA, self.interval[1]]

        return self.interval


    def stop_condition(self):
        """Checks the optimization stopping condition."""
        condition1 = np.abs(self.interval[0] - self.interval[1]) > self.ftol
        condition2 = self.iteration_counter < self.max_iterations
        return condition1 and condition2


    def optimize(self):
        """Iterate the optimization algorithm until stopping conditions - and, 
        hopefully, the optimum - are reached."""
        self.iteration_counter = 0
        self.f_evals = 0
        while self.stop_condition():
            self.iteration()
            self.iteration_counter += 1

        self.x_optimum = self.interval[0]
        return self.x_optimum
