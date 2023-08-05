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

"""Module contains network models."""

import multiprocessing as mp
import numpy as np
import pandas as pd

from typing import Iterable, Union, Optional, Callable

from .. import utils, config

# Set up logging
logger = config.logger

__all__ = ['TraversalModel', 'random_linear_activation_function']


class BaseNetworkModel:
    """Base model for network simulations."""

    def __init__(self, edges: pd.DataFrame):
        """Initialize model."""
        assert isinstance(edges, pd.DataFrame), f'edges must be pandas DataFrame, got "{type(edges)}"'
        assert 'source' in edges.columns, f'edges DataFrame must contain "source" column'
        assert 'target' in edges.columns, f'edges DataFrame must contain "target" column'
        self.edges = edges

    @property
    def n_nodes(self) -> int:
        """Unique nodes in edges."""
        return np.unique(self.edges[['source', 'target']].values.flatten()).shape[0]

    @property
    def has_results(self) -> bool:
        """Check if model has results."""
        if isinstance(getattr(self, 'results', None), pd.DataFrame):
            return True
        return False

    def run(self,
            n_cores: int = 5,
            iterations: int = 100,
            **kwargs: dict) -> None:
        """Run model."""
        # Note that we initialize each process by making "edges" a global argument
        pool = mp.Pool(processes=n_cores,
                       initializer=self.initializer)

        # Each process will take about the same amount of time
        # So we want each process to take a single batch of iterations/n_cores runs
        kwargs['iterations'] = int(iterations/n_cores)
        calls = [{**kwargs, **{'position': i}} for i in range(int(n_cores))]

        res = list(pool.imap_unordered(self._worker_wrapper, calls, chunksize=1))

        self.results = pd.concat(res, axis=0)
        self.iterations = iterations

    def _worker_wrapper(self, kwargs: dict):
        return self.model(**kwargs)

    def initializer(self):
        pass

    def model(self):
        pass


