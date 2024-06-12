from copy import deepcopy


def ride_pricing_option1(state, params, spaces):
    space1 = deepcopy(spaces[0])
    idle_drivers = [x for x in state["Drivers"] if x["State"] == "Idle"]

    if len(idle_drivers) < 0:
        return None
    assert False, "Implement"
    return [space1]
