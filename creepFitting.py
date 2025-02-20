import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from lmfit import Model





def creepFit(df,sigmaList,tempList,option):
    
    if type(sigmaList) is str:
        sigmaList=[int(x) for x in sigmaList.split(',')]
        tempList=[int(x) for x in tempList.split(',')]      

    listOdd=list(range(1,df.shape[1],2))
    listEven=list(range(0,df.shape[1],2))
    colors=['blue','green','red','orange','yellow','purple','black','cyan','grey','brown']
    # plt.figure(figsize=(8, 6))
    fig,ax = plt.subplots(figsize=(7,5))

    # i=0
    for i in range(0,int(len(sigmaList))):
        # for k in range(0,numberList[j]):
            
        #converting the E-modulus(MPa) v.s. time (h) to strain v.s. time (s)
        df[listOdd[i]]=df[listOdd[i]].map(lambda x: sigmaList[i]/x)
        df[listEven[i]]=df[listEven[i]].map(lambda x: x*3600)
        #Plotting the experimental data
        ax.plot(df[listEven[i]].dropna(),df[listOdd[i]].dropna(), label=f'{tempList[i]}°C-{sigmaList[i]}MPa Data',color=colors[i])
        # i+=1




    ############## Calibration

    # Combine the data
    combined_time = np.concatenate([df[listEven[i]].dropna() for i in range(0,len(listEven))])
    combined_epsilon = np.concatenate([df[listOdd[i]].dropna() for i in range(0,len(listEven))])

    # Combine the corresponding stress values
    combinedSigma = np.concatenate([np.full_like(df[listOdd[i]].dropna(),sigmaList[i]) for i in range(0,int(len(sigmaList)))])
    combinedTemp = np.concatenate([np.full_like(df[listOdd[i]].dropna(),tempList[i]) for i in range(0,int(len(tempList)))])+273
    # Temperature
    # combinedTemp_temp=[tempList[i] for i in range(len(numberList)) for j in range(numberList[i]) ]
    # combinedTemp = np.concatenate([np.full_like(df[listOdd[i]].dropna(),combinedTemp_temp[i]) for i in range(0,int(len(sigmaList)))])+273


    # Creep strain model function
    def creep_model(t,  C1, C2, C3, C4):
        return ((1 / (combinedSigma**C2 * np.exp(-C4 / combinedTemp) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))


    if option=='LMFIT':
  


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
    else:
        ### CURVE FIT MODEL ###
        # Initial guess for parameters C1, C2, C3, C4
        initial_guess = ([0.0000000001, 0, -50,0], [1, 50, 0,np.inf])
        # Fit the model to the experimental data for Sigma 
        params, covariance = curve_fit(creep_model, combined_time, combined_epsilon, bounds=initial_guess,maxfev=100000)
        # Print the optimized parameters
        print("Optimized parameters for Sigma = 5 MPa:", params)


    # Plot the experimental data and the fitted model
    def creep_model_test(t,stress,temp,C1,C2,C3,C4):
        return ((1 / (stress**C2 * np.exp(-C4 / (temp)) * C1 * t * (1 - C3)))**(1 / (C3 - 1)))

    i=0
    for sigma in sigmaList:
        timeSpace = np.logspace(np.log10(df[listEven[i]][0]), np.log10(df[listEven[i]][len(df[listEven[i]].dropna())-1]), num=100)
        ax.plot(timeSpace,creep_model_test(timeSpace,sigma,tempList[i]+273,*params),label=f'Fitted Model - {tempList[i]:.0f}°C - {sigma} MPa',linestyle='--',color=colors[i])
        i=i+1
            


    #Figure modification
    ax.set_xlabel('Time')
    # plt.xscale('log')
    ax.set_ylabel('Creep Strain')


    def format_value(value):
        if abs(value) < 0.001 or abs(value) > 10000:
          return f"{value:.2e}"  # Scientific notation with 2 decimal places
        else:
          return f"{value:.2f}"  # Fixed-point notation with 2 decimal places
    formattedParams = [format_value(p) for p in params]
    formatted_params_str = ', '.join(formattedParams)




    ax.set_title(f'Creep Strain Model Calibration for parameter: \n [C1 C2 C3 C4] = [{formatted_params_str}]')
    ax.legend()
    ax.grid(True)
    
    return params,fig


    # Replace 'your_file.xlsx' with the actual file name
file_path = '3G fitting data _2 temp.xlsx'


def main():
    # Load the data from Excel
    df = pd.read_excel(file_path,header=None)

    # Extract time and creep strain columns for both temperatures
    sigmaList=[5,10,15,20,5,10]
    tempList=[23,23,23,23,40,40]

    option=None

    parameters, plot = creepFit(df,sigmaList,tempList,option)

    # Show the plot
    plot.savefig('fitted_data_40C lmfit', dpi=300)
    plt.show()

if __name__ =='__main__':
    main()

