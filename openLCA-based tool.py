# -*- coding: utf-8 -*-
"""
Created on Sat May 18 21:42:22 2024

@author: runan
"""

import ifcopenshell

#Import IFC
ifc_file_path = r'C:\Users\runan\Documents\Masterproef\Revit\IFC_PoC_Studentenhuis_DenBlok_masonry_CLT.ifc'
ifc_file = ifcopenshell.open(ifc_file_path)



#Get number of layers for the building elements
def get_number_of_layers(ifc_file_path):
    layers_count = []
    try:
        ifc_file = ifcopenshell.open(ifc_file_path)
    except Exception as e:
        print(f"Error opening IFC file: {e}")
        return []

    # Iterate over entities in the order they appear in the IFC file
    for entity in ifc_file.by_type('IfcBuildingElement'):
        if entity.is_a('IfcSlab') or entity.is_a('IfcWall') or entity.is_a('IfcRoof'):
            layer_count = 0
            if hasattr(entity, 'HasAssociations'):
                for association in entity.HasAssociations:
                    if association.is_a('IfcRelAssociatesMaterial'):
                        material = association.RelatingMaterial
                        if material.is_a('IfcMaterialLayerSetUsage'):
                            layer_count = len(material.ForLayerSet.MaterialLayers)
            layers_count.append(layer_count)

    return layers_count

if __name__ == "__main__":
    layers_count = get_number_of_layers(ifc_file_path)
    print(layers_count)



#Remove zeros
def remove_zeros(my_list):
    return [item for item in my_list if item != 0]

layers_count_no_zeros = remove_zeros(layers_count)
print(layers_count_no_zeros)



#Length of list
def print_list_length(my_list):
    length = len(my_list)
    print(f"The length of the list is: {length}")

print_list_length(layers_count_no_zeros)



#Obtains element types from IFC file
def extract_element_types_from_ifc(ifc_file_path):
    element_types = []
    
    element_classes = ['IfcSlab', 'IfcWall', 'IfcRoof']
    
    for element_class in element_classes:
        for product in ifc_file.by_type(element_class):
            product_type = product.is_a()
            if product_type not in ['IfcBuilding', 'IfcBuildingStorey', 'IfcSite'] and product_type not in element_types:
                element_types.append(product_type)
                
    return element_types

if __name__ == "__main__":
    element_types = extract_element_types_from_ifc(ifc_file_path)
    
    
    
#Obtains materials from each layer of a building element
def get_materials(ifc_file_path):
    materials = []
    try:
        ifc_file = ifcopenshell.open(ifc_file_path)
    except Exception as e:
        print(f"Error opening IFC file: {e}")
        return []

    for entity in ifc_file.by_type('IfcBuildingElement'):
        if entity.is_a('IfcSlab') or entity.is_a('IfcWall') or entity.is_a('IfcRoof'):
            if hasattr(entity, 'HasAssociations'):
                for association in entity.HasAssociations:
                    if association.is_a('IfcRelAssociatesMaterial'):
                        material = association.RelatingMaterial
                        if material.is_a('IfcMaterialLayerSetUsage'):
                            material_layer_set = material.ForLayerSet
                            for layer in material_layer_set.MaterialLayers:
                                if layer.Material:
                                    material_name = layer.Material.Name
                                    materials.append(material_name)

    return materials

if __name__ == "__main__":
    materials = get_materials(ifc_file_path)

    if materials:
        materials_lowercase = [x.casefold() for x in materials]
        print(materials_lowercase)
    else:
        print("No materials found or error reading the IFC file.")
        
    

#Length of list
def print_list_length(my_list):
    length = len(my_list)
    print(f"The length of the list is: {length}")

print_list_length(materials_lowercase)



