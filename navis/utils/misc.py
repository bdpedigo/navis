#    This script is part of navis (http://www.github.com/schlegelp/navis).
#    Copyright (C) 2018 Philipp Schlegel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

import inspect
import requests
import urllib

import numpy as np
import pandas as pd

from collections import defaultdict
from functools import wraps
from typing import Optional, Union, List, Iterable, Dict, Tuple, Any

from .. import config, core, transforms
from .eval import is_mesh
from .iterables import is_iterable, make_iterable

# Set up logging
logger = config.logger


def sizeof_fmt(num, suffix='B'):
    """Bytes to Human readable."""
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def make_volume(x: Any) -> 'core.Volume':
    """Try making a navis.Volume from input object."""
    if isinstance(x, core.Volume):
        return x
    if is_mesh(x):
        inits = dict(vertices=x.vertices, faces=x.faces)
        for p in ['name', 'id', 'color']:
            if hasattr(x, p):
                inits[p] = getattr(x, p, None)
        return core.Volume(**inits)

    raise TypeError(f'Unable to coerce input of type "{type(x)}" to navis.Volume')


def map_neuronlist(desc: str = "",
                   can_zip: List[Union[str, int]] = [],
                   must_zip: List[Union[str, int]] = [],
                   progress: bool = True):
    """Run function on all neurons in the NeuronList.

    Parameters
    ----------
    desc :          str
                    Descriptor to show in the progress bar if run over multiple
                    neurons.
    can_zip/
    must_zip :      list
                    Names of keyword arguments that need to be zipped together
                    with the neurons in the neuronlist. For example:

                      some_function(NeuronList([n1, n2, n3]), [p1, p2, p3])

                    Should be executed as:

                      some_function(n1, p1)
                      some_function(n2, p2)
                      some_function(n3, p3)

                    `can_zip` will be zipped only if the length matches the
                    length of the neuronlist. If a `can_zip` argument has only
                    one value it will be re-used for all neurons.

                    `must_zip` arguments have to have one value for each of the
                    neurons.

                    Single ``None`` values are always just passed through.

                    Note that for this to consistently work the parameters in
                    question have to be keyword-only (*).
    progress :      bool
                    Whether to show a progress bar or not. Overrruled by
                    ``config.pbar_hide``.

    To-implement
    ------------

    allow_parallel : bool
                    If True and the function is called with `parallel=True`,
                    will use multiple cores to process the neuronlist.

    """
    # TODO:
    # - make can_zip/must_zip work with positional-only argumens to, i.e. let
    #   it work with integers instead of strings
    # - in theory, we could also implement parallel processing here

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            nl = None
            if args:
                # If there are positional arguments, the first one is thought to
                # be the input neuron(s)
                nl = args[0]
                nl_key = '_args'
            else:
                # If not, we have to cross our fingers and hope that there is
                # either an "x", a "neuron" or a "neurons" keyword argument
                for key in ('x', 'neuron', 'neurons'):
                    if key in kwargs:
                        nl = kwargs[key]
                        nl_key = key
                        break

            if isinstance(nl, type(None)):
                raise ValueError('Unable to identify the neurons for call'
                                 f'{function}:\n {args}\n {kwargs}')

            # If we have a neuronlist
            if isinstance(nl, core.NeuronList):
                # Pop the neurons from kwargs or args so we don't pass the
                # neurons twice
                if nl_key == '_args':
                    args = args[1:]
                else:
                    _ = kwargs.pop(nl_key)

                # See if function has inplace parameter
                sig = inspect.signature(function)
                has_inplace = 'inplace' in sig.parameters
                # If function has an inplace parameter
                if has_inplace:
                    # See if user has specified inplace, if not use the default
                    inplace = kwargs.pop('inplace', sig.parameters['inplace'].default)
                    # If not inplace make a copy (which will be returned)
                    if not inplace:
                        nl = nl.copy()

                # Parse "can zip" arguments
                can_zip_kwargs = [{} for n in nl]
                for p in can_zip:
                    # Skip if not present or is None
                    if p not in kwargs or isinstance(kwargs[p], type(None)):
                        continue

                    if is_iterable(kwargs[p]):
                        # If iterable but length does not match complain
                        le = len(kwargs[p])
                        if le != len(nl):
                            raise ValueError(f'Got {le} values of `{p}` for '
                                             f'{len(nl)} neurons.')

                        # Zip
                        for i, v in enumerate(kwargs.pop(p)):
                            can_zip_kwargs[i][p] = v

                # Parse "must zip" arguments
                must_zip_kwargs = [{} for n in nl]
                for p in must_zip:
                    # Skip if not present or is None
                    if p not in kwargs or isinstance(kwargs[p], type(None)):
                        continue

                    values = make_iterable(kwargs.pop(p))
                    if len(values) != len(nl):
                        raise ValueError(f'Got {len(values)} values of `{p}` for '
                                         f'{len(nl)} neurons.')

                    # Zip
                    for i, v in enumerate(values):
                        must_zip_kwargs[i][p] = v

                # Whether we want to hide the progress bar
                hide = config.pbar_hide or not progress or len(nl) == 1

                # Whether we need to/can specify inplace=True
                if has_inplace:
                    kwargs['inplace'] = True

                # Now run the function for each neuron
                for i, n in config.tqdm(enumerate(nl),
                                        desc=desc,
                                        disable=hide,
                                        total=len(nl),
                                        leave=config.pbar_leave):

                    _ = function(n, *args, **kwargs,
                                 **can_zip_kwargs[i], **must_zip_kwargs[i])

                return nl
            else:
                # If single neuron just pass through
                return function(*args, **kwargs)
        return wrapper
    return decorator


