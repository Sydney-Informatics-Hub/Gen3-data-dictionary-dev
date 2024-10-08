import gen3schemadev
import pandas as pd

def generate_objects_sheet(bundle : gen3schemadev.ConfigBundle):
    columns = ["ID","TITLE","CATEGORY","DESCRIPTION","DEFINITION_REFS","NAMESPACE","SYSTEM_PROPERTIES"]
    data=[]
    for object_name in bundle.objects:
        obj = bundle.objects[object_name]
        try:
            obj.get_namespace()
        except KeyError:
            obj.set_namespace("")

        try:
            referred_props = obj.get_properties()["$ref"].strip()
            if referred_props == "_definitions.yaml#/ubiquitous_properties":
                referred_props = ""
            else:
                referred_props = f"""[{referred_props.split("/")[1]}]"""
        except Exception:
            referred_props = ""


        obj_data = {columns[0]:obj.get_id(),
                    columns[1]: obj.get_title(),
                    columns[2]: obj.get_category().value,
                    columns[3]: obj.get_description(),
                    columns[4]: referred_props,
                    columns[5]: obj.get_namespace(),
                    columns[6]: ";".join(obj.get_systemProperties())}
        data.append(obj_data)
    return pd.DataFrame(data)


def get_link_data(link: gen3schemadev.Gen3Link, id: str, group: gen3schemadev.Gen3LinkGroup | None = None, group_name = None):
    columns = ["SCHEMA", "NAME", "PARENT", "BACKREF", "LABEL", "MULTIPLICITY", "REQUIRED", "SUBGROUP", "EXCLUSIVE",
               "SG_REQUIRED"]
    data = {}
    link_data = link.get_data()

    if group:
        group_data = group.get_data()
    else:
        group_data = {}

    data[columns[0]] = id
    data[columns[1]] = link_data["name"]
    data[columns[2]] = link_data["target_type"]
    data[columns[3]] = link_data["backref"]
    data[columns[4]] = link_data["label"]
    data[columns[5]] = link_data["multiplicity"]
    data[columns[6]] = link_data.get("required", None)
    data[columns[7]] = group_name
    data[columns[8]] = group_data.get("exclusive", None)
    data[columns[9]] = group_data.get("required", None)
    return data

def generate_links_sheet(bundle: gen3schemadev.ConfigBundle):

    data = []

    for object_name in bundle.objects:
        obj = bundle.objects[object_name]
        object_name = object_name[:-5]
        grp_id = 1
        for link in obj.get_links():
            if isinstance(link,gen3schemadev.Gen3LinkGroup):
                group_name = f"""{object_name}_{grp_id}"""
                # Need to work out what this schema counts thing is meant to be about
                # And test on yaml files where there are subgroups present - e.g. annotation
                # schema_counts[object_name] = schema_counts.get(object_name, 1) + 1
                grp_id = grp_id+1
                for l in link.get_links():
                    link_data = get_link_data(l, obj.get_id(), link, group_name)
                    data.append(link_data)
            else:
                data.append(get_link_data(link,obj.get_id()))
    return pd.DataFrame(data)


def generate_properties_sheets(bundle: gen3schemadev.ConfigBundle):
    columns = ["VARIABLE_NAME", "OBJECT", "REQUIRED", "TYPE", "DESCRIPTION", "ARRAY_ITEMS_TYPE", "PREFERRED",
               "FORMAT", "PATTERN", "NUM_MIN", "NUM_MAX", "UNITS", "TERM", "TERM_REF", "TERM_SOURCE", "TERM_ID",
               "TERM_URL", "CDE_ID", "CDE_VERSION"]
    
    enum_columns = ["type_name", "enum", "enum_definition", "source", "term_id", "version"]
    
    data = []
    enum_data = []
    
    enum_id = 1

    for object_name in bundle.objects:
        obj = bundle.objects[object_name]
        properties = obj.get_properties()
        for prop in properties:
            prop_data = properties[prop]

            # skip referred props
            if isinstance(prop_data,str):
                continue

            # Collect any term data
            term_data = prop_data.get("termDef", {})
            if isinstance(term_data, list):
                # Property has a list of associated terms
                keys = ["term","source","term_id","term_version","term_url","cde_id","cde_version"]
                res = {k: [] for k in keys}
                for d in term_data:
                    for k in res.keys():
                        res[k].append(d.get(k, None))
                term_data = res
            
            # Handle enum properties
            enum_type = None
            if "enum" in prop_data:
                enum_type = f"enum_{enum_id}"
                enum_id = enum_id + 1

                if "enumDef" in prop_data:
                    enumDef = pd.DataFrame(prop_data["enumDef"]).set_index("enumeration")
                else:
                    enumDef = pd.DataFrame()
                
                for enum in prop_data["enum"]:
                
                    enum_dict = {enum_columns[0]: enum_type,
                                 enum_columns[1]: enum,
                    }

                    if enum in enumDef.index:
                        enum_dict[enum_columns[2]] = enum
                        enum_dict[enum_columns[3]] = enumDef.at[enum,"source"]
                        enum_dict[enum_columns[4]] = enumDef.at[enum,"term_id"]
                        enum_dict[enum_columns[5]] = enumDef.at[enum,"version_date"]

                    enum_data.append(enum_dict)
            

            prop_dict = {columns[0]: prop,
                         columns[1]: obj.get_id(),
                         columns[2]: prop in obj.get_required(),
                         columns[3]: prop_data.get("type", enum_type), #What about multiple types?
                         columns[4]: prop_data.get("description", None),
                         columns[5]: prop_data.get("items", {}).get("type", None),
                         columns[6]: prop in obj.get_data().get("preferred", []),
                         columns[7]: prop_data.get("format", None),
                         columns[8]: prop_data.get("pattern", None), # pattern could get pushed to _definitions.yaml or _terms.yaml for terms. Follow?
                         columns[9]: prop_data.get("minimum", None),
                         columns[10]: prop_data.get("maximum", None),
                         columns[11]: prop_data.get("units", None), #this is a guess
                         columns[12]: term_data.get("term", None),
                         columns[13]: prop_data.get("term", {}).get("$ref", None), 
                         # if a term is only in the yaml by ref, do we want to grab the ref and populated other fields?
                         columns[14]: term_data.get("source", None),
                         columns[15]: term_data.get("term_id", None), # what about term_version?
                         columns[16]: term_data.get("term_url", None),
                         columns[17]: term_data.get("cde_id", None),
                         columns[18]: term_data.get("cde_version", None),
            }

            data.append(prop_dict)

    return pd.DataFrame(data), pd.DataFrame(enum_data)


if __name__ == "__main__":
    FOLDER = "schema/thyroid"
    bundle= gen3schemadev.ConfigBundle(FOLDER)

    obj_sheet = generate_objects_sheet(bundle)
    link_sheet = generate_links_sheet(bundle)
    properties_sheet, enum_sheet = generate_properties_sheets(bundle)
    
    with pd.ExcelWriter('output.xlsx') as writer:
        obj_sheet.to_excel(writer, sheet_name='object_definitions')
        link_sheet.to_excel(writer, sheet_name='link_definitions')
        properties_sheet.to_excel(writer, sheet_name='property_definitions')
        enum_sheet.to_excel(writer, sheet_name='enum_definitions')