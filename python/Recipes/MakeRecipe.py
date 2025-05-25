import openmc
import openmc.data as data
import numpy as np
import lxml.etree as etree

class Materials2Recipes:
    def __init__(self, input_xml, output_name):

        model = openmc.Model.from_model_xml(input_xml)
        self.materials = model.materials
        #self.materials = openmc.Materials.from_xml(input_xml)
            
        self.name = output_name

        self.read_and_export()
        return
        
    def read_and_export(self):
        root = etree.Element('recipes')
        self.mat = self.compressify(self.materials)
        recipe = self.recipify(self.mat)
        root.append(recipe)
        
        recipes = etree.ElementTree(root)
        recipes.write(f'{self.name}.xml', pretty_print=True)
        return

    @staticmethod
    def compressify(materials):
        depletable = [mat.depletable for mat in materials]
        d_materials = list(np.array(materials)[depletable])

        materials_mass = []
        nuc_mass = {}
        for mat in d_materials:
            material_mass = mat.volume*1e-6 * mat.density
            materials_mass += [material_mass]
            for nuc, per, pt in mat.nuclides:
                try:
                    nuc_mass[nuc] += per * material_mass
                except:
                    nuc_mass[nuc] = per * material_mass
                    
        material = openmc.Material()
        for nuc, mass in nuc_mass.items():
            material.add_nuclide(nuc, mass/ sum(materials_mass), 'wo')

        print(sum(materials_mass))
        return material

    
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
            zaid = str(zaid)
            _id.text = '0'*(5-len(zaid)) + zaid
            nuclide.append(_id)
            
            comp = etree.Element('comp')
            comp.text = str(per)
            nuclide.append(comp)
    
            recipe.append(nuclide)
        
        return recipe

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-o")
    args = parser.parse_args()
    Materials2Recipes(args.i, args.o)


