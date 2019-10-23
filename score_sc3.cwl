#!/usr/bin/env cwl-runner
#
# Example score submission file
#
cwlVersion: v1.0
class: CommandLineTool
baseCommand: score_sc3.py

hints:
  DockerRequirement:
    dockerPull: docker.synapse.org/syn20692756/scoring_harness:v2

inputs:
  - id: inputfile
    type: File
  - id: goldstandard
    type: File
  - id: check_validation_finished
    type: boolean?

arguments:
  - valueFrom: $(inputs.inputfile.path)
    prefix: -f
  - valueFrom: $(inputs.goldstandard.path)
    prefix: -g
  - valueFrom: results.json
    prefix: -r
  - valueFrom: '/TreeCmp'
    prefix: -p

requirements:
  - class: InlineJavascriptRequirement
     
outputs:
  - id: results
    type: File
    outputBinding:
      glob: results.json
