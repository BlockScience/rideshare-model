This wiring should encapsulate all the state updates that might happen from a new ride. This set of mechanisms is not defined yet as there are some design choices.

This wiring would be a parallel block as everything should be updated simultaneously.

Possible mechanisms that could be in this wiring would include:

1. A mechanism that changes some state variable on the driver to "going to pickup location" or something
2. A mechanism that might remove money from the user account (although that might be better after a completed ride)
3. A mechanism that, if an event queue is used, adds the event of the pickup to the queue
	1. As in an object that has (time_to_pickup, user_id, driver_id)
4. Any mechanisms for updates to the [[rider]] state