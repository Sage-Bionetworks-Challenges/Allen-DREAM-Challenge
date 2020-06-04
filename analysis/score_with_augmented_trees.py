"""Score Predictions with Different Trees

This will calculate the RF and Triplet distances with TreeCmp, using
the **submission** tree as the reference tree (-r) and the augmented
trees as the input (-i).
"""

import argparse
import os
import subprocess

from scipy.special import comb
import pandas as pd
import dendropy


def reroot_and_remap_submission(submissionfile):
    """Reroot tree if applicable, and remap nodes if non-binary tree."""
    pred_tree = dendropy.Tree.get(file=open(submissionfile, 'r'),
                                  schema="newick",
                                  tree_offset=0)
    pred_tree.suppress_unifurcations()
    root_taxon = pred_tree.find_node_with_taxon_label('root')

    # If 'root' node is in the middle, must reroot the tree.
    if root_taxon:
        pred_tree.reroot_at_node(root_taxon, update_bipartitions=False)
    output = "rerooted.nw"
    with open(output, "w") as rerooted_tree:
        pred_tree.write(file=rerooted_tree, schema="newick")
    return output


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

    # Calculating larger trees require more memory, so increase heap
    # space (Xmx) to 2G.
    cmd = ['java', '-Xmx2G',
           '-jar', path_treecmp_jar,
           '-P', '-N',
           '-r', path_reference_newick,
           '-i', path_input_newick,
           '-o', path_score_output,
           '-d', 'rc', 'tt']
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
    pd.read_csv(path_score_output, sep='\t', nrows=1)


def create_final_output(sc, output):
    """Create output file of the trees and their scores

    sc2 will use YuleAvg scores and sc3 will use normalizaed scores
    """

    scores = pd.read_csv("tmp.out", sep="\t")
    results = scores.loc[:, ["Tree", "Tree_taxa",
                             "RefTree_taxa", "Common_taxa"]]

    if sc == "sc2":
        results.loc[:, "RF_score"] = scores.loc[:, "R-F_Cluster_toYuleAvg"]
        results.loc[:, "Triples_score"] = scores.loc[:, "Triples_toYuleAvg"]
    else:
        n = scores.loc[:, "Common_taxa"]

        # Normalize RF distance.
        rf = scores.loc[:, "R-F_Cluster"]
        results.loc[:, "RF_score"] = min(1, rf/(n - 3))

        # Normalize triplet distance.
        triples = scores.loc[:, "Triples"]
        results.loc[:, "Triples_score"] = 3 * triples / \
            (2 * comb(n, 3, repetition=False))

    results.to_csv(output, sep="\t", index=False)

    # Delete temp file.
    os.remove("tmp.out")


def main():
    """Main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--submission", required=True)
    parser.add_argument("-r", "--resampled_trees", required=True)
    parser.add_argument("-sc", "--subchallenge", required=True,
                        choices=["sc2", "sc3"])
    parser.add_argument("-o", "--output", default="results.out")

    args = parser.parse_args()

    # Reroot and remap submission tree if needed, then score against
    # the augmented trees (including original goldstandard).
    rerooted_submission_path = reroot_and_remap_submission(
        args.submission)
    get_scores(rerooted_submission_path, args.resampled_trees,
               f"tmp.out", "../TreeCmp/")

    # Create output file with only the scores needed.
    create_final_output(args.subchallenge, args.output)


if __name__ == "__main__":
    main()
