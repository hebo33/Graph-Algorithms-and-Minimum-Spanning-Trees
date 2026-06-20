from typing import List, Dict, Tuple, Optional, Callable

################ CODE FROM A1 ################
class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        name (str): The label or identifier of the vertex.
        children (Dict[str, Tuple[str, str, float]]):
            A mapping between child vertex names and edges.
            Each edge is represented as a tuple:
                (source vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None):
        """
        Initializes a Vertex.

        Args:
            name (str): The label or identifier of the vertex.
            children (Optional[Dict[str, Tuple[str, str, float]]]):
                A mapping between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """
        Returns all edges from this vertex.

        Returns:
            List[Tuple[str, str, float]]: The list of edges from this vertex.
        """
        lst = []
        for key in self.children:
            lst.append(self.children[key])
        return lst

class Graph:
    """
    Represents a graph consisting of multiple vertices.

    Attributes:
        vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """
        Initializes a Graph.

        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """
        Returns all vertices in the graph.

        Returns:
            List[Vertex]: The list of vertices in the graph.
        """
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """
        Checks if vertex v_name is a child of vertex u_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the potential child vertex.

        Returns:
            bool: True if the vertex v_name is a child of the vertex u_name, False otherwise.
        """
        for v in self.get_vertices():
            if v.name == u_name:
                lst = v.get_children()
                for e in lst:
                    if e[1] == v_name:
                        return True
        return False

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """
        Retrieves the edge between u_name and v_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the child vertex.

        Returns:
            Optional[Tuple[str, str, float]]: The edge if it exists,
            or None if no such edge is found.
        """
        for v in self.get_vertices():
            if v.name == u_name:
                lst = v.get_children()
                lst2 = []
                for e in lst:
                    if e[1] == v_name:
                        return e
        return None


################ CODE FROM A1 ################

# Union-Find (Disjoint Set) data structure
class UnionFind:
    def __init__(self, elements: List[str]):
        """
        Initializes the Union-Find data structure for n elements.
        Initially, each element is in its own set (its parent is itself).
        The rank (or size) of each set is initialized to 0.

        Parameters:
        elements (List[str]): The list of elements in the Union-Find data structure.
        """
        self.parent = {elem: elem for elem in elements}
        self.rank = {elem: 0 for elem in elements}

    def find(self, x: str) -> str:
        """
        Find the root (or representative) of the set containing the element x.

        Args:
        x (str): The element whose root we want to find.

        Returns:
        str: The root of the set that contains x.
        """
        parent = self.parent[x]
        if parent == x:
            return parent
        return self.find(parent)

    def union(self, x: str, y: str) -> bool:
        """Union (or merge) the sets containing elements x and y.
        Return True if union was successful.
        If x and y are already in the same set, do nothing (return False).

        Args:
            x (str): The first element (set to be united).
            y (str): The second element (set to be united).

        Returns:
        bool: True if x and y are successfully unioned.
              False if x and y are already in the same set (no union nedded).
        """
        x_root = self.find(x)
        y_root = self.find(y)

        # x and y in the same set
        if x_root == y_root:
            return False

        # x and y not in the same set
        if self.rank[x_root] < self.rank[y_root]: # Union x set to y set
            self.parent[x_root] = y_root
        elif self.rank[x_root] > self.rank[y_root]: # Union y set to x set
            self.parent[y_root] = x_root
        else: # A tie in the ranks, union x set to y set
            self.parent[x_root] = y_root
            self.rank[y_root] = self.rank[x_root] + 1

        return True

# Function to implement Kruskal's algorithm
def kruskal_mst(graph: Graph) -> List[Tuple[str, str, float]]:
    """
    Kruskal's Algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (Graph): The graph for which we compute the MST.

    Returns:
        List[Tuple[str, str, float]]: A list of edges in the MST.
        Each edge is represented as a tuple (source vertex, destination vertex, weight).
    """

    result = []  # The final MST

    # Step 1: Get edge list
    edge_lst0 = []

    vertices = graph.get_vertices()
    for v in vertices:
        # v.children is a dict mapping name -> edge tuple
        for edge in v.children.values():
            edge_lst0.append(edge)

    # Step 2: Sort edges by weight
    edge_lst1 = []

    if not edge_lst0:
        return edge_lst1

    # Simple selection-sort style
    while edge_lst0:
        smallest = edge_lst0[0]
        for edge in edge_lst0:
            if edge[2] <= smallest[2]:
                smallest = edge
        edge_lst0.remove(smallest)
        edge_lst1.append(smallest)

    # Step 3: Initialize Union-Find data structures
    v_names = [v.name for v in vertices]
    union_find = UnionFind(v_names)

    # Step 4: Iterate over the sorted edges to build MST
    for edge in edge_lst1:
        if union_find.find(edge[0]) != union_find.find(edge[1]):
            result.append(edge)
            union_find.union(edge[0], edge[1])

        if len(result) == len(v_names) - 1:
            return result

    return result

    # Suggested steps
    # Step 1: Get edge list
    # Step 2: Sort edges by weight
    # Step 3: Initialize Union-Find data structures
    # (to track the connected sets of vertices as we add edges to the MST)
    # Step 4: Iterate over the sorted edges to build MST



# Function to implement Prim's algorithm
def prim_mst(graph: Graph) -> List[Tuple[str, str, float]]:
    """
    Prim's Algorithm for Minimum Spanning Tree (MST).

    Args:
        graph (Graph): The graph for which we compute the MST.

    Returns:
        List[Tuple[str, str, float]]: A list of edges in the MST.
            Each edge is represented as a tuple (source vertex, destination vertex, weight).
    """

    result = []  # The final MST
    vertices = graph.get_vertices()

    # Step 1: Pick starting vertex
    # Step 1 (a): Empty graph
    if not vertices:
        return result
    # Step 1 (b): Single vertex graph
    if len(vertices) == 1:
        return result
    # Step 1 (c): Regular graph with >= 2 vertices

    # Step 2: Get starting node edges
    start_vertex = vertices[0]
    o_set = [edge for edge in start_vertex.children.values()]  # outgoing edges
    c_set = [start_vertex.name]  # visited set (names only)

    # Step 3–4: Continue until MST has |V| - 1 edges
    while len(result) < len(vertices) - 1:

        # Open set empty → no MST possible
        if not o_set:
            return result

        # Find smallest edge in o_set
        smallest = o_set[0]
        for edge in o_set:
            if edge[2] <= smallest[2]:
                smallest = edge

        # Remove the smallest edge from open set
        o_set.remove(smallest)

        u, v, w = smallest

        # Skip if destination is already visited (prevents cycle)
        if v in c_set:
            continue

        # Accept this edge
        result.append(smallest)
        c_set.append(v)

        # Add all outgoing edges from vertex v
        for vertex in vertices:
            if vertex.name == v:
                for edge in vertex.children.values():
                    if edge[1] not in c_set:
                        o_set.append(edge)

    return result
