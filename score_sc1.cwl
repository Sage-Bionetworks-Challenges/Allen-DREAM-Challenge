#!/usr/bin/env cwl-runner
#
# Score subchallenge 1
#
cwlVersion: v1.0
class: CommandLineTool
baseCommand: score_sc1.py

hints:
  DockerRequirement:
    dockerPull: docker.synapse.org/syn20692756/scoring_harness:v3

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
