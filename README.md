# sbx_coassembly
This is an extension to the [Sunbeam pipeline](https://github.com/sunbeam-labs/sunbeam) to perform co-assembly of reads from all samples from a given project.

## Installing

Clone the repo into your sunbeam `extensions/` folder, installing requirements through Conda, and adding the new options to your existing configuration file. Make sure you've [installed Sunbeam](https://sunbeam.readthedocs.io/en/latest/quickstart.html) first!

    source activate sunbeam
    cd $SUNBEAM_DIR
    git clone https://github.com/louiejtaylor/sbx_coassembly/ extensions/sbx_coassembly
    conda install --file extensions/sbx_coassembly/requirements.txt

Add the options to your config file (replace "sunbeam_config.yml" with the name of your config file).

    cat extensions/sbx_coassembly/config.yml >> sunbeam_config.yml

## Running

To run an extension, simply run Sunbeam as usual with your extension's target rule specified:

    sunbeam run --configfile=sunbeam_config.yml all_coassemble

## Contents

 - `requirements.txt` specifies the extension's dependencies
 - `config.yml` contains configuration options that can be specified by the user when running an extension
 - `sbx_template.rules` contains the rules (logic/commands run) of the extension
 
    

