import math
import re


def get_name():
    '''
    Requests the users name for personalization

    INPUT:   Manual input of users name.
    RETURNS: Capitalized String value of name.
    '''

    print()
    asking = True
    name = ""
    while asking:
        print("Hi, my name is GUMP-9000.")
        name = input("What is your first name? ")
        nm_re = re.compile("\w+")
        match_obj = nm_re.match(name)
        if match_obj != None:
            name = name.lower()
            name = name.capitalize()

            asking = False
        else:
            print("*** My mother programmed me not to work with strangers.")
            print()
    return name


def show_menu(name: str, state: int):
    '''
    Displays personalized options menu.
    Options dependent of program state.
    State = 1 - needs list data
    State = 2 - has list data

    INPUT:   Users Name, Program State, Manually chosen option.
    RETURNS: String of option number chosen.
    '''

    asking = True
    value = ""
    while asking:
        menu_title = name + "'s Menu"
        input_string = ""
        print()
        print(f"Hello {name}. Here are your options.")
        print()
        print(menu_title)
        print("="*len(menu_title))
        print("0) Quit.")
        print("1) Enter a set of lists.")
        if state > 1:
            print("2) Calculate Support, Confidence, and Lift for rules.")
            print("3) Determine frequent lists of items.")
            input_string = "Please enter a number from 0 to 3: "
        else:
            input_string = "Please select either 0 or 1: "

        print()
        value = input(input_string)
        if value == "1" or value == "0":
            asking = False
        elif state > 1 and len(value) == 1 and value in "23":
            asking = False
        else:
            print(f"*** I'm sorry, {name}. That is not a valid option.")

    return value


def get_all_lists(name: str):
    '''
    Accepts manually input list data.

    INPUT:  Manually entered list data.
    OUTPUT: List of lists containing data.
    '''

    instr = '''
    - Enter all lists, with individual items seperated by a comma.
    (i.e. a,b,c,d)
    - If you make a mistake, type "-" to retype the previous list.
    - When you are finished, type "Done" to stop.
    - Spaces between items and capitalization is ignored 
    (i.e. bread,milk = Bread, Milk)

    '''

    all_lists = []
    print()
    print(instr)
    more_lists = True
    list_count = 0

    while more_lists:
        list_count += 1
        list_items = input(f"List #{list_count}:")
        if list_items == "-":
            print(f"*** I'll let you retype that, {name}.")
            all_lists.pop()
            list_count -= 2
        elif list_items.lower() == "done":
            print(f"*** You did a good job entering your lists, {name}.")
            more_lists = False
        else:
            this_list = list_items.split(",")
            all_lists.append(this_list)

    return all_lists


def get_rule(name: str):
    '''
    Accepts manually entered rules from user.
    Validates rule syntax.

    INPUT:   Manually entered rule.
    RETURNS: List of left and right sides of rule.
    '''
    rule = ""
    re_word = re.compile("\w+")
    arrow = "->"

    asking = True
    while asking:
        print()
        print("Enter your rule in the format 'a,b -> x,y'")
        print("Sets may include 1 or more items.")
        print()
        rule = input("Please type your rule here: ")
        if arrow in rule:
            apos = rule.index(arrow)
            left_side = rule[0:apos].strip()
            right_side = rule[apos+2:len(rule)].strip()
            lmatch = ("match" in str(re_word.match(left_side)))
            rmatch = ("match" in str(re_word.match(right_side)))
            is_valid = lmatch and rmatch
            if apos > 0 and is_valid:
                # downstream formatting
                left_list = str(left_side).split(",")
                right_list = str(right_side).split(",")
                rule = [left_list, right_list]
                asking = False
            else:
                print(
                    f"*** I'm sorry {name}, but I cannot process the rule without both sides.")
        else:
            print(
                f"*** I'm sorry {name}, I cannot process your rule without an arrow ' -> '.")

    return rule


def get_frequency(name: str):
    '''
    Request the desired frequency from the user

    INPUT:   Manual input of integer
    RETURNS: Integer value
    '''
    freq_num = 0
    print()
    asking = True
    while asking:
        freq = input("What is the desired frequency (whole number only)? ")
        fr_re = re.compile("\d+")
        match_obj = fr_re.match(freq)
        if match_obj != None:
            freq_num = int(freq)
            asking = False
        else:
            print(f"*** I'm sorry, {name}, but that is not a whole number. ")
            # print()
    return freq_num


def generate_singles(all_lists: list):
    '''
       Breaks longer lists into single itemed lists.
       Used for frequent list calculation

       INPUT:   All lists entered by user
       RETURNS: List of single value lists containing unique items.
    '''

    item_set = set()
    # use set to find unique values easily
    for this_list in all_lists:
        for item in this_list:
            item = item.lower().strip()
            item_set.add(item)

        # reprocessing for downstream
        # re-format into list of lists.
        all_items = []
        for item in item_set:
            all_items.append([item])
        all_items.sort()

        return all_items


