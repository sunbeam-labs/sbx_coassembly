import os
import pytest
import shutil
import subprocess as sp
import sys
import tempfile


@pytest.fixture
def setup():
    temp_dir = tempfile.mkdtemp()

    reads_fp = os.path.abspath(".tests/data/reads/")
    hosts_fp = os.path.abspath(".tests/data/hosts/")

    project_dir = os.path.join(temp_dir, "project/")

    sp.check_output(["sunbeam", "init", "--data_fp", reads_fp, project_dir])

    config_fp = os.path.join(project_dir, "sunbeam_config.yml")

    mapping_fp = os.path.join(project_dir, "mapping.yml")

    with open(mapping_fp, "w") as f:
        f.write("A: ['A702', 'A741', 'A745', 'A746', 'A747']\n")
        f.write("B: ['B702', 'B741', 'B745', 'B746', 'B747']\n")
        f.write("Other: ['DNAfreewater1.20220214', 'Extractblankswab1.20220214', 'Extractemptywell1.20220214', 'mockdna1.20220214']")

    config_str = f"sbx_mapping: {{genomes_fp: {mapping_fp}}}"
    sp.check_output(
        [
            "sunbeam",
            "config",
            "modify",
            "-i",
            "-s",
            f"{config_str}",
            f"{config_fp}",
        ]
     )

    config_str = f"qc: {{host_fp: {hosts_fp}}}"
    sp.check_output(
        [
            "sunbeam",
            "config",
            "modify",
            "-i",
            "-s",
            f"{config_str}",
            f"{config_fp}",
        ]
    )

    yield temp_dir, project_dir

    shutil.rmtree(temp_dir)


@pytest.fixture
def run_sunbeam(setup):
    temp_dir, project_dir = setup

    output_fp = os.path.join(project_dir, "sunbeam_output")

    try:
        # Run the test job
        sp.check_output(
            [
                "sunbeam",
                "run",
                "--conda-frontend",
                "conda",
                "--profile",
                project_dir,
                "all_coassemble",
                "--directory",
                temp_dir,
            ]
        )
    except sp.CalledProcessError as e:
        shutil.copytree(os.path.join(output_fp, "logs/"), "logs/")
        shutil.copytree(os.path.join(project_dir, "stats/"), "stats/")
        sys.exit(e)

    shutil.copytree(os.path.join(output_fp, "logs/"), "logs/")
    shutil.copytree(os.path.join(project_dir, "stats/"), "stats/")

    all_final_contigs_fp = os.path.join(
        output_fp, "assembly/coassembly/all_final_contigs.fa"
    )

    benchmarks_fp = os.path.join(project_dir, "stats/")

    yield all_final_contigs_fp, benchmarks_fp


def test_full_run(run_sunbeam):
    (
        all_final_contigs_fp,
        benchmarks_fp,
    ) = run_sunbeam

    # Check output
    assert os.path.exists(all_final_contigs_fp)
