
class TrieTree:

    root = {}
    end = '/'

    def __init__(self):
        pass

    def add_term(self, term):
        node = self.root
        for char in term:
            node = node.setdefault(char, {})
        node[self.end] = None

    def find_term(self, term):
        pass