def lock_neuron(function):
    """Lock neuron while function is executed.

    This makes sure that temporary attributes aren't re-calculated as changes
    are being made.

    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        # Lock if first argument is a neuron
        if isinstance(args[0], core.BaseNeuron):
            args[0]._lock = getattr(args[0], '_lock', 0) + 1
        try:
            # Execute function
            res = function(*args, **kwargs)
        except BaseException:
            raise
        finally:
            # Unlock neuron
            if isinstance(args[0], core.BaseNeuron):
                args[0]._lock -= 1
        # Return result
        return res
    return wrapper


def is_url(x: str) -> bool:
    """Return True if str is URL.

    Examples
    --------
    >>> from navis.utils import is_url
    >>> is_url('www.google.com')
    False
    >>> is_url('http://www.google.com')
    True

    """
    parsed = urllib.parse.urlparse(x)

    if parsed.netloc and parsed.scheme:
        return True
    else:
        return False


def _type_of_script() -> str:
    """Return context (terminal, jupyter, iPython) in which navis is run."""
    try:
        ipy_str = str(type(get_ipython()))  # type: ignore
        if 'zmqshell' in ipy_str:
            return 'jupyter'
        else:  # if 'terminal' in ipy_str:
            return 'ipython'
    except BaseException:
        return 'terminal'


def is_jupyter() -> bool:
    """Test if navis is run in a Jupyter notebook.

    Examples
    --------
    >>> from navis.utils import is_jupyter
    >>> # If run outside a Jupyter environment
    >>> is_jupyter()
    False

    """
    return _type_of_script() == 'jupyter'


def set_loggers(level: str = 'INFO'):
    """Set levels for all associated module loggers.

    Examples
    --------
    >>> from navis.utils import set_loggers
    >>> from navis import config
    >>> # Get current level
    >>> lvl = config.logger.level
    >>> # Set new level
    >>> set_loggers('INFO')
    >>> # Revert to old level
    >>> set_loggers(lvl)

    """
    config.logger.setLevel(level)


def set_pbars(hide: Optional[bool] = None,
              leave: Optional[bool] = None,
              jupyter: Optional[bool] = None) -> None:
    """Set global progress bar behaviors.

    Parameters
    ----------
    hide :      bool, optional
                Set to True to hide all progress bars.
    leave :     bool, optional
                Set to False to clear progress bars after they have finished.
    jupyter :   bool, optional
                Set to False to force using of classic tqdm even if in
                Jupyter environment.

    Returns
    -------
    Nothing

    Examples
    --------
    >>> from navis.utils import set_pbars
    >>> # Hide progress bars after finishing
    >>> set_pbars(leave=False)
    >>> # Never show progress bars
    >>> set_pbars(hide=True)
    >>> # Never use Jupyter widget progress bars
    >>> set_pbars(jupyter=False)

    """
    if isinstance(hide, bool):
        config.pbar_hide = hide

    if isinstance(leave, bool):
        config.pbar_leave = leave

    if isinstance(jupyter, bool):
        if jupyter:
            if not is_jupyter():
                logger.error('No Jupyter environment detected.')
            else:
                config.tqdm = config.tqdm_notebook
                config.trange = config.tnrange
        else:
            config.tqdm = config.tqdm_classic
            config.trange = config.trange_classic

    return


def unpack_neurons(x: Union[Iterable, 'core.NeuronList', 'core.NeuronObject'],
                   raise_on_error: bool = True
                   ) -> List['core.NeuronObject']:
    """Unpack neurons and returns a list of individual neurons.

    Examples
    --------
    This is mostly for doc tests:

    >>> from navis.utils import unpack_neurons
    >>> from navis.data import example_neurons
    >>> nl = example_neurons(3)
    >>> type(nl)
    <class 'navis.core.neuronlist.NeuronList'>
    >>> # Unpack list of neuronlists
    >>> unpacked = unpack_neurons([nl, nl])
    >>> type(unpacked)
    <class 'list'>
    >>> type(unpacked[0])
    <class 'navis.core.neurons.TreeNeuron'>
    >>> len(unpacked)
    6

    """
    neurons: list = []

    if isinstance(x, (list, np.ndarray, tuple)):
        for l in x:
            neurons += unpack_neurons(l)
    elif isinstance(x, core.BaseNeuron):
        neurons.append(x)
    elif isinstance(x, core.NeuronList):
        neurons += x.neurons
    elif raise_on_error:
        raise TypeError(f'Unknown neuron format: "{type(x)}"')

    return neurons


def set_default_connector_colors(x: Union[List[tuple], Dict[str, tuple]]
                                 ) -> None:
    """Set default connector colors.

    Parameters
    ----------
    x :         list-like | dict
                New default connector colors. Can be::

                   list : [(r, g, b), (r, g, b), ..]
                   dict : {'cn_label': (r, g, b), ..}

    """
    if not isinstance(x, (dict, list, np.ndarray)):
        raise TypeError(f'Expect dict, list or numpy array, got "{type(x)}"')

    config.default_connector_colors = x

    return


def parse_objects(x) -> Tuple['core.NeuronList',
                              List['core.Volume'],
                              List[np.ndarray],
                              List]:
    """Categorize objects e.g. for plotting.

    Returns
    -------
    Neurons :       navis.NeuronList
    Volume :        list of navis.Volume (trimesh.Trimesh will be converted)
    Points :        list of arrays
    Visuals :       list of vispy visuals

    Examples
    --------
    This is mostly for doc tests:

    >>> from navis.utils import parse_objects
    >>> from navis.data import example_neurons, example_volume
    >>> import numpy as np
    >>> nl = example_neurons(3)
    >>> v = example_volume('LH')
    >>> p = nl[0].nodes[['x', 'y', 'z']].values
    >>> n, vols, points, vis = parse_objects([nl, v, p])
    >>> type(n), len(n)
    (<class 'navis.core.neuronlist.NeuronList'>, 3)
    >>> type(vols), len(vols)
    (<class 'list'>, 1)
    >>> type(vols[0])
    <class 'navis.core.volumes.Volume'>
    >>> type(points), len(points)
    (<class 'list'>, 1)
    >>> type(points[0])
    <class 'numpy.ndarray'>
    >>> type(vis), len(points)
    (<class 'list'>, 1)

    """
    # Make sure this is a list.
    if not isinstance(x, list):
        x = [x]

    # If any list in x, flatten first
    if any([isinstance(i, list) for i in x]):
        # We need to be careful to preserve order because of colors
        y = []
        for i in x:
            y += i if isinstance(i, list) else [i]
        x = y

    # Collect neuron objects, make a single NeuronList and split into types
    neurons = core.NeuronList([ob for ob in x if isinstance(ob,
                                                            (core.BaseNeuron,
                                                             core.NeuronList))],
                              make_copy=False)

    # Collect visuals
    visuals = [ob for ob in x if 'vispy' in str(type(ob))]

    # Collect and parse volumes
    volumes = [ob for ob in x if not isinstance(ob, (core.BaseNeuron,
                                                     core.NeuronList))
                                 and is_mesh(ob)]
    # Add templatebrains
    volumes += [ob.mesh for ob in x if isinstance(ob, transforms.templates.TemplateBrain)]
    # Converts any non-navis meshes into Volumes
    volumes = [core.Volume(v) if not isinstance(v, core.Volume) else v for v in volumes]

    # Collect dataframes with X/Y/Z coordinates
    dataframes = [ob for ob in x if isinstance(ob, pd.DataFrame)]
    if [d for d in dataframes if False in np.isin(['x', 'y', 'z'], d.columns)]:
        logger.warning('DataFrames must have x, y and z columns.')
    # Filter to and extract x/y/z coordinates
    dataframes = [d for d in dataframes if False not in [c in d.columns for c in ['x', 'y', 'z']]]
    dataframes = [d[['x', 'y', 'z']].values for d in dataframes]

    # Collect arrays
    arrays = [ob.copy() for ob in x if isinstance(ob, np.ndarray)]
    # Remove arrays with wrong dimensions
    if [ob for ob in arrays if ob.shape[1] != 3 and ob.shape[0] != 2]:
        logger.warning('Arrays need to be of shape (N, 3) for scatter or (2, N)'
                       ' for line plots.')
    arrays = [ob for ob in arrays if any(np.isin(ob.shape, [2, 3]))]

    points = dataframes + arrays

    return neurons, volumes, points, visuals


def make_url(baseurl, *args: str, **GET) -> str:
    """Generate URL.

    Parameters
    ----------
    *args
                Will be turned into the URL. For example::

                    >>> make_url('http://neuromorpho.org', 'neuron', 'fields')
                    'http://neuromorpho.org/neuron/fields'

    **GET
                Keyword arguments are assumed to be GET request queries
                and will be encoded in the url. For example::

                    >>> make_url('http://neuromorpho.org', 'neuron', 'fields',
                    ...          page=1)
                    'http://neuromorpho.org/neuron/fields?page=1'

    Returns
    -------
    url :       str


    Examples
    --------
    >>> from navis.utils import is_url, make_url
    >>> url = make_url('http://www.google.com', 'test', query='test')
    >>> url
    'http://www.google.com/test?query=test'
    >>> is_url(url)
    True

    """
    url = baseurl
    # Generate the URL
    for arg in args:
        arg_str = str(arg)
        joiner = '' if url.endswith('/') else '/'
        relative = arg_str[1:] if arg_str.startswith('/') else arg_str
        url = requests.compat.urljoin(url + joiner, relative)
    if GET:
        url += f'?{urllib.parse.urlencode(GET)}'
    return url
