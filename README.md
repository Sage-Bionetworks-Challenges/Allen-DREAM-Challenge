# Allen-DREAM-Challenge
Infrastructure and analysis code for the [Allen Institute Cell Lineage Reconstruction DREAM Challenge](https://www.synapse.org/AllenCellLineage) (2019).

## Challenge Questions

### Sub-challenge 1
Reconstruct the lineage of each of 30 colonies in the best possible way using only the barcode information and data from 76 colonies given with their reconstructed trees as a training set.

### Sub-challenge 2
Lineage reconstruction from inheritable and irreversible recording events for a 1000 cells in silico lineage and using for training 100 reconstructed lineages from surrogate trees of 100 cells.

### Sub-challenge 3
Lineage reconstruction from inheritable and irreversible recording events for a 10,000 cells in silico lineage and using for training 100 reconstructed lineages from similar trees of around 1000 cells.

## Assessment
For all sub-challenges, evaluation of distance between the ground truth and the reconstructed lineages will be assessed using the [Robinsons-Fould or RF metric](https://link.springer.com/chapter/10.1007/BFb0102690) and the [Triplets Distance](https://academic.oup.com/sysbio/article/45/3/323/1616252).

## How to Score

### Requirements
* `pip3 install cwltool`
* A Synapse account / configuration file (earn more [here](https://docs.synapse.org/articles/client_configuration.html#for-developers))
* A Synapse submission (learn more [here](https://docs.synapse.org/articles/evaluation_queues.html#submissions))

### Usage

To score a prediction file, run the following command:

```bash
cwltool workflow.cwl --submissionId 12345 \
                      --adminUploadSynId syn123 \
                      --submitterUploadSynId syn456 \
                      --workflowSynapseId syn789 \
                      --synaspeConfig ~/.synapseConfig
```
where:
* `submissionId` - Synapse submission ID
* `adminUploadSynId` - Syanspe ID of a folder accessible only to the submission queue administrator
* `submitterUploadSynId` - Synapse ID of a folder accessible to the submitter
* `workflowSynapseId` - Synapse ID of an entity containing a reference to the workflow file(s)
* `synapseConfig` - filepath to your Synapse credentials
