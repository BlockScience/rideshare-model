def event_queue_request_ride(state, params, spaces):

    # Only trigger if the event queue action is request ride
    if state["Event Queue"][0].action != "Request Ride":
        return

    t = state["Event Queue"][0].t
    spaces = state["Event Queue"][0].spaces

    print(t, spaces)

    assert False
