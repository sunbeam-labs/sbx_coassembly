<img src="https://github.com/sunbeam-labs/sunbeam/blob/stable/docs/images/sunbeam_logo.gif" width=120, height=120 align="left" />

# sbx_coassembly

<!-- Badges start -->
[![Tests](https://github.com/sunbeam-labs/sbx_coassembly/actions/workflows/tests.yml/badge.svg)](https://github.com/sunbeam-labs/sbx_coassembly/actions/workflows/tests.yml)
[![Super-Linter](https://github.com/sunbeam-labs/sbx_coassembly/actions/workflows/linter.yml/badge.svg)](https://github.com/sunbeam-labs/sbx_coassembly/actions/workflows/linter.yml)
<!-- Badges end -->

A [Sunbeam](https://github.com/sunbeam-labs/sunbeam) extension to perform co-assembly of reads from arbitrary groups of samples from a given project using Megahit.

## Installation

To install, activate your conda environment (using the name of your environment) and use `sunbeam extend`:

    conda activate <i>sunbeamX.X.X</i>
    sunbeam extend https://github.com/sunbeam-labs/sbx_coassembly.git

## Usage

To generate coassembled samples, create a project, define your groupings, and use the `all_coassemble` target:

    sunbeam init --data_fp /path/to/reads/ /path/to/project/
    printf "A: ['A_d1', 'A_d2', 'A_d3']\nB: ['B_d1', 'B_d3']" > mapping.yml
    sunbeam config modify -i -f /path/to/project/sunbeam_config.yml -s 'sbx_coassembly: {{group_file: {/path/to/mapping.yml}}}'
    sunbeam run --profile /path/to/project/ all_coassemble

N.B. For sunbeam versions <4 the last command will be something like `sunbeam run --configfile /path/to/project/sunbeam_config.yml all_coassemble`.

## Configuration

If you'd like to coassemble all of your samples, no further input is needed!

If no grouping file is specified this extension by default co-assembles all samples. If you'd like to group specific samples, you need to provide a mapping file, then point to that mapping file in your config file. For example, if you have three samples from individual A (A_d1, A_d2, A_d3) and two from individual B (B_d1, B_d3), and you'd like to make one coassembly for each individual, you first need a mapping file like this (I'll call it `mapping.yml`):

    A: ['A_d1', 'A_d2', 'A_d3']
    B: ['B_d1', 'B_d3']

Here, the bracketed items in the list (i.e. `'A_d1'` or `'B_d3'` are your full sample names and must match the sample names Sunbeam knows. (Look in your `samples.csv` file if you're not sure of the names). The keys at the beginning of the lines are the group names--you can use any valid Python variable name here. After making this mapping file, make sure to edit your config file to point to this mapping file:

```
...
sbx_coassembly:
  threads: 4
  group_file: '/path/to/mapping.yml'
```

## Legacy Installation

For sunbeam versions <3 or if `sunbeam extend` isn't working, you can use `git` directly to install an extension:

    git clone https://github.com/sunbeam-labs/sbx_coassembly.git extensions/sbx_coassembly

and then include it in the config for any given project with:

    cat extensions/sbx_coassembly/config.yml >> /path/to/project/sunbeam_config.yml
