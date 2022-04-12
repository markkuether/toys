
# Pseudo-random number tester
# seed value = 1
x0 = 1
m_start = 5
m_stop = 100
file_path = "C:/Users/Public/Documents/"
file_name = "pseudo_rnd_test.csv"
full_file = file_path + file_name


def ideal_params(params: list):
    '''
    Tests whether the set of parameters
    generates an ideal set of pseudo random
    numbers according to the formula

    X(n+1) = (A*X(n) + C) MOD M

    Ideal sets contain unique remainders
    of length M. 
    '''

    # xn = initial seed - not considered for set.
    m, a, c, xn = params
    stop = False
    nums = set([])
    while not stop:
        xn = (a*xn+c) % m
        if xn in nums:
            stop = True
        else:
            nums.add(xn)

    return bool(len(nums) == m)


# Set seed = 1
x0 = 1
is_ideal = False

params_file = open(full_file, "w")
header = "M,A,C\n"
params_file.write(header)

for m in range(m_start, m_stop+1):
    for a in range(1, m):
        nums = set([])
        for c in range(1, m):
            params = [m, a, c, x0]
            is_ideal = ideal_params(params)
            if is_ideal:
                param_list = str(m) + "," + str(a) + "," + str(c) + "\n"
                params_file.write(param_list)
#                print(f"     a={a}, c={c} is good.")
params_file.close()
