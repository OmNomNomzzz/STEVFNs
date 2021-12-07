#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 16:48:21 2021

@author: aniqahsan
"""

############ Import packages #######
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize as optim
import cvxpy as cp
import time

######## Define Parameters ###########
np.random.seed(0)
N = 3# number of nodes
C_G =  np.array([1.,0.9,0.8])# np.random.rand(3)#
C_G2 = np.array([0.1,0.2,0.3])# np.random.rand(3) * 0.1
Z = np.array([[0.,1,1],[0,0,1],[0,0,0]])
V_min = np.array([0.9, 0.9, 0.9])
V_max = np.array([1.1, 1.1, 1.1])
P_D = np.array([0.1, 0.2, 0.3])
P_G_max = np.array([3.,3,3])
P_G_min = np.array([0.,0,0])
P_MAX = np.array([[0.,1,1],[0,0,1],[0,0,0]])
ALPHA = np.array([[0.,0.9,0.9],[0,0,0.9],[0,0,0]])
V0 = 100.


###### Build Parameters ##############

Z = Z + Z.T
P_MAX = P_MAX + P_MAX.T
ALPHA = ALPHA + ALPHA.T

for counter1 in range(Z.shape[0]):
    Z[counter1,counter1] = -sum(Z[counter1])
    P_MAX[counter1,counter1] = P_G_max[counter1]



###### Define CVXPY Parameters and Valriables #######
V = cp.Variable(N, value = np.random.rand(N))
P_G = cp.Variable(N, nonneg=True, value = np.random.rand(N))
C_G = cp.Parameter(N, nonneg=True, value = C_G)
C_G2 = cp.Parameter(N, nonneg=True, value = C_G2)
Z = cp.Parameter((N,N), NSD = True, value = Z)
V0 = cp.Parameter(nonneg=True, value = V0)
P_D = cp.Parameter(N, nonneg=True, value = P_D)
P_MAX = cp.Parameter((N,N), nonneg=True, value = P_MAX)
P_G_min = cp.Parameter(N, nonneg=True, value = P_G_min)
V0Z = cp.Parameter((N,N), NSD=True, value = V0.value*Z.value)

######## Define CVXPY Expressions #######

P_out = -V0*(Z@V)
P_out = -V0Z@V
# P_G = P_D + P_out
P = cp.multiply(V0Z, cp.hstack([cp.reshape(V, (3,1)),]*N) - cp.vstack([cp.reshape(V, (1,3)),]*N)) + cp.diag(P_G)
cost1 = cp.multiply(C_G, P_G)
cost2 = cp.multiply(C_G2, cp.power(P_G,2))
P_G2 = P_G**2
cost2 = cp.multiply(C_G2, P_G2)
cost = cp.sum(cost1 + cost2)
# cost = cp.sum(cost2)

P_out_full = -(cp.multiply((V0+V),(Z@V)))
P_out_violation =  P_out_full - P_out
curtailment_violation = P_G - P_D - P_out_full

######## Define CVXPY Problem #######

#### define DCOPF ####
obj = cp.Minimize(cost)
constraints = []
constraints += [P_G>=P_G_min]
constraints += [P<=P_MAX]
constraints += [P_G == P_D + P_out]
constraints += [V[0] == 0]

prob_DCOPF = cp.Problem(obj, constraints)

prob_DCOPF.solve(solver=cp.ECOS)


#### define DCOPF with curtailment at nodes ###
constraints = []
constraints += [P_G>=P_G_min]
constraints += [P<=P_MAX]
constraints += [P_G >= P_D + P_out]
constraints += [V[0] == 0]

prob_DCOPF_ineq = cp.Problem(obj, constraints)

prob_DCOPF_ineq.solve(solver=cp.ECOS)

##### define STEVFNs linear losses without curtailment at nodes ####
alpha = np.random.rand(N,N)
alpha = alpha + alpha.T
alpha = 1.0 - 0.05 * alpha
alpha = alpha - np.diag(np.diag(alpha))

alpha = 1.0 - (np.abs(P.value) * Z.value)/V0.value**2
alpha = alpha - np.diag(np.diag(alpha))


P_STEVFNs = cp.Variable(shape = (N,N), nonneg=1)

ALPHA = cp.Parameter(shape = (N,N))
ALPHA.value = alpha
P_G_STEVFNs = cp.diag(P_STEVFNs)
P_flow_STEVFNs = P_STEVFNs - cp.diag(P_G_STEVFNs)
P_out_STEVFNs = P_flow_STEVFNs @ np.ones(N)
P_in_STEVFNs_linear = cp.multiply(ALPHA,P_flow_STEVFNs).T @ np.ones(N)
P_Net_STEVFNs_linear = P_D + P_out_STEVFNs - P_in_STEVFNs_linear - P_G_STEVFNs

cost_STEVFNs = cp.sum(cp.multiply(C_G, P_G_STEVFNs)) + cp.sum(cp.multiply(C_G2, P_G_STEVFNs**2))

constraints_STEVFNs = []
constraints_STEVFNs += [P_Net_STEVFNs_linear == 0]



obj_STEVFNs = cp.Minimize(cost_STEVFNs)

prob_STEVFNs = cp.Problem(obj_STEVFNs, constraints_STEVFNs)

prob_STEVFNs.solve()


##### define STEVFNs linear losses with curtailment at nodes ####
constraints_STEVFNs_ineq = []
constraints_STEVFNs_ineq += [P_Net_STEVFNs_linear <= 0]

prob_STEVFNs_ineq = cp.Problem(obj_STEVFNs, constraints_STEVFNs_ineq)

prob_STEVFNs_ineq.solve()

##### define STEVFNs quadratic losses with curtailment at nodes ####
beta = Z.value / V0.value**2
beta = beta - np.diag(np.diag(beta))

BETA = cp.Parameter(shape = (N,N), nonneg=1)
BETA.value = beta
P_in_STEVFNs_quad =  (P_flow_STEVFNs - cp.multiply(BETA, P_flow_STEVFNs**2)).T @ np.ones(N)
P_Net_STEVFNs_quad = P_D + P_out_STEVFNs - P_in_STEVFNs_quad - P_G_STEVFNs

constraints_STEVFNs_quad = []
constraints_STEVFNs_quad += [P_Net_STEVFNs_quad <= 0]

prob_STEVFNs_quad = cp.Problem(obj_STEVFNs, constraints_STEVFNs_quad)

prob_STEVFNs_quad.solve()



######### Define Functions ############

def build_random_Z(N):
    Z = np.zeros((N,N))
    for counter1 in range(N-1):
        Z[counter1,counter1+1:] = np.random.rand(N-counter1-1) * 1.
    Z = Z + Z.T
    for counter1 in range(Z.shape[0]):
        Z[counter1,counter1] = -sum(Z[counter1])
    return Z




######## Run Code ###########



# N_runs = 10
# V_diffs = np.zeros(N_runs)
# P_G_diffs = np.zeros(N_runs)
# value_diffs = np.zeros(N_runs)
# P_out_violation_list = []
# P_out_violation_list_ineq = []
# curtailment_violation_list = []
# curtailment_violation_list_ineq = []


# for counter1 in range(N_runs):
#     C_G.value = np.ones(N) + 1 * np.random.rand(N)
#     C_G2.value = 0.1 * (np.ones(N) + 1 * np.random.rand(N))
#     P_D.value = np.random.rand(N)
#     Z.value = build_random_Z(N)
#     V0Z.value =  V0.value*Z.value
#     prob_DCOPF.solve(solver=cp.ECOS)
#     # print("Without curtailment")
#     # print("P_out violation = \n", P_out_violation.value)
#     # print("curtailment_violation = \n", curtailment_violation.value)
#     P_out_violation_list += [P_out_violation.value]
#     curtailment_violation_list += [curtailment_violation.value]
#     v1 = V.value
#     P_G_1 = P_G.value
#     value_1 = prob_DCOPF.value
#     prob_DCOPF_ineq.solve(solver=cp.ECOS)
#     v2 = V.value
#     P_G_2 = P_G.value
#     value_2 = prob_DCOPF_ineq.value
#     v_dif = np.max(np.abs(v2-v1))
#     P_G_diff = np.max(np.abs(P_G_2 - P_G_1))
#     value_diff = np.abs(value_2 - value_1)
#     # print("With curtailment")
#     # print("P_out violation = \n", P_out_violation.value)
#     # print("curtailment_violation = \n", curtailment_violation.value)
#     # print("Cost difference = ", value_2 - value_1)
#     P_out_violation_list_ineq += [P_out_violation.value]
#     curtailment_violation_list_ineq += [curtailment_violation.value]
#     V_diffs[counter1] = v_dif
#     P_G_diffs[counter1] = P_G_diff
#     value_diffs[counter1] = value_diff

# P_out_violation_array = np.array(P_out_violation_list)
# P_out_violation_array_ineq = np.array(P_out_violation_list_ineq)
# curtailment_violation_array = np.array(curtailment_violation_list)
# curtailment_violation_array_ineq = np.array(curtailment_violation_list_ineq)


# plt.plot(P_out_violation_array.flatten())
# plt.plot(P_out_violation_array_ineq.flatten())
# plt.show()
# plt.plot(curtailment_violation_array.flatten())
# plt.plot(curtailment_violation_array_ineq.flatten())
# plt.show()

# start_time = time.time()

# prob_DCOPF.solve(solver=cp.ECOS)

# time_taken_1 = time.time() - start_time
# print("Time taken = ", time_taken_1)
# print("Cost = ", prob_DCOPF.value)
# print("V value = ", V.value)
# print("P value = ", P.value)
# print("P_G value = ", P_G.value)
# print("Solver used = ", prob_DCOPF.solver_stats.solver_name)


# start_time = time.time()

# prob_DCOPF_ineq.solve(solver=cp.ECOS)

# # for counter1 in range(1000):
# #     prob.solve(solver=cp.SCS)

# time_taken_2 = time.time() - start_time
# print("Time taken = ", time_taken_2)
# print("T2/T1 = ", time_taken_2/time_taken_1)
# print("Cost = ", prob_DCOPF_ineq.value)
# print("V value = ", V.value)
# print("P value = ", P.value)
# print("P_G value = ", P_G.value)
# print("Solver used = ", prob_DCOPF_ineq.solver_stats.solver_name)
