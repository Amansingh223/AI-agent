class StateGraph:
    def __init__(self, state_type):
        self.state_type = state_type
        self.nodes = {}
        self.edges = {}
        self.entry = None
        self.finish = None

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, from_node, to_node):
        self.edges[from_node] = to_node

    def set_entry_point(self, node_name):
        self.entry = node_name

    def set_finish_point(self, node_name):
        self.finish = node_name

    def compile(self):
        def run(initial_state):
            state = dict(initial_state)
            current = self.entry
            while current:
                step_func = self.nodes[current]
                result = step_func(state)
                state.update(result)
                current = self.edges.get(current)
            return state
        return type("CompiledGraph", (), {"invoke": staticmethod(run)})
