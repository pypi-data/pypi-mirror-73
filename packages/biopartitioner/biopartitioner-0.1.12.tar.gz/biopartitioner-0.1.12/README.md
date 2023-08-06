# Bio Partitioner ![Docker Image CI](https://github.com/david30907d/bio-partitioner/workflows/Docker%20Image%20CI/badge.svg)

## Install
### For User
1. `pip install biopartitioner`
2. Demo Code:
```python
from biopartitioner.factory import PartitionerFactory
partitioner_caller = PartitionerFactory.create_partitioner("vcf")
dataset = "fixtures/scaffold.vcf"
vcf_partioner = partitioner_caller(dataset=dataset, partition_num=8)
vcf_partioner.partition()
```
3. You'll see vcf partition files at current folder.

### For Developer
1. Python dependencies:
    1. `virtualenv venv; . venv/bin/activate`
    2. `pip install poetry`
    3. `poetry install`
2. Npm dependencies, for linter, formatter and commit linter (optional):
    1. `brew install npm`
    2. `npm ci`

# Run

1. `npm run test`
2. You'll see 10 vcf partition files at your folder

## Test

1. test: `npm run test`
2. Run all linter before commitment would save some effort: `npm run check`
