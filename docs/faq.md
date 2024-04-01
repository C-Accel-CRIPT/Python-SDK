# Frequently Asked Questions

<br/>

**Q:** Where can I find more information about the [CRIPT](https://criptapp.org) data model?

**A:** _Please feel free to review the
[CRIPT data model document](https://pubs.acs.org/doi/suppl/10.1021/acscentsci.3c00011/suppl_file/oc3c00011_si_001.pdf)
and the [CRIPT research paper](https://pubs.acs.org/doi/10.1021/acscentsci.3c00011)_

---

**Q:** What does this error mean?

**A:** _Please visit the Exceptions documentation_

---

**Q:** Where do I report an issue that I encountered?

**A:** _Please feel free to report issues to our [GitHub repository](https://github.com/C-Accel-CRIPT/Python-SDK)._
_We are always looking for ways to improve and create software that is a joy to use!_

---

**Q:** Where can I find more CRIPT examples?

**A:** _Please visit [CRIPT Scripts](https://criptscripts.org) where there are many CRIPT examples ranging from CRIPT graphs drawn out from research papers, Python scripts, TypeScript scripts, and more!_

---

**Q:** Where can I find more example code?

**A:** _We have written a lot of tests for our software, and if needed, those tests can be referred to as example code to work with the Python SDK software. The Python SDK tests are located within the [GitHub repository/tests](https://github.com/C-Accel-CRIPT/Python-SDK/tree/main/tests), and there they are broken down to different kinds of tests_

---

**Q:** How can I contribute to this project?

**A:** _We would love to have you contribute!
Please read our [contributing guidelines](https://github.com/C-Accel-CRIPT/Python-SDK/blob/main/CONTRIBUTING.md)
and our [code of conduct](https://github.com/C-Accel-CRIPT/Python-SDK/blob/main/CODE_OF_CONDUCT.md) to get started.
Feel free to contribute to any bugs you find, any issues within the
[GitHub repository](https://github.com/C-Accel-CRIPT/Python-SDK/issues), or any features you want._

---

**Q:** This repository is awesome, how can I build a plugin to add to it?

**A:** _We have built this code with plugins in mind! Please visit the
[CRIPT Python SDK GitHub repository Wiki](https://github.com/C-Accel-CRIPT/Python-SDK/wiki)
tab for developer documentation._

---

**Q:** Is there documentation detailing the internal workings of the code?

**A:** _Absolutely! For an in-depth look at the CRIPT Python SDK code,
consult the [GitHub repository wiki internal documentation](https://github.com/C-Accel-CRIPT/Python-SDK/wiki)._

---

**Q:** I have this question that is not covered anywhere, where can I ask it?

**A:** _Please visit the [CRIPT Python SDK repository](https://github.com/C-Accel-CRIPT/Python-SDK)
and ask your question within the
[discussions tab Q/A section](https://github.com/C-Accel-CRIPT/Python-SDK/discussions/categories/q-a)_

---

**Q:** Where is the best place where I can contact the CRIPT Python SDK team for questions or support?

**A:** _We would love to hear from you! Please visit our [CRIPT Python SDK Repository GitHub Discussions](https://github.com/C-Accel-CRIPT/cript-excel-uploader/discussions) to easily send us questions.
Our [repository's issue page](https://github.com/C-Accel-CRIPT/Python-SDK/issues) is also another good way to let us know about any issues or suggestions you might have.
A GitHub account is required._

---

**Q:** How can I report security issues?

**A:** _Please visit the [CRIPT Python SDK GitHub repository security tab](https://github.com/C-Accel-CRIPT/Python-SDK/security) for any security issues._

---

**Q:** Where can I find the release notes for each SDK version?

**A:** _The release notes can be found on our
[CRIPT Python SDK repository releases section](https://github.com/C-Accel-CRIPT/Python-SDK/releases)_

---

**Q:** Besides the user documentation, is there any developer documentation that I can read through on how
the code is written to get a better grasp of it?

**A:** _You bet! There are documentation for developers within the
[CRIPT Python SDK Wiki](https://github.com/C-Accel-CRIPT/Python-SDK/wiki).
There you will find documentation on everything from how our code is structure,
how we aim to write our documentation, CI/CD, and more._

---

**Q:** What can I do, when my `api.search(...)` fails with a `cript.nodes.exception.CRIPTJsonDeserializationError` or similar?

**A:** _There is a solution for you. Sometimes CRIPT can contain nodes formatted in a way that the Python SDK does not understand. We can disable the automatic conversion from the API response into SDK nodes. Here is an example of how to achieve this:
```python
# Create API object in with statement, here it assumes host, token, and storage token are in your environment variables
with cript.API() as api:
    # Find the paginator object, which is a python iterator over the search results.
    materials_paginator = cript_api.search(node_type=cript.Material, search_mode=cript.SearchModes.NODE_TYPE)
    # Usually you would do
    # `materials_list = list(materials_paginator)`
    # or
    # for node in materials_paginator:
    #    #do node stuff
    # But now we want more control over the iteration to ignore failing node decoding.
    # And store the result in a list of valid nodes
    materials_list = []
    # We use a while True loop to iterate over the results
    while True:
        # This first try catches, when we reach the end of the search results.
	# The `next()` function raises a StopIteration exception in that case
        try:
	    # First we try to convert the current response into a node directly
            try:
                material_node = next(materials_paginator)
	    # But if that fails, we catch the exception from CRIPT
            except cript.CRIPTException as exc:
                # In case of failure, we disable the auto_load_function temporarily
                materials_paginator.auto_load_nodes = False
		# And only obtain the unloaded node JSON instead
                material_json = next(materials_paginator)
		# Here you can inspect and manually handle the problem.
		# In the example, we just print it and ignore it otherwise
		print(exc, material_json)
            else:
		# After a valid node is loaded (try block didn't fail)
		# we store the valid node in the list
                materials_list += [material_node]
            finally:
	        # No matter what happened, for the next iteration we want to try to obtain
		# an auto loaded node again, so we reset the paginator state.
                materials_paginator.auto_load_nodes = True
        except StopIteration:
	    # If next() of the paginator indicates an end of the search results, break the loop
            break
```


_We try to also have type hinting, comments, and docstrings for all the code that we work on so it is clear and easy for anyone reading it to easily understand._

_if all else fails, contact us on our [GitHub Repository](https://github.com/C-Accel-CRIPT/Python-SDK)._
