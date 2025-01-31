from bnetbase import Variable, Factor, BN
import csv
import itertools
import time


def normalize(factor: Factor) -> Factor:
    '''
    Normalize the factor such that its values sum to 1.
    Do not modify the input factor.

    :param factor: a Factor object. 
    :return: a new Factor object resulting from normalizing factor.
    '''
    # Step 1: Create a new factor with the same scope
    new_factor = Factor(f"{factor.name}_normalized", factor.get_scope())

    # Step 2: Calculate the total sum of the factor's values
    total_sum = sum(factor.values)

    # Step 3: Prepare variables and their domains
    variables = factor.get_scope()
    domains = [var.domain() for var in variables]

    # Step 4: Save current assignments
    saved_assignments = [var.get_assignment_index() for var in variables]

    # Step 5: Iterate over all possible assignments
    for assignment in itertools.product(*domains):
        # Set variable assignments
        for var, value in zip(variables, assignment):
            var.set_assignment(value)

        # Retrieve the original value
        original_value = factor.get_value_at_current_assignments()

        # Compute the normalized value
        if total_sum != 0:
            normalized_value = original_value / total_sum
        else:
            normalized_value = 0  # Handle zero total sum appropriately

        # Set the normalized value in the new factor
        new_factor.add_value_at_current_assignment(normalized_value)

    # Step 6: Restore original assignments
    for var, index in zip(variables, saved_assignments):
        var.set_assignment_index(index)

    return new_factor


def restrict(factor: Factor, variable: Variable, value: str) -> Factor:
    '''
    Restrict a factor by assigning value to variable.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to restrict.
    :param value: the value to restrict the variable to
    :return: a new Factor object resulting from restricting variable to value.
             This new factor no longer has variable in it.

    '''
    # Step 1: Identify the new scope (exclude the restricted variable)
    new_scope = [var for var in factor.get_scope() if var != variable]

    # Step 2: Create a new factor with the new scope
    new_factor = Factor(f"{factor.name}_restricted_{variable.name}_{value}", new_scope)

    # Step 3: Prepare variables and their domains
    variables = factor.get_scope()
    domains = [var.domain() for var in variables]

    # Step 4: Save current assignments
    saved_assignments = [var.get_assignment_index() for var in variables]

    # Step 5: Iterate over all possible assignments
    for assignment in itertools.product(*domains):
        # Create a mapping of variables to their assigned values
        assignment_dict = dict(zip(variables, assignment))

        # Check if the variable has the specified value
        if assignment_dict[variable] == value:
            # Set assignments for all variables
            for var, val in assignment_dict.items():
                var.set_assignment(val)

            # Retrieve the value from the original factor
            original_value = factor.get_value_at_current_assignments()

            # Set assignments in the new factor (excluding the restricted variable)
            for var in new_scope:
                var.set_assignment(assignment_dict[var])

            # Add the value to the new factor
            new_factor.add_value_at_current_assignment(original_value)

    # Step 6: Restore original assignments
    for var, index in zip(variables, saved_assignments):
        var.set_assignment_index(index)

    return new_factor

def sum_out(factor: Factor, variable: Variable) -> Factor:
    '''
    Sum out a variable variable from factor factor.
    Do not modify the input factor.

    :param factor: a Factor object.
    :param variable: the variable to sum out.
    :return: a new Factor object resulting from summing out variable from the factor.
             This new factor no longer has variable in it.
    '''
    # Step 1: Identify the new scope (exclude the summed-out variable)
    new_scope = [var for var in factor.get_scope() if var != variable]
    new_factor = Factor(f"{factor.name}_sumout_{variable.name}", new_scope)

    # Step 2: Prepare variables and domains
    new_vars = new_factor.get_scope()
    new_domains = [var.domain() for var in new_vars]
    sumout_domain = variable.domain()

    # Step 3: Save current assignments
    all_vars = factor.get_scope()
    saved_assignments = [var.get_assignment_index() for var in all_vars]

    # Step 4: Iterate over all possible assignments of the new scope
    for assignment in itertools.product(*new_domains):
        total = 0  # Initialize sum accumulator

        # Map variables to their assigned values
        assignment_dict = dict(zip(new_vars, assignment))

        # For each value of the summed-out variable
        for sumout_val in sumout_domain:
            # Build full assignment including the summed-out variable
            full_assignment = assignment_dict.copy()
            full_assignment[variable] = sumout_val

            # Set variable assignments
            for var, assigned_value in full_assignment.items():
                var.set_assignment(assigned_value)

            # Retrieve the original value
            original_value = factor.get_value_at_current_assignments()

            # Accumulate the sum
            total += original_value

        # Set assignments for new factor (only variables in new scope)
        for var, assigned_value in assignment_dict.items():
            var.set_assignment(assigned_value)

        # Assign the accumulated sum to the new factor
        new_factor.add_value_at_current_assignment(total)

    # Step 5: Restore original assignments
    for var, index in zip(all_vars, saved_assignments):
        var.set_assignment_index(index)

    return new_factor

