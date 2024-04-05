#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:32:51 2023

@author: eveomett

Lab 4: MAUP and data.  See details on Canvas page

Make sure to say where/when you got your data!
"""

import pandas as pd
import geopandas as gpd
import maup
import time

# from class
from gerrychain import Graph, Partition, proposals, updaters, constraints, accept, MarkovChain, Election
from gerrychain.updaters import cut_edges, Tally
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from functools import partial

maup.progress.enabled = True

ct_df = gpd.read_file("./CT/CT.shp")

print(ct_df)


graph = Graph.from_geodataframe(ct_df)

# updaters
updaters = {
    "cut_edges": cut_edges,
    "population": Tally("TOTPOP", alias="population"),
}

initial_partition = Partition(graph=graph, assignment="CD", updaters=updaters)

# function to apply the recom proposal
def custom_proposal(partition):
    return recom(
        partition=partition,  
        pop_col="TOTPOP",  
        epsilon=0.05,  
        node_repeats=1, 
        pop_target=700000.0
    )

pop_tolerance=0.02

population_constraint = constraints.within_percent_of_ideal_population(
    initial_partition, 
    pop_tolerance, 
    pop_key='population')

chain = MarkovChain(
    proposal=custom_proposal,
    constraints=[population_constraint],
    accept=always_accept,
    initial_state=initial_partition,
    total_steps=10  # Number of steps the chain will take
)

for partition in chain:
    print(partition)

