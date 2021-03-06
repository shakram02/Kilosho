from enum import Enum


class ElementType(Enum):
    """
    To make checking for grammar element type easier
    And to make a special case for the epsilon object
    """
    Epsilon = 1
    Terminal = 2
    OrOperation = 3
    NonTerminal = 4
    Dollar = 5


# Abstract class
class GrammarElement:
    """
    Base class for all grammar blocks, Terminals, Non terminals and operations
    """

    def __init__(self, element_type, name: str):
        self.type = element_type
        self.productions = [[]]
        self.current_production_index = 0
        self.name = name

    def __str__(self):
        # return "Name: '" + self.name + ", Type: " + self.type.name
        return "Name: '" + self.name + "'"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return id(self)

    def has_epsilon(self):
        """
        Tells whether the non terminal has an epsilon in its definition 
        """
        for production in self.productions:
            for el in production:
                if el.type == ElementType.Epsilon:
                    return True
        return False


class OrOperation(GrammarElement):
    def __init__(self):
        super().__init__(ElementType.OrOperation, "")


class Terminal(GrammarElement):
    """
        Terminal grammar element 
    """

    def __init__(self, name: str):
        super().__init__(ElementType.Terminal, name)

    @staticmethod
    def create_epsilon():
        """
        Creates an epsilon element
        :return: The epsilon object
        """
        e = Terminal('\L')
        e.type = ElementType.Epsilon
        return e

    @staticmethod
    def create_dollar():
        """
        Creates a dollar element
        Represents the end of input
        :return: The dollar object
        """
        d = Terminal('$')
        d.type = ElementType.Dollar
        return d

    def __eq__(self, other):
        if self.type == ElementType.Epsilon and other.type == ElementType.Epsilon:
            return True

        if self.type == other.type and self.name == other.name:
            return True

        return False

    def __ne__(self, other):
        if self.type == ElementType.Epsilon and other.type == ElementType.Epsilon:
            return True

        if self.type != other.type:
            return True

        if self.name != other.name:
            return True

        return False

    # def __str__(self):
    #     return str({'name': self.name, 'rule': self.productions, 'type': self.type.name})
    #
    # def __repr__(self):
    #     return str({'name': self.name, 'rule': self.productions, 'type': self.type.name})

    def __hash__(self):
        return super.__hash__(self)


class NonTerminal(GrammarElement):
    """
        Represents a non terminal
    """

    def __init__(self, name: str):
        super().__init__(ElementType.NonTerminal, name)

    def and_with(self, other: GrammarElement):
        """
        If the rule is empty it adds the element to it, if not, it concatenates 
        The provided element with the last one in the rule. The concatenation doesn't 
        have an operation object to make things simple
        :param other: Terminal or Non-terminal to be appended
        :return Self, ( a context to allow chaining )
        """

        self.productions[self.current_production_index].append(other)
        return self  # Allow chaining

    def or_with(self, other: GrammarElement):
        """
        ORs the last element in the rule with the provided element
        :param other: Grammar element to OR with
        :return: Self, ( a context to allow chaining )
        """

        self.current_production_index += 1
        self.productions.append([other])
        return self
