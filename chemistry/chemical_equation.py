from chempy import Substance, Reaction, balance_stoichiometry


class ChemicalEquation():
    def __init__(self, reactants: list, products:list):
        self.reactants = set(reactants)
        self.products = set(products)
    
    
    def stoichimetric_equation(self) -> str:
        reaction = balance_stoichiometry(self.reactants, self.products)
        balanced_reaction = Reaction(*reaction)
        substances = {name: Substance.from_formula(name) for name in balanced_reaction.keys()}
        return balanced_reaction.html(substances)
    
    
if __name__ == "__main__":
    reactants = ['H2', 'O2']
    products = ['H2O']
    equation = ChemicalEquation(reactants, products)
    print(equation.stoichimetric_equation())