#Obtains thicknesses from each layer of a building element   
def get_thicknesses(ifc_file_path):
    thicknesses = []
    ifc_file = ifcopenshell.open(ifc_file_path)

    for entity in ifc_file.by_type('IfcBuildingElement'):
        if entity.is_a('IfcSlab') or entity.is_a('IfcWall') or entity.is_a('IfcRoof'):
            if hasattr(entity, 'HasAssociations'):
                for association in entity.HasAssociations:
                    if association.is_a('IfcRelAssociatesMaterial'):
                        material = association.RelatingMaterial
                        if material.is_a('IfcMaterialLayerSetUsage'):
                            for layer in material.ForLayerSet.MaterialLayers:
                                thickness = round(layer.LayerThickness)
                                thicknesses.append(thickness)
    return thicknesses

if __name__ == "__main__":
    thicknesses = get_thicknesses(ifc_file_path)
    print(thicknesses)
    
    
    
#Rounding thicknesses
def round_numbers_to_three_decimals(numbers):
    return [round(num, 2) for num in numbers]

rounded_thicknesses = round_numbers_to_three_decimals(thicknesses)
print(rounded_thicknesses)



#Length of list
def print_list_length(my_list):
    length = len(my_list)
    print(f"The length of the list is: {length}")

print_list_length(rounded_thicknesses)



#Obtains Gross area from each building element    
area_values = []

def collect_quantities(property_definition):
    if 'IfcElementQuantity' == property_definition.is_a():
        for quantity in property_definition.Quantities:
            if 'IfcQuantityArea' == quantity.is_a() and ('GrossArea' == quantity.Name or 'GrossSideArea' == quantity.Name or 'GrossFloorArea' == quantity.Name):
                rounded_value = round(quantity.AreaValue, 3)
                area_values.append(rounded_value)

products = ifc_file.by_type('IfcBuildingElement')

ordered_area_values = []

for product in products:
    product_area_values = [] 
    if product.IsDefinedBy:
        definitions = product.IsDefinedBy
        for definition in definitions:
            if 'IfcRelDefinesByProperties' == definition.is_a():
                property_definition = definition.RelatingPropertyDefinition
                if 'IfcElementQuantity' == property_definition.is_a():
                    for quantity in property_definition.Quantities:
                        if 'IfcQuantityArea' == quantity.is_a() and ('NetArea' == quantity.Name or 'NetSideArea' == quantity.Name or 'NetFloorArea' == quantity.Name):
                            rounded_value = round(quantity.AreaValue, 3)
                            product_area_values.append(rounded_value)
            if 'IfcRelDefinesByType' == definition.is_a():
                type = definition.RelatingType
                if type.HasPropertySets:
                    for property_definition in type.HasPropertySets:
                        if 'IfcElementQuantity' == property_definition.is_a():
                            for quantity in property_definition.Quantities:
                                if 'IfcQuantityArea' == quantity.is_a() and ('NetArea' == quantity.Name or 'NetSideArea' == quantity.Name or 'NetFloorArea' == quantity.Name):
                                    rounded_value = round(quantity.AreaValue, 3)
                                    product_area_values.append(rounded_value)
    ordered_area_values.extend(product_area_values)

print(ordered_area_values)



#Length of list
def print_list_length(my_list):
    length = len(my_list)
    print(f"The length of the list is: {length}")

print_list_length(ordered_area_values)

    

#Multiplies values in a list if it has more layers
def multiply_values(number_list, value_list):
    result = []
    for number, value in zip(number_list, value_list):
        result.extend([value] * number)
    return result

element_types_multiplied = multiply_values(layers_count_no_zeros, element_types)
areas_multiplied = multiply_values(layers_count_no_zeros, ordered_area_values)
print(areas_multiplied)   



#Length of list
def print_list_length(my_list):
    length = len(my_list)
    print(f"The length of the list is: {length}")

print_list_length(areas_multiplied)
   

    
#Obtains the volume from each layer of a building element
def multiply_lists(list1, list2):
    result = []
    for val1, val2 in zip(list1, list2):
        result.append(val1 * (val2)/1000)
    return result

volume_values = multiply_lists(areas_multiplied, rounded_thicknesses)
print(volume_values)


    
#Rounding volumes
def round_numbers_to_three_decimals(numbers):
    return [round(num, 3) for num in numbers]

