from grammar_elements import *


class PrefixNode:
    def __init__(self, el: GrammarElement, prefix_length, parent):
        self.prefix = el.name
        self.prefix_length = prefix_length
        self.parent = parent
        # Prefix nodes
        self.children = []
        # Grammar element arrays
        self.alts = []

    def __str__(self):
        return "Prefix: \"{}\"".format(self.prefix) + " Children: \'{}\'".format(self.children) \
               + " Alts:\"{}\"".format(self.alts)

    def __repr__(self):
        return self.__str__()

    def get_child_named(self, el_name: str):
        for (i, child) in enumerate(self.children):
            if child.prefix == el_name:
                return i

        return None


class PrefixTree:
    """
    Prefix tree to implement longest prefix matching for left factoring
    Pass it a non terminal to generate a prefix tree for it   
    """

    def __init__(self, g: NonTerminal):
        # Dictionary with key = element name, val = tree
        self.children = {}
        # Table of factored out elements
        self.__factored_table = {}
        self.non_terminal = g
        self.create_tree()

    def create_tree(self):
        # This iterator gives the alternatives of the non terminal
        for alt in self.non_terminal:
            el = alt[0]

            if el.name in self.children.keys():
                node = self.children[el.name]
            else:
                node = PrefixNode(el, 0, None)
                self.children[el.name] = node

            # alternatives of length 1 will be added directly
            if len(alt) == 1:
                node.alts.append(alt)
                continue

            alt_cpy = alt[:]
            del alt[0]
            self.create_chain(node, alt, alt_cpy)

    def create_chain(self, start_node: PrefixNode, elements: list, full_alt: list):
        """
        Creates a prefix tree of the given alternative, then stores the alternative
        at the bottom of this tree
        :param start_node: Head of the tree 
        :param elements: list containing alternatives and used only to traverse deeper in the tree
        :param full_alt: The alternative itself without being modified to be stored at the end
        """
        while len(elements) > 1:
            head = elements[0]
            matching_child = start_node.get_child_named(head.name)

            # Advance
            if matching_child is None:
                node = PrefixNode(head, start_node.prefix_length + 1, start_node)
                start_node.children.append(node)
            else:
                node = start_node.children[matching_child]

            del elements[0]
            start_node = node

        # Create a node with the element's name

        # Leaf of the tree is the full alternative, and all the previous
        # nodes are the prefix
        alt_str = PrefixTree.__to_string(full_alt)[0:-1]

        start_node.alts.append(full_alt)
        if alt_str not in self.__factored_table.keys():
            self.__factored_table[alt_str] = []

        self.__factored_table[alt_str].append(full_alt)

    def get_factored_out(self):
        """
        Returns the terminals that can be factored out
        """
        prefixes = {}
        for key in self.__factored_table.keys():
            alts = self.__factored_table[key]
            prefixes[key] = alts

        PrefixTree.__add_leftovers(prefixes)

        return prefixes

    @staticmethod
    def __add_leftovers(prefixes: dict):
        """
        Get the leftovers, those who have exact match with another prefix
        i.e, ab | abc | abd --> ab will be in the node a, abc & abd will be in the path a-b
        so we add the alternative ab to the list, and then will be translated to epsilon when
        generating the new non terminal
        :param prefixes: Table containing prefixes with leftovers 
        """
        # Sort keys by length to get the leftovers in the right way
        keys = sorted(prefixes.keys(), key=lambda x: len(x))

        for key in keys:
            leftover_key = key[0:-1]
            if len(leftover_key) == 0:
                continue

            if leftover_key in keys:
                # This is a leftover
                leftovers = prefixes[leftover_key]

                # this filters the items for the following case
                # ab, ax, a are children of node 'a'
                # abc, abd are children of node 'ab' -> extract the 'ab' for the 'a' node
                # and add it to the 'ab' node
                filtered = filter(lambda x: PrefixTree.__to_string(x) == key, leftovers)
                for alt in filtered:
                    prefixes[key].append(alt)
                    prefixes[leftover_key].remove(alt)

                if len(prefixes[leftover_key]) == 0:
                    del prefixes[leftover_key]

    def get_alternatives_at(self, start_node: PrefixNode, node_prefix: str):
        """
        Gets the alternatives of a non-terminal with a given prefix starting 
        from a given node, i.e searches the tree for some prefix 
        """
        if start_node.prefix == node_prefix:
            return start_node.alts
        else:
            alts = []
            for child in start_node.children:
                for alt in self.get_alternatives_at(child, node_prefix):
                    alts.append(alt)

            return alts

    def get_tree_head(self, prefix):
        if prefix in self.children.keys():
            return self.children[prefix]
        return None

    def print_debug(self):
        for key in self.children:
            PrefixTree.__print_tree_dfs(self.children[key])

    @staticmethod
    def __print_tree_dfs(node: PrefixNode):
        print(node.prefix_length * "\t", "Node:", node.prefix)
        for alt in node.alts:
            print(node.prefix_length * "\t", alt)

        for child in node.children:
            print(child.prefix)
            print(child.children)
            PrefixTree.__print_tree_dfs(child)

    @staticmethod
    def __to_string(alternative):
        alt_str = ""
        for el in alternative:
            alt_str += el.name
        return alt_str