def build_candidates(items: list):
    '''
    Combines list of items into longer lists.

    INPUT:   List of items for combining.
    RETURNS: List of combined items.
    '''
    candidates = []
    for sample in range(0, len(items)-1):
        for test in range(sample+1, len(items)):
            # Singles to Doubles
            if len(items[0]) == 1:
                new_item = items[sample] + items[test]
                candidates.append(new_item)

            # Doubles and higher
            else:
                list_len = len(items[0])
                join_len = list_len-1
                joiner = items[sample][0:join_len]  # produces a list
                tester = items[test][0:join_len]  # produces a list
                joiner.sort()
                tester.sort()
                if joiner == tester:
                    first = [items[sample][join_len]]
                    second = [items[test][join_len]]
                    new_item = joiner + first + second
                    candidates.append(new_item)

    return candidates


def build_freq_lists(all_lists: list, candidates: list, min_supp: int):
    '''
    Determine if candidate list items reaches the minimum support
    within all lists to be classified as a "frequent list".

    INPUTS:  All lists, candidate list, minimum support level.
    RETURNS: List only containing items reaching minimum support level.
    '''

    frequent_lists = []
    for candidate in candidates:
        if count_items(all_lists, candidate) >= min_supp:
            frequent_lists.append(candidate)

    return frequent_lists


def count_items(all_lists: list, comp_list: list):
    '''
    Counts instances of rule items within full list entered by user

    INPUT:   All lists entered by user, list of items.
    RETURNS: Integer value of count.
    '''

    full_count = 0
    for each_list in all_lists:
        clean_list = str(each_list).lower().strip()
        list_count = 0
        for each_item in comp_list:
            clean_item = str(each_item).lower().strip()
            if clean_item in clean_list:
                list_count += 1

        if list_count == len(comp_list):
            full_count += 1
    return full_count


def calc_items(all_lists: list, this_rule: list):
    '''
    Calculates Support, Confidence, and Lift of specific rule.

    INPUT:   All lists entered by user, user rule split into lists.
    RETURNS: 3-Tuple of support, confidence, and lift measures.
    '''
    left_count = count_items(all_lists, this_rule[0])
    together_rule = this_rule[0] + this_rule[1]
    together_count = count_items(all_lists, together_rule)
    support = together_count/len(all_lists)
    confidence = together_count/left_count
    right_count = count_items(all_lists, this_rule[1])
    right_support = right_count/len(all_lists)
    lift = confidence/right_support

    return (support, confidence, lift)


def print_freq_results(all_lists: list, min_support: int):
    '''
    Calculates item frequency and prints items with frequency

    INPUT:   All lists, minimum support value.
    RETURNS: None - results printed.
    '''
    cand_count = 2
    rounds = 0
    candidates = []
    while cand_count > 1 or rounds > 10:
        rounds += 1
        print()
        print(f"ROUND #{rounds}:")
        if rounds == 1:
            candidates = generate_singles(all_lists)
        else:
            candidates = build_candidates(candidates)
        print("CANDIDATES")
        print("==========")
        if len(candidates) > 0:
            for item in candidates:
                item_count = count_items(all_lists, item)
                print(f"{item}:{item_count}", end="  ")
        else:
            print("No other list candidates found", end="")
        print()
        # print(candidates)

        candidates = build_freq_lists(all_lists, candidates, min_support)
        cand_count = len(candidates)
        print()
        print("LIST OF FREQ ITEMS")
        print("==================")
        if len(candidates) > 0:
            for item in candidates:
                item_count = count_items(all_lists, item)
                print(f"{item}:{item_count}", end="  ")
        else:
            print("No frequent items in candidates found.", end="")
        print()


#####################################################
count = 0
name = get_name()
running = True
state = 1
all_lists = []
while running:
    option = show_menu(name, state)
    if option == "0":
        running = False
    elif option == "1":  # Enter List
        all_lists = get_all_lists(name)
        state = 2
    elif option == "2":  # calc support & conf
        more_rules = True
        while more_rules:
            rule = get_rule(name)
            scl_tuple = calc_items(all_lists, rule)
            supp_percent = round(scl_tuple[0]*100, 1)
            conf_percent = round(scl_tuple[1]*100, 1)
            lift_percent = round(scl_tuple[2]*100, 1)
            print(
                f"Support: {supp_percent}%, Confidence: {conf_percent}%, Lift: {lift_percent}%")
            print()
            more = input("More Rules (Y/N)? ")
            if more.lower() != "y":
                more_rules = False
    else:  # calc frequency
        min_support = get_frequency(name)
        print_freq_results(all_lists, min_support)
print(f"*** It has been nice working with you, {name}")
