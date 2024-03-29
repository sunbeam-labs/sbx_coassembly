FROM condaforge/mambaforge:latest

# Setup
WORKDIR /home/sbx_coassembly_env

COPY envs/sbx_coassembly_env.yml ./

# Install environment
RUN mamba env create --file sbx_coassembly_env.yml --name sbx_coassembly_env

ENV PATH="/opt/conda/envs/sbx_coassembly_env/bin/:${PATH}"

# "Activate" the environment
SHELL ["conda", "run", "-n", "sbx_coassembly_env", "/bin/bash", "-c"]

# Run
CMD "bash"