# Calculates information
import math
import os
import csv
import pandas as pd


def instructions():
    inst1 = '''
    This program collects categorical data and calculates the information
    needed and gained for each category. This can be used to determine
    the effectiveness of each split in a tree.  
    The information can either be entered manually, or read in from a 
    CSV file.

    CSV ENTERED DATA:
    =================
    This uses the program directory, which is provided when you choose to 
    read in a csv file. Copy the CSV file to that directory or folder.
    Type in the name of the file (i.e. abc.csv) to read the file. 
    The results will then be displayed.

    MANUALLY ENTERED DATA:
    ======================
    You will first need to enter the names of each category (column).
    After entering in the last column name, type "done" on the
    next line.  This program accepts up to 20 categories.
    '''
    inst2 = '''
    After designating the columns, you enter the data for each column.
    For faster entry, type in the minimum number of characters needed
    to represent the category, then press Enter.  For example, if the 
    categories are "<15", "15 to 30", ">30", you could use "l", "m", "g"
    for "Less", "Middle", "Greater" to represent the categories.

    If you make a mistake, typing "-" and pressing Enter will step back 
    to the last entry. Type "Done" when finished with the first category. 
    This program accepts up to 100 records.

    The results will print out after the last data is entered.
    '''

    print(inst1)
    z = input("(Press Enter to Continue)")
    print(inst2)
    z = input("(Press Enter to Continue)")


def menu():
    menu_text = '''
    Small Data Set Information Calculator
    =====================================

    Main Menu
    =========
    1) Instructions
    2) Enter Data
    3) Get Data from CSV
    4) Exit

    Please enter an option 1-4 :'''

    menu_opt = input(menu_text)
    return menu_opt


def get_filename():
    '''
    Looks up app path, gets file name, and appends the name to the path
    Returns the full path.

    INPUT:   None
    RETURNS: Full Path string
    '''
    app_path = os.getcwd()
    print(f"Copy the csv file to this programs folder:\n{app_path}")
    print()
    filename = input("Type in the csv filename here (i.e. xyz.csv): ")
    fullpath = app_path + os.sep + filename
    return fullpath


def get_from_csv(file: str):
    '''
    Reads csv file into pandas dataframe
    Extracts column titles and column data

    INPUT:   Full path file name
    RETURNS: List of lists containing column names and data.
    '''

    all_data = []
    data_container = []
    info_df = pd.read_csv(file)

    columns = list(info_df.columns)
    all_data.append(columns)
    for item in columns:
        data_list = list(info_df[item])
        data_container.append(data_list)
    all_data.append(data_container)
    return all_data


def get_manual_columns():
    '''
    Gathers the names of the columns from the user.

    INPUT:   None
    RETURNS: List of column names
    '''

    columns = []
    finished = False
    col_count = 0
    while not finished:
        col_count += 1
        col_name = input(f"What is the name of column #{col_count}: ")
        if col_name.lower() == "done" or col_count > 19:
            finished = True
        else:
            columns.append(col_name)
    return columns


def get_manual_data(column_list: list):
    '''
    Gathers column data for each column from user.

    INPUT:   List of column names
    RETURNS: List of lists of column data.
    '''
    all_lists = []
    data_len = 0
    print()

    for column in column_list:
        this_list = []
        finished = False
        data_count = 0
        print()
        print(f"Data for {column}:")
        print("="*(len(column)+10))

        while not finished:
            data_count += 1

            if data_count == data_len:
                print(f"(ENTER if done, '-' if error)", end="")
            else:
                print(f"#{data_count}: ", end="")
            value = input()
            if value.lower() == "done":
                finished = True
                data_len = data_count
            elif value == "-":
                print("oops - ", end="")
                this_list.pop()
                data_count -= 2
            elif len(value) < 1:
                pass  # make sure that null is not appended to list.
            else:
                this_list.append(value)

            if data_count == 100 or data_count == data_len:
                finished = True

        all_lists.append(this_list)
    return all_lists


def tabulate_data(data: list):
    '''
    Determines if each category entry within each
    column corresponds to a positive or negative result
    within the last column.

    Tallies the number of positive and negative
    results for each category in each column.

    INPUT:   All data
    RETURNS: List of dictionaries with tally results.
    '''
    tabulated_data = []
    pos_results = []
    neg_results = []

    # Get binary counts of category column
    # Assumed to be last column
    cat_len = len(data)
    cat_list = data[cat_len-1]
    cat_tally = dict()
    for item in cat_list:
        if item in cat_tally:
            cat_tally[item] += 1
        else:
            cat_tally[item] = 1

    # Extract the two categories from dictionary
    categories = list(cat_tally.keys())
    if len(categories) == 1:
        categories.append("not "+categories[0])
    if len(categories) > 2:
        return tabulated_data

    # Loop through remaining columns
    for index in range(cat_len):
        pos_counts = dict()
        neg_counts = dict()

        # Loop through rows of each column
        for row, item in enumerate(data[index]):
            # Make sure we have a listing for each item
            # in both dictionaries
            if item not in pos_counts:
                pos_counts[item] = 0
            if item not in neg_counts:
                neg_counts[item] = 0

            # Determine if row item corresponds to positive or negative category.
            if cat_list[row] == categories[0]:
                pos_counts[item] += 1
            else:
                neg_counts[item] += 1

        # Tabulate results
        pos_results.append(pos_counts)
        neg_results.append(neg_counts)
    tabulated_data.append(pos_results)
    tabulated_data.append(neg_results)

    return tabulated_data


