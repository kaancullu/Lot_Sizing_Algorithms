import numpy as np
import pandas as pd
from itertools import islice


# NOTES
#     Functions that will be used in common in all algorithms are included in this module.



#     orderPeriods() takes indices of order periods and orders as input. By applying the following operations, it finds the total order for each order period.
#
#         Ex : Let
#
#              #INPUT
#                  period_indices = [0,2,4,8]
#                  demands = [100,200,300,400,500,600,700,800]
#
#              #OUTPUT
#                  orders will be -> [[100,200],[300,400],[500,600,700,800]]
#                  total_order_each_period = [300,700,2600]
#
#     ########################################################################################################################################################
#
#     calculateCost() calculates the total variable cost. It uses orderPeriods function to calculation.
#
#         Ex : Let
#
#              #INPUT
#                  orderPeriods = [0,2,4,8]
#                  demands = [100,200,300,400,500,600,700,800]
#                  total_cost = 0
#                  order_cost = 100
#                  holding_cost = 1
#
#              #OUTPUT
#                  total_cost will be -> 5300
#                  Q_ will be -> [300,700,2600]
#
#
#              -------------------------------------------------------------------------------------------------------------------------------------------
#                  Q_ hold the total_order_each_period because in operations of orderPeriods all elements from this transaction are reset.
#
#                  def calculateCost(order_periods, demand, total_cost, holding_cost, order_cost):
#                     RT, Q = orderPeriods(order_periods,demand)
#                     Q_ = Q.copy()
#                     for i, item in enumerate(RT):
#                         for j in item:
#                             Q[i] = Q[i] - j  <------------------------------------ Because of that line
#                             total_cost += Q[i]*holding_cost
#
#                     total_cost += len(RT)*order_cost
#                     return total_cost, Q_
#             -------------------------------------------------------------------------------------------------------------------------------------------
#
#     ########################################################################################################################################################
#
#     visualize() function print the results on screen



def orderPeriods(period_indices, demands):
    demands = iter(demands)
    length_to_split = [period_indices[i+1]-period_indices [i] for i in range(len(period_indices)-1)]
    orders = [list(islice(demands, elem)) for elem in length_to_split]
    total_order_each_period = [sum(i) for i in orders]
    return orders, total_order_each_period

def calculateCost(order_periods, demand, total_cost, holding_cost, order_cost):
    RT, Q = orderPeriods(order_periods,demand)
    Q_ = Q.copy()
    for i, item in enumerate(RT):
        for j in item:
            Q[i] = Q[i] - j
            total_cost += Q[i]*holding_cost
    
    total_cost += len(RT)*order_cost
    return total_cost, Q_

def visualize(order_periods, Q, demand, total_cost):
    order_periods = order_periods[:-1]
    q = np.zeros(len(demand))
    q[order_periods] = Q
    res = np.vstack((demand, q))
    
    column_names = range(1,len(demand)+1)
    df = pd.DataFrame(res,columns = column_names, index =["RT","Q"])
    print(df)
    print(f"\nTotal Variable Cost = ${total_cost}")