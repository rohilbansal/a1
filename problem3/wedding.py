'''
The Marriage Problem Abstraction:
• Monte Carlo Descent

– State Space: Represented by an M-element vector, where the index of each element corresponds
to a certain guest, and each element has a non-negative integer as its value corresponding to the
index of the table where the guest are seated. M is the total number of the guests.

– Initial State: No guests have been seated in any table, represented by an m-element vector
where each element is set to 0, which means that the corresponding guest has not been seated in
any table yet.

– Goal State: Every guest has been seated in a table and the number of the tables is as least as
possible, represented by an M-element vector where no elements are 0 and the maximum element
is as least as possible.

– Cost Function: It equals to the number of the tables.

– Successor function: Assign a table to a guest who has not been seated yet, given the condition
that

    1. This new state is never visited before
    2. After assigning, the number of guests in the assigned table will not exceed a given number
    N, and
    3. Guests in that table do not know each other before. 
	It is represented by assigning a positive integer P to an element which is currently 0, and
	making sure that after assigning
        ∗ The new state is not in our visited state records.
        ∗ The number of P in the vector will not exceed N.
        ∗ Guests with the index that has an element of P do not know each other.

– Edge Weights: It will equal 0 or 1. If after assigning, there will be one more table, then edge
weight equals to 1. Otherwise, if the number of tables do not change, the edge weight equals to 0.

– Heuristic Function: It equals to the number of the tables,. Since we directly take the cost
    function as the heuristic function, it must be admissible.
                h(s) = numberof tables

– Algorithm:
1 Repeat L times (in my code, L = 10 * the number of the guests):
2 s = initial state
3 Repeat K times (in my code, K = 10 * the number of the guests):
    1 If s is our goal, then return s
    2 Pick s' from the successors of s at random
    3 If h(s') ≤ h(s) (we want to find the s' that makes h(s') as least as possible!), then s = s'
    4 Else with probability of exp(-(h(s')-h(s))/T), s = s' In my code, because h(s') is either
        equal to h(s) or 1 ≥ h(s), so in this case I can directly replace h(s') − h(s) by 1. And
        T = MAX TEMPERATU RE ∗ (1 the times we repeat 2)/K), which makes T decrease as
        the times we repeat 2) increases.
    5 After repeating Step 1 and 2 L times, L results will be got. Then the algorithm compares
        the results with each other based on the number of the tables and chooses the result with
        the least number of tables as the final result.

∗ The problem I met is though Monte Carlo is much faster, it struggles to get the best result
sometimes when just running it once. Therefore I repeat it several times and choose the best
result as the final result.

• A* Search Approach
The Abstract is similar to Monte Carlo

– State Space: Represented by an M-element vector, where the index of each element corresponds
to a certain guest, and each element has a non-negative integer as its value corresponding to the
index of the table where the guest are seated. M is the total number of the guests.

– Initial State: No guests have been seated in any table, represented by an m-element vector
where each element is set to 0, which means that the corresponding guest has not been seated in
any table yet.

– Goal State: Every guest has been seated in a table and the number of the tables is as least as
possible, represented by an m-element vector where no elements are 0 and the maximum element
is as least as possible.

– Cost Function : It equals to the number of the tables.

– Successor Function: Assign a table to a guest who has not been seated yet, given the condition
that 1) this new state is never visited before, 2) after assigning, the number of guests in the assigned
table will not exceed a given number N, and 3) guests in that table do not know each other before.
It is represented by assigning a positive integer P to an element which is currently 0, and making
sure that after assigning, 1) the new state is not in our visited state records, 2) the number of
P in the vector will not exceed N, and 3) guests with the index that has an element of P do not
know each other.

– Edge Weights: It will equal 0 or 1. If after assigning, there will be one more table, then edge
weight equals to 1. Otherwise, if the number of tables do not change, the edge weight equals to 0.

– Heuristic Function: t equals to the number of the tables,. Since we directly take the cost
function as the heuristic function, it must be admissible.
h(s) = the number of tables

– Algorithm:
∗ Add initial state to the fringe. The fringe is implemented by using a priority queue (in
    Python, its called heapq). The priority is generated first based on the number of the tables
    in the state. If there are two states with the same total number of the tables, then they will
    be compared based on the order they are added to the fringe.
∗ Repeated while fringe is not empty:
    · Pop the head h of the fringe
    · If h is our goal, return h
    · Push the successors of h into the fringe
∗ Return False
'''

import sys
import heapq
import random
import math

class tables_guests:
    tables = {}
    guests = {}
    max_table_index = 0
    def __init__(self, ini_max_table_index, ini_tables, ini_guests):
        self.max_table_index = ini_max_table_index
        self.tables = ini_tables
        self.guests = ini_guests

def create_dictionary(file_path):
    count = 0
    name_list = []
    name_dictionary_temp = {}
    number_dictionary_temp = {}
    relationship_dictionary_temp = {}
    f = open(file_path, 'rU')
    for line in f:
        name_list.append( line.lstrip().rstrip().split(' ') )
    f.close()
    for line in name_list:
        for name in line:
            if name not in name_dictionary_temp:
                count += 1
                name_dictionary_temp[name] = count                
    for key in name_dictionary_temp:
        number_dictionary_temp[ name_dictionary_temp[key] ] = key
    for line in name_list:
        relationship_dictionary_temp[ name_dictionary_temp[ line[0] ] ] \
        = [ name_dictionary_temp[ line[i] ] for i in range(1, len(line)) ]
    return [name_dictionary_temp, number_dictionary_temp, relationship_dictionary_temp, count]        

