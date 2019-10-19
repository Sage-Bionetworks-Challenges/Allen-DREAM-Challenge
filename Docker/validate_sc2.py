#!/usr/bin/env python3

"""Validate SC2."""

import argparse
import json

import dendropy


def valid_tree_size(tree):
    """Check size of prediction tree."""

    return len(tree.taxon_namespace) == 1000


def valid_leaf_names(tree):
    """Check that prediction tree uses correct leaf labels."""

    valid_names = ["x " + "%04d" %
                   i for i in range(1000)]
    return all([leaf.label in valid_names
                for leaf in tree.taxon_namespace])


def main(submission, entity_type, results):
    """Validate submission and write results to JSON.

    Args:
        submission: input file
        entity: Synapse entity type
        results: output file
    """

    invalid_reasons = []

    if submission is None:
        invalid_reasons = [
            f"Expected FileEntity type but found {entity_type}"]
    else:
        try:
            pred_tree = dendropy.Tree.get(file=open(submission, 'r'),
                                          schema="newick",
                                          tree_offset=0)
        except Exception:
            invalid_reasons = [
                "Prediction tree not a valid Newick tree format"]
        else:
            if not valid_tree_size(pred_tree):
                invalid_reasons.append(
                    "Prediction tree does not have 1,000 cell lines")

            if not valid_leaf_names(pred_tree):
                invalid_reasons.append(
                    "Leaf names should be cell IDs, e.g x_0000")

    prediction_file_status = "INVALID" if invalid_reasons else "VALID"

    result_dict = {'prediction_file_errors': "\n".join(invalid_reasons),
                   'prediction_file_status': prediction_file_status,
                   'round': 1}

    with open(results, 'w') as out:
        out.write(json.dumps(result_dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission_file",
                        required=True, help="Submission File")
    parser.add_argument("-e", "--entity_type",
                        required=True, help="Synapse entity type")
    parser.add_argument("-r", "--results",
                        required=True, help="Results filename")

    args = parser.parse_args()
    main(args.submission_file, args.entity_type, args.results)
