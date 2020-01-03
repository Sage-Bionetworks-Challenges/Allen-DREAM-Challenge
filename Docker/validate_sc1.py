#!/usr/bin/env python3

"""Validate SC1."""

import argparse
import json

import dendropy

import validate


def check_header(header):
    """Check that the header is two columns only: dreamID and nw."""

    error = ""
    try:
        dream_id, nwk = header.rstrip("\r\n").replace("\"", "").split("\t")
    except ValueError:
        error = "Two tab-delimited columns are expected"
    else:
        if dream_id != "dreamID" or nwk != "nw":
            error = "Column headers should be: 'dreamID', 'nw'"
    return error


def check_id(dream_id):
    """Check that dreamID is integer from 1 to 30."""

    error = ""
    try:
        dream_id = int(dream_id)
        assert 1 <= dream_id <= 30
    except (ValueError, AssertionError):
        error = "dreamID(s) should be a number from 1 to 30"
    return error, dream_id


def check_tree(tree):
    """Check that prediction tree is valid Newick-format."""

    error = ""
    try:
        tree = dendropy.Tree.get(
            data=tree.strip("\""),
            schema="newick")

    except Exception as err:
        error = f"Prediction tree(s) not a valid Newick tree format: {err}"

    return error, tree


def get_gs_trees(gs_file):
    """Map dreamID to goldstandard tree."""

    def get_key_val(line):
        key, _, value = line.strip().partition("\t")
        return int(key), value.strip("\"")

    with open(gs_file) as gold:
        gold.readline()  # ignore header
        return dict(get_key_val(line) for line in gold)


def main(submission, entity_type, goldstandard, results):
    """Validate submission and write results to JSON.

    Args:
        submission: input file
        entity:
        goldstandard: truth file
        results: output file
    """

    invalid_reasons = set()

    if submission is None:
        invalid_reasons = {
            f"Expected FileEntity type but found {entity_type}"}
    else:
        with open(submission) as pred:
            error = check_header(pred.readline())
            if error:
                invalid_reasons.add(error)
            else:
                gs_data = get_gs_trees(goldstandard)

                for row in pred:

                    columns = row.rstrip("\r\n").split("\t")

                    if len(columns) > 1:
                        id_error, tree_id = check_id(columns[0])
                        tree_error, pred_tree = check_tree(columns[1])

                        format_error = "".join([id_error, tree_error])
                        if format_error:
                            invalid_reasons.add(
                                f"dreamId {tree_id:02d}: " + format_error)
                        else:
                            gs_tree = dendropy.Tree.get(data=gs_data[tree_id],
                                                        schema="newick")
                            errors = validate.validate_tree(pred_tree, gs_tree)
                            if errors:
                                invalid_reasons.add(
                                    f"dreamId {tree_id:02d}: " + errors[0])
                    else:
                        invalid_reasons.add(
                            "Two tab-delimited columns are expected")

    prediction_file_status = "INVALID" if invalid_reasons else "VALIDATED"

    result_dict = {'prediction_file_errors': "\n".join(sorted(invalid_reasons))[:500],
                   'prediction_file_status': prediction_file_status,
                   'round': 1}

    with open(results, 'w') as out:
        out.write(json.dumps(result_dict))


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
