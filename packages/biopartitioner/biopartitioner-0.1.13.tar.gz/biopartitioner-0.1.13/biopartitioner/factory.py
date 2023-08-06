from biopartitioner.partitioner.vcf_partitioner import VCFPartitioner


class PartitionerFactory(object):
    @classmethod
    def create_partitioner(cls, type_of_dataset):
        if type_of_dataset == "vcf":
            return VCFPartitioner
        else:
            raise Exception("Invalid partitioner")
