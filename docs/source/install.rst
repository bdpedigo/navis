.. _installing:

Install
=======

Installation instructions come in two flavours:

1. **Quick install**: if you know what you are doing
2. **Step-by-step instructions** : if you are new to Python

.. topic:: By the way

   You can try navis without having to install **anything**! Simply follow this
   link to `Binder <https://mybinder.org/v2/gh/schlegelp/navis/master?urlpath=tree>`_:
   they are kindly hosting a Jupyter notebook server with the most up-to-date version
   of navis. Just navigate and open ``examples/start_here.ipynb`` to have
   a crack at it!


Quick install
-------------

Requires Python 3.6 or later.

If you don't already have it, get the Python package manager `PIP <https://pip.pypa.io/en/stable/installing/>`_.

To get the minimal most recent version from PyPI (see below for optional extras) use:

::

   pip3 install navis

To get the most recent development version from
`Github <https://github.com/schlegelp/navis>`_ use:

::

   pip3 install git+git://github.com/schlegelp/navis@master


**Installing from source**

Instead of using PIP to install from Github, you can also install manually:

1. Download the source (e.g a ``tar.gz`` file from
   https://github.com/schlegelp/navis/tree/master/dist)

2. Unpack and change directory to the source directory
   (the one with ``setup.py``).

3. Run ``python setup.py install`` to build and install

.. note::
   There are two optional dependencies that you might want to install manually:
   :ref:`pyoctree <pyoc>` and :ref:`rpy2 <rpy>`. The latter is only relevant if
   you intend to use navis's R wrappers.


Step-by-step instructions
-------------------------

.. raw:: html

    <ol type="1">
      <li><strong>Check if Python 3 is installed and install if
                  necessary</strong>.<br> Linux and Mac should already come
                  with Python distribution(s) but you need to figure out if
                  you have Python 2, Python 3 or both:
                  <br>
                  Open a terminal, type in
                  <pre>python3 --version</pre>
                  and press enter. You should get something similar to either of
                  this:
      </li>
          <ol type="a">
              <li>
                  <pre>python3: command not found</pre>
                  No Python 3 installed. See below box on how to install Python 3.
              </li>
              <li>
                  <pre>Python 3.7.4 :: Anaconda, Inc.</pre>
                  Python 3 is already installed. Nice! Proceed with step 2.
              </li>
          </ol>
      </li>
      <li>
        <strong>Get the Python package manager <a href="https://pip.pypa.io">PIP</a>.</strong><br>
        Try running this in a terminal:
        <pre>pip3 install --upgrade pip</pre>
        If you already have PIP, this should update it to the most recent version.
        If you get: <pre>pip3: command not found</pre> follow this
        <a href="https://pip.pypa.io/en/stable/installing/">link</a> to download
        and install PIP.
      </li>
      <li>
        <strong>Install navis and its dependencies</strong>.<br>
        Open a terminal and run:
        <pre>pip3 install navis</pre>
        to install the most recent version of navis and all of its
        <em>mandatory</em> dependencies. <strong>You can also use this command
        to update an existing install of navis!</strong>
      </li>
      <li>
        <strong>Done!</strong> Go to <em>Tutorial</em> to get started.
      </li>
    </ol>

.. raw:: html

    <div class="alert alert-danger alert-trim" role="alert">
      Missing permissions to write can mess up
      installations using <strong>PIP</strong>. If you get a
      <code>"..permission denied.."</code> error, try running the same command
      as admin: <code>sudo pip3 install ...</code>
    </div>

.. topic:: Installing Python 3

   On **Linux** and **OSX (Mac)**, simply go to https://www.python.org to
   download + install Python3 (version 3.6 or later). I recommend getting 3.7 as
   3.8 may still cause problems with some of navis' dependencies.

   On **Windows**, things are bit more tricky. While navis is written in pure
   Python, some of its dependencies are written in C for speed and need to be
   compiled - which a pain on Windows. I strongly recommend installing a
   scientific Python distribution that comes with "batteries included".
   `Anaconda <https://www.continuum.io/downloads>`_ is a widespread solution
   that comes with its own package manager ``conda``.

.. note::
   If you intend to use navis' interface with R, you need to install the
   optional dependency :ref:`rpy2 <rpy>`.


Dependencies
------------

Mandatory
+++++++++

If you installed navis using ``PIP``, mandatory dependencies should have been
installed automatically.

`NumPy <http://www.numpy.org/>`_
  Provides matrix representation of graphs and is used in some graph
  algorithms for high-performance matrix computations.

`Pandas <http://pandas.pydata.org/>`_
  Provides advanced dataframes and indexing.

`Vispy <http://vispy.org/>`_
  Used to visualise neurons in 3D. This requires you to have *one* of
  the supported `backends <http://vispy.org/installation.html#backend-requirements>`_
  installed. During automatic installation navis will try installing the
  `PyQt5 <http://pyqt.sourceforge.net/Docs/PyQt5/installation.html>`_ backend
  to fullfil this requirement.

`Plotly <https://plot.ly/python/getting-started/>`_
  Used to visualise neurons in 3D. Alternative to Vispy based on WebGL.

`NetworkX <https://networkx.github.io>`_
  Graph analysis library written in pure Python. This is the standard library
  used by navis.

`ncollpyde <https://pypi.org/project/ncollpyde>`_
  Used to check e.g. if objects are within volume.

`SciPy <http://scipy.org>`_
  Provides tons of scientific computing tools: sparse matrix representation
  of graphs, pairwose distance computation, hierarchical clustering, etc.

`Matplotlib <http://matplotlib.sourceforge.net/>`_
  Essential for all 2D plotting.

`Seaborn <https://seaborn.pydata.org>`_
  Used e.g. for its color palettes.

`tqdm <https://pypi.python.org/pypi/tqdm>`_
  Neat progress bars.

`PyPNG <https://pythonhosted.org/pypng/>`_
  Generates PNG images. Used for taking screenshot from 3D viewer. Install
  from PIP: ``pip3 install pypng``.


Optional
++++++++

Navis provides extra functionality or performance improvements with optional extras.

Extras can be directly, or along with navis with

::

   pip3 install navis[extra1,extra2]


The user-facing extras, the dependencies they install,
and how to install those dependencies directly, are below.
You can install all of them with the ``all`` extra.


.. _pykd:

``kdtree``: `pykdtree <https://github.com/storpipfugl/pykdtree>`_
  Faster than scipy's cKDTree implementation. If available, will be used to
  speed up e.g. NBLAST.

  ::

    pip3 install pykdtree

.. _pyoc:

``octree``: `PyOctree <https://pypi.python.org/pypi/pyoctree/>`_
  Slower alternative to ncollpyde.

  ::

    pip3 install pyoctree

.. _rpy:

``r``: `Rpy2 <https://rpy2.readthedocs.io/en/version_2.8.x/overview.html#installation>`_ (``r``)
  Provides interface with R. This allows you to use e.g. R packages from
  https://github.com/jefferis and https://github.com/alexanderbates. Note that
  this package is not installed automatically as it would fail if R is not
  already installed on the system. You have to install Rpy2 manually!

  ::

    pip3 install rpy2

.. _shapely:

``shapely``: `Shapely <https://shapely.readthedocs.io/en/latest/>`_ (``shapely``)
  This is used to get 2D outlines of navis.Volumes.

  ::

    pip3 install shapely

.. _igraph:

``igraph``: `iGraph <http://igraph.org/>`_
  For advanced users.

  By default navis uses the `NetworkX <https://networkx.github.io>`_ graph
  library for most of the computationally expensive functions. NetworkX is
  written in pure Python, well maintained and easy to install.

  If you need that extra bit of speed, there is iGraph.
  It is written in C and therefore very fast.
  If available, navis will try using iGraph over NetworkX.
  iGraph is difficult to install, though,
  because you have to install the C core first
  and then its Python bindings, ``python-igraph``.
