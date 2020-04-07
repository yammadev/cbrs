# Import
import numpy as np
import pandas as pd
from scipy.spatial import distance

# Main
def main():
    # [1] Get the input .csv library and problem cases
    # {pandas.DataFrame}
    library, cases = pd.read_csv('input/library.csv'), pd.read_csv('input/cases.csv')

    # Print
    print('\n> Library & Problem cases')
    print(f'\n{library}')
    print(f'\n{cases}')

    # Select columns from library to use as base cases, except solutions
    base = library.iloc[:, range(library.shape[1] - 1)]      # Exclude last column

    # Print
    # print('\n> Base')
    # print(f'\n{base}')

    # [2] One-hot encoding
    base = pd.get_dummies(base)
    problems = pd.get_dummies(cases)

    # Print
    print('\n> One-hot encoding')
    print(f'\n{base}')
    print(f'\n{problems}\n')

    # [3] Calculate
    # [3.1] Get inverse covariance matrix for the base cases
    covariance_matrix = base.cov()                                      # Covariance
    inverse_covariance_matrix = np.linalg.pinv(covariance_matrix)       # Inverse

    # [3.2] Move through all problem cases
    for i in range(problems.shape[0]):
        # Get case row to evaluate
        case_row = problems.loc[i, :]

        # Empty distances array to store mahalanobis distances obtained comparing each library cases
        distances = np.zeros(base.shape[0])

        # For each base cases (library) rows
        for j in range(base.shape[0]):
            # Get base case row
            base_row = base.loc[j, :]

            # [3.3] Calculate mahalanobis distance between case row and base cases, and store it
            distances[j] = distance.mahalanobis(case_row, base_row, inverse_covariance_matrix)

        # [3.4] Returns the index (row) of the minimum value in distances
        min_distance_row = np.argmin(distances)

        # [3.5] Get solution based on index of found minimun distance, and append it to main library
        # From cases, append library similar solution
        case = np.append(cases.iloc[i, :], library.iloc[min_distance_row, -1])

        # Print
        print(f'> For case/problem {i}: {cases.iloc[i, :].to_numpy()}, solution is {case[-1]}')

        # [4] Store
        # Get as operable pandas Series
        case = pd.Series(case, index = library.columns)         # Case + Sol
        library = library.append(case, ignore_index = True)     # Append

    # [4.1] Output
    print('\n> Output library')
    print(f'\n{library}')

# Call
if __name__ == '__main__':
    main()
