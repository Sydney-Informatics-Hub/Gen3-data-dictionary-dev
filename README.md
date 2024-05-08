# Gen3-data-dictionary-dev

This repository contains dev notes and instructions for how to create and manage a Gen3 data dictionary using the [Australian BioCommons Gen3 Schema Dev tools](https://github.com/AustralianBioCommons/gen3schemadev) and [UMCCR-dictionary](https://github.com/AustralianBioCommons/umccr-dictionary) for USyd use cases.  

## Set up and tooling

Run notebooks provided here with [PyCharm community edition](https://www.jetbrains.com/pycharm/download) or VScode. 

## Generate the schema DAG

See [USyd gen3 data dictionary repo](https://github.com/Sydney-Informatics-Hub/usyd-gen3-data-dictionary). 

1. Get a copy of the code 

```bash
test -d usyd-gen3-data-dictionary || git submodule add https://github.com/Sydney-Informatics-Hub/usyd-gen3-data-dictionary usyd-gen3-data-dictionary
```

2. Launch containers. Need to have Docker desktop installed to run the following commands: 

```bash
cd ./usyd-gen3-data-dictionary && git pull
make pull # pull updates/dependencies for project
make up # spin up containers 
make ps # display status of containers
```

3. Refactor the yamls into json 

```bash 

make compile program=thyroid # write schema to json 
make validate program=thyroid # do validation checks
```

4. Generate and visualise the DAG 

```bash
open http://localhost:8080/#schema/thyroid_dev.json
```