rounded_volumes = round_numbers_to_three_decimals(volume_values)
print(rounded_volumes)   


    
#Transforms the layer materials to general material categroies   
materials_lowercase = [x.casefold() for x in materials]

def categorize_string(input_string):
    keywords = {
        "hcs": "HCS",
        "clt": "CLT",
        "screed": "SCREED",
        "oak": "WOOD",
        "wood": "WOOD",
        "lumber": "WOOD",
        "plywood": "WOOD",
        "pine": "WOOD",
        "aluminium": "STEEL",
        "steel": "STEEL",
        "metal": "STEEL",
        "iron": "STEEL",
        "brick": "MASONRY",
        "masonry": "MASONRY",
        "concrete": "CONCRETE",
        "rock wool": "INSULATION",
        "glass wool": "INSULATION",
        "flexible insulation": "INSULATION",
        "rigid insulation": "INSULATION",
        "gypsum": "GYPSUM"
    }

    for keyword, category in keywords.items():
        if keyword in input_string:
            return category
    return "OTHER"

def transform_strings(input_list):
    transformed_list = []
    for string in input_list:
        category = categorize_string(string)
        transformed_list.append(category)
    return transformed_list

transformed_materials_list = transform_strings(materials_lowercase)
print(transformed_materials_list)



#Joins material and volume lists
def join_lists_and_remove_other(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length")
    
    result = [f"{item1}-{item2}" if isinstance(item2, str) else f"{item1}-{str(item2)}" for item1, item2 in zip(list1, list2)]
    result = [item for item in result if "OTHER" not in item]
    
    return result

material_volume = join_lists_and_remove_other(transformed_materials_list, rounded_volumes)
print(material_volume)



#Sums up volumes from same material category
def sum_values_by_name(input_list):
    sum_dict = {}
    
    for item in input_list:
        name, value = item.split("-")
        value = float(value)
        if name in sum_dict:
            sum_dict[name] += value
        else:
            sum_dict[name] = value
    
    result = [f"{name}-{value}" for name, value in sum_dict.items()]
    
    return result

summed_volumes = sum_values_by_name(material_volume)



#Rounding summed volumes
import re
def round_numbers_in_list(string_list):
    rounded_list = []
    for item in string_list:
        match = re.search(r'-([\d\.]+)', item)
        if match:
            number = float(match.group(1))
            rounded_number = round(number, 3)
            new_item = re.sub(r'-[\d\.]+', f'-{rounded_number}', item)
            rounded_list.append(new_item)
        else:
            rounded_list.append(item)
    return rounded_list

rounded_summed_volumes = round_numbers_in_list(summed_volumes)
print(rounded_summed_volumes)



#Storing material volumes
def extract_values(input_list):
    masonry_volumes = 0
    insulation_volumes = 0
    concrete_volumes = 0
    gypsum_volumes = 0 
    screed_volumes = 0
    HCS_volumes = 0
    CLT_volumes = 0
    wood_volumes = 0
    steel_volumes = 0
    
    for item in input_list:
        name, value = item.split("-")
        value = float(value)
        if name == "MASONRY":
            masonry_volumes += value
        elif name == "INSULATION":
            insulation_volumes += value
        elif name == "CONCRETE":
            concrete_volumes += value
        elif name == "GYPSUM":
            gypsum_volumes += value
        elif name == "SCREED":
            screed_volumes += value
        elif name == "HCS":
            HCS_volumes += value
        elif name == "CLT":
            CLT_volumes += value
        elif name == "WOOD":
            wood_volumes += value
        elif name == "STEEL":
            steel_volumes += value
    
    
    return masonry_volumes, insulation_volumes, concrete_volumes, gypsum_volumes, screed_volumes, HCS_volumes, CLT_volumes, wood_volumes, steel_volumes

masonry_volumes, insulation_volumes, concrete_volumes, gypsum_volumes, screed_volumes, HCS_volumes, CLT_volumes, wood_volumes, steel_volumes = extract_values(rounded_summed_volumes)

print(masonry_volumes)
print(insulation_volumes)
print(concrete_volumes)
print(screed_volumes)
print(wood_volumes)
print(steel_volumes)
print(HCS_volumes)
print(CLT_volumes)
print(gypsum_volumes)

masonry_mass = masonry_volumes * 955
insulation_mass = insulation_volumes * 20
concrete_mass = concrete_volumes * 2482
screed_mass = screed_volumes * 2000
wood_mass = wood_volumes * 500
steel_mass = steel_volumes * 7850
HCS_mass = HCS_volumes * 1370
CLT_mass = CLT_volumes * 1025
gypsum_mass = gypsum_volumes * 1800

total_mass = masonry_mass + insulation_mass + concrete_mass + screed_mass + wood_mass + steel_mass + HCS_mass + CLT_mass + gypsum_mass



#Create corresponding openLCA processes and product systems
import olca_ipc as ipc
import olca_schema as o

client = ipc.Client(8080) 

cement_flow = client.get(o.Flow, name = "Portland cement")
sand_flow = client.get(o.Flow, name = "Quartz sand (0/2)")
aggregates_flow = client.get(o.Flow, name = "Gravel (2/32)")
water_flow = client.get(o.Flow, name = "Tap water_technology mix_at user_EU-28+3_S")
steel_flow = client.get(o.Flow, name = "Steel hot rolled coil")
softwood_flow = client.get(o.Flow, name = "Sawn wood, softwood_planed, dried_at plant_EU-28+3_S")
brick_flow = client.get(o.Flow, name = "Clay brick (pored)")
insulation_flow = client.get(o.Flow, name = "Glass wool")
hardwood_flow = client.get(o.Flow, name = "Sawn wood, hardwood_planed, dried_at plant_EU-28+3_S")
gypsum_flow = client.get(o.Flow, name = "Gypsum")

mass = client.get(o.FlowProperty, name="Mass")


#Concrete C30/37 process
concrete_C30_flow = o.new_flow("Concrete C30/37", o.FlowType.PRODUCT_FLOW, mass)
client.put(concrete_C30_flow)

concrete_C30 = o.new_process("Concrete C30/37")
o.new_output(concrete_C30, concrete_C30_flow, 2368).is_quantitative_reference = True
o.new_input(concrete_C30, cement_flow, 300)
o.new_input(concrete_C30, sand_flow, 803)
o.new_input(concrete_C30, aggregates_flow, 1100)
o.new_input(concrete_C30, water_flow, 165)
client.put(concrete_C30)

#Reinforced concrete C30/37 process
reinforced_concrete_C30_flow = o.new_flow("Reinforced concrete C30/37", o.FlowType.PRODUCT_FLOW, mass)
client.put(reinforced_concrete_C30_flow)

reinforced_concrete_C30 = o.new_process("Reinforced concrete C30/37")
o.new_output(reinforced_concrete_C30, reinforced_concrete_C30_flow, 2482).is_quantitative_reference = True
o.new_input(reinforced_concrete_C30, steel_flow, 47.52)
o.new_input(reinforced_concrete_C30, concrete_C30_flow, 2353.57)
client.put(reinforced_concrete_C30)


#Steel process
steel = o.new_process("Steel")
o.new_output(steel, steel_flow, 7850).is_quantitative_reference = True
o.new_input(steel, steel_flow, 7850)
client.put(steel)


#Wood process
softwood = o.new_process("Wood")
o.new_output(softwood, softwood_flow, 500).is_quantitative_reference = True
o.new_input(softwood, softwood_flow, 500)
client.put(softwood)


#Cement mortar process
cement_mortar_flow = o.new_flow("Cement mortar", o.FlowType.PRODUCT_FLOW, mass)
client.put(cement_mortar_flow)

cement_mortar = o.new_process("Cement mortar")
o.new_output(cement_mortar, cement_mortar_flow, 2100).is_quantitative_reference = True
o.new_input(cement_mortar, cement_flow, 420)
o.new_input(cement_mortar, sand_flow, 1680)
client.put(cement_mortar)


#Brick process
brick = o.new_process("Brick")
o.new_output(brick, brick_flow, 950).is_quantitative_reference = True
o.new_input(brick, brick_flow, 950)
client.put(brick)


#Masonry process
masonry_flow = o.new_flow("Masonry", o.FlowType.PRODUCT_FLOW, mass)
client.put(masonry_flow)

masonry = o.new_process("Masonry")
o.new_output(masonry, masonry_flow, 955).is_quantitative_reference = True
o.new_input(masonry, brick_flow, 761)
o.new_input(masonry, cement_flow, 39)
o.new_input(masonry, sand_flow, 155)
client.put(masonry)


#Insulation process
insulation = o.new_process("Insulation")
o.new_output(insulation, insulation_flow, 20).is_quantitative_reference = True
o.new_input(insulation, insulation_flow, 20)
client.put(insulation)


#Screed process
screed_flow = o.new_flow("Screed", o.FlowType.PRODUCT_FLOW, mass)
client.put(screed_flow)

screed = o.new_process("Screed")
o.new_output(screed, screed_flow, 2000).is_quantitative_reference = True
o.new_input(screed, cement_flow, 372)
o.new_input(screed, sand_flow, 1480)
o.new_input(screed, water_flow, 148)
client.put(screed)


#CLT process
CLT_flow = o.new_flow("CLT", o.FlowType.PRODUCT_FLOW, mass)
client.put(CLT_flow)

CLT = o.new_process("CLT")
o.new_output(CLT, CLT_flow, 1025).is_quantitative_reference = True
o.new_input(CLT, hardwood_flow, 975)
o.new_input(CLT, steel_flow, 50)
client.put(CLT)


#Concrete C50/60 process
concrete_C50_flow = o.new_flow("Concrete C50/60", o.FlowType.PRODUCT_FLOW, mass)
client.put(concrete_C50_flow)

concrete_C50 = o.new_process("Concrete C50/60")
o.new_output(concrete_C50, concrete_C50_flow, 2453).is_quantitative_reference = True
o.new_input(concrete_C50, cement_flow, 550)
o.new_input(concrete_C50, sand_flow, 745)
o.new_input(concrete_C50, aggregates_flow, 960)
o.new_input(concrete_C50, water_flow, 198)
client.put(concrete_C50)


#HCS process
HCS_flow = o.new_flow("HCS", o.FlowType.PRODUCT_FLOW, mass)
client.put(HCS_flow)

HCS = o.new_process("HCS")
o.new_output(HCS, HCS_flow, 1370).is_quantitative_reference = True
o.new_input(HCS, concrete_C50_flow, 1350)
o.new_input(HCS, steel_flow, 20)
client.put(HCS)


#Gypsum process
gypsum = o.new_process("Gypsum")
o.new_output(gypsum, gypsum_flow, 1800).is_quantitative_reference = True
o.new_input(gypsum, gypsum_flow, 1800)
client.put(gypsum)



#Building process
building_flow = o.new_flow("Building", o.FlowType.PRODUCT_FLOW, mass)
client.put(building_flow)

building = o.new_process("Building")
o.new_output(building, building_flow, total_mass).is_quantitative_reference = True
o.new_input(building, reinforced_concrete_C30_flow, concrete_mass)
o.new_input(building, steel_flow, steel_mass)
o.new_input(building, softwood_flow, wood_mass)
o.new_input(building, masonry_flow, masonry_mass)
o.new_input(building, insulation_flow, insulation_mass)
o.new_input(building, screed_flow, screed_mass)
o.new_input(building, CLT_flow, CLT_mass)
o.new_input(building, HCS_flow, HCS_mass)
o.new_input(building, gypsum_flow, gypsum_mass)
client.put(building)


config = o.LinkingConfig(
    prefer_unit_processes=True,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(concrete_C30, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(reinforced_concrete_C30, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(steel, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(softwood, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(masonry, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(insulation, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(screed, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(CLT, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(concrete_C50, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(HCS, config)

config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(gypsum, config)


config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
system_ref = client.create_product_system(building, config)



    