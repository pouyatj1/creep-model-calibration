# Documentation for Creep Model Calibration Program

## Overview

This program is designed to calibrate a "strain hardening creep" model based on experimental data. It utilizes two different methods for model fitting: `LMFIT` from the `lmfit` library and `curve_fit` from `scipy.optimize`. The calibration results are visualized through plots and can be saved as images. The program features a graphical user interface (GUI) built with `Tkinter` for ease of use.

## Components

1. **Data Processing and Calibration**: Implemented in `creepFitting.py`.
2. **GUI Application**: Implemented in `mainProg.py`.

### `creepFitting.py`

This file contains the core functionality for data processing and model fitting. Can be executed without the GUI.

#### Key Functions

- **`creepFit(df, sigmaList, tempList, option)`**: 
  - **Purpose**: Fits a strain hardening creep model to the experimental data.
  - **Parameters**:
    - `df`: DataFrame containing the experimental data.
    - `sigmaList`: List of applied constant stresses.
    - `tempList`: List of temperatures corresponding to each dataset.
    - `option`: Fitting method option ('LMFIT' or 'Curve_fit (default)').
  - **Returns**:
    - `params`: Optimized parameters for the creep model.
    - `fig`: Matplotlib figure object containing the plot of the data and fitted model.

#### Creep Model

- **Model Function**:
Strain hardening model available in Ansys 



### `mainProg.py`

This file provides a graphical user interface (GUI) for interacting with the calibration program.

#### Key Functions

- **`fig_to_array(fig)`**: Converts a Matplotlib figure to a NumPy array for displaying in Tkinter.
- **`process_data()`**: Reads user inputs, processes the data using the `creepFit` function, and displays results and plots.


## Installation and Usage

### Requirements

- **Python Libraries**:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `lmfit`
  - `tkinter` (usually included with Python)


### Running the Program

1. **Prepare Data**:
   - Ensure you have an Excel file with the required experimental data.
   - for each dataset, first collumn represents the time in hours and the second column represents the creep modulus. the program automatically convers the data to time in seconds and creep strain.

2. **Run the GUI**:
   - Execute the GUI script (`mainProg.py`) to open the Tkinter application.

3. **Use the GUI**:
   - Select the Excel file containing the data.
   - Enter the stress values as comma-separated lists. (e.g.: 5,10,15,5,10,5,10 for a 4 datasets at temperature1, 2 at temperature2 and 2 at temperature3).
   - Enter the temperature values as comma-separated lists. (e.g.: 23,23,23,23,40,40,60,60 for a 4 datasets at temperature1, 2 at temperature2 and 2 at temperature3)
   - Choose the calibration model (LMFit or Curve_fit).
   - Click "Process" to perform calibration and display results.
   - Optionally, save the plot using the "Save Image" button.

4. **Analyze Results**:
   - View the calibrated parameters and the fitted model plot.
   - Use the saved plot for further analysis or reporting.

## Troubleshooting

- **Excel File Issues**:
  - Ensure the Excel file has no headers or extra formatting that could interfere with reading data.
