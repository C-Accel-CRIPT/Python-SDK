---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: "1.3"
      jupytext_version: 1.13.6
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

This tutorial guides you through an example material synthesis workflow using the CRIPT Python SDK.

Before you start, make sure the [cript](https://pypi.org/project/cript/) python package is installed.

## Installation

```bash
pip install cript
```

# Connect to CRIPT

To connect to CRIPT, you must enter a `host` and an `API Token`. For most users, `host` will be `https://criptapp.org`.

!!! Warning "Keep API Token Secure"
To ensure security, avoid storing sensitive information like tokens directly in your code.
Instead, use environment variables.
Storing tokens in code shared on platforms like GitHub can lead to security incidents.
Anyone that possesses your token can impersonate you on the [CRIPT](https://criptapp.org/) platform.
Consider [alternative methods for loading tokens with the CRIPT API Client](). <!--- trunk-ignore(markdownlint/MD042) -->
In case your token is exposed be sure to immediately generate a new token to revoke the access of the old one
and keep the new token safe.

```python
import cript

with cript.API(host="http://development.api.mycriptapp.org/", token="123456"):
    pass
```

You may notice, that we are not executing any code inside the context manager block.
If you were to write a python script, compared to a jupyter notebook, you would add all the following code inside that block.
Here in a jupyter notebook, we need to connect manually. We just have to remember to disconnect at the end.

```python
api = cript.API("http://development.api.mycriptapp.org/", None)
api = api.connect()
```

# Create a Project

All data uploaded to CRIPT must be associated with a [project](../../nodes/primary_nodes/project) node.
[Project](../../nodes/primary_nodes/project) can be thought of as an overarching research goal.
For example, finding a replacement for an existing material from a sustainable feedstock.

```python
# create a new project in the CRIPT database
project = cript.Project(name="My first project.")
```

# Create a Collection node

For this project, you can create multiple collections, which represent a set of experiments.
For example, you can create a collection for a specific manuscript,
or you can create a collection for initial screening of candidates and one for later refinements etc.

So, let's create a collection node and add it to the project.

```python
collection = cript.Collection(name="Initial screening")
# We add this collection to the project as a list.
project.collection += [collection]
```

!!! note "Viewing CRIPT JSON"
Note, that if you are interested into the inner workings of CRIPT,
you can obtain a JSON representation of your data graph at any time to see what is being sent to the API.

```python
print(project.json)
print("\nOr more pretty\n")
print(project.get_json(indent=2).json)
```

# Create an Experiment node

The [collection node](../../nodes/primary_nodes/collection) holds a series of
[Experiment nodes](../../nodes/primary_nodes/experiment) nodes.

And we can add this experiment to the collection of the project.

```python
experiment = cript.Experiment(name="Anionic Polymerization of Styrene with SecBuLi")
collection.experiment += [experiment]
```

# Create an Inventory

An [Inventory](../../nodes/primary_nodes/inventory) contains materials,
that are well known and usually not of polymeric nature.
They are for example the chemical you buy commercially and use as input into your synthesis.

For this we create this inventory by adding the [Material](../../nodes/primary_nodes/material) we need one by one.

```python
# create a list of identifiers as dictionaries to
# identify your material to the community and your team
my_solution_material_identifiers = [
    {"chemical_id": "598-30-1"}
]

solution = cript.Material(
    name="SecBuLi solution 1.4M cHex",
    identifiers=my_solution_material_identifiers
)
```

These materials are simple, notice how we use the SMILES notation here as an identifier for the material.
Similarly, we can create more initial materials.

```python
toluene = cript.Material(name="toluene", identifiers=[{"smiles": "Cc1ccccc1"}, {"pubchem_id": 1140}])
styrene = cript.Material(name="styrene", identifiers=[{"smiles": "c1ccccc1C=C"}, {"inchi": "InChI=1S/C8H8/c1-2-8-6-4-3-5-7-8/h2-7H,1H2"}])
butanol = cript.Material(name="1-butanol", identifiers=[{"smiles": "OCCCC"}, {"inchi_key": "InChIKey=LRHPLDYGYMQRHN-UHFFFAOYSA-N"}])
methanol = cript.Material(name="methanol", identifiers=[{"smiles": "CO"}, {"names": ["Butan-1-ol", "Butyric alcohol", "Methylolpropane", "n-Butan-1-ol", "methanol"]}])
```

Now that we defined those materials, we can combine them into an inventory
for easy access and sharing between experiments/projects.

```python
inventory = cript.Inventory(
    name="Common chemicals for poly-styrene synthesis",
    material=[solution, toluene, styrene, butanol, methanol],
)
collection.inventory += [inventory]
```

# Create a Process node

A [Process](../../nodes/primary_nodes/process) is a step in an experiment.
You decide how many [Process](../../nodes/primary_nodes/process) are required for your experiment,
so you can list details for your experiment as fine-grained as desired.
Here we use just one step to describe the entire synthesis.

```python
process = cript.Process(
    name="Anionic of Synthesis Poly-Styrene",
    type="multistep",
    description="In an argon filled glove box, a round bottom flask was filled with 216 ml of dried toluene. The "
    "solution of secBuLi (3 ml, 3.9 mmol) was added next, followed by styrene (22.3 g, 176 mmol) to "
    "initiate the polymerization. The reaction mixture immediately turned orange. After 30 min, "
    "the reaction was quenched with the addition of 3 ml of methanol. The polymer was isolated by "
    "precipitation in methanol 3 times and dried under vacuum.",
)
experiment.process += [process]
```

# Add Ingredients to a Process

From a chemistry standpoint, most experimental processes, regardless of whether they are carried out in the lab
or simulated using computer code, consist of input ingredients that are transformed in some way.
Let's add ingredients to the [Process](../../nodes/primary_nodes/process) that we just created.
For this we use the materials from the inventory.
Next, define [Quantities](../../nodes/subobjects/quantity) nodes indicating the amount of each
[Ingredient](../../nodes/subobjects/ingredient) that we will use in the [Process](../../nodes/primary_nodes/process).

```python
initiator_qty = cript.Quantity(key="volume", value=1.7e-8, unit="m**3")
solvent_qty = cript.Quantity(key="volume", value=1e-4, unit="m**3")
monomer_qty = cript.Quantity(key="mass", value=0.455e-3, unit="kg")
quench_qty = cript.Quantity(key="volume", value=5e-3, unit="m**3")
workup_qty = cript.Quantity(key="volume", value=0.1, unit="m**3")
```

Now we can create an [Ingredient](../../nodes/subobjects/ingredient)
node for each ingredient using the [Material](../../nodes/primary_nodes/material)
and [quantities](../../nodes/subobjects/quantities) attributes.

```python
initiator = cript.Ingredient(
    keyword=["initiator"], material=solution, quantity=[initiator_qty]
)

solvent = cript.Ingredient(
    keyword=["solvent"], material=toluene, quantity=[solvent_qty]
)

monomer = cript.Ingredient(
    keyword=["monomer"], material=styrene, quantity=[monomer_qty]
)

quench = cript.Ingredient(
    keyword=["quench"], material=butanol, quantity=[quench_qty]
)

workup = cript.Ingredient(
    keyword=["workup"], material=methanol, quantity=[workup_qty]
)

```

Finally, we can add the `Ingredient` nodes to the `Process` node.

```python
process.ingredient += [initiator, solvent, monomer, quench, workup]
```

# Add Conditions to the Process

Its possible that our `Process` was carried out under specific physical conditions. We can codify this by adding
[Condition](../../nodes/subobjects/condition) nodes to the process.

```python
temp = cript.Condition(key="temperature", type="value", value=25, unit="celsius")
time = cript.Condition(key="time_duration", type="value", value=60, unit="min")
process.condition = [temp, time]
```

# Add a Property to a Process

We may also want to associate our process with certain properties. We can do this by adding
[Property](../../nodes/subobjects/property) nodes to the process.

```python
yield_mass = cript.Property(key="yield_mass", type="number", value=47e-5, unit="kilogram", method="scale")
process.property += [yield_mass]
```

# Create a Material node (process product)

Along with input [Ingredients](../../nodes/subobjects/ingredient), our [Process](../../nodes/primary_nodes/process)
may also produce product materials.

First, let's create the [Material](../../nodes/primary_nodes/material)
that will serve as our product. We give the material a `name` attribute and add it to our
[Project]((../../nodes/primary_nodes/project).

```python
polystyrene = cript.Material(name="polystyrene", identifiers=[])
project.material += [polystyrene]
```

Let's add some `Identifiers` to the material to make it easier to identify and search.

```python
# create a name identifier
polystyrene.identifiers += [{"names": ["poly(styrene)", "poly(vinylbenzene)"]}]

# create a BigSMILES identifier
polystyrene.identifiers += [{"bigsmiles": "[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"}]
# create a chemical repeat unit identifier
polystyrene.identifiers += [{"chem_repeat": ["C8H8"]}]
```

Next, we'll add some [Property](../../nodes/subobjects/property) nodes to the
[Material](../../nodes/primary_nodes/material) , which represent its physical or virtual
(in the case of a simulated material) properties.

```python
# create a phase property
phase = cript.Property(key="phase", value="solid", type="none", unit=None)
# create a color property
color = cript.Property(key="color", value="white", type="none", unit=None)

# add the properties to the material
polystyrene.property += [phase, color]
```

**Congratulations!** You've just created a process that represents the polymerization reaction of Polystyrene, starting with a set of input ingredients in various quantities, and ending with a new polymer with specific identifiers and physical properties.

Now we can save the project to CRIPT via the api object.

```python
project.validate()
print(project.get_json(indent=2, condense_to_uuid={}).json)
# api.save(project)
```

```python
# Don't forget to disconnect once everything is done
api.disconnect()
```
