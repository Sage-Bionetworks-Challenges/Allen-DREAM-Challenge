#!/usr/bin/env python3

import argparse
import json
import dendropy


def check_header(header):
    """Check that the header is two columns only: dreamID and nw."""

    error = ""
    try:
        dream_id, nw = header.rstrip("\r\n").replace("\"", "").split("\t")
    except ValueError:
        error = "Two tab-delimited columns are expected: 'dreamID', 'nw'"
    else:
        if dream_id != "dreamID" or nw not in ["ground", "nw"]:
            error = "Column headers should be: 'dreamID', 'nw'"
    return error


def check_id(dream_id):
    """Check that dreamID is integer from 1 to 30."""

    error = ""
    try:
        dream_id = int(dream_id)
        assert 1 <= dream_id <= 30
    except ValueError:
        error = "dreamID should be an integer"
    except AssertionError:
        error = f"Unknown dreamID found: {dream_id}"
    return error, dream_id


def check_tree(tree):
    """Check that prediction tree is valid Newick-format."""

    error = ""
    try:
        tree = dendropy.Tree.get(
            data=tree,
            schema="newick")

    except Exception:
        error = "A prediction tree is not a valid Newick tree format"

    return error, tree


def get_gs_trees(gs_file):
    def get_pair(line):
        key, sep, value = line.strip().partition("\t")
        return int(key), value.strip("\"")

    with open(gs_file) as gs:
        gs.readline()  # ignore header
        return dict(get_pair(line) for line in gs)


def main(submission, entity_type, goldstandard, results):
    """Validate submission and write results to JSON.

    Args:
        submission: input file
        entity:
        goldstandard: truth file
        results: output file
    """

    invalid_reasons = set()

    # Validation 1: submission is a file, not a Synapse project.
    if submission is None:
        invalid_reasons = {
            f"Expected FileEntity type but found {entity_type}"}
    else:
        with open(submission) as pred:

            # Validation 2: only two columns: dreamID, nw
            error = check_header(pred.readline())
            if error:
                invalid_reasons.add(error)
            else:
                gs_data = get_gs_trees(goldstandard)

                for row in pred:

                    columns = row.rstrip("\r\n").split("\t")
                    id_error, tree_id = check_id(columns[0])
                    tree_error, pred_tree = check_tree(columns[1])

                    if id_error or tree_error:
                        invalid_reasons.add(id_error)
                        invalid_reasons.add(tree_error)
                    else:

                        # Validation 6: tree uses barcode as label names.
                        try:
                            gs_tree = dendropy.Tree.get(
                                data=gs_data[tree_id], schema="newick")
                            valid_names = [
                                t.label for t in gs_tree.taxon_namespace]
                            taxons = all(
                                [t.label in valid_names
                                    for t in pred_tree.taxon_namespace])
                            assert taxons

                        except AssertionError:
                            invalid_reasons.add(
                                "Unknown leaf labels found; only use barcodes"
                                + " as label names, e.g. 1_2012210001")

    prediction_file_status = "INVALID" if invalid_reasons else "VALID"

    result = {'prediction_file_errors': "\n".join(invalid_reasons),
              'prediction_file_status': prediction_file_status,
              'round': 1}

    with open(results, 'w') as out:
        out.write(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission_file",
                        required=True, help="Submission File")
    parser.add_argument("-g", "--goldstandard",
                        required=True, help="Truth File")
    parser.add_argument("-e", "--entity_type",
                        required=True, help="Synapse entity type")
    parser.add_argument("-r", "--results",
                        required=True, help="Results filename")

    args = parser.parse_args()
    main(args.submission_file, args.entity_type,
         args.goldstandard, args.results)
