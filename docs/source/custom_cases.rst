Creating custom cases
=====================

Creating a custom case requires to define your own python class which derives from a base class which in turn sets all required parameters. The skeleton outline of this new class looks as follows

.. code-block:: python
    :linenos:

    from input.cases.BaseCase.BaseCase import *
    from src.CaseGenerator.Properties.GlobalVariables import *
    import os

    class YourCaseName(BaseCase):
        """Creates the flow setup for YourCaseName"""

        def __init__(self):
            pass

        def create_case(self):
            self.update_case({})

.. note::
    Here, we have used the name ``YourCaseName`` as the class name. You will need to change that to something more relevant to your case. The folder within the ``input/cases`` directory needs to have exactly the same name, including the samel capitalisation (all cases use CamelCase here). For example, if you have a case called ``ChannelFlow``, you need to create a directory ``input/cases/ChannelFlow`` in which you have a python file called ``ChannelFlow.py``, which contains a class definition called ``ChannelFlow``. This naming convention is important as this scheme will be used to discover new cases.

There are two methods that we can use to shape our case setup; the constructor ``__init__`` and the ``create_case`` method.

The constructor ``__init__`` is used to create parameters, using a method that we inherit from the ``BaseCase`` class. In here we can specify parameters that we want to expose to the user that are case specific and can be changed during the simulation setup. For example, we may want the user to be able to change the Reynolds number and turbulence model that is used during the calculation. If this is what we are trying to achieve, then the following code would do that for us

.. code-block:: python
    :linenos:

    from input.cases.BaseCase.BaseCase import *
    from src.CaseGenerator.Properties.GlobalVariables import *
    import os

    class YourCaseName(BaseCase):
        """Creates the flow setup for YourCaseName"""

        def __init__(self):
            self.add_parameters('reynolds_number', 6000000)
            self.add_parameters('rans_model', RansModel.kOmegaSST)

        def create_case(self):
            self.update_case({})

Defining these parameter itself will have no influence on the actual case setup, rather, this provides an interface between the user and the case setup, though the link between the two has to be established by us manually, which we do in the ``create_case()`` method. We can also see here that we don't use a string here to define the RANS turbulence model, rather, we set a predefined value based on a global variable, that we imported at the top of the file. You can look into the global variable files to see which definitions are available.

Next, we have to provide the actual case setup. This is done in the ``create_case()`` method, which calls the base class' ``update_case()`` method, which in turn accepts one parameter which is a dictionary. This dictionary contains all the specific settings that make this case unique, from the mesh, material properties to turbulence model settings and custom post-processing routines. To avoid duplication and out-of-date documentation, you will need to check the ``BaseClass.py`` file within the ``input/cases/BaseClass`` directory, which contains all possible settings, along with comments to explain their usage. We don't have to copy all of this information into our own case, we only need to override those settings that are different for our case (and will, at a minimum, include the mesh, boundary condition and material setup). Suffice to say that the dictionary that is passed into ``update_case()`` contains several sub-dictionary that make up our entire case setup.

Since we have included some parameters in our constructor, let's have a look how we can include these in our setup. Checking the ``update_case()`` method in the BaseClass, we see that the Reynolds number is defined in the ``flow_properties`` sub-dictionary. So we could write the following initially

.. code-block:: python
    :linenos:

    from input.cases.BaseCase.BaseCase import *
    from src.CaseGenerator.Properties.GlobalVariables import *
    import os

    class YourCaseName(BaseCase):
        """Creates the flow setup for YourCaseName"""

        def __init__(self):
            self.add_parameters('reynolds_number', 6000000)
            self.add_parameters('rans_model', RansModel.kOmegaSST)

        def create_case(self):
            self.update_case({
                'flow_properties': {
                    'flow_type': FlowType.incompressible,
                    'const_viscosity': True,
                    'input_parameters_specification_mode': Dimensionality.non_dimensional,
                    'non_dimensional_properties': {
                        'Re': 100,
                    }
                }
            })

We have hard-coded the Reynolds number here on line 19, but we want to use the Reynolds number parameter we defined int he constructor (i.e. line 9). But first, in order to use it, we need to tell the case generator what type of variable we are expecting here and convert it (this is necessary as we later read these parameters from the command line which all by default are text/strings and number will not be usable in calculations). The base class provides some functionality for that, in this case we are expecting the Reynolds number to be of type ``float``, see we can convert the Reynolds number as

.. code-block:: python
    :linenos:

    from input.cases.BaseCase.BaseCase import *
    from src.CaseGenerator.Properties.GlobalVariables import *
    import os

    class YourCaseName(BaseCase):
        """Creates the flow setup for YourCaseName"""

        def __init__(self):
            self.add_parameters('reynolds_number', 6000000)
            self.add_parameters('rans_model', RansModel.kOmegaSST)

        def create_case(self):
            self.update_case({
                'flow_properties': {
                    'flow_type': FlowType.incompressible,
                    'const_viscosity': True,
                    'input_parameters_specification_mode': Dimensionality.non_dimensional,
                    'non_dimensional_properties': {
                        'Re': self.to_float(BaseCase.parameters['reynolds_number']),
                    }
                }
            })

We see that we can access any parameter we defined from the base case's parameter collection (e.g. ``BaseCase.parameters[]``) and that we use the ``self.to_float()`` method to convert our paramter to float. There are alos methods available to convert to ``int`` and ``bool``, i.e. ``self.to_int()`` and ``self.to_bool()``.

Let's look at the RANS turbulence model, which is slightly more involved. There is a section for ``turbulence_properties`` within the case setup's dictionary, so we may extend the ``update_case()`` method as

.. code-block:: python
    :linenos:

    from input.cases.BaseCase.BaseCase import *
    from src.CaseGenerator.Properties.GlobalVariables import *
    import os

    class YourCaseName(BaseCase):
        """Creates the flow setup for YourCaseName"""

        def __init__(self):
            self.add_parameters('reynolds_number', 6000000)
            self.add_parameters('rans_model', RansModel.kOmegaSST)

        def create_case(self):
            self.update_case({
                'flow_properties': {
                    'flow_type': FlowType.incompressible,
                    'const_viscosity': True,
                    'input_parameters_specification_mode': Dimensionality.non_dimensional,
                    'non_dimensional_properties': {
                        'Re': self.to_float(BaseCase.parameters['reynolds_number']),
                    }
                },
                'turbulence_properties': {
                    'turbulence_type': TurbulenceType.rans,
                    'RansModel': self.to_python_expression(BaseCase.parameters['rans_model']),
                },
            })

Here, we are using anoher method ``self.to_python_expression()``, which we invoke on the RANS model selection. We do that since we are accessing a global variable, but when we set this global variable, python has no idea that we mean that, it just interprets everything as a string as mentioned above so we need to tell python to treat this variable as python code, rather than a string, so we use this conversion routine to allow for using global variables as well during our case setup.

In this way, we can set up any other case in a similar fashion, you can examine the example cases that come with the case generator to get an idea of how to setup cases in general and what options we have available. To generate your case then, you use the same command as described in the :doc:`usage <usage>` section 