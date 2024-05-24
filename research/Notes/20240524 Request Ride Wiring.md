## Summary

The following is a work in progress note aiming at defining a wiring for when a [[Request Ride Wiring|rider requests a ride]].

## Structure

The wiring will be a stack block of:
1. [[Request Ride Boundary Action]]
2. [[Ride Pricing Policy]]
3. [[Ride Confirmation Policy]]
4. [[Request Ride Mechanisms Wiring]]

## Notes

There are two places where the wiring might terminate early: [[Ride Pricing Policy]] if no drivers are available and [[Ride Confirmation Policy]] if the [[Rider]] does not agree with the response.