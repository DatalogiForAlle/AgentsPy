#!/usr/bin/env python3
from agents import *

miner_model = Model("Graph issue", 100, 100)

miner_model.line_chart("foo", (42, 42, 42))

# Uncomment this line to remove the error
#miner_model.add_slider("bar", 1, 1, 1)

run(miner_model)