def expected_info(pos: int, neg: int):
    '''
    Calculate the expected information based on the
    number of positive and negative categorizations.

    INPUT:   Positive and negative categorization counts.
    RETURNS: Expected Information value as decimal.
    '''
    total = pos + neg
    pp = pos/total
    np = neg/total
    if pp == 0 and np == 0:
        ei = 0
    elif pp > 0 and np == 0:
        ei = -pp*math.log2(pp)
    elif pp == 0 and np > 0:
        ei = -np*math.log2(np)
    else:
        ei = -(pp*math.log2(pp))-(np*math.log2(np))

    return ei


def calculate_information(tab_data: list, col_names: list):
    '''
    Calculates expected, needed, and gaine information from
    tabulated data for all columns.

    INPUT:   Tabulated data as list of dictionaries, names of columns.
    RETURNS: List of expected info decimal, needed info list, gained info list.
    '''
    ei = 0
    needed_info = dict()
    gained_info = dict()
    positive_results = tab_data[0]
    negative_results = tab_data[1]
    col_count = len(positive_results)

    # Total number of records
    total = 0
    for cat in positive_results[0]:
        total += positive_results[0][cat]
        total += negative_results[0][cat]

    # Expected Info = -P/T*(log_2(P/T))-N/T*(log_2(n/t))
    # Needed Info = Cat1/T*(EI(Cat1P,Cat1N))+...
    # Gained Info = EI-Info(Cat1)

    # Loop over all columns
    for index in range(col_count-1):
        # extract pos and neg dictionaries
        pos_vals = positive_results[index]
        neg_vals = negative_results[index]
        col_info_needed = 0
        for cat in pos_vals.keys():
            cat_tot = pos_vals[cat] + neg_vals[cat]
            col_info_needed += (cat_tot/total) * \
                expected_info(pos_vals[cat], neg_vals[cat])
        needed_info[columns[index]] = col_info_needed

    # Expected Info
    pos_vals = positive_results[col_count-1]
    neg_vals = negative_results[col_count-1]
    categories = list(pos_vals.keys())
    if len(categories) == 1:
        categories.append("not "+categories[0])
        neg_vals[categories[1]] = 0
    pos_num = pos_vals[categories[0]]
    neg_num = neg_vals[categories[1]]
    ei = expected_info(pos_num, neg_num)

    # Information Gained
    for col in needed_info.keys():
        gained_info[col] = ei-needed_info[col]

    return [ei, needed_info, gained_info]


def print_counted_data(counted_data: list, col_names: list):
    # Utility routine
    pos_results = counted_data[0]
    neg_results = counted_data[1]

    for index in range(len(pos_results)):
        print(f"{col_names[index]}: ")
        pcd = pos_results[index]
        ncd = neg_results[index]
        for key in pcd.keys():
            print(f"{key}: {pcd[key]}, {ncd[key]}")

        print()


def print_data(columns: list, data: list):
    # Utility routine
    for col_index, column in enumerate(columns):
        print()
        print(f"{column}")
        print("="*(len(column)))
        data_list = data[col_index]
        for item in data_list:
            print(item)


def print_summary(columns: list, summary: list):
    '''
    Summary of Results

    Input:   List of columns, list of summary data.
    Returns: None - output printed to screen.
    '''
    exp_info = summary[0]
    needed_info_d = summary[1]
    gained_info_d = summary[2]
    print()
    print(f"Expected Info: {round(exp_info,3)}")

    col_num = len(columns)
    for index in range(col_num-1):
        print()
        print(f"{columns[index]}")
        print("="*len(columns[index]))
        print(f"Needed Info: {round(needed_info_d[columns[index]],3)}")
        print(f"Gained Info: {round(gained_info_d[columns[index]],3)}")


#############################
keep_running = True
while keep_running:
    keep_asking = True
    while keep_asking:
        opt = menu()
        if opt in ("1", "2", "3", "4"):
            keep_asking = False
    if opt == "1":
        instructions()
    elif opt == "2":
        columns = get_manual_columns()
        data = get_manual_data(columns)
        counted_data = tabulate_data(data)
        result_data = calculate_information(counted_data, columns)
        print_summary(columns, result_data)
    elif opt == "3":
        filename = get_filename()
        all_data = get_from_csv(filename)
        columns = all_data[0]
        data = all_data[1]
        counted_data = tabulate_data(data)
        result_data = calculate_information(counted_data, columns)
        print_summary(columns, result_data)
    else:
        keep_running = False
