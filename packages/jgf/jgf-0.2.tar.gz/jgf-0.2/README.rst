
JGF(Z) format implementation
============================

This package implements export and import functions for the JSON Graph Format (gZipped) ``JGF(Z)`` (https://jsongraphformat.info). Supported input formats/libraries are ``networkx``\ , ``igraph``\ , ``numpy`` matrices and ``JXNF`` files. All network, node and edges attributes are saved as well.

Authors
^^^^^^^


* `Filipi N. Silva <filsilva@iu.edu>`_


.. raw:: html

   <!-- ### Contributors
   - Franco Pestilli (franpest@indiana.edu) -->




.. raw:: html

   <!-- ### Funding  -->
   <!-- [![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853) -->





.. raw:: html

   <!-- ### Citations

   1. Adai, Alex T., Shailesh V. Date, Shannon Wieland, and Edward M. Marcotte. "LGL: creating a map of protein function with an algorithm for visualizing very large biological networks." Journal of molecular biology 340, no. 1 (2004): 179-190. [https://doi.org/10.1016/j.jmb.2004.04.047](https://doi.org/10.1016/j.jmb.2004.04.047) -->



Installation
------------

You can install this package using ``pip``\ :

.. code-block:: bash

   pip install jgf

or install it from this git repository:

.. code-block:: bash

   git clone <repository URL>
   cd <repository PATH>
   pip install -e ./

Example of use
--------------

To use the library in igraph environment simply import the correct module and run ``save`` or ``load`` functions:

.. code-block:: python

   import igraph as ig
   import jgf.igraph as jig

   g = ig.Graph.Famous("Zachary")

   # will save a compressed file
   jig.save(g,"zachary.jgfz")

   g, = jig.load("zachary.jgfz")
