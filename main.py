"""
SAT Solver

The Davis-Putnam-Logemann-Loveland (DPLL) algorithm is a recursive, backtracking-based search algorithm for 
deciding the satisfiability of propositional logic formulas in CNF (Conjunctive Normal Form).
"""

class ImplicationGraph: 
    def __init__(self):
        self.vertices = {} # Key: Literal, Value: Decision levels
        self.edges = {} # Key: Literal, Value: Set of literals it implies
        self.conflict_node = None # Conflict node

    def add_vertex(self, literal, decision_level):
        if literal not in self.vertices: 
            self.vertices[literal] = decision_level
            self.edges[literal] = set()

    def add_edge(self, antecedent, consequent):
        # Check if vertices exist before adding an edge
        if antecedent not in self.vertices: 
            raise ValueError(f"Antecedent vertex {antecedent} does not exist.")
        if consequent not in self.vertices: 
            raise ValueError(f"Consequent vertex {consequent} does not exist.")

        self.edges[antecedent].add(consequent)

    def add_conflict(self, conflicting_clause):
        self.conflict_node = 'k' # Label the conflicting node as k
        for literal in conflicting_clause: 
            # For each literal in the conflicting clause, add an edge from its negation to k 
            negated_literal = -literal
            if negated_literal in self.vertices: 
                self.edges[negated_literal].add(self.conflict_node)
            else: 
                raise ValueError(f"Literal {-literal} does not exist.")

    def display(self): 
        print("Vertices: ")
        for v, dl in self.vertices.items(): 
            print(f"Vertex: {v}, {dl}")
        
        print("\nEdges: ")
        for v, implications in self.edges.items(): 
            print(f"{v} -> {implications}")
        
        if self.conflict_node: 
            print("Conflict node: ", self.conflict_node)

def DPLL(formula):
    def decide(formula, assignments, implication_graph): 
        """
        Chooses an unassigned variable and assigns a truth value.
        Implement Jeroslow-Wang heuristics for decision making.
        """
        j_literal_map = {}
        for clause in formula: 
            for literal in clause: 
                if literal in assignments or -literal in assignments: 
                    continue
                if literal not in j_literal_map: 
                    j_literal_map[literal] = 0
                j_literal_map[literal] += 2 ** len(clause)

        # Selecting the literal with the maximum J(l) value.
        chosen_literal = max(j_literal_map, key=j_literal_map.get, default=None)

        # Return False when there are no more unassigned variable to assign.
        return chosen_literal is not None
            
    def BCP(formula, assignments, decision_level, implication_graph):
        """
        Perform Boolean Constraint Propagation.

        Args:
            formula (list of lists): The CNF formula represented as a list of clauses.
            assignments (dict): Current assignments of variables.
            decision_level (int): Current decision level.

        Returns:
            str: "conflict" if a conflict is encountered, otherwise None.
        """
        while True:
            unit_clause_found = False
            for clause in formula:
                unassigned_literals, false_count = [], 0
                for literal in clause:
                    if literal in assignments:
                        if assignments[literal] == False:
                            false_count += 1
                    else:
                        unassigned_literals.append(literal)

                if false_count == len(clause) - 1 and len(unassigned_literals) == 1:
                    unit_clause_found = True
                    unassigned_literal = unassigned_literals[0]

                    # Assign the value to the unassigned literal to satisfy the clause
                    assignments[unassigned_literals[0]] = True 

                    # Update the implication graph 
                    implication_graph.add_vertex(unassigned_literal, decision_level)
                    for literal in clause: 
                        if literal != unassigned_literal: 
                            negated_literal = -literal
                            if negated_literal not in implication_graph.vertices: 
                                implication_graph.add_vertex(negated_literal, decision_level)
                            implication_graph.add_edge(negated_literal, unassigned_literal)

                if false_count == len(clause): 
                    # Add conflict node and update the graph 
                    implication_graph.add_conflict(clause)
                    return "conflict"

            if not unit_clause_found:
                print("Did not find unit clauses.")
                break

        return None

    def analyze_conflict(): 
        """
        Determines the backtracking level or detects unsatisfiability.
        """
        pass

    def backtrack(dl):
        """
        Resets the current decision level to 'dl' and undoes assignments at decision levels higher than 'dl'.
        """
        pass

    # Initialize assignments and decision level
    assignments = {}
    decision_level = 0

    # Create an instance of the Implication Graph
    implication_graph = ImplicationGraph()

    # Check for immediate conflicts. 
    if BCP(formula, assignments, decision_level, implication_graph) == "conflict":
        return "Unsatisfiable"

    # Main DPLL loop
    while True: 
        if not decide(formula, assignments, implication_graph): 
            return "Satisfiable"
        else:
            while BCP(formula, assignments, decision_level, implication_graph) == "conflict":
                backtrack_level = analyze_conflict(implication_graph, decision_level)
                if backtrack_level < 0: 
                    return "Unsatisfiable"
                backtrack(assignments, decision_level, backtrack_level, implication_graph)

# Example CNF formula represented as a list of lists
cnf_formula = [[1, -2, 3], [-1, 4], [2, -3, -4]]

# Calling the DPLL function with the CNF formula
result = DPLL(cnf_formula)

print("The formula is:", "Satisfiable" if result == "Satisfiable" else "Unsatisfiable")
