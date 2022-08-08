import numpy as np
import pandas as pd
from Utilities import orderPeriods, calculateCost, visualize

# BASIC NOTES
#
#     -> variable with single pre underscore(_) represent the values used for calculation only. These are not gettable values.
#
#         Ex: Let assume x is an object of PartPeriodAlgorithm.
#         If you try to get any variable with single pre underscore (like x._total_cost), you'll get an error.
#
#     -> __init__() is constructor method in python.
#
#     -> Method names of all classes are the same for easy understanding. But operations are totally different from each other.
#        So the definition of methods will be explained in PartPeriodBalancing class only.



class Algorithms:
    
    class PartPeriodBalancing:
        

        def __init__(self, demand, order_cost, holding_cost):
            self.demand = demand 
            self.order_cost = order_cost
            self.holding_cost = holding_cost
            self._total_cost = 0 # total variable cost
            self._order_periods = [0]  
            self._current_period = 0 
            self._T = -1  # indices starts with zero. That is the reason why init. value of _T is -1.
            self._APP = 0
            self._EPP = order_cost/holding_cost
            self.next_step() #calling next_step method
                
            

        # The next_step method calculate APP then it calls check().
        def next_step(self):
            self._T += 1
            RT = self.demand[self._current_period]*(self._T)
            self._APP += RT
            return self.check() # calling 
        

        # After the calculation of APP check() checks the condition (APP<EPP) if it's true then calls isfinish() else calls reset()
        def check(self):
            if self._APP < self._EPP:
                self._current_period += 1
                return self.isfinish() 
            else:
                return self.reset()
            

        # reset() method resets the values after order periods. So current_period increases by 1 but T resets.

        def reset(self):
            self._APP = 0
            self._T = -1
            self._order_periods.append(self._current_period)
            return self.next_step()
                
            

        # After each iteration isfinished() checks (current period<length of demand) if the iteration has finished.

        def isfinish(self):
            if self._current_period > len(self.demand)-1:
                self._order_periods.append(len(self.demand))
                self.calculate_period_cost() 
                
            else:
                return self.next_step()
            
        
        def calculate_period_cost(self):
            self._total_cost, self.Q = calculateCost(self._order_periods, self.demand, self._total_cost, self.holding_cost, self.order_cost)
            
            
        def print_result(self):
            visualize(self._order_periods, self.Q, self.demand, self._total_cost)
            
    
    
    
    class SilverMeal:
        
        def __init__(self, demand, order_cost, holding_cost):
            self.demand = demand
            self.order_cost = order_cost
            self.holding_cost = holding_cost
            self._total_cost = 0
            self._order_periods = [0] 
            self._current_period = 0
            self._T = -1
            self._HC = 0   # sum of h(t-1)Rt
            self._TCR = order_cost
            self._rate_stack = order_cost * 10   # it is initial value to compare with the next value for TCR(T)/T (Like a Big M)
            self.next_step()
                
        
        def next_step(self):
            self._T += 1
            RT = self.demand[self._current_period]*(self._T)
            self._HC += RT * self.holding_cost
            self._TCR = self._HC + self.order_cost
            self.rate = self._TCR / (self._T+1)
            return self.check()
        
    
        def check(self):
            if self.rate < self._rate_stack:
                self._rate_stack = self.rate
                self._current_period += 1
                return self.isfinish() 
            else:
                self._rate_stack = self.order_cost * 10
                return self.reset()
    
        
        def reset(self):
            self._T = -1
            self._HC = 0
            self._TCR = self.order_cost
            self._order_periods.append(self._current_period)
            return self.next_step()
                
            
        def isfinish(self):
            if self._current_period > len(self.demand)-1:
                self._order_periods.append(len(self.demand))
                return self.calculate_period_cost() 
                
            else:
                return self.next_step()
            
            
        def calculate_period_cost(self):
            self._total_cost, self.Q = calculateCost(self._order_periods, self.demand, self._total_cost, self.holding_cost, self.order_cost)
            
        
        def print_result(self):
            visualize(self._order_periods, self.Q, self.demand, self._total_cost)
    
    
    
    class LeastUnitCost:
        
        def __init__(self, demand, order_cost, holding_cost):
            self.demand = demand
            self.order_cost = order_cost
            self.holding_cost = holding_cost
            self._total_cost = 0
            self._order_periods = [0] 
            self._current_period = 0
            self._T = -1
            self._sum_of_RT = 0
            self._HC = 0   
            self._TCR = order_cost
            self._rate_stack = 10*4   # it is initial value to compare with the next value for TCR(T)/sumOf(Rt) (Like a Big M)
            self.next_step()
                
        
        def next_step(self):
            self._T += 1
            RT = self.demand[self._current_period]
            self._sum_of_RT += RT 
            RT = RT * (self._T)
            self._HC += RT * self.holding_cost
            self._TCR = self._HC + self.order_cost
            self.rate = self._TCR / self._sum_of_RT
            return self.check()
        
    
        def check(self):
            if self.rate <= self._rate_stack:
                self._rate_stack = self.rate
                self._current_period += 1
                return self.isfinish() 
            else:
                self._rate_stack = self.order_cost * 10
                return self.reset()
    
        
        def reset(self):
            self._T = -1
            self._HC = 0
            self._TCR = self.order_cost
            self._sum_of_RT = 0
            self._order_periods.append(self._current_period)
            return self.next_step()
        
            
        def isfinish(self):
            if self._current_period > len(self.demand)-1:
                self._order_periods.append(len(self.demand))
                
                return self.calculate_period_cost() 
            
            else:
                return self.next_step()
            
            
        def calculate_period_cost(self):
            self._total_cost, self.Q = calculateCost(self._order_periods, self.demand, self._total_cost, self.holding_cost, self.order_cost)
            
            
        def print_result(self):
            visualize(self._order_periods, self.Q, self.demand, self._total_cost)
            
            
