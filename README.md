# sbx_coassembly
This is an extension to the [Sunbeam pipeline](https://github.com/sunbeam-labs/sunbeam) to perform co-assembly of reads from arbitrary groups of samples from a given project using megahit.

## Installing

To install (see legacy instructions below):

    sunbeam extend https://github.com/louiejtaylor/sbx_coassembly/

Paramaters for `sbx_coassembly` are automatically added on `sunbeam init`. If you're installing an extension in a project where you already have a config file, run the following to add the options for your newly added extension to your config (the `-i` flag means in-place config file modification; remove the `-i` flag to see the new config in stdout):

    sunbeam config update -i sunbeam_config.yml

## Configuration

If you'd like to coassemble all of your samples, no further input is needed! [Jump to Running](https://github.com/louiejtaylor/sbx_coassembly#running)

If no grouping file is specified this extension by default co-assembles all samples. If you'd like to group specific samples, you need to provide a mapping file, then point to that mapping file in your config file. For example, if you have three samples from individual A (A_d1, A_d2, A_d3) and two from individual B (B_d1, B_d3), and you'd like to make one coassembly for each individual, you first need a mapping file like this (I'll call it `mapping.yml`):

    A: ['A_d1', 'A_d2', 'A_d3']
    B: ['B_d1', 'B_d3']

Here, the bracketed items in the list (i.e. `'A_d1'` or `'B_d3'` are your full sample names and must match the sample names Sunbeam knows. (Look in your `samples.csv` file if you're not sure of the names). The keys at the beginning of the lines are the group names--you can use any valid Python variable name here. After making this mapping file, make sure to edit your config file to point to this mapping file:

```python
...
sbx_coassembly:
  threads: 4
  group_file: '/path/to/your/mapping.yml'
```

## Running

Finally, run Sunbeam as usual with your extension's target rule specified:

    sunbeam run --configfile=sunbeam_config.yml --use-conda all_coassemble

The `--use-conda` flag is required to let Snakemake know that you want to use the conda environment(s) included with your extension.

This rule generates co-assambled contigs in the following location: `sunbeam_output/assembly/coassembly/{group}_final_contigs.fa`

## Contents

 - `requirements.txt` specifies the extension's dependencies
 - `config.yml` contains configuration options that can be specified by the user when running an extension
 - `sbx_template.rules` contains the rules (logic/commands run) of the extension
 
------

## Installing (legacy instructions for sunbeam <3.0)

Clone the repo into your sunbeam `extensions/` folder, installing requirements through Conda, and adding the new options to your existing configuration file. Make sure you've [installed Sunbeam](https://sunbeam.readthedocs.io/en/latest/quickstart.html) first!

    source activate sunbeam
    cd $SUNBEAM_DIR
    git clone https://github.com/louiejtaylor/sbx_coassembly/ extensions/sbx_coassembly

Add the options to your config file (replace "sunbeam_config.yml" with the name of your config file).

    cat extensions/sbx_coassembly/config.yml >> sunbeam_config.yml

