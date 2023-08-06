from pathlib import Path

from biopartitioner.factory import PartitionerFactory


def test_crawl_every_page():
    partitioner_caller = PartitionerFactory.create_partitioner("vcf")
    dataset = "fixtures/scaffold.vcf"
    vcf_partioner = partitioner_caller(
        dataset=dataset, partition_num=8, working_dir="."
    )
    vcf_partioner.partition()
    if __debug__:
        for idx in range(8):
            if not Path(f"{idx}.vcf").exists():
                raise AssertionError(f"{idx}.vcf not found!")
