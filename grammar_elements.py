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


# Abstract class
class GrammarElement:
    def __init__(self, name: str):
        self.type = None
        self.rule = None
        self.name = name


class OrOperation(GrammarElement):
    def __init__(self):
        super().__init__("")
        super().type = ElementType.OrOperation


class Terminal(GrammarElement):
    """
        Terminal grammar element 
    """

    def __init__(self, name: str):
        super().__init__(name)
        super.type = ElementType.Terminal

    @staticmethod
    def create_epsilon():
        """
        Creates an epsilon element
        :return: The epsilon object
        """
        e = Terminal("")
        e.type = ElementType.Epsilon
        return e


class NonTerminal(GrammarElement):
    """
        Represents a non terminal
    """

    def __init__(self, name: str):
        super().__init__(name)
        super.type = ElementType.NonTerminal
        self.name = ""
        self.rule = []

    def and_with(self, other: GrammarElement):
        """
        If the rule is empty it adds the element to it, if not, it concatenates 
        The provided element with the last one in the rule. The concatenation doesn't 
        have an operation object to make things simple
        :param other: Terminal or Non-terminal to be appended
        :return Self, ( a context to allow chaining )
        """
        self.rule.append(other)
        return self  # Allow chaining

    def or_with(self, other: GrammarElement):
        """
        ORs the last element in the rule with the provided element
        :param other: Grammar element to OR with
        :return: Self, ( a context to allow chaining )
        """
        self.rule.append(OrOperation())
        self.rule.append(other)
        return self
