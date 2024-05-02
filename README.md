# Gen3-data-dictionary-dev

This repository contains dev notes and instructions for how to create and manage a Gen3 data dictionary using the [Australian BioCommons Gen3 Schema Dev repository](https://github.com/AustralianBioCommons/gen3schemadev) for USyd use cases.  

## Set up and tooling

Run notebooks provided here with [PyCharm community edition](https://www.jetbrains.com/pycharm/download) or VScode. Notebooks/scripts TBC. 

### Gen3 schema dev repository

Contains tools and notebooks for creating and managing Gen3 data dictionaries used by Australian BioCommons to automate routine tasks with Gen3. 

* [`gen3schemadev`](https://github.com/AustralianBioCommons/gen3schemadev/tree/main/gen3schemadev) is an object relational mapping library for Gen3 schemas
* [`jupyter`](https://github.com/AustralianBioCommons/gen3schemadev/tree/main/jupyter) contains notebooks for schema development and schema development using gdocs as a template, and plausible/synthetic data creation. 

## Creating a schema from existing data dictionary 

See [`schema_template_framework.ipynb`](schema_template_framework.ipynb) for example of how we used the Kidsfirst data dictionary as a template for a new schema for a different project. Used `gen3schemadev` library to work with the bundle. Before running do the following: 

```bash
# Clone kf-dictionary repository, will be using this as template: 
git clone https://github.com/uc-cdis/kf-dictionary.git
```

```bash
# Clone Australian BioCommons schema repository, this is where we will save thyroid schema:
git clone https://github.com/AustralianBioCommons/gen3schemadev.git
```

```bash
# Copy the kf yamls across to the AustralianBioCommons/gen3schemadev codebase: 
mkdir ./gen3schemadev/schema/kidsfirst
cp -r kf-dictionary/gdcdictionary/schemas/* ./gen3schemadev/schema/kidsfirst
```

```python
# Setup virtual environment and install libraries from gen3schemadev 
python3 -m venv .venv
source .venv/bin/activate
cd ./gen3schemadev && pip3 install -r requirements.txt
python3 
```

```python
import os
import gen3schemadev
import networkx as nx
from gen3schemadev.schemabundle import ConfigBundle
import pandas as pd
```

### Remove unwanted objects from the new schema

```python
bundle = ConfigBundle("/Users/gsam0138/Documents/Projects/Gen3-data-dictionary-dev/gen3schemadev/schema/kidsfirst")
bundle.objects['participant.yaml'].get_data()

data = []
for obj in bundle.objects:
    for attrib in bundle.objects[obj].get_properties():
        data.append({"object":obj,"property":attrib})
dataframe = pd.DataFrame(data)
dataframe.to_excel("./kf_objects.xlsx",index=False)
```

Manually remove rows from Excel doc for objects that are not needed in the new schema. The following objects have been removed in their entirety:  

* `aliquot.yaml`
* `submitted_aligned_reads.yaml`
* `submitted_unaligned_reads.yaml`
* `alignment_workflow.yaml`
* `run_metadata.yaml`
* `germline_variation_index.yaml`
* `annotated_somatic_mutation.yaml`
* `simple_somatic_mutation.yaml`
* `aligned_reads_metric.yaml`
* `somatic_mutation_index.yaml`
* `read_group.yaml`
* `somatic_annotation_workflow.yaml`
* `aligned_reads_index.yaml`
* `germline_mutation_calling_workflow.yaml`
* `family.yaml`
* `simple_germline_variation.yaml`
* `read_group_qc.yaml`
* `family_relationship.yaml`
* `somatic_mutation_calling_workflow.yaml`
* `aligned_reads.yaml`

```python 
# How was this removed from the bundle

```

### Remove unwanted properties from remaining objects

Trim the following properties from the remaining objects specified in `kf_properties_trimmed.xlsx`. The following have been removed: 

* `participant.yaml`: is_proband, family_id, families, lost_to_followup, days_lost_to_followup, disease_type
* `demographic.yaml`: age_at_last_followup_days, race
* `outcome.yaml`: disease_related, age_at_event_days
* `phenotype.yaml`: hpo_id, snomed_id_phenotype
* `sample.yaml`: time_between_clamping_and_freezing, time_between_excision_and_freezing 

```python
# How was this removed from the bundle
```

### Add new properties to remaining objects

Add the following properties to outcomes in `thyroid_properties_new.xlsx`: 

* `self_report.yaml`
*  `surgery.yaml`

### Add new objects to the schema

Add the following objects to the new schema: 

* `surgery_report.yaml`
* `patient_outcomes.yaml` 

## Resources 

* [UMCCR's Gen3 builder](https://australianbiocommons.github.io/umccr-dictionary/)