def multiply(factor_list):
    '''
    Multiply a list of factors together.
    Do not modify any of the input factors. 

    :param factor_list: a list of Factor objects.
    :return: a new Factor object resulting from multiplying all the factors in factor_list.
    '''
    # Collect variables from all factors while preserving order
    new_scope_vars = []
    for factor in factor_list:
        for var in factor.get_scope():
            if var not in new_scope_vars:
                new_scope_vars.append(var)

    # Create the new factor
    new_factor = Factor("ProductFactor", new_scope_vars)
    domains = [var.domain() for var in new_scope_vars]
    saved_assignments = {var: var.get_assignment_index() for var in new_scope_vars}

    # Iterate over all possible assignments
    for assignment in itertools.product(*domains):
        # Map variables to their assigned values
        assignment_dict = dict(zip(new_scope_vars, assignment))

        # Set variable assignments
        for var, value in assignment_dict.items():
            var.set_assignment(value)

        # Initialize product accumulator
        product = 1.0

        # Multiply values from each factor
        for factor in factor_list:
            # Retrieve value from the factor
            factor_value = factor.get_value_at_current_assignments()
            product *= factor_value

        # Add the product to the new factor
        new_factor.add_value_at_current_assignment(product)

    # Restore original variable assignments
    for var, index in saved_assignments.items():
        var.set_assignment_index(index)

    return new_factor

def ve(bayes_net, var_query, EvidenceVars):
    '''

    Execute the variable elimination algorithm on the Bayesian network bayes_net
    to compute a distribution over the values of var_query given the 
    evidence provided by EvidenceVars. 

    :param bayes_net: a BN object.
    :param var_query: the query variable. we want to compute a distribution
                     over the values of the query variable.
    :param EvidenceVars: the evidence variables. Each evidence variable has 
                         its evidence set to a value from its domain 
                         using set_evidence.
    :return: a Factor object representing a distribution over the values
             of var_query. that is a list of numbers, one for every value
             in var_query's domain. These numbers sum to 1. The i-th number
             is the probability that var_query is equal to its i-th value given 
             the settings of the evidence variables.

    For example, assume that
        var_query = A with Dom[A] = ['a', 'b', 'c'], 
        EvidenceVars = [B, C], and 
        we have called B.set_evidence(1) and C.set_evidence('c'), 
    then VE would return a list of three numbers, e.g. [0.5, 0.24, 0.26]. 
    These numbers would mean that 
        Pr(A='a'|B=1, C='c') = 0.5, 
        Pr(A='a'|B=1, C='c') = 0.24, and 
        Pr(A='a'|B=1, C='c') = 0.26.

    '''
    # Step 1: Restrict factors based on the evidence
    restricted_factors = []
    for factor in bayes_net.factors():
        new_factor = factor  # Start with the original factor
        for evidence in EvidenceVars:
            if evidence in new_factor.get_scope():
                new_factor = restrict(new_factor, evidence, evidence.get_evidence())
        restricted_factors.append(new_factor)

    # Step 2: Eliminate all variables except the query variable
    remaining_factors = restricted_factors[:]
    variables_to_eliminate = [v for v in bayes_net.variables() if v != var_query and v not in EvidenceVars]
    for variable in variables_to_eliminate:
        # Find all factors involving the variable
        factors_to_multiply = [f for f in remaining_factors if variable in f.get_scope()]
        # Remove these factors from the remaining factors list
        remaining_factors = [f for f in remaining_factors if f not in factors_to_multiply]
        if factors_to_multiply:
            # Multiply all the factors involving the variable
            product_factor = multiply(factors_to_multiply)
            # Sum out the variable
            summed_out_factor = sum_out(product_factor, variable)
            # Add the resulting factor back to the list
            remaining_factors.append(summed_out_factor)

    # Step 3: Multiply all remaining factors
    if remaining_factors:
        final_factor = multiply(remaining_factors)
    else:
        # If there are no remaining factors, create a uniform factor over var_query
        final_factor = Factor(f"Uniform_{var_query.name}", [var_query])
        uniform_value = 1.0 / var_query.domain_size()
        for value in var_query.domain():
            var_query.set_assignment(value)
            final_factor.add_value_at_current_assignment(uniform_value)

    # Step 4: Normalize the resulting factor
    total = sum(final_factor.values)
    if total == 0:
        print("Warning: Sum of final factor values is zero. Returning uniform probabilities.")
        normalized_factor = Factor(f"Normalized_{var_query.name}", [var_query])
        uniform_value = 1.0 / var_query.domain_size()
        for value in var_query.domain():
            var_query.set_assignment(value)
            normalized_factor.add_value_at_current_assignment(uniform_value)
    else:
        normalized_factor = normalize(final_factor)

    # Ensure the factor's scope is [var_query]
    if normalized_factor.get_scope() != [var_query]:
        # Sum out any remaining variables except var_query
        variables_in_factor = normalized_factor.get_scope()
        variables_to_eliminate = [v for v in variables_in_factor if v != var_query]
        for variable in variables_to_eliminate:
            normalized_factor = sum_out(normalized_factor, variable)

    return normalized_factor


