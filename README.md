# Allen-DREAM-Challenge
Infrastructure and analysis code for the [Allen Institute Cell Lineage Reconstruction DREAM Challenge](https://www.synapse.org/AllenCellLineage) (2019).

## Challenge Questions

### Sub-challenge 1
Reconstruct the lineage of each of 30 colonies in the best possible way using only the barcode information and data from 76 colonies given with their reconstructed trees as a training set.

### Sub-challenge 2
Lineage reconstruction from inheritable and irreversible recording events for a 1000 cells in silico lineage and using for training 100 reconstructed lineages from surrogate trees of 100 cells.

### Sub-challenge 3
Lineage reconstruction from inheritable and irreversible recording events for a 10,000 cells in silico lineage and using for training 100 reconstructed lineages from similar trees of around 1000 cells.

### Example Reconstructions for Sub-challenges
For each sub-challenge, we present an example and a different algorithm to reconstruct a tree.  You can look at the example code [here](https://www.synapse.org/#!Synapse:syn20692755/wiki/597065).

## Assessment
For all sub-challenges, evaluation of distance between the ground truth and the reconstructed lineages will be assessed using the [Robinsons-Fould or RF metric](https://link.springer.com/chapter/10.1007/BFb0102690) and the [Triplets Distance](https://academic.oup.com/sysbio/article/45/3/323/1616252).

![RF and Triplet Distances](https://github.com/Sage-Bionetworks-Challenges/Allen-DREAM-Challenge/blob/master/metrics_diagram.png?raw=true)

Ground truth files can be found under the `groundtruth_files/` folder.

## How to Score

### Requirements
* `pip3 install cwltool`
* [Docker](https://www.docker.com/get-started)
* [Synapse account](https://www.synapse.org/) (so that you can pull the scoring harness model)

### Usage

#### Sub-challenge 1
To score a prediction file for SC1, run the following command:

```bash
cwltool score_sc1.cwl --inputfile /path/to/file.txt \
                      --goldstandard /path/to/file.txt 
```
where:
* `inputfile` - filepath to the prediction file
* `goldstandard` - filepath to the SC1 ground truth file (available in `groundtruth_files/`)

##### Example

```bash
cwltool score_sc1.cwl --inputfile sample_predictions/sc1.txt \
                      --goldstandard groundtruth_files/sc1.txt
```

This will output the following scores into an outfile file called `results.json`:

```json
{
    "RF_average": 0.5277933333333333,
    "Triples_average": 0.5970300000000001,
    "prediction_file_status": "SCORED"
}
```

#### Sub-challenge 2
To score a prediction file for SC2, run the following command:

```bash
cwltool score_treecmp.cwl --inputfile /path/to/file.nw \
                          --goldstandard /path/to/file.nw \
                          --runnum 1
```
where:
* `inputfile` - filepath to the prediction file
* `goldstandard` - filepath to the SC2 ground truth file (available in `groundtruth_files/`)
* `runnum` - number of runs/iterations

##### Example

```bash
cwltool score_treecmp.cwl --inputfile sample_predictions/sc2.nw \
                          --goldstandard groundtruth_files/sc2.nw \
                          --runnum 1
```

This will output the following scores into an outfile file called `results.json`:

```json
{
    "RF": 0.7201,
    "Triples": 0.944,
    "prediction_file_status": "SCORED"
}
```

#### Sub-challenge 3
To score a prediction file for SC3, run the following command:

```bash
cwltool score_sc3.cwl --inputfile /path/to/file.nw \
                      --goldstandard /path/to/file.nw 
```
where:
* `inputfile` - filepath to the prediction file
* `goldstandard` - filepath to the SC3 ground truth file (available in `groundtruth_files/`)

##### Example

```bash
cwltool score_sc3.cwl --inputfile sample_predictions/sc3.txt \
                      --goldstandard groundtruth_files/sc3.txt
```

This will output the following scores into an outfile file called `results.json`:

```json
{
    "RF": 0.40584785795732203,
    "Triples": 0.21377180208546165,
    "prediction_file_status": "SCORED"
}
```
