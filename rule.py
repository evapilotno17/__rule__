import random
import shutil
import time
import sys

random.seed(time.time())

"""
    purpose:
        - create a class for displaying and printing wolfram like rule based automata
        - there are 8 possible configurations for (left, cell, right)
        - a "rule" tells the automata the next state of "cell" for every possible configuration
        - thus, there are 1<<8 possible rules
        - rule "110" is considered to be "turing complete", although i don't understand how
        
        
        - some special rules:
            110

        
"""

class Rule:
    def __init__(self, state=110, rule=None, wrap=False, center=True):
        if isinstance(state, int):
            self.state = [False for i in range(state)]
            self.state[state//2 if center else 0] = True
        elif isinstance(state, list):
            self.state = [bool(i) for i in state]
        elif isinstance(state, str):
            self.state = [bool(ord(i) - ord('0')) for i in state]
        else:
            raise ValueError(f"invalid state: {state}")
        self.rule = rule or int(random.random() * (1<<8))
        self.wrap = wrap
    
    @staticmethod
    def getmask(state, idx, wrap=False):
        return (state[idx-1] if idx>=0 else (state[-1] if wrap else 0)) * 4 + (state[idx]) * 2+ (state[idx+1] if idx+1<len(state) else (state[0] if wrap else 0))

    @staticmethod
    def next(state, rule, wrap=False):
        nstate = [False for i in range(len(state))]
        for i in range(len(state)):
            nstate[i] = (rule >> (Rule.getmask(state, i))) & 1
        return nstate

    @staticmethod
    def display(state, blocks=None):
        if blocks is None:
            blocks = ['  ','██']
        for bit in state:
            print(blocks[bit], end="")
        print()

    def evolve(self, t=None, blocks=None):
        if blocks is None:
            blocks = ['  ', '██']
        if t is None:
            # width:height of the standard monospaced font is ~ 0.5
            t = int(len(self.state) * len(blocks[0]) / 2)
        print(f"INITIATING RULE {self.rule}. If your randomly generated rule is $110, the basilisk has you")
        for i in range(t):
            Rule.display(self.state)
            self.state = Rule.next(self.state, self.rule, self.wrap)


def main():
    args = sys.argv
    cols, rows = shutil.get_terminal_size()
    rule = int(args[1]) if len(args)>1 else int(random.random() * (1<<8))
    state = int(args[2]) if len(args)>2 else (cols//2 - 10)
    state = [int(random.random() * 2) for i in range(state)]
    rule = Rule(state=state, rule=rule, center=True)
    rule.evolve(t=rows)


if __name__ == "__main__":
    main()