def successors(current_tables_guests):
    succ_temp = []
    guests_not_seated = [i for i in range(1, total_number_of_guests + 1) \
                         if current_tables_guests.guests[i] == 0]
    available_tables = [i for i in range(1, current_tables_guests.max_table_index+1) \
                        if len(current_tables_guests.tables[i]) < N]
    #print(current_tables_guests.guests)
    #print(guests_not_seated)
    #print(current_tables_guests.tables)
    #print(available_tables)
    #print()
    for guest in guests_not_seated:
        find_table = False
        new_tables = current_tables_guests.tables.copy()
        new_guests = current_tables_guests.guests.copy()
        for table in available_tables:
            know_each_other = False
            for guest_sitting_here in current_tables_guests.tables[table]:
                if guest_sitting_here in relationship_dictionary:
                    if guest in relationship_dictionary[guest_sitting_here]:
                        know_each_other = True
                if guest in relationship_dictionary: 
                    if guest_sitting_here in relationship_dictionary[guest]:
                        know_each_other = True
            if know_each_other:
                continue
            find_table = True
            new_tables[table] = new_tables[table] + [guest]
            new_guests[guest] = table
            new_max_table_index = current_tables_guests.max_table_index
            break
        if not find_table:
            new_tables[current_tables_guests.max_table_index + 1] = [guest]
            new_guests[guest] = current_tables_guests.max_table_index + 1
            new_max_table_index = current_tables_guests.max_table_index + 1
        new_tables_guests = tables_guests(new_max_table_index, new_tables, new_guests)
        if get_signature(new_tables_guests.guests) not in visited_states_dictionary:
            succ_temp.append(new_tables_guests)
    return succ_temp            

def get_signature(current_state):
    state_signature = ''
    for item in sorted ( current_state.items() ):
        state_signature = state_signature + str(item[1])
    return state_signature

def printable_result(assignments):
    table_information = ''
    for table in sorted( assignments.tables.items() ):
        each_table_information = ','.join( [ number_dictionary[i] for i in sorted(table[1])] )
        table_information = table_information + each_table_information + '   '
    print( str(assignments.max_table_index) +'   ' + table_information)
        
def assign_table_a_star(initial_tables_guests):
    fringe = []
    count_flag = 0
    heapq.heappush(fringe, (initial_tables_guests.max_table_index, count_flag, initial_tables_guests))
    visited_states_dictionary[get_signature(initial_tables_guests.guests)] = True    
    while len(fringe) > 0:
        head = heapq.heappop(fringe)
        if 0 not in head[2].guests.values():
            print(count_flag)
            return head[2]
        visited_states_dictionary[get_signature(head[2].guests)] = True
        #print(head[2].max_table_index)
        for s in successors(head[2]):
            count_flag += 1
            heapq.heappush(fringe, (s.max_table_index, count_flag, s))
        #if count_flag > 2000:
        #    break
    return  False

def assign_table_monte_carlo(initial_tables_guests):
    MAX_TRIES = 10 * total_number_of_guests
    MAX_TEMPERATURE = 10000
    MAX_ITERATION = 10 * total_number_of_guests
    tries = 0
    temp_solution = tables_guests( total_number_of_guests, initial_tables_guests.tables.copy(), initial_tables_guests.guests.copy() )
    while tries < MAX_TRIES:
        count_flag = 0
        current_tables_guests = initial_tables_guests
        visited_states_dictionary = {}
        visited_states_dictionary[get_signature(current_tables_guests.guests)] = True
        current_successors = successors(current_tables_guests)    
        while len(current_successors) > 0 and count_flag < MAX_ITERATION:
            index = random.randint(0, len(current_successors) - 1 )
            #print(index)
            #print(len(current_successors))
            one_possible_successor = current_successors[index]
            del(current_successors[index])
            if get_signature(one_possible_successor.guests) in visited_states_dictionary:
                continue
            if 0 not in one_possible_successor.guests.values():
                if one_possible_successor.max_table_index <= temp_solution.max_table_index:
                    temp_solution = one_possible_successor
                break
            visited_states_dictionary[get_signature(one_possible_successor.guests)] = True
            if one_possible_successor.max_table_index == current_tables_guests.max_table_index \
            or random.random() < math.exp( -1/(MAX_TEMPERATURE*(1-count_flag/MAX_ITERATION) ) ):
                current_tables_guests = one_possible_successor
                current_successors = successors(current_tables_guests)
            count_flag += 1
        tries += 1    
        #if count_flag > 2000:
        #    break
    return  temp_solution                

N = int(sys.argv[2])
[name_dictionary, number_dictionary, relationship_dictionary, total_number_of_guests] \
= create_dictionary(sys.argv[1])
visited_states_dictionary = {}
initial_max_table_index = 0
initial_tables = {}
initial_guests = {}
for i in range(1, total_number_of_guests + 1):
    initial_guests[i] = 0
initial_tables_guests = tables_guests(initial_max_table_index, initial_tables, initial_guests)

possible_table_assignment = assign_table_monte_carlo(initial_tables_guests)
'''
If you want to use A star searching algorithm rather than Monte Carlo Descent, though I strongly do not suggest so,
please comment out the above statement and use the following statement. Thanks!
'''
#possible_table_assignment = assign_table_a_star(initial_tables_guests)
if possible_table_assignment:
    printable_result(possible_table_assignment)
else:
    print('Life is so hard!')

