notes: 

systematic vulnerabilities
coordinated behavior - test case

generate weighted directed graph, treat each of the node as a region/location/discrete bucket, edges expected travel time between buckets (weighted), used as substitute for geography. driver can be in bucket but have to move along the graph. 

wighted graph with n nodes is a weighted n X n matrix

rider in place  place, existing shortest path algorithm (network x) shortest path = input into pricing model

when a driver doesn't have a rider -> random walk

network x python lib

queue clearing problem

algorithm 7 below:	
https://repository.upenn.edu/entities/publication/5eb4284f-77f5-4728-907a-8def213b785d

https://github.com/1Hive/conviction-voting-cadcad/blob/master/model_structure.ipynb

reach out in firstbatch

[The Art of Mathematical Modeling](https://hackmd.io/@blockscience/rketbTyGA)

[PSUU in Practice](https://hackmd.io/@blockscience/Hy3p_ueJC)

[Engineering note](https://hackmd.io/@blockscience/SkRVn5EAT)

https://ocw.mit.edu/courses/16-842-fundamentals-of-systems-engineering-fall-2015/resources/mit16_842f15_ses1se_ovr_vw/

https://www.mathworks.com/videos/why-models-are-essential-to-digital-engineering-1652969543566.html
**Zhargam:**  
i think it would also be good for us to start a thread here with references.  

- here is the distributed kalman filter reference [https://ieeexplore.ieee.org/document/4434303](https://ieeexplore.ieee.org/document/4434303)
- here is another paper i like on learning in networks: [https://www.sciencedirect.com/science/article/abs/pii/S0899825612000851](https://www.sciencedirect.com/science/article/abs/pii/S0899825612000851)
- i also regularly use this tutorial as a reference of distributed systems: [https://ieeexplore.ieee.org/document/8716798](https://ieeexplore.ieee.org/document/8716798)

**Jamsheed:**  
Here are useful references for deriving a minimal set of necessary conditions for a stable network under incomplete information and node asymmetry--the main ref is Song & Schaar (2015), working up from the seminal paper of Jackson and Wolinsky (1996), but the others are important to explore compatible learning paradigms and agent optimization horizons. (Working paper versions exist for most of these via e.g. google scholar.)  

- Sun & Parilina (2024), “[Dynamic network formation with ordered partitioning and incomplete information](https://doi.org/10.1007/s13235-024-00552-z)”, _Dynamic Games and Applications (2024)_, online.
- Herings, Mauleon & Vannetelbosch (2018), “[Stability of networks under horizon-K farsightedness](https://doi.org/10.1007/s00199-018-1119-7)”, _Economic Theory_ 68, pp. 177-201.
- Song & Schaar (2015), “[Dynamic network formation with incomplete information](https://doi.org/10.1007/s00199-015-0858-y)”, _Economic Theory_ 59, pp. 301-331.
- Herings, Mauleon & Vannetelbosch (2009), “[Farsightedly stable networks](https://doi.org/10.1016/j.geb.2008.12.009)”, _Games and Economic Behavior_ 67, pp. 526-541.
- Jackson & Wolinsky (1996), “[A strategic model of social and economic networks](https://doi.org/10.1006%2Fjeth.1996.0108)”, _Journal of Economic Theory_ 106, pp. 265-295.

**Danilo**  

- **Zanchetta, A.D.L.; Coulibaly, P. Recent Advances in Real-Time Pluvial Flash Flood Forecasting.** **_Water_** **2020,** **_12_****, 570.** **[https://doi.org/10.3390/w12020570](https://doi.org/10.3390/w12020570)**
- **Abrego-Perez, A.L.; Pacheco-Carvajal, N.; Diaz-Jimenez, M.C. Forecasting Agricultural Financial Weather Risk Using PCA and SSA in an Index Insurance Model in Low-Income Economies.** **_Appl. Sci._** **2023,** **_13_****, 2425.** **[https://doi.org/10.3390/app13042425](https://doi.org/10.3390/app13042425)**
![[Screenshot 2024-05-17 at 12.48.31 PM.png]]


destination survey data:
[https://data.ny.gov/Transportation/MTA-Origin-Destination-and-Travel-Surveys/hexe-btds/about_data](https://data.ny.gov/Transportation/MTA-Origin-Destination-and-Travel-Surveys/hexe-btds/about_data)

pitch in by using NY data ^^

[https://jisajournal.springeropen.com/articles/10.1186/s13174-021-00136-9](https://jisajournal.springeropen.com/articles/10.1186/s13174-021-00136-9) 




The assumptions made in the optimal control model for ride-sharing platforms are as follows:

1. Two actors: The system consists of two main actors - passengers, represented by the number of ride requests, and drivers, who are available to accept and fulfill these ride requests.
2. Dynamic pricing: The platform charges passengers a price p(t), which is a function of time and depends on various factors such as the number of available drivers, base cost, distance, and trip duration.
3. Reference price: At any given time t, a passenger will accept the ride if the charged price p(t) is less than or equal to their reference price R. The reference price is the maximum price a passenger is willing to pay for the ride based on their perception of the service's value.
4. Passenger utility: The utility or benefit to the passenger is the difference between their reference price R and the actual price p charged by the platform, i.e., R-p, if they are served. If the passenger is not served (i.e., if p > R), their utility is zero.
5. Ride request rate: The rate at which ride requests arrive, denoted by μ, depends on the reference price R and the actual price p charged by the platform.
6. Single ride per passenger: Each passenger takes a single ride and then leaves the system. This assumption simplifies the model by not considering repeat customers or multiple rides by the same passenger within the considered time frame.
7. Price sensitivity: Passengers are negatively sensitive to the price, meaning that higher prices lead to fewer ride requests. This sensitivity is assumed to be instantaneous, affecting the passenger's decision for the current ride.
8. Platform costs: The ride-share platform incurs two types of costs: a. Service cost (∈): This cost is associated with serving each customer and includes expenses related to developing, optimizing, and operating the application, as well as attracting and training drivers. b. Price change cost (β): This cost is incurred when the platform changes the ride price. It is assumed to be quadratic, meaning that the marginal impact of changing the ride price increases as the magnitude of the price change increases.

These assumptions simplify the real-world complexities of ride-sharing platforms to create a manageable optimal control model that focuses on the key aspects of pricing dynamics and profit maximization.


I apologize for the incomplete response. Let me continue with the step-by-step guide on designing a rideshare model for cadCAD.

Step 1: Identify the key variables and agents
- Determine the main variables that affect the rideshare system, such as the number of ride requests, available drivers, ride price, and customer satisfaction.
- Define the agents in the system, typically passengers and drivers.

Step 2: Define the system dynamics
- Establish the relationships between the variables and agents, such as how the number of ride requests and available drivers influence the ride price.
- Consider factors like supply and demand, pricing strategies, and customer behavior.

Step 3: Formulate the state variables and state update functions
- State variables represent the system's state at any given time. In a rideshare model, these could include the number of ride requests, available drivers, and ride price.
- State update functions define how the state variables change over time based on the system dynamics and agent interactions.

Step 4: Develop the pricing mechanism
- Create a pricing function that determines the ride price based on relevant factors, such as the number of ride requests, available drivers, distance, and time of day.
- Incorporate dynamic pricing strategies, such as surge pricing during peak hours or high-demand periods.

Step 5: Model customer behavior
- Develop a function that represents customer decision-making, such as whether to request a ride based on the current price and their willingness to pay.
- Consider factors like price sensitivity, waiting time tolerance, and alternative transportation options.

Step 6: Implement the driver decision-making process
- Model how drivers decide to accept or reject ride requests based on factors like distance, traffic conditions, and expected earnings.
- Incorporate driver incentives and penalties to encourage desired behaviors.

Step 7: Set up the simulation environment in cadCAD
- Define the initial state of the system, including the number of ride requests, available drivers, and starting ride price.
- Specify the time steps for the simulation and the duration of the simulation run.

Step 8: Implement the state transition functions
- Translate the state update functions and agent decision-making processes into cadCAD's state transition functions.
- Ensure that the functions accurately capture the system dynamics and agent interactions.

Step 9: Run simulations and analyze results
- Execute the cadCAD simulation with different parameter settings and scenarios.
- Collect and analyze the simulation results, focusing on key performance indicators like ride fulfillment rate, average waiting time, driver utilization, and platform revenue.

Step 10: Validate and refine the model
- Compare the simulation results with real-world data, if available, to assess the model's accuracy and validity.
- Refine the model by adjusting parameters, updating functions, or incorporating additional factors based on the validation process.

Step 11: Conduct sensitivity analysis
- Perform sensitivity analysis by varying key parameters and observing their impact on the system's performance.
- Identify the most influential factors and use these insights to inform pricing strategies and operational decisions.

Step 12: Iterate and improve
- Continuously monitor the model's performance and make necessary updates as the real-world system evolves.
- Incorporate new features, pricing strategies, or agent behaviors to keep the model relevant and accurate.

By following these steps, you can design a rideshare model that captures the essential dynamics and interactions of the system, allowing you to simulate and analyze various scenarios in cadCAD. Remember to start with a simpler model and gradually add complexity as needed, ensuring that each component is thoroughly tested and validated along the way.






-when deriving factors determine exhaustive / non exhaustive
-should we be flexible or not in each factor

rider / drive agents
entities - platform 

update the intersts & stakeholders

requirement vs desirable
admissable vs 

agent based vs population based
topological componets (complex or simple)