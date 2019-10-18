#!/usr/bin/env python3
"""TreeCmp Scoring"""
import argparse
import json
import os
import subprocess

import pandas as pd


def run_treecmp(path_reference_newick, path_input_newick, path_score_output,
                path_to_treecmp):
    """Run TreeCmp

    Args:
        path_reference_newick: Path to reference tree
        path_input_newick: Path to input tree
        path_score_output: Path to scores
        path_to_treecmp: Path to TreeCmp
    """
    path_treecmp_jar = os.path.join(path_to_treecmp, 'bin/TreeCmp.jar')
    #  Metrics for rooted trees
    metrics = {
        "rooted": "mc rc ns tt mp mt co",
        "unrooted": "ms rf pd qt um"
    }

    cmd = ['java', '-jar', path_treecmp_jar,
           '-P', '-N', '-I'
           '-r', path_reference_newick,
           '-i', path_input_newick,
           '-o', path_score_output,
           '-d', 'mc', 'rc', 'tt']
    # cmd.extend(metrics['rooted'].split(' '))
    subprocess.check_call(cmd)


def get_scores(path_truth_newick, path_submission_newick, path_score_output,
               path_to_treecmp):
    """Get scores

    Args:
        path_reference_newick: Path to reference tree
        path_input_newick: Path to input tree
        path_score_output: Path to scores
        path_to_treecmp: Path to TreeCmp
    """
    run_treecmp(path_reference_newick=path_truth_newick,
                path_input_newick=path_submission_newick,
                path_score_output=path_score_output,
                path_to_treecmp=path_to_treecmp)
    df_metrics = pd.read_csv(path_score_output, sep='\t', nrows=1)
    return df_metrics


def main(submissionfile, goldstandard, results, path_to_treecmp, run_num=1):
    """Get scores and write results to json

    Args:
        submissionfile: Participant submission file path
        goldstandard: Goldstandard file path
        results: File to write results to
        path_to_treecmp: Path to TreeCmp
    """
    score_dict = {}
    prediction_file_status = "SCORED"
    rf_scores = []
    triple_scores = []
    for _ in range(run_num):
        scores = get_scores(goldstandard, submissionfile,
                            "treecmp_results.out",
                            path_to_treecmp)
        rf_scores.append(scores.T[0].loc['R-F_Cluster_toYuleAvg'])
        triple_scores.append(scores.T[0].loc['Triples_toYuleAvg'])

    score_dict['RF'] = sum(rf_scores)/len(rf_scores)
    score_dict['Triples'] = sum(triple_scores)/len(triple_scores)

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
    parser.add_argument("-n", "--runnum", type=int, required=True,
                        help="Number of runs")
    args = parser.parse_args()
    main(args.submissionfile, args.goldstandard, args.results, args.treecmp,
         run_num=args.runnum)
