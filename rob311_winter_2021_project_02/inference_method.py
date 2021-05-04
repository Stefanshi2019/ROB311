from collections import deque
from support import definite_clause

### THIS IS THE TEMPLATE FILE
### WARNING: DO NOT CHANGE THE NAME OF FILE OR THE FUNCTION SIGNATURE


def pl_fc_entails(symbols_list : list, KB_clauses : list, known_symbols : list, query : int) -> bool:
    """
    pl_fc_entails function execute+s the Propositional Logic forward chaining algorithm (AIMA pg 258).
    It verifies whether the Knowledge Base (KB) entails the query
        Inputs
        ---------
            symbols_list  - a list of symbol(s) (have to be integers) used for this inference problem
            KB_clauses    - a list of definite_clause(s) composed using the numbers present in symbols_list
            known_symbols - a list of symbol(s) from the symbols_list that are known to be true in the KB (facts)
            query         - a single symbol that needs to be inferred

            Note: Definitely check out the test below. It will clarify a lot of your questions.

        Outputs
        ---------
        return - boolean value indicating whether KB entails the query
    """

    ### START: Your code

    # keep track of all visited clauses, initialize all to false
    print("symbols are:", symbols_list)
    print("clauses are:")
    for clause in KB_clauses:
        print(clause.body, clause.conclusion)
    print("goal is: ", query)
    print("known symbols are:", known_symbols)
    visited = {}
    for symbol in symbols_list:
        visited[symbol] = False

    # keep track of all solved clauses, if all elements in body are in known/visited,
    # the conclusion is known to be true. Initialize all solved clauses to false
    solved_clause = {}
    for clause in KB_clauses:
        solved_clause[clause] = False

    # iterate symbols until either query is found or all symbols are visited
    while len(known_symbols) != 0:
        node = known_symbols.pop()
        # return found query if the current node is known to be true
        if node == query:
            print("solved")
            return True
        # if this is an unvisited node
        if visited[node] == False:
            # make this node visited
            visited[node] = True
            print("node is", node)
            # now the knowledge base has expanded, try if a clause can be solved
            for clause in KB_clauses:
                # if a clause is not solved
                if solved_clause[clause] == False:
                    # iterate all body elements in clause,
                    # if body elements are known/visited,
                    # then we solved this clause, append its conclusion to known symbols
                    solved = True
                    for sym in clause.body:
                        if visited[sym] == False:
                            solved = False
                            break
                    if solved:
                        known_symbols.append(clause.conclusion)
                        solved_clause[clause] = True

    print("not solved")
    return False

    ### END: Your code


# SAMPLE TEST
if __name__ == '__main__':

    # Symbols used in this inference problem (Has to be Integers)
    symbols = [1, 2, 3, 4, 5, 6, 7, 8]

    # Clause a: 1 and 2 => 9
    # Clause b: 9 and 4 => 5
    # Clause c: 1 => 4
    KB = [definite_clause([5], 6), definite_clause([4,7], 8)]

    # Known Symbols 1, 2
    known_symbols = [1, 2, 3, 4, 5]

    # Does KB entail 5?
    entails = pl_fc_entails(symbols, KB, known_symbols, 8)

    print("Sample Test: " + ("Passed" if entails == True else "Failed"))
