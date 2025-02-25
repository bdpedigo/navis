.. _whats_new:

What's new?
===========
This is a selection of features added, changes made and bugs fixed in each version.
For a full list of changes please see the
`commits <https://github.com/schlegelp/navis/commits/master>`_ on navis' Github
repository.

.. list-table::
   :widths: 7 7 86
   :header-rows: 1

   * - Version
     - Date
     -
   * - 0.5.3
     - 10/04/18
     - - new functions: :func:`navis.nblast_smart`, :func:`navis.write_google_binary`, :func:`navis.synblast`, :func:`navis.symmetrize_brain`
       - :func:`navis.plot3d` (plotly): ``hover_name=True`` will show neuron names on hover
       - :func:`navis.plot2d`: ``rasterize=True`` will rasterize neurons (but not axes or labels) to help keep file sizes low
       - :func:`navis.simplify_mesh` now supports 3 backends: Blender3D, ``open3d`` or ``pymeshlab``
       - :func:`navis.make_dotprops` can now produce ``Dotprops`` purely from skeleton edges (set ``k=None``)
       - reworked :func:`navis.write_swc` (faster, easier to work with)
       - a new type of landmark-based transform: moving least square transforms (thanks to Chris Barnes)
       - vispy :class:`navis.Viewer`: press B to show a bounding box
       - moved tests from Travis to Github Actions (this now also includes testing tutorial notebooks)
       - a great many small and big bug fixes
   * - 0.5.2
     - 02/02/21
     - - new functions: :func:`navis.xform`, :func:`navis.write_google_binary`
       - :func:`navis.downsample_neuron` now also works on ``Dotprops``
       - Neurons:
         - connectors are now included in bounding boxes
       - NeuronLists:
         - added progress bar for division / multiplication
   * - 0.5.1
     - 10/01/21
     - - a couple under-the-hood improvements and bugfixes
   * - 0.5.0
     - 05/01/21
     - - new functions for transforming spatial data (locations, neurons, etc) between brain spaces:
           - :func:`navis.xform_brain` transforms data from one space to another
           - :func:`navis.mirror_brain` mirrors data about given axis
           - see the new :ref:`tutorials<example_gallery>` for explanations
           - low-level interfaces to work with affine, H5-, CMTK- and thin plate spline transforms
       - de-cluttered top level namespace: some more obscure functions are now only available through modules
   * - 0.4.3
     - 22/12/20
     - - more small bug fixes
   * - 0.4.2
     - 22/12/20
     - - some small bug fixes
   * - 0.4.1
     - 06/12/20
     - - hotfix for critical bug in NBLAST
   * - 0.4.0
     - 06/12/20
     - - native implementation of NBLAST: :func:`navis.nblast` and :func:`navis.nblast_allbyall`!
       - new parameter :func:`navis.plot3d` (plotly backend) with ``hover_id=True`` will show node IDs on hover
       - :func:`navis.Volume.resize` has now ``inplace=False`` as default
   * - 0.3.4
     - 24/11/20
     - - improved :class:`navis.Dotprops`:
           - more control over generation in :func:`navis.make_dotprops`
           - :class:`navis.Dotprops` now play nicely with R interface
   * - 0.3.3
     - 23/11/20
     - - new module: ``models`` for modelling networks and neurons
       - new functions :func:`navis.resample_along_axis`, :func:`navis.insert_nodes`, :func:`navis.remove_nodes`
       - full rework of :class:`navis.Dotprops`:
           - make them a subclass of BaseNeuron
           - implement ``nat:dotprops`` in :func:`navis.make_dotprops`
           - added :func:`navis.read_nrrd` and :func:`navis.write_nrrd`
           - side-effect: renamed ``navis.from_swc`` -> ``read_swc`` and ``navis.to_swc`` -> ``write_swc``
           - improved conversion between nat and navis ``Dotprops``
       - full rework of topology-related functions:
           - :func:`navis.strahler_index`, :func:`navis.segregation_index`, :func:`navis.bending_flow`, :func:`navis.flow_centrality` and :func:`navis.split_axon_dendrite` now work better, faster and more accurately. See their docs for details.
           - new function: :func:`navis.arbor_segregation_index`
       - new ``color_by`` and ``shade_by`` parameters for ``plot3d`` and ``plot2d`` that lets you color/shade a
         neuron by custom properties (e.g. by Strahler index or compartment)
       - neurons are now more memory efficient:
           - pandas "categoricals" are used for connector and node "type" and "label" columns
           - add a ``.memory_usage`` method analogous to that of ``pandas.DataFrames``
       - :class:`navis.NeuronList` can now be pickled!
       - made :class:`navis.Viewer` faster
       - :func:`navis.prune_twigs` can now (optionally) prune by `exactly` the desired length
       - improved ``navis.NeuronList.apply``
       - small bugfixes and improvements
   * - 0.3.2
     - 18/10/20
     - - :func:`navis.plot2d` and :func:`navis.plot3d` now accept ``trimesh.Trimesh`` directly
       - :func:`navis.in_volume` now works with any mesh-like object, not just ``navis.Volumes``
       - lots of small bugfixes and improvements
   * - 0.3.1
     - 07/10/20
     - - new function :func:`navis.rewire_neuron`
       - improve :func:`navis.heal_fragmented_neuron` and :func:`navis.stitch_neurons`: now much much faster
       - :func:`navis.reroot_neuron` can now reroot to multiple roots in one go
       - :func:`navis.plot3d` now accepts a ``soma`` argument
       - improved caching for neurons
       - improved multiplication/division of neurons
       - faster ``r.nblast`` and ``r.nblast_allbyall``
       - ``r.xform_brain`` now also adjusts the soma radius
       - ``neuprint.fetch_skeletons`` now returns correct soma radius
       - lots of small bugfixes
   * - 0.3.0
     - 06/10/20
     - - started module to manipulate mesh data: see :func:`navis.simplify_mesh`
       - improved interfaces with R NBLAST and ``xform_brain``
       - improved attribute caching for neurons
   * - 0.2.3
     - 06/09/20
     - - new Neuron property ``.label`` that if present will be used for plot legends
       - new function for R interface: :func:`navis.interfaces.r.load_rda`
       - Blender interface: improved scatter plot generation
   * - 0.2.2
     - 15/08/20
     - - new ``plot3d`` parameter: with plotly backend, use ``fig`` to add data to existing plotly figure
       - new ``plot3d`` parameter: with vispy backend, use ``center=False`` to not re-center camera on adding new data
       - new ``r.mirror_brain`` parameter: use e.g. ``via='FCWB'`` if source space does not have mirror transform
       - new ``NeuronList`` method: ``append()`` works like ``list.append()``
       - first implementation of smarter (re-)calculation of temporary Neuron properties using ``.is_stale`` property
       - Neurons can now be multiplied/divided by array/list of x/y/z coordinates for non-isometric transforms
       - fix issues with newer rpy2 versions
       - various improvements and bug fixes
   * - 0.2.1
     - 20/07/20
     - - new ``plot3d`` parameter: with plotly backend, use ``radius=True`` plots TreeNeurons with radius
       - new ``plot2d`` parameter: ``orthogonal=False`` sets view to perspective
       - various improvements to e.g. ```nx2neuron``
   * - 0.2.0
     - 29/06/20
     - - new neuron class :class:`~navis.MeshNeuron` that consists of vertices and faces
       - new :class:`~navis.TreeNeuron` property ``.volume``
       - we now use `ncollpyde <https://pypi.org/project/ncollpyde>`_ for ray casting (intersections)
       - clean-up in neuromorpho interface
       - fix bugs in :class:`~navis.Volume` pickling
       - new example data from the Janelia hemibrain data set
       - breaking changes: :func:``~navis.nx2neuron`` now returns a :class:`~navis.TreeNeuron` instead of a ``DataFrame``
   * - 0.1.16
     - 26/05/20
     - - many small bugfixes
   * - 0.1.15
     - 15/05/20
     - - improvements to R and Blender interface
       - improved loading from SWCs (up to 2x faster)
       - TreeNeurons: allow rerooting by setting the ``.root`` attribute
   * - 0.1.14
     - 05/05/20
     - - emergency fixes for 0.1.13
   * - 0.1.13
     - 05/05/20
     - - new function :func:`navis.vary_color`
       - improvements to Blender interface and various other functions
   * - 0.1.12
     - 02/04/20
     - - :class:`~navis.Volume` is now sublcass of ``trimesh.Trimesh``
   * - 0.1.11
     - 28/02/20
     - - removed hard-coded swapping and translation of axes in the Blender interface
       - improved :func:`navis.stitch_neurons`: much faster now if you have iGraph
       - fixed errors when using multiprocessing (e.g. in ``NeuronList.apply``)
       - fixed bugs in :func:`navis.downsample_neuron`
   * - 0.1.10
     - 24/02/20
     - - fixed bugs in Blender interface introduced in 0.1.9
   * - 0.1.9
     - 24/02/20
     - - removed hard-coded swapping and translation of axes in the Blender interface
       - fixed bugs in stitch_neurons
   * - 0.1.8
     - 21/02/20
     - - Again lots of fixed bugs
       - Blame myself for not keeping track of changes
   * - 0.1.0
     - 23/05/19
     - - Made lots of fixes
       - Promised myself to be better at tracking changes
   * - 0.0.1
     - 29/01/19
     - - First commit, lots to fix.