def naive_bayes_model(data_file, variable_domains = {"Work": ['Not Working', 'Government', 'Private', 'Self-emp'], "Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'], "Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'], "MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'], "Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'], "Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'], "Gender": ['Male', 'Female'], "Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'], "Salary": ['<50K', '>=50K']}, class_var = Variable("Salary", ['<50K', '>=50K'])):
    '''
   NaiveBayesModel returns a BN that is a Naive Bayes model that 
   represents the joint distribution of value assignments to 
   variables in the Adult Dataset from UCI.  Remember a Naive Bayes model
   assumes P(X1, X2,.... XN, Class) can be represented as 
   P(X1|Class)*P(X2|Class)* .... *P(XN|Class)*P(Class).
   When you generated your Bayes bayes_net, assume that the values 
   in the SALARY column of the dataset are the CLASS that we want to predict.
   @return a BN that is a Naive Bayes model and which represents the Adult Dataset. 
    '''
    ### READ IN THE DATA
    input_data = []
    with open(data_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None) #skip header row
        for row in reader:
            input_data.append(row)

    ### DOMAIN INFORMATION REFLECTS ORDER OF COLUMNS IN THE DATA SET
    #variable_domains = {
    #"Work": ['Not Working', 'Government', 'Private', 'Self-emp'],
    #"Education": ['<Gr12', 'HS-Graduate', 'Associate', 'Professional', 'Bachelors', 'Masters', 'Doctorate'],
    #"Occupation": ['Admin', 'Military', 'Manual Labour', 'Office Labour', 'Service', 'Professional'],
    #"MaritalStatus": ['Not-Married', 'Married', 'Separated', 'Widowed'],
    #"Relationship": ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    #"Race": ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'],
    #"Gender": ['Male', 'Female'],
    #"Country": ['North-America', 'South-America', 'Europe', 'Asia', 'Middle-East', 'Carribean'],
    #"Salary": ['<50K', '>=50K']
    #}
        ### READ IN THE DATA
        input_data = []
        with open(data_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader, None)  # Skip header row
            for row in reader:
                input_data.append(row)

        ### Initialize Variables for Each Attribute
        variables = {}
        for var_name, domain in variable_domains.items():
            variables[var_name] = Variable(var_name, domain)

        ### Initialize Factors for Each Variable, Conditioning on Salary
        factors = []

        # Factor for Salary (Prior Probability)
        salary_counts = {value: 0 for value in variables['Salary'].domain()}
        for row in input_data:
            salary_value = row[-1]  # Assuming Salary is the last column
            salary_counts[salary_value] += 1
        total_count = len(input_data)
        salary_factor = Factor("P(Salary)", [variables['Salary']])
        factor_values = []
        for salary_value in variables['Salary'].domain():
            probability = salary_counts[salary_value] / total_count
            factor_values.append([salary_value, probability])
        salary_factor.add_values(factor_values)
        factors.append(salary_factor)

        # Factors for other attributes, conditioning on Salary
        for attribute in headers[:-1]:  # Exclude 'Salary'
            attribute_counts = {}
            for salary_value in variables['Salary'].domain():
                attribute_counts[salary_value] = {attr_value: 0 for attr_value in variables[attribute].domain()}

            for row in input_data:
                salary_value = row[-1]
                attribute_value = row[headers.index(attribute)]
                attribute_counts[salary_value][attribute_value] += 1

            attribute_factor = Factor(f"P({attribute}|Salary)", [variables[attribute], variables['Salary']])
            factor_values = []
            for attribute_value in variables[attribute].domain():
                for salary_value in variables['Salary'].domain():
                    count = attribute_counts[salary_value][attribute_value]
                    salary_total = salary_counts[salary_value]
                    if salary_total > 0:
                        probability = count / salary_total
                    else:
                        probability = 0.0  # Handle division by zero
                    factor_values.append([attribute_value, salary_value, probability])
            attribute_factor.add_values(factor_values)
            factors.append(attribute_factor)

        ### Create the Bayesian Network
        bayes_net = BN("NaiveBayesAdultDataset", list(variables.values()), factors)

        return bayes_net


