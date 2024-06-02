## Summary

The following research note proposes using an [[Global State-Event Queue|event queue]] for taking care of:

1. The [[Request Ride Wiring|requests for rides]] that are coming up
2. The timing of any [[Complete Ride Wiring|rides be complete]]
3. Potentially some control actions related to the probing of the latest rides or things happening for demand prediction or similar.

## Event Queue Structure

- The [[Global State-Event Queue|event queue]] will be a list of elements with the type of [[Event Queue Element Type]]
- The following is the type definition:
![[Event Queue Element Type]]
- Finally, at all times the queue will be sorted so that the element that is popped out has the minimum date and the event queue is ordered by date in this way
## Event Queue Starting State

- There are three options for starting state:
	- If a parameter is used which fills up the starting state with an event queue that is reasonable. It could be over a timeframe of a month for example and denote every single ride request that is going to happen
	- The [[Request Ride Wiring]] could always append the next ride request each time. This would mean that the starting state of the queue would be just one single ride request and the queue would continue to fill up one at a time after each wiring completes.
	- A combination could be used to do a similar thing by having a parameter fill in the next time each [[rider]] present in the system is going to request a ride, but then use the second method to fill in the next time after it for that specific rider. I.e. if there is N riders in the system then at any time there are exactly N events in the event queue for requesting rides
## Example