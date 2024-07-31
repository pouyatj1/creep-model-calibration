import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Assuming your Excel file has three columns: 'Time_23', 'Creep Strain_23', 'Time_60', 'Creep Strain_60'
# Replace 'your_file.xlsx' with the actual file name
#os.chdir('C:\Work\Projects\NG shut-off valve\Material\calibration at 45/')
file_path = 'C:/Work/Projects/In progress/3G Copression fitting/Sim/Report/3G fitting data.xlsx'
file_path = '3G fitting data _2.xlsx'

# file_path = 'Fit all.xlsx'
# Load the data from Excel
df = pd.read_excel(file_path,2,header=None)

# Extract time and creep strain columns for both temperatures
time_5MPa = df[0].dropna()*3600
creep_strain_5MPa = 5/df[1].dropna()
time_10MPa = df[2].dropna()*3600
creep_strain_10MPa = 10/df[3].dropna()
time_15MPa = df[4].dropna()*3600
creep_strain_15MPa = 15/df[5].dropna()
time_20MPa = df[6].dropna()*3600
creep_strain_20MPa = 20/df[7].dropna()


# Plot the original data and interpolated data
plt.figure(figsize=(8, 6))

# # Plot original data points
plt.plot(time_5MPa, creep_strain_5MPa, label='23°C-5MPa Data', color='blue')
plt.plot(time_10MPa, creep_strain_10MPa, label='23°C-10MPa Data', color='green')
plt.plot(time_15MPa, creep_strain_15MPa, label='23°C-15MPa Data', color='red')
plt.plot(time_20MPa, creep_strain_20MPa, label='23°C-20MPa Data', color='orange')


# #plt.xscale("log")
# # Set labels and title
# plt.xlabel('Time')
# plt.ylabel('Creep Strain')
# plt.title('Experimental creep strain v.s. time')
# plt.legend()
# plt.grid(True)

# # Show the plot
# plt.savefig('C:/Work\Projects/NG shut-off valve/Material/Creep exp data/Py/experimental_data', dpi=300)
# plt.show()




############## Calibration

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Load experimental data from Excel
#file_path = 'experimental_data.xlsx'  # Replace with your actual file path
#df = pd.read_excel(file_path)

stresses=[5,10,15,20]

# Combine the data
combined_time = np.concatenate([globals()[f'time_{stress}MPa'] for stress in stresses])
combined_epsilon = np.concatenate([globals()[f'creep_strain_{stress}MPa'] for stress in stresses])

# Combine the corresponding stress values
sigma_5MPa = 5.0
sigma_10MPa = 10.0
sigma_15MPa = 15.0
sigma_20MPa = 20.0

combined_sigma = np.concatenate([np.full_like(time_5MPa, sigma_5MPa), np.full_like(time_10MPa, sigma_10MPa),np.full_like(time_15MPa, sigma_15MPa), np.full_like(time_20MPa, sigma_20MPa)])


combined_temp = 40+273
# Temperature
T = 318  # Replace with your actual temperature
#C4=13000
# Creep strain model function
def creep_model(t, C1, C2, C3, C4):
    return ((1 / (combined_sigma**C2 * np.exp(-C4 / combined_temp) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

# Initial guess for parameters C1, C2, C3, C4
initial_guess = ([0.0000000001, 0, -50,0], [1, 50, 0,np.inf])

# Fit the model to the experimental data for Sigma = 5 MPa
params, covariance = curve_fit(creep_model, combined_time, combined_epsilon, bounds=initial_guess,maxfev=100000)

# Print the optimized parameters
print("Optimized parameters for Sigma = 5 MPa:", params)


# Plot the experimental data and the fitted model
#plt.figure(figsize=(8, 6))

# Plot experimental data for Sigma = 5 MPa
#plt.scatter(time_5, epsilon_5MPa, label='Experimental Data (Sigma = 5 MPa)', color='blue',alpha=0.2)

# Plot experimental data for Sigma = 10 MPa
#plt.scatter(time_10, epsilon_10MPa, label='Experimental Data (Sigma = 10 MPa)', color='red',alpha=0.2)

# Plot fitted model for both datasets
#plt.plot(combined_time, creep_model(combined_time, *params), label='Fitted Model', linestyle='--', color='green')


# params = np.array([0.1, 12, -10.0, -2000])
# list=[]
# for c in time_5MPa[:4]:
#     list.extend([c,2*c])
# time_5MPa = pd.DataFrame(list)

# list=[]
# for c in time_10MPa[:4]:
#     list.extend([c,2*c])
# time_10MPa = pd.DataFrame(list)

# list=[]
# for c in time_15MPa[:4]:
#     list.extend([c,2*c])
# time_15MPa = pd.DataFrame(list)

# list=[]
# for c in time_20MPa[:4]:
#     list.extend([c,2*c])
# time_20MPa = pd.DataFrame(list)




def creep_model_5(t, C1, C2, C3, C4):
    return ((1 / (5**C2 * np.exp(-C4 / (273+40)) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

plt.plot(time_5MPa, creep_model_5(time_5MPa, *params), label='Fitted Model - 23C - 5 MPa', linestyle='--', color='blue')

def creep_model_10(t, C1, C2, C3, C4):
    return ((1 / (10**C2 * np.exp(-C4 / (273+40)) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

plt.plot(time_10MPa, creep_model_10(time_10MPa, *params), label='Fitted Model - 23C -10 MPa', linestyle='--', color='green')

def creep_model_15(t, C1, C2, C3, C4):
    return ((1 / (15**C2 * np.exp(-C4 / (273+40)) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

plt.plot(time_15MPa, creep_model_15(time_15MPa, *params), label='Fitted Model - 23C - 15 MPa', linestyle='--', color='red')

def creep_model_20(t, C1, C2, C3, C4):
    return ((1 / (20**C2 * np.exp(-C4 / (273+40)) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

plt.plot(time_20MPa, creep_model_20(time_20MPa, *params), label='Fitted Model - 23C - 20 MPa', linestyle='--', color='orange')

# Set labels and title
plt.xlabel('Time')
# plt.xscale('log')
plt.ylabel('Creep Strain')
plt.title(f'Creep Strain Model Calibration for parameter: \n [C1 C2 C3 C4] = {params}')
plt.legend()
plt.grid(True)

# Show the plot
plt.savefig('C:/Work\Projects/In progress/3G Copression fitting/docs/Creep calibration/fitted_data_23C', dpi=300)

plt.show()


