# mlnd-pkg
Small distribution building and PyPi packaging experiment

## Usage
gorimboptim module implements DichotomousLineSearch class, which is a line search
optimizer.

`from gorimboptim import DichotomousLineSearch`

Constructor arguments include cost function, optimization interval, f(x) tolerance,
and iteration limit.

Method `optimize()` returns optimum point x for a given cost function and 
interval.