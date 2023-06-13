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

Before you start, make sure the `cript` python package is installed.

# Connect to CRIPT

To connect to CRIPT, you must enter a `host` and an `API Token`. For most users, `host` will be `https://criptapp.org`.
Here we assume that your API key is stored in an environment variable called `CRIPT_TOKEN`.
You can export your token like this by executing `export CRIPT_TOKEN="my token text"` on the command line for mac or linux, more permanently, you can add this line to `~/.bashrc` if you are using `bash` as a shell.

```python
import cript

with cript.API("http://development.api.mycriptapp.org/", None):
    pass
```

The `None` arguments signals here, that we read the token from the environment as discussed above.
You may notice, that we are not executing any code inside the context manager block. If you were to write a python script, compared to a jupyter notebook, you would add all of the following code inside that block.
Here in a jupyter notebook, we need to connect manually. We just have to remember to disconnect at the end.

```python
api = cript.API("http://development.api.mycriptapp.org/", None)
api = api.connect()
```

# Create a Project

All data uploaded to CRIPT must be associated with a `Project` node. `Project` can be thought of as an overarching research goal. For example finding a replacement for an existing material from a sustainable feedstock.

```python
# create a new project in the CRIPT database
project = cript.Project(name="My first project.")
```

# Create a Collection node

For this project you can create multiple collections, which represent a set of experiments.
For example, you can create a collection for a specific manuscript, or you can create a collection for initial screening of candidates and one for later refinements etc.

So, let's create a collection node and add it to the project.

```python
collection = cript.Collection(name="Initial screening")
# We add this collection to the project as a list.
project.collection += [collection]
```

Note, that if you are interested into the inner workings of CRIPT, you can obtain a JSON representation of your data graph at any time.

```python
print(project.json)
print("\nOr more pretty\n")
print(project.get_json(indent=2).json)
```

# Create an Experiment node

The collection holds a series of `Experiment` nodes.
Every experiment holds processes and data related this particular experiment.

And we can add this experiment to the collection of the project.

```python
experiment = cript.Experiment(name="Anionic Polymerization of Styrene with SecBuLi")
collection.experiment += [experiment]
```

# Create an Inventory

An `Inventory` contains materials, that are well known and usually not of polymeric nature.
The are for example the chemical you buy commercially and use as input into your synthesis.

For this we create this inventory by adding the `Material`s we need one by one.

```python
solution = cript.Material(name="SecBuLi solution 1.4M cHex", identifiers=[{"smiles": "[Li]C(C)CC"}])
```

These materials are simple, notice how we use the SMILES notation here as an identifier for the material.
Similarly, we can create more initial materials.

```python
toluene = cript.Material(name="toluene", identifiers=[{"smiles": "Cc1ccccc1"}])
styrene = cript.Material(name="styrene", identifiers=[{"smiles": "c1ccccc1C=C"}])
butanol = cript.Material(name="1-butanol", identifiers=[{"smiles": "OCCCC"}])
methanol = cript.Material(name="methanol", identifiers=[{"smiles": "CO"}])
```

Now that we defined those materials, we can combine them into an inventory for easy access and sharing between experiments/projects.

```python
inventory = cript.Inventory(name="Common chemicals for poly-styrene synthesis", material=[solution, toluene, styrene, butanol, methanol])
collection.inventory += [inventory]
```

# Create a Process node

A `Process` is a step in an experiment. You decide how many `Process` are required for your experiment, so you can list details for your experiment as fine grained as desired.
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

From a chemistry standpoint, most experimental processes, regardless of whether they are carried out in the lab or simulated using computer code, consist of input ingredients that are transformed in some way. Let's add ingredients to the `Process` that we just created.
For this we use the materials from the inventory.
Next, define `Quantity` nodes indicating the amount of each `Ingredient` that we will use in the `Process`.

```python
initiator_qty = cript.Quantity(key="volume", value=1.7e-8, unit="m**3")
solvent_qty = cript.Quantity(key="volume", value=1e-4, unit="m**3")
monomer_qty = cript.Quantity(key="mass", value=0.455e-3, unit="kg")
quench_qty = cript.Quantity(key="volume", value=5e-3, unit="m**3")
workup_qty = cript.Quantity(key="volume", value=0.1, unit="m**3")
```

Now we can create an `Ingredient` node for each ingredient using the `material` and `quantities` attributes.

```python
initiator = cript.Ingredient(keyword=["initiator"], material=solution, quantity=[initiator_qty])
solvent = cript.Ingredient(keyword=["solvent"], material=toluene, quantity=[solvent_qty])
monomer = cript.Ingredient(keyword=["monomer"], material=styrene, quantity=[monomer_qty])
quench = cript.Ingredient(keyword=["quench"], material=butanol, quantity=[quench_qty])
workup = cript.Ingredient(keyword=["workup"], material=methanol, quantity=[workup_qty])
```

Finally, we can add the `Ingredient` nodes to the `Process` node.

```python
process.ingredient += [initiator, solvent, monomer, quench, workup]
```

# Add Conditions to the Process

Its possible that our `Process` was carried out under specific physical conditions. We can codify this by adding `Condition` nodes to the process.

```python
temp = cript.Condition(key="temperature", type="value", value=25, unit="celsius")
time = cript.Condition(key="time_duration", type="value", value=60, unit="min")
process.condition = [temp, time]
```

# Add a Property to a Process

We may also want to associate our process with certain properties. We can do this by adding `Property` nodes to the process.

```python
yield_mass = cript.Property(key="yield_mass", type="number", value=47e-5, unit="kilogram", method="scale")
process.property += [yield_mass]
```

# Create a Material node (process product)

Along with input `Ingredients`, our `Process` may also produce product materials.

First, let's create the `Material` that will serve as our product. We give the material a `name` attribute and add it to our `Project`.

```python
polystyrene = cript.Material(name="polystyrene", identifiers=[])
project.material += [polystyrene]
```

Let's add some `Identifier`s to the material to make it easier to identify and search.

```python
# create a name identifier
polystyrene.identifiers += [{"names": ["poly(styrene)", "poly(vinylbenzene)"]}]

# create a BigSMILES identifier
polystyrene.identifiers += [{"bigsmiles": "[H]{[>][<]C(C[>])c1ccccc1[<]}C(C)CC"}]
# create a chemical repeat unit identifier
polystyrene.identifiers += [{"chem_repeat": ["C8H8"]}]
```

Next, we'll add some `Property` nodes to the `Material`, which represent its physical or virtual (in the case of a simulated material) properties.

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
print(project.get_json(indent=2).json)
# api.save(project)
```

```python
# Don't forget to disconnect once everything is done
api.disconnect()
```
