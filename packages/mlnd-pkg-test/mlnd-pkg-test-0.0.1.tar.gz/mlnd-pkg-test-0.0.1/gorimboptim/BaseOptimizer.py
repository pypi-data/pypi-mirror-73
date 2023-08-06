class Optimizer:
    """Base optimizer class."""
    def __init__(self, cost_function, ftol):
        """
        Initialize base Optimizer class.
        Args:
            cost_function: one dimensional function to optimize.
            ftol: cost function tolerance.
        """
        self.f_evals = 0
        self.cost_function = cost_function
        self.ftol = ftol
        
        
    def evaluate(self, x):
        """Wrapper that calls the cost function and increments Cost Function
        Evaluations (FEvals) counter."""
        result = self.cost_function(x)
        self.f_evals += 1
        return result
        
    
    def optimize(self):
        raise NotImplementedError