import yaml

COASSEMBLY_FP = ASSEMBLY_FP / "coassembly"
SBX_COASSEMBLY_VERSION = open(get_ext_path("sbx_coassembly") / "VERSION").read().strip()


def zip3l(l1, l2, l3):
    return list(zip(l1, l2, l3))


def coassembly_groups(fp, sample_list):
    if fp == "":
        K = ["all"] * (len(sample_list) * 2)
        V = list(sorted(sample_list)) * 2
        R = [1] * len(sample_list) + [2] * len(sample_list)
        return [K, V, R]
    groups = yaml.safe_load(open(str(fp)).read())
    sorted_keys = sorted(groups.keys())
    K = []  # group
    V = []  # sample
    for k in sorted_keys:
        K += [k] * len(groups[k])
        V += groups[k]
    R = [1] * len(V) + [2] * len(V)
    return [K + K, V + V, R]


localrules:
    all_coassemble,


rule all_coassemble:
    input:
        a=expand(
            str(COASSEMBLY_FP / "{group}_final_contigs.fa"),
            group=list(
                set(
                    coassembly_groups(
                        Cfg["sbx_coassembly"]["group_file"], Samples.keys()
                    )[0]
                )
            ),
        ),
        b=expand(
            str(COASSEMBLY_FP / "agglomerate" / "{sample}_{group}_{rp}.fastq"),
            zip3l,
            group=coassembly_groups(
                Cfg["sbx_coassembly"]["group_file"], Samples.keys()
            )[0],
            sample=coassembly_groups(
                Cfg["sbx_coassembly"]["group_file"], Samples.keys()
            )[1],
            rp=coassembly_groups(Cfg["sbx_coassembly"]["group_file"], Samples.keys())[
                2
            ],
        ),


rule prep_samples_for_concatenation_paired:
    input:
        r1=str(QC_FP / "decontam" / "{sample}_1.fastq.gz"),
        r2=str(QC_FP / "decontam" / "{sample}_2.fastq.gz"),
    output:
        r1=temp(str(COASSEMBLY_FP / "agglomerate" / "{sample}_{group}_1.fastq")),
        r2=temp(str(COASSEMBLY_FP / "agglomerate" / "{sample}_{group}_2.fastq")),
    benchmark:
        BENCHMARK_FP / "prep_samples_for_concatenation_paired_{sample}_{group}.tsv"
    log:
        LOG_FP / "prep_samples_for_concatenation_paired_{sample}_{group}.log",
    threads: Cfg["sbx_coassembly"]["threads"]
    conda:
        "envs/sbx_coassembly_env.yml"
    container:
        f"docker://sunbeamlabs/sbx_coassembly:{SBX_COASSEMBLY_VERSION}"
    shell:
        """
        pigz -d -p {threads} -c {input.r1} > {output.r1}
        pigz -d -p {threads} -c {input.r2} > {output.r2}
        """


rule combine_groups_paired:
    input:
        rules.all_coassemble.input.b,
    output:
        r1=str(COASSEMBLY_FP / "fastq" / "{group}_1.fastq.gz"),
        r2=str(COASSEMBLY_FP / "fastq" / "{group}_2.fastq.gz"),
    params:
        w1=str(str(COASSEMBLY_FP / "agglomerate") + str("/*{group}_1.fastq")),
        w2=str(str(COASSEMBLY_FP / "agglomerate") + str("/*{group}_2.fastq")),
    threads: Cfg["sbx_coassembly"]["threads"]
    conda:
        "envs/sbx_coassembly_env.yml"
    container:
        f"docker://sunbeamlabs/sbx_coassembly:{SBX_COASSEMBLY_VERSION}"
    shell:
        """
        cat {params.w1} | pigz -p {threads} > {output.r1}
        cat {params.w2} | pigz -p {threads} > {output.r2}
        """


rule coassemble_paired:
    input:
        r1=str(COASSEMBLY_FP / "fastq" / "{group}_1.fastq.gz"),
        r2=str(COASSEMBLY_FP / "fastq" / "{group}_2.fastq.gz"),
    output:
        str(COASSEMBLY_FP / "{group}_final_contigs.fa"),
    benchmark:
        BENCHMARK_FP / "coassemble_paired_{group}.tsv"
    log:
        LOG_FP / "coassemble_paired_{group}.log",
    params:
        assembly_dir=str(COASSEMBLY_FP / "{group}"),
    threads: Cfg["sbx_coassembly"]["threads"]
    conda:
        "envs/sbx_coassembly_env.yml"
    container:
        f"docker://sunbeamlabs/sbx_coassembly:{SBX_COASSEMBLY_VERSION}"
    shell:
        """
        megahit -1 {input.r1} -2 {input.r2} -t {threads} -o {params.assembly_dir} 2>&1 | tee {log}
        mv {params.assembly_dir}/final.contigs.fa {output}
        """
