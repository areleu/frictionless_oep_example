import frictionless as fl
from pprint import pprint
import json

def replace_primarykey(resource):
    resource["schema"]["primaryKey"] = "id"
    return resource

def drop_foreignkeys(resource):
    resource["schema"]["primaryKey"] = "id"
    resource["schema"] = {k:v for k,v in resource["schema"].items() if k != "foreignKeys"}
    return resource

def clean_field(field):
    new_field = {k:v for k,v in field.items() if k in ["name", "description", "type"]}
    new_field["type"] = "number" if new_field["type"] in ["int", "bigint"] else new_field["type"]
    return new_field 

def drop_field_extras(resource):
    resource["schema"]["fields"] = [clean_field(f) for f in resource["schema"]["fields"]]
    return resource


def main():
    with open('datapackage\datapackage.json', "r", encoding="utf8") as file:
        descriptor = json.load(file)

    descriptor["resources"] = [replace_primarykey(r) for r in descriptor["resources"]]
    descriptor["resources"] = [drop_foreignkeys(r) for r in descriptor["resources"]]
    descriptor["resources"] = [drop_field_extras(r) for r in descriptor["resources"]]
    package =  fl.Package(descriptor=descriptor)
    
    data = package.get_resource("model_draft.wind_turbine_domestic_lod_geoss_tp_oeo")

    pprint(data.read_rows())

if __name__=="__main__":
    main()