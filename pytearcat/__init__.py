from .gr import (def_coords as coords, create_metric as metric, christoffel, riemann, ricci,
                 ricci_scalar as riccis, einstein, geodesic)

from .tensor import (setorder as order, series, new_var as var, new_con as con, new_fun as fun, new_ten as ten,
                    LeviCivita as lcivita, KroneckerDelta as kdelta, D, C ,display, set_space_time as spacetime,
                     simplify, expand, factor, det)
