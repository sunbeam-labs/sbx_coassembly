<img src="https://github.com/sunbeam-labs/sunbeam/blob/stable/docs/images/sunbeam_logo.gif" width=120, height=120 align="left" />

# sbx_coassembly

<!-- Badges start -->
[![Tests](https://github.com/sunbeam-labs/sbx_coassembly/actions/workflows/tests.yml/badge.svg)](https://github.com/sunbeam-labs/sbx_coassembly/actions/workflows/tests.yml)
![Condabot](https://img.shields.io/badge/condabot-active-purple)
[![DockerHub](https://img.shields.io/docker/pulls/sunbeamlabs/sbx_coassembly)](https://hub.docker.com/repository/docker/sunbeamlabs/sbx_coassembly/)
<!-- Badges end -->

A [Sunbeam](https://github.com/sunbeam-labs/sunbeam) extension to perform co-assembly of reads from arbitrary groups of samples from a given project using Megahit.

## Configuration

If you'd like to coassemble all of your samples, no further input is needed!

If no grouping file is specified this extension by default co-assembles all samples. If you'd like to group specific samples, you need to provide a mapping file, then point to that mapping file in your config file. For example, if you have three samples from individual A (A_d1, A_d2, A_d3) and two from individual B (B_d1, B_d3), and you'd like to make one assembly for each individual, you first need a mapping file like this (I'll call it `mapping.yml`):

    A: ['A_d1', 'A_d2', 'A_d3']
    B: ['B_d1', 'B_d3']

Here, the bracketed items in the list (e.g. `'A_d1'` or `'B_d3'`) are your full sample names and must match the sample names Sunbeam knows. (Look in your `samples.csv` file if you're not sure of the names). The keys at the beginning of the lines are the group names -- you can use any valid Python variable name here. After making this mapping file, make sure to edit your config file to point to this mapping file:

```
...
sbx_coassembly:
  threads: 4
  group_file: '/path/to/mapping.yml'
```

## Docs

More [docs](https://sunbeam.readthedocs.io/en/stable/extensions.html).