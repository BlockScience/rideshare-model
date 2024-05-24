
## 1) State Feedback: 

State feedback is a control design technique where the controller uses the system's state variables to generate a control signal. The state variables represent the internal dynamics of the system and provide a complete description of its behavior. In state feedback control, the control signal is calculated as a linear combination of the state variables, multiplied by a set of gains called the feedback gains.

The main idea behind state feedback is to drive the system's state variables to desired values or to stabilize the system around a desired operating point. By properly selecting the feedback gains, the designer can shape the system's response, improve its performance, and ensure stability.

State feedback control requires that all state variables are measurable or can be estimated. When some state variables are not directly measurable, an observer (discussed next) can be used to estimate them based on the available measurements.

## 2) Observer Design: 

An observer, also known as a state estimator, is a control design technique used to estimate the state variables of a system when they cannot be directly measured. The observer uses a mathematical model of the system, along with the available measurements (inputs and outputs), to estimate the values of the unmeasured state variables.

The observer design involves constructing a dynamical system that mimics the behavior of the actual system. The observer receives the same inputs as the actual system and uses the available measurements to update its estimate of the state variables. The observer's dynamics are designed such that the estimation error (the difference between the actual and estimated state variables) converges to zero over time.

Observers are particularly useful in state feedback control when some state variables are not measurable. The estimated state variables from the observer can be used in place of the actual state variables to calculate the control signal.

## 3. Optimal Control: 

Optimal control is a control design technique that aims to find the best possible control signal that minimizes a given performance criterion while satisfying system constraints. The performance criterion is typically expressed as a cost function, which quantifies the desired behavior of the system, such as minimizing energy consumption, tracking error, or time to reach a target state.

In optimal control, the designer formulates an optimization problem that includes the system dynamics, constraints, and the cost function. The solution to this optimization problem yields the optimal control signal that minimizes the cost function while respecting the constraints.

There are various approaches to solving optimal control problems, depending on the nature of the system and the cost function. Some common methods include:

- Linear Quadratic Regulator (LQR): Used for linear systems with quadratic cost functions.
- Model Predictive Control (MPC): Solves an optimization problem over a finite horizon, considering system constraints.
- Dynamic Programming: Breaks down the optimization problem into smaller subproblems and solves them recursively.

Optimal control provides a systematic way to design controllers that achieve the best possible performance while considering system limitations and constraints. However, it can be computationally intensive and may require accurate system models.

These three control design techniques - state feedback, observer design, and optimal control - are powerful tools in modern control theory. They can be used independently or in combination to design effective controllers for a wide range of systems, from simple linear systems to complex nonlinear systems.


![[Screenshot 2024-05-22 at 10.07.06 PM.png]]


![[Screenshot 2024-05-22 at 10.10.11 PM.png]]


![](https://images.squarespace-cdn.com/content/v1/5b2d76525cfd790c4a218093/1608499253557-IWU2T1UMIWEMFM8Q9I5O/Control_Map_ver4.png)

