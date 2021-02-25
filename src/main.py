import sys


# TODO: implement adequate parsing, not a parody that I have now
def parse(input_file_path):
    element_transitions = dict()  # element: (start_state, end_state)
    state_transitions = dict()  # start_state: (element, end_state)
    with open(input_file_path, "r") as input_file:
        size_of_q, size_of_sigma = [int(size) for size in input_file.readline().split()]

        index_of_initial_state = int(input_file.readline().split()[0])
        list_of_indices_of_terminal_states = \
            [int(term) for term in list(input_file.readline().split())[1:]]

        for line in range(size_of_sigma + 1):
            element = input_file.readline().split()[0]
            element_transitions[element] = []

            for x in range(size_of_q):
                row = input_file.readline().split()

                if x not in state_transitions:
                    state_transitions[x] = []

                for y in range(size_of_q):
                    if row[y] == "1":
                        element_transitions[element].append((x, y))
                        state_transitions[x].append((element, y))

    return [index_of_initial_state, list_of_indices_of_terminal_states,
            element_transitions, state_transitions]


def get_normal_delta_representation(transitions):
    """
    :param transitions: {state:[(element1,state1), (element1, state2), ...]}
    :return: {state:{element:(state1, state2, ...), ...}
    """
    adequate_q = dict()
    for state in transitions:
        adequate_q[state] = dict()
        for transition in transitions[state]:
            if transition[0] in adequate_q[state]:  # element
                adequate_q[state][transition[0]].add(transition[1])
            else:
                adequate_q[state][transition[0]] = {transition[1]}
    return adequate_q


def epsilon_nfa_to_nfa(prev):
    # TODO: add term states
    flag = 1
    while flag:
        new = {}
        flag = 0
        for state in prev:
            new[state] = {}
            for transition in prev[state].items():
                if transition[0] == '\\e':
                    for new_state in transition[1]:
                        new[state] = merge(new[state], prev[new_state])
                    flag = 1
                elif transition[0] not in new[state]:
                    new[state][transition[0]] = transition[1]
                else:
                    new[state][transition[0]].add(transition[1])
        prev = new
    return new


def merge(dict1, dict2):
    for transition in dict2.items():
        if transition[0] in dict1:
            dict1[transition[0]] | set(transition[1])
        else:
            dict1[transition[0]] = transition[1]
    return dict1


def find_entries(state, dct):
    entries = set()
    for key in dct:
        if set(state) & set(key):
            entries.add(key)
    return entries


def prepare_for_dfa(dct):
    new_dct = {}
    for i in dct.items():
        new_dct[(i[0],)] = i[1]
    return new_dct


if __name__ == '__main__':
    # # TODO: add checking of the argument provided
    # given_file_path = sys.argv[1]
    #
    # # Parsing file to get automata represented as a list:
    # # [index of initial state, list of indices of terminal states,
    # #  transitions: element:[(pair of states), ....]
    # #  state transitions: {state:[(element1,state1), (element1, state2), ...]} ]
    # automata = parse(given_file_path)
    #
    # # If we have epsilon-NFA, convert it to NFA:
    # automata = epsilon_nfa_to_nfa(automata)
    #
    # # Convert automata to DFA:
    # # Initially new Q is empty, I suppose
    # new_element_transitions = dict()
    # new_state_transitions = dict()
    # q = []
    # new_delta = dict()
    #
    # # костильний метод для отримання переходів,
    # # приберу його коли буду нормально парсити, а не як зараз:/
    # delta = get_normal_delta_representation(automata[3])
    # # for i in delta.items():
    # #     print(i)
    #
    # q.append((automata[0],))
    #
    # for state in q:
    #     new_delta[state] = dict()
    #
    #     for element in state:
    #         for transition in delta[element]:
    #             transition_state_set = delta[element][transition]
    #             if transition not in new_delta[state]:
    #                 new_delta[state][transition] = transition_state_set
    #             else:
    #                 new_delta[state][transition].union(transition_state_set)
    #             new_state = tuple(transition_state_set)
    #             # for other_state in q:
    #             #     if element in state:
    #             #         new_delta[state][transition].union(new_delta[other_state][element])
    #             if new_state not in q:
    #                 q.append(new_state)
    # print(f"     {'  '.join(list(str(i) for i in range(len(automata[2]))))}")
    # for i in new_delta:
    #     print(f"{i}   {'  '.join(list(str(i) for i in range(len(new_delta))))}")
    prev = {0: {'\\e': {1}},
            1: {'\\0': {0, 1}, '\\1': {2}},
            2: {'\\e': {0}}}
    init_states = {0, 1, 2}
    init_elements = {'\\0', '\\1'}
    initial = {0}
    term = {2}

    # Epsilon-NFA to NFA:
    flag = 1
    while flag:
        new = {}
        flag = 0
        for state in prev:
            new[state] = {}
            for transition in prev[state].items():
                if transition[0] == '\\e':
                    for new_state in transition[1]:
                        new[state] = merge(new[state], prev[new_state])
                    flag = 1
                elif transition[0] not in new[state]:
                    new[state][transition[0]] = transition[1]
                else:
                    new[state][transition[0]].add(transition[1])
        prev = new

    for i in new:
        print(f"{i}   {new[i]}")

    # NFA to DFA:
    prev = prepare_for_dfa(prev)
    flag = 1
    while flag:
        new = {}
        flag = 0
        for state in prev:
            temp = set()  # Holds new possible states
            entries = find_entries(state, new)
            if entries:
                for entry in entries:
                    new[entry] = merge(new[entry], prev[state])
                    temp = temp | set(tuple(i) for i in new[entry].values())
            else:
                new[state] = prev[state]
                temp = temp | set(tuple(i) for i in new[state].values())

            for key in temp:
                if set(key) not in list(set(i) for i in new):
                    new[tuple(key)] = {}
                    if set(key) not in list(set(i) for i in prev):
                        flag = 1
        prev = new

    for i in new:
        print(f"{i}   {new[i]}")

    # DFA to cDFA:
    absorbing_state = "absorbing"
    flag = 0
    for state in new:
        for element in init_elements:
            if element not in new[state]:
                flag = 1
                new[state][element] = {absorbing_state}
    if flag:
        new[(absorbing_state,)] = {}
        for element in init_elements:
            new[(absorbing_state,)][element] = {absorbing_state}

    for i in new:
        print(f"{i}   {new[i]}")