def explore(bayes_net, question):
    '''
    Input: bayes_net --- a BN object (a Bayesian Network)
           question --- an integer indicating the question to be calculated. Options are:
               1. What percentage of the women in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
               2. What percentage of the men in the data set end up with a P(S=">=$50K"|E1) that is strictly greater than P(S=">=$50K"|E2)?
               3. What percentage of the women in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
               4. What percentage of the men in the data set with P(S=">=$50K"|E1) > 0.5 actually have a salary over $50K?
               5. What percentage of the women in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
               6. What percentage of the men in the data set are assigned a P(Salary=">=$50K"|E1) > 0.5, overall?
           @return a percentage (between 0 and 100)
    '''
    # Load the test dataset (adult-test.csv)
    input_data = []
    with open('data/adult-test.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader, None)  # Skip the header row
        for row in reader:
            input_data.append(row)

    # Map header names to indices for easy access
    header_indices = {header: index for index, header in enumerate(headers)}

    # Define core evidence set E1 (Work, Occupation, Education, Relationship Status)
    core_evidence_vars = ['Work', 'Occupation', 'Education', 'Relationship']
    extended_evidence_vars = core_evidence_vars + ['Gender']

    # Create a variable dictionary for quick access
    variables = {var.name: var for var in bayes_net.variables()}

    # Initialize counts
    count = 0
    total = 0

    # Lists to store results for questions 3 and 4
    women_predicted_over_50k = []
    men_predicted_over_50k = []

    for row in input_data:
        # Extract data for the current individual
        data_point = {header: row[header_indices[header]] for header in headers}
        gender = data_point['Gender']
        salary = data_point['Salary']

        # Reset evidence for all variables before setting new evidence
        for var in variables.values():
            var.evidence_index = None  # Unset evidence

        # Set up evidence for E1
        for var_name in core_evidence_vars:
            var_value = data_point[var_name]
            variables[var_name].set_evidence(var_value)

        # Query variable
        salary_var = variables['Salary']
        salary_var.evidence_index = None  # Ensure no evidence is set on the query variable

        # Evidence variables for E1
        evidence_vars_E1 = [variables[var_name] for var_name in core_evidence_vars]

        # Compute P(Salary >= $50K | E1)
        factor_E1 = ve(bayes_net, salary_var, evidence_vars_E1)
        index_GE50K = salary_var.domain().index('>=50K')
        prob_GE50K_E1 = factor_E1.values[index_GE50K]

        # Set up evidence for E2
        for var_name in extended_evidence_vars:
            var_value = data_point[var_name]
            variables[var_name].set_evidence(var_value)

        # Evidence variables for E2
        evidence_vars_E2 = [variables[var_name] for var_name in extended_evidence_vars]

        # Compute P(Salary >= $50K | E2)
        factor_E2 = ve(bayes_net, salary_var, evidence_vars_E2)
        prob_GE50K_E2 = factor_E2.values[index_GE50K]

        # Reset evidence for all variables before next iteration
        for var in variables.values():
            var.evidence_index = None  # Unset evidence

        # Process based on the question
        if question == 1 and gender == 'Female':
            # Q1: Women where P(Salary >= $50K | E1) > P(Salary >= $50K | E2)
            if prob_GE50K_E1 > prob_GE50K_E2:
                count += 1
            total += 1

        elif question == 2 and gender == 'Male':
            # Q2: Men where P(Salary >= $50K | E1) > P(Salary >= $50K | E2)
            if prob_GE50K_E1 > prob_GE50K_E2:
                count += 1
            total += 1

        elif question == 3 and gender == 'Female':
            # Q3: Women with P(Salary >= $50K | E1) > 0.5 who actually earn >= $50K
            if prob_GE50K_E1 > 0.5:
                total += 1
                if salary == '>=50K':
                    count += 1

        elif question == 4 and gender == 'Male':
            # Q4: Men with P(Salary >= $50K | E1) > 0.5 who actually earn >= $50K
            if prob_GE50K_E1 > 0.5:
                total += 1
                if salary == '>=50K':
                    count += 1

        elif question == 5 and gender == 'Female':
            # Q5: Percentage of women assigned P(Salary >= $50K | E1) > 0.5
            if prob_GE50K_E1 > 0.5:
                count += 1
            total += 1

        elif question == 6 and gender == 'Male':
            # Q6: Percentage of men assigned P(Salary >= $50K | E1) > 0.5
            if prob_GE50K_E1 > 0.5:
                count += 1
            total += 1

    # Calculate the percentage
    if total == 0:
        percentage = 0  # Avoid division by zero
    else:
        percentage = (count / total) * 100

    return percentage


if __name__ == '__main__':
    nb = naive_bayes_model('data/adult-train.csv')
    for i in range(1,7):
        print("explore(nb,{}) = {}".format(i, explore(nb, i)))