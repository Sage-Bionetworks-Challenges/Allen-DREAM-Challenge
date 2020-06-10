"""Create New Trees

Create new augmented trees based on a goldstandard tree, which will
later be used as the input file to TreeCmp.
"""

import argparse

from random import shuffle
import dendropy


def augment_tree(tree_to_edit, percent):
    """Prune leaf nodes from the given tree and return the new tree.

    Args:
        tree_to_edit (str): filepath to tree
        percent (float): percentage of leaf nodes to prune off
    """
    tree = dendropy.Tree.get(file=open(tree_to_edit, "r"),
                             schema="newick",
                             tree_offset=0)
    leaf_nodes = tree.leaf_nodes()
    shuffle(leaf_nodes)
    to_prune = leaf_nodes[:int(len(leaf_nodes)*percent)]
    tree.prune_nodes(to_prune)
    tree.suppress_unifurcations()
    return tree.as_string("newick")


def main():
    """Main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--goldstandard", required=True)
    parser.add_argument("-sc", "--subchallenge", required=True,
                        choices=["sc2", "sc3", "sc3-final"])
    parser.add_argument("-p", "--percent", default=0.3)
    parser.add_argument('-n', "--number_trees", default=100)

    args = parser.parse_args()
    gs = args.goldstandard
    with open(f"resampled_trees_{args.subchallenge}.txt", "w") as out:
        gs_tree = dendropy.Tree.get(file=open(gs, "r"),
                                    schema="newick",
                                    tree_offset=0)
        out.write(gs_tree.as_string("newick"))

        for _ in range(args.number_trees):
            augmented_tree = augment_tree(gs, args.percent)
            out.write(augmented_tree)


if __name__ == "__main__":
    main()
