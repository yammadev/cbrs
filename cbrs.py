# Import
import numpy as np
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sn

# Main
def main():
    # [1] Get the input .csv library and problem cases
    # {pandas.DataFrame}
    library, cases = pd.read_csv('input/library.csv'), pd.read_csv('input/cases.csv')

    # Print
    print('\n> Initial Library')
    print(f'\n{library}')
    # print(f'\n{cases}')

    # Select columns from library to use as base cases, except solutions
    base = library.iloc[:, range(library.shape[1] - 1)]      # Exclude last column (solution)

    # Print
    # print('\n> Base')
    # print(f'\n{base}')

    # [2] Initial One-hot encoding
    base = pd.get_dummies(base)
    problems = pd.get_dummies(cases)

    # Print
    # print('\n> One-hot encoding')
    # print(f'\n{base}')
    # print(f'\n{problems}\n')

    # [3] Calculate
    # Print
    print('\n> Calculating\n')

    # Move through all problem cases
    for i in range(problems.shape[0]):
        # Print
        # print(f'\n{base} for problem {i}')

        # [3.1] Get inverse covariance matrix for the base cases
        covariance_matrix = base.cov()                                      # Covariance
        inverse_covariance_matrix = np.linalg.pinv(covariance_matrix)       # Inverse

        # [3.2] Get case row to evaluate
        case_row = problems.loc[i, :]

        # Empty distances array to store mahalanobis distances obtained comparing each library cases
        distances = np.zeros(base.shape[0])

        # [3.3] For each base cases rows
        for j in range(base.shape[0]):
            # Get base case row
            base_row = base.loc[j, :]

            # [3.4] Calculate mahalanobis distance between case row and base cases, and store it
            distances[j] = distance.mahalanobis(case_row, base_row, inverse_covariance_matrix)

        # [3.5] Returns the index (row) of the minimum value in distances calculated
        min_distance_row = np.argmin(distances)

        # [4] Get solution based on index of found minimum distance, and append it to main library
        # From cases, append library 'similar' solution
        case = np.append(cases.iloc[i, :], library.iloc[min_distance_row, -1])

        # Print
        print(f'> For case/problem {i}: {cases.iloc[i, :].to_numpy()}, solution is {case[-1]}')

        # [5] Store
        # Get as operable pandas Series
        case = pd.Series(case, index = library.columns)         # Case with Solution
        library = library.append(case, ignore_index = True)     # Append to library

        # Save 'covariance heat map (biased)' output as file
        sn.heatmap(np.cov(base, bias = True), annot = True, fmt = 'g')
        plt.gcf().set_size_inches(12, 6)
        plt.title(f'Covariance Heat map #{i} \n Library cases stored {j} - Base to solve problem {i}')
        plt.savefig(f'output/covariance_heat_map_{i}.png', bbox_inches='tight')
        plt.close()

        # [6] Reuse
        base = library.iloc[:, range(library.shape[1] - 1)]     # Exclude last column (solution)
        base = pd.get_dummies(base)                             # Get new one-hot encoded base

    # [7] Output
    print('\n> Output library')
    print(f'\n{library}')

    # Save 'library' output as file
    library.to_csv('output/library.csv', index = False)

# Call
if __name__ == '__main__':
    main()
