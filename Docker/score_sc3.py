#!/usr/bin/env python3
"""Score subchallenge 1"""
import argparse
import json

import scipy.special

import score


def main(submissionfile, goldstandard, results, path_to_treecmp):
    """Get scores and write results to json

    Args:
        submissionfile: Participant submission file path
        goldstandard: Goldstandard file path
        results: File to write results to
        path_to_treecmp: Path to TreeCmp
    """
    score_dict = {}
    prediction_file_status = "SCORED"

    scores = score.get_scores(goldstandard, submissionfile,
                              "treecmp_results.out",
                              path_to_treecmp)

    n = scores.T[0].loc['Common_taxa']
    rf = scores.T[0].loc['R-F_Cluster']
    triples = scores.T[0].loc['Triples']
    triples_score = 3*triples/(2*scipy.special.comb(n, 3, repetition=False))
    rf_score = rf/(n - 3)

    score_dict['RF'] = rf_score
    score_dict['Triples'] = triples_score
    score_dict['prediction_file_status'] = prediction_file_status
    with open(results, 'w') as output:
        output.write(json.dumps(score_dict))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--submissionfile", required=True,
                        help="Submission File")
    parser.add_argument("-r", "--results", required=True,
                        help="Scoring results")
    parser.add_argument("-g", "--goldstandard", required=True,
                        help="Goldstandard for scoring")
    parser.add_argument("-p", "--treecmp", required=True,
                        help="Path to treecmp")
    args = parser.parse_args()
    main(args.submissionfile, args.goldstandard, args.results, args.treecmp)
