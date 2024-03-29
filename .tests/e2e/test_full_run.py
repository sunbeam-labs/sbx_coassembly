import pytest
import shutil
import subprocess as sp
import sys
import tempfile
from pathlib import Path


@pytest.fixture
def setup():
    temp_dir = Path(tempfile.mkdtemp())

    reads_fp = Path(".tests/data/reads/").resolve()
    hosts_fp = Path(".tests/data/hosts/").resolve()

    project_dir = temp_dir / "project/"

    sp.check_output(["sunbeam", "init", "--data_fp", reads_fp, project_dir])

    config_fp = project_dir / "sunbeam_config.yml"

    mapping_fp = project_dir / "mapping.yml"

    with open(mapping_fp, "w") as f:
        f.write("A: ['A702', 'A741', 'A745', 'A746', 'A747']\n")
        f.write("B: ['B702', 'B741', 'B745', 'B746', 'B747']\n")
        f.write(
            "Other: ['DNAfreewater1.20220214', 'Extractblankswab1.20220214', 'Extractemptywell1.20220214', 'mockdna1.20220214']"
        )

    config_str = f"sbx_coassembly: {{group_file: {mapping_fp}}}"
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


@pytest.fixture
def run_sunbeam(setup):
    temp_dir, project_dir = setup
    output_fp = project_dir / "sunbeam_output"
    log_fp = output_fp / "logs"
    stats_fp = project_dir / "stats"

    # Run the test job
    try:
        sp.check_output(
            [
                "sunbeam",
                "run",
                "--profile",
                project_dir,
                "all_coassemble",
                "--directory",
                temp_dir,
            ]
        )
    except sp.CalledProcessError as e:
        shutil.copytree(log_fp, "logs/")
        shutil.copytree(stats_fp, "stats/")
        sys.exit(e)

    shutil.copytree(log_fp, "logs/")
    shutil.copytree(stats_fp, "stats/")

    output_fp = project_dir / "sunbeam_output"
    benchmarks_fp = project_dir / "stats/"

    yield output_fp, benchmarks_fp


def test_full_run(run_sunbeam):
    output_fp, benchmarks_fp = run_sunbeam

    assembly_fp = output_fp / "assembly" / "coassembly"
    A_fp = assembly_fp / "A_final_contigs.fa"
    B_fp = assembly_fp / "B_final_contigs.fa"
    Other_fp = assembly_fp / "Other_final_contigs.fa"

    assert A_fp.exists()
    assert B_fp.exists()
    assert Other_fp.exists()
