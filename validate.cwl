#!/usr/bin/env cwl-runner
#
# Validate SC2 & SC3
#
cwlVersion: v1.0
class: CommandLineTool
baseCommand: validate.py

hints:
  DockerRequirement:
    dockerPull: docker.synapse.org/syn20692756/scoring_harness:v3

inputs:
  - id: inputfile
    type: File
  - id: goldstandard
    type: File
  - id: entity_type
    type: string

arguments:
  - valueFrom: $(inputs.inputfile)
    prefix: -s
  - valueFrom: $(inputs.goldstandard.path)
    prefix: -g
  - valueFrom: $(inputs.entity_type)
    prefix: -e
  - valueFrom: results.json
    prefix: -r

requirements:
  - class: InlineJavascriptRequirement
     
outputs:
  - id: results
    type: File
    outputBinding:
      glob: results.json   

  - id: status
    type: string
    outputBinding:
      glob: results.json
      loadContents: true
      outputEval: $(JSON.parse(self[0].contents)['prediction_file_status'])

  - id: invalid_reasons
    type: string
    outputBinding:
      glob: results.json
      loadContents: true
      outputEval: $(JSON.parse(self[0].contents)['prediction_file_errors'])
