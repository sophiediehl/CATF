CATF
====

Clean Air Task Force

Code for modelling in "A Cost Assessment of Synthetic Inertia," by Sophie Diehl, August 2014.

frequency_response.py models the frequency excursion over time of a test grid with given physical parameters in response to a sudden loss in generation of a given size. "main" plots the response usiing matplotlib.pyplot.

lowest_cost_solution.py iterates over many combinations of ancillary service quantities to determine the least-cost combination of ancillary service increases that can allow the system to avoid under-frequency load shedding after suddenly losing the given generation amount.

rspin_pricing.py is an example of how csv data files from ERCOT's market information website were opened and compared to give information about the cost of ancillary services like regular spinning reserve.
