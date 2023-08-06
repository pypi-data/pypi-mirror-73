import os
from pm4pycvxopt import util

from pm4pycvxopt.util.lp.versions import cvxopt_solver, cvxopt_solver_custom_align, cvxopt_solver_custom_align_ilp, cvxopt_solver_custom_align_arm

from pm4py.util.lp import factory


custom_solver = cvxopt_solver_custom_align
try:
    # for ARM-based Linux, we need to use a different call to GLPK
    if "arm" in str(os.uname()[-1]):
        custom_solver = cvxopt_solver
except:
    pass

factory.CVXOPT = "cvxopt"
factory.CVXOPT_SOLVER_CUSTOM_ALIGN = "cvxopt_solver_custom_align"
factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP = "cvxopt_solver_custom_align_ilp"

factory.VERSIONS_APPLY[factory.CVXOPT] = cvxopt_solver.apply
factory.VERSIONS_GET_PRIM_OBJ[factory.CVXOPT] = cvxopt_solver.get_prim_obj_from_sol
factory.VERSIONS_GET_POINTS_FROM_SOL[factory.CVXOPT] = cvxopt_solver.get_points_from_sol

factory.VERSIONS_APPLY[factory.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.apply
factory.VERSIONS_GET_PRIM_OBJ[factory.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.get_prim_obj_from_sol
factory.VERSIONS_GET_POINTS_FROM_SOL[
    factory.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.get_points_from_sol

factory.VERSIONS_APPLY[factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.apply
factory.VERSIONS_GET_PRIM_OBJ[factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.get_prim_obj_from_sol
factory.VERSIONS_GET_POINTS_FROM_SOL[
    factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.get_points_from_sol
factory.DEFAULT_LP_SOLVER_VARIANT = factory.CVXOPT_SOLVER_CUSTOM_ALIGN

try:
    from pm4py.util.lp import solver as factory

    factory.CVXOPT = "cvxopt"
    factory.CVXOPT_SOLVER_CUSTOM_ALIGN = "cvxopt_solver_custom_align"
    factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP = "cvxopt_solver_custom_align_ilp"

    factory.VERSIONS_APPLY[factory.CVXOPT] = cvxopt_solver.apply
    factory.VERSIONS_GET_PRIM_OBJ[factory.CVXOPT] = cvxopt_solver.get_prim_obj_from_sol
    factory.VERSIONS_GET_POINTS_FROM_SOL[factory.CVXOPT] = cvxopt_solver.get_points_from_sol

    factory.VERSIONS_APPLY[factory.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.apply
    factory.VERSIONS_GET_PRIM_OBJ[factory.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.get_prim_obj_from_sol
    factory.VERSIONS_GET_POINTS_FROM_SOL[
        factory.CVXOPT_SOLVER_CUSTOM_ALIGN] = custom_solver.get_points_from_sol

    factory.VERSIONS_APPLY[factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.apply
    factory.VERSIONS_GET_PRIM_OBJ[factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.get_prim_obj_from_sol
    factory.VERSIONS_GET_POINTS_FROM_SOL[
        factory.CVXOPT_SOLVER_CUSTOM_ALIGN_ILP] = cvxopt_solver_custom_align_ilp.get_points_from_sol
    factory.DEFAULT_LP_SOLVER_VARIANT = factory.CVXOPT_SOLVER_CUSTOM_ALIGN
except:
    pass

from pm4py.algo.conformance.alignments.versions import state_equation_a_star

state_equation_a_star.DEFAULT_LP_SOLVER_VARIANT = factory.CVXOPT_SOLVER_CUSTOM_ALIGN

from pm4py.objects.stochastic_petri import lp_perf_bounds

lp_perf_bounds.DEFAULT_LP_SOLVER_VARIANT = factory.CVXOPT

from pm4py.algo.conformance.alignments import factory as align_factory

align_factory.DEFAULT_VARIANT = align_factory.VERSION_STATE_EQUATION_A_STAR


__version__ = '0.0.9'
__doc__ = "Process Mining for Python - CVXOpt Support"
__author__ = 'PADS'
__author_email__ = 'pm4py@pads.rwth-aachen.de'
__maintainer__ = 'PADS'
__maintainer_email__ = "pm4py@pads.rwth-aachen.de"
