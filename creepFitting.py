import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from lmfit import Model


# Replace 'your_file.xlsx' with the actual file name
file_path = '3G fitting data _2.xlsx'


# Load the data from Excel
df = pd.read_excel(file_path,2,header=None)

# Extract time and creep strain columns for both temperatures
listOdd=list(range(1,df.shape[1],2))
listEven=list(range(0,df.shape[1],2))

sigmaList=[5,10,15,20]
tempList=40
colors=['blue','green','red','orange']
plt.figure(figsize=(8, 6))
for i in range(0,int((len(sigmaList)))):
    #converting the E-modulus(MPa) v.s. time (h) to strain v.s. time (s)
    df[listOdd[i]]=df[listOdd[i]].map(lambda x: sigmaList[i]/x)
    df[listEven[i]]=df[listEven[i]].map(lambda x: x*3600)
    #Plotting the experimental data
    plt.plot(df[listEven[i]].dropna(),df[listOdd[i]].dropna(), label=f'{tempList}°C-{sigmaList[i]}MPa Data',color=colors[i])





############## Calibration

# Combine the data
combined_time = np.concatenate([df[listEven[i]].dropna() for i in range(0,4)])
combined_epsilon = np.concatenate([df[listOdd[i]].dropna() for i in range(0,4)])

# Combine the corresponding stress values
combinedSigma = np.concatenate([np.full_like(df[listOdd[i]].dropna(),sigmaList[i]) for i in range(0,4)])

# Temperature
combined_temp = 40+273

# T = 318  # Replace with your actual temperature
#C4=13000
# Creep strain model function
# def creep_model(t, C1, C2, C3, C4):
#     return ((1 / (combinedSigma**C2 * np.exp(-C4 / combined_temp) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))
def creep_model(t,  C1, C2, C3, C4):
    return ((1 / (combinedSigma**C2 * np.exp(-C4 / combined_temp) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))



### CURVE FIT MODEL ###
# Initial guess for parameters C1, C2, C3, C4
initial_guess = ([0.0000000001, 0, -50,0], [1, 50, 0,np.inf])
# Fit the model to the experimental data for Sigma 
params, covariance = curve_fit(creep_model, combined_time, combined_epsilon, bounds=initial_guess,maxfev=100000)
# Print the optimized parameters
print("Optimized parameters for Sigma = 5 MPa:", params)


### LMFIT MODEL ###
model = Model(creep_model)
parameters = model.make_params(C1=0.1,C2=20,C3=-20,C4=1000)
parameters['C1'].set(min=0.00000000001,max=10)
parameters['C2'].set(min=0.,max=50)
parameters['C3'].set(min=-50,max=0)
parameters['C4'].set(min=1,max=100000)
result = model.fit(combined_epsilon,parameters,t=combined_time)

# Print the optimized parameters
print("Optimized parameters for Sigma = 5 MPa:", result.fit_report())

params = []
# Extract all parameters into a dictionary
params_dict = {param_name: (param.value, param.stderr) for param_name, param in result.params.items()}

# Extract the parameters
for param_name, (value, stderr) in params_dict.items():
    params.append(value)


# Plot the experimental data and the fitted model

def creep_model_test(t,stress,C1,C2,C3,C4):
    return ((1 / (stress**C2 * np.exp(-C4 / (273+40)) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

i=0
for sigma in sigmaList:
    timeSpace = np.logspace(np.log10(df[listEven[i]][0]), np.log10(df[listEven[i]][len(df[listEven[i]].dropna())-1]), num=100)
    plt.plot(timeSpace,creep_model_test(timeSpace,sigma,*params),label=f'Fitted Model - {tempList}°C - {sigma} MPa',linestyle='--',color=colors[i])
    i=i+1

#Figure modification
plt.xlabel('Time')
# plt.xscale('log')
plt.ylabel('Creep Strain')
plt.title(f'Creep Strain Model Calibration for parameter: \n [C1 C2 C3 C4] = {params}')
plt.legend()
plt.grid(True)

# Show the plot
plt.savefig('fitted_data_40C lmfit', dpi=300)

plt.show()