class TraversalModel(BaseNetworkModel):
    """Model for traversing a network starting with given seed nodes.

    What this does:

      1. Grab all already visited nodes (starting with ``seeds`` in step 1)
      2. Find all downstream nodes of these
      3. Probabilistically traverse based on the weight of the connecting edges
      4. Add those newly visited nodes to the pool & repeat from beginning
      5. Stop when every (connected) neuron was visited or we reached ``max_steps``

    Parameters
    ----------
    edges :             pandas.DataFrame
                        DataFrame representing an edge list. Must minimally have
                        a ``source`` and ``target`` column.
    seeds :             iterable
                        Seed nodes for traversal. Nodes that aren't found in
                        ``edges['source']`` will be (silently) removed.
    weights :           str, optional
                        Name of a column in ``edges`` used as weights. If not
                        provided, all edges will be given a weight of 1. If using
                        the default activation function the weights need to be
                        between 0 and 1.
    max_steps :         int
                        Limits the number of steps for each iteration.
    traversal_func :    callable, optional
                        Function that determines whether a given edge will be
                        traversed or not in a given step. Must take numpy array
                        (N, 1) of edge weights and return an array with
                        True/False of equal size. Defaults to
                        :func:`~navis.models.network_models.random_linear_activation_function`
                        which will linearly scale probability of traversal
                        from 0 to 100% between edges weights 0 to 0.3.

    Examples
    --------
    >>> from navis.models import TraversalModel
    >>> import networkx as nx
    >>> import numpy as np
    >>> # Generate a random graph
    >>> G = nx.fast_gnp_random_graph(1000, .2, directed=True)
    >>> # Turn into edge list
    >>> edges = nx.to_pandas_edgelist(G)
    >>> # Add random edge weights
    >>> edges['weight'] = np.random.random(edges.shape[0])
    >>> # Initialize model
    >>> model = TraversalModel(edges, seeds=list(G.nodes)[:10])
    >>> # Run model
    >>> model.run(iterations=1000)
    >>> # Get a summary
    >>> model.summary.tail()
          layer_min  layer_max  layer_mean  layer_median
    node
    995           2          2        2.00             2
    996           2          3        2.33             2
    997           2          2        2.00             2
    998           2          2        2.00             2
    999           2          2        2.00             2

    Above Graph was traversed quickly (3 steps max). Let's adjust the
    traversal function:

    >>> from navis.models import random_linear_activation_function
    >>> # Use a lower probability for activation
    >>> def my_act(x):
    ...     return random_linear_activation_function(x, max_w=10)
    >>> model = TraversalModel(edges, seeds=list(G.nodes)[:10],
    ...                        traversal_func=my_act)
    >>> model.summary.tail()
          layer_min  layer_max  layer_mean  layer_median
    node
    995           2          4       3.210           3.0
    996           2          4       3.280           3.0
    997           2          4       3.260           3.0
    998           2          4       3.320           3.0
    999           2          4       3.195           3.0

    """

    def __init__(self,
                 edges: pd.DataFrame,
                 seeds: Iterable[Union[str, int]],
                 weights: Optional[str] = 'weight',
                 max_steps: int = 15,
                 traversal_func: Optional[Callable] = None):
        """Initialize model."""
        super().__init__(edges=edges)

        if not weights:
            edges['weight'] = 1
            weights = 'weight'

        assert weights in edges.columns, f'"{weights}" must be column in edge list'

        # Remove seeds that don't exist
        self.seeds = edges[edges.source.isin(seeds)].source.unique()

        if len(self.seeds) == 0:
            raise ValueError('None of the seeds where among edge list sources.')

        self.weights = weights
        self.max_steps = max_steps

        if isinstance(traversal_func, type(None)):
            self.traversal_func = random_linear_activation_function
        elif callable(traversal_func):
            self.traversal_func = traversal_func
        else:
            raise ValueError('`traversal_func` must be None or a callable')

    @property
    def summary(self) -> pd.DataFrame:
        """Per-node summary."""
        return getattr(self, '_summary', self.make_summary())

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        s = f'{self.__class__}: {self.edges.shape[0]} edges; {self.n_nodes}' \
            f' unique nodes; {len(self.seeds)} seeds;' \
            f' traversal_func {self.traversal_func}.'
        if self.has_results:
            s += f' Model ran with {self.iterations} iterations.'
        else:
            s += ' Model has not yet been run.'
        return s

    def make_summary(self) -> pd.DataFrame:
        """Generate summary."""
        if not self.has_results:
            logger.error('Must run simulation first.')

        summary = self.results.groupby('node',
                                       as_index=False).steps.agg(['min',
                                                                  'max',
                                                                  'mean',
                                                                  'median'])

        summary.rename({'min': 'layer_min',
                        'mean': 'layer_mean',
                        'max': 'layer_max',
                        'median': 'layer_median'}, axis=1, inplace=True)

        self._summary = summary
        return self._summary

    def model(self, iterations: int = 100, **kwargs) -> None:
        """Run a single model.

        Use ``.run`` to use parallel processes.

        """
        # For some reason this is required for progress bars in Jupyter to show
        print(' ', end='', flush=True)
        # For faster access, use the raw array
        edges = self.edges[['source', 'target', self.weights]].values

        # For some reason the progress bar does not show unless we have a print here
        all_infected = None
        for it in config.trange(iterations,
                                disable=config.pbar_hide,
                                leave=config.pbar_leave,
                                position=kwargs.get('position', 0)):
            # Set infected to source
            infected = np.array([[1, s] for s in self.seeds])
            this_edges = edges

            for i in range(2, self.max_steps + 1):
                # Get out edges of the infected nodes -> do this in 2 steps to save time on the second
                pre_infected = np.isin(this_edges[:, 0].astype(int), infected[:, 1])
                post_infected = np.isin(this_edges[:, 1].astype(int), infected[:, 1])
                out_edges = this_edges[pre_infected & ~post_infected]
                this_edges = this_edges[~(pre_infected & ~post_infected)]

                # Stop if everything that can be infected has been infected
                if out_edges.size == 0:
                    break

                # Collect weights
                w = out_edges[:, 2]

                # Infected edges
                inf_edges = out_edges[self.traversal_func(w)]

                # Keep track
                if not inf_edges.size == 0:
                    new_inf = np.unique(inf_edges[:, 1]).astype(int)
                    infected = np.concatenate((infected, [[i, b] for b in new_inf]), axis=0)

            # Save this round of infection
            if not isinstance(all_infected, np.ndarray):
                all_infected = infected
            else:
                all_infected = np.concatenate((all_infected, infected), axis=0)

        self.iterations = iterations

        return pd.DataFrame(all_infected, columns=['steps', 'node']).astype(int)


def random_linear_activation_function(w: np.ndarray,
                                      min_w: float = 0,
                                      max_w: float = .3) -> np.ndarray:
    """Random linear activation function.

    Parameters
    ----------
    w :     np.ndarray
            (N, 1) array containing the edge weights.
    min_w : float
            Value of ``w`` at which probability of activation is 0%.
    max_w : float
            Value of ``w`` at which probability of activation is 100%.

    Returns
    -------
    np.ndarray
            True or False values for each edge.

    """
    # Generate a random number between 0 and 1 for each connection
    r = np.random.rand(w.shape[0])

    # Normalize weights to bounds
    w_norm = (w - min_w) / (max_w - min_w)

    # Test active
    act = w_norm >= r

    return act
