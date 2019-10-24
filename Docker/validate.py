#!/usr/bin/env python3

"""Validate SC2 & SC3."""

import argparse
import json

import dendropy


def valid_tree_size(tree, size):
    """Check size of prediction tree."""

    return len(tree.taxon_namespace) == size


def valid_leaf_names(tree, gs_file, root_exists=False):
    """Check that prediction tree uses correct leaf labels."""

    gs_tree = dendropy.Tree.get(file=open(gs_file, 'r'),
                                schema="newick",
                                tree_offset=0)

    valid_names = set([t.label for t in gs_tree.taxon_namespace])
    if root_exists:
        valid_names.add('root')
    submission_names = set([t.label for t in tree.taxon_namespace])
    intersect = valid_names.intersection(submission_names)
    all_exist = len(intersect) == len(valid_names)

    return all_exist


def main(submission, entity_type, goldstandard, size, results):
    """Validate submission and write results to JSON.

    Args:
        submission: input file
        entity: Synapse entity type
        results: output file
    """

    invalid_reasons = []
    root_exists = False
    if submission is None:
        invalid_reasons = [
            f"Expected FileEntity type but found {entity_type}"]
    else:
        try:
            pred_tree = dendropy.Tree.get(file=open(submission, 'r'),
                                          schema="newick",
                                          tree_offset=0)
            root_node_exists = pred_tree.find_node_with_label('root')
            root_taxon_exists = pred_tree.find_node_with_taxon_label('root')
            if not root_node_exists:
                if root_taxon_exists:
                    size = size + 1
                    root_exists = True
                else:
                    raise ValueError("Must have 'root' in tree")
                # pred_tree.reroot_at_node(find_root, update_bipartitions=False)
            # pred_tree.write(file=open('treefile.tre', 'r'), schema="newick")
        except Exception as err:
            invalid_reasons = [
                f"Prediction tree not a valid Newick tree format: {err}"]
        else:
            if not valid_tree_size(pred_tree, size):
                invalid_reasons.append(
                    f"Prediction tree does not have {size:,} cell lines")

            if not valid_leaf_names(pred_tree, goldstandard,
                                    root_exists=root_exists):
                invalid_reasons.append(
                    "Leaf names should be cell identifiers.")

    prediction_file_status = "INVALID" if invalid_reasons else "VALIDATED"

    result_dict = {'prediction_file_errors': "\n".join(invalid_reasons)[:500],
                   'prediction_file_status': prediction_file_status,
                   'round': 1}

    with open(results, 'w') as out:
        out.write(json.dumps(result_dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission_file",
                        required=True, help="Submission file")
    parser.add_argument("-g", "--goldstandard",
                        required=True, help="Truth file")
    parser.add_argument("-e", "--entity_type",
                        required=True, help="Synapse entity type")
    parser.add_argument("-n", "--size", type=int,
                        required=True, help="Size of tree")
    parser.add_argument("-r", "--results",
                        required=True, help="Results file")

    args = parser.parse_args()
    main(args.submission_file, args.entity_type,
         args.goldstandard, args.size, args.results)
