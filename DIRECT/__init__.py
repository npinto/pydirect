# -*- coding: utf-8 -*-
"""
DIRECT - A python wrapper to the DIRECT algorithm.
==================================================

DIRECT is a method to solve global bound constraint optimization problems and
was originally developed by D. R. Jones, C. D. Perttunen and B. E. Stuckmann.
It is designed to find **global** solutions of mathematical optimization problems of the from

.. math::

       \min_ {x \in R^n} f(x)

subject to

.. math::

       x_L \leq  x  \leq x_U

Where :math:`x` are the optimization variables (with upper an lower
bounds), :math:`f(x)` is the objective function.

The DIRECT package uses the fortan implementation of DIRECT written by
Joerg.M.Gablonsky, DIRECT Version 2.0.4.

.. codeauthor:: Amit Aides <amitibo@tx.technion.ac.il>
"""

# Author: Amit Aides <amitibo@tx.technion.ac.il>
#
# License: EPL.


import numpy as np
from .direct import direct

__version_info__ = ('1', '0')
__version__ = '.'.join(__version_info__)

ERROR_MESSAGES = (
    'Maximum number of levels has been reached.',
    'An error occured while the function was sampled',
    'There was an error in the creation of the sample points',
    'Initialization failed',
    'maxf is too large'
    'u[i] < l[i] for some i'
)

SUCCESS_MESSAGES = (
    'Number of function evaluations done is larger then maxf',
    'Number of iterations is equal to maxT',
    'The best function value found is within fglper of the (known) global optimum',
    'The volume of the hyperrectangle with best function value found is below volper',
    'The volume of the hyperrectangle with best function value found is smaller then volper'
)

def solve(
    objective,
    l,
    u,
    eps=1e-4,
    maxf=20000,
    maxT=6000,
    algmethod=0,
    fglobal=-1e100,
    fglper=0.01,
    volper=-1.0,
    sigmaper=-1.0,
    logfilename='DIRresults.txt',
    user_data=None
    ):
    """
    Solve an optimization problem using the DIRECT (Dividing Rectangles) algorithm.
    It can be used to solve general nonlinear programming problems of the form:

    .. math::

           \min_ {x \in R^n} f(x)

    subject to

    .. math::

           x_L \leq  x  \leq x_U
    
    Where :math:`x` are the optimization variables (with upper an lower
    bounds), :math:`f(x)` is the objective function.

    Parameters
    ----------
    objective : function pointer
        Callback function for evaluating objective function.
        The callback functions accepts two parameters: x (value of the
        optimization variables at which the objective is to be evaluated) and
        user_data, an arbitrary data object supplied by the user.
        The function should return a tuple of two values: the objective function
        value at the point x and a value (flag) that is set to 1 if the function
        is not defined at point x (0 if it is defined).
    
    l : array-like, shape = [n]
        Lower bounds on variables, where n is the dimension of x.
        
    u : array-like, shape = [n]
        Upper bounds on variables, where n is the dimension of x.
        
    eps : float
        Ensures sufficient decrease in function value when a new potentially
        optimal interval is chosen (default 1e-4).

    maxf : integer
        Approximate upper bound on objective function evaluations (default 20000).
        NOTE:
        Maximal allowed value is 90000 see documentation of fotran library.
    
    maxT : integer
        Maximum number of iterations (default 6000).
        NOTE:
        Maximal allowed value is 6000 see documentation of fotran library.
        
    algmethod : integer
        0 - Use the original DIRECT algorithm
        1 - Use the modified DIRECT-l algorithm
    
    fglobal : float
        Function value of the global optimum. If this value is not known set this
        to a very large negative value (default -1e100).
        
    fglper : float
        Terminate the optimization when the percent error satisfies:
        
        .. math::

            100*(f_{min} - f_{global})/\max(1, |f_{global}|) \leq f_{glper}
        
        (default 0.01)
        
    volper : float
        Terminate the optimization once the volume of a hyperrectangle is less
        than volper percent of the original hyperrectangel (default -1.0).
        
    sigmaper : float
        Terminate the optimization once the measure of the hyperrectangle is less
        than sigmaper (default -1.0)
        
    logfilename : string
        Name of logfile (default 'DIRresults.txt').
        
    user_data : object
        Arbitrary python object used for passing data to the objective function
        (default None).
    
    Returns
    -------
    x : array, shape = [n]
        Final point obtained in the optimization.
    
    fmin : float
        The value of the function at x.
    
    ierror : string
        Status message.

    """
    
    def _objective_wrap(x, iidata, ddata, cdata, n, iisize, idsize, icsize):
        """
        To simplify the python objective we use a wrapper objective that complies
        with the required fortran objective.
        """
        return objective(x, user_data)
        
    #
    # Dummy values so that the python wrapper will comply with the required
    # signature of the fortran library.
    #
    iidata = np.ones(0, dtype=np.int32)
    ddata = np.ones(0, dtype=np.float64)
    cdata = np.ones([0,40], dtype=np.uint8)

    #
    # Call the DIRECT algorithm
    #
    x, fmin, ierror = direct(
                        _objective_wrap,
                        eps,
                        maxf,
                        maxT,
                        np.array(l, dtype=np.float64),
                        np.array(u, dtype=np.float64),
                        algmethod,
                        logfilename, 
                        fglobal,
                        fglper,
                        volper,
                        sigmaper,
                        iidata,
                        ddata,
                        cdata
                        )

    if ierror < 0:
        raise Exception(ERROR_MESSAGES[abs(ierror)-1])
        
    return x, fmin, SUCCESS_MESSAGES[ierror-1]
