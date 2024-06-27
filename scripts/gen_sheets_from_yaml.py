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
                    columns[2]: obj.get_category(),
                    columns[3]: obj.get_description(),
                    columns[4]: referred_props,
                    columns[5]: obj.get_namespace(),
                    columns[6]: ";".join(obj.get_systemProperties())}
        data.append(obj_data)
    return pd.DataFrame(data)

def get_link_data(link: gen3schemadev.Gen3Link, id: str, group_name = None):
    columns = ["SCHEMA", "NAME", "PARENT", "BACKREF", "LABEL", "MULTIPLICITY", "REQUIRED", "SUBGROUP", "EXCLUSIVE",
               "SG_REQUIRED"]
    data = {}
    link_data = link.get_data()

    data[columns[0]] = id
    data[columns[1]] = link_data["name"]
    data[columns[2]] = link_data["target_type"]
    data[columns[3]] = link_data["backref"]
    data[columns[4]] = link_data["label"]
    data[columns[5]] = link_data["multiplicity"]
    data[columns[6]] = link_data.get("required", None)
    data[columns[7]] = link_data.get("subgroup", None)
    data[columns[8]] = link_data.get("exclusive", None)
    data[columns[9]] = link_data.get("sg_required", None)
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
                schema_counts[object_name] = schema_counts.get(object_name, 1) + 1
                grp_id = grp_id+1
                for link in link.get_links():
                    link_data = get_link_data(link, obj.get_id() ,group_name)
                    data.append(link_data)
            else:
                data.append(get_link_data(link,obj.get_id()))
    return pd.DataFrame(data)


if __name__ == "__main__":
    FOLDER = "schema/thyroid"
    bundle= gen3schemadev.ConfigBundle(FOLDER)

    obj_sheet = generate_objects_sheet(bundle)
    link_sheet = generate_links_sheet(bundle)