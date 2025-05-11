import openmc
import openmc.data as data
import numpy as np
import lxml.etree as etree

class Materials2Recipes:
    def __init__(self, input_xml, output_name):

        model = openmc.Model.from_model_xml(input_xml)
        self.materials = model.materials
            
        self.name = output_name

        self.read_and_export()
        return
        
    def read_and_export(self):
        root = etree.Element('recipes')
        for mat in self.materials:
            if mat.depletable:
                recipe = self.recipify(mat)
                root.append(recipe)
        
        recipes = etree.ElementTree(root)
        recipes.write(f'{self.name}.xml', pretty_print=True)
        return
        
    @staticmethod
    def recipify(mat):
        which = set()
        subdict = {}
        for nuc in mat.nuclides:
            z, a, _ = data.zam(nuc.name)
            zaid = z*1000 + a
            percent = nuc.percent
            subdict[zaid] = percent
            which.add(nuc.percent_type)
    
        which = list(which)
        assert(len(which) == 1)
        if which[0] == 'ao':
            which = 'atom'
        else:
            which = 'mass'
            
        recipe = etree.Element('recipe')
        
        name = etree.Element('name')
        name.text = mat.name
        recipe.append(name)
        
        basis = etree.Element('basis')
        basis.text = which
        recipe.append(basis)
    
        for zaid, per in subdict.items():
            nuclide = etree.Element('nuclide')
            
            _id = etree.Element('id')
            _id.text = str(zaid)
            nuclide.append(_id)
            
            comp = etree.Element('comp')
            comp.text = str(per)
            nuclide.append(comp)
    
            recipe.append(nuclide)
        
        return recipe

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("i")
    parser.add_argument("o")
    args = parser.parse_args()
    Materials2Recipes(args.i, args.o)


