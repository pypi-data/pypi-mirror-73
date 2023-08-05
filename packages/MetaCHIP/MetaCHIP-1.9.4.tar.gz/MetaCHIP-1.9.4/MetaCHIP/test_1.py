# from ete3 import Tree
#
#
# def subset_tree(tree_file_in, leaf_node_list, tree_file_out):
#     tree_in = Tree(tree_file_in, format=0)
#     tree_in.prune(leaf_node_list, preserve_branch_length=True)
#     tree_in.write(format=0, outfile=tree_file_out)
#
#
#
# tree_file_in    = '/Users/songweizhi/Desktop/NorthSea18bins_p3_species_tree.newick'
# tree_file_out   = '/Users/songweizhi/Desktop/NorthSea18bins_p3_species_tree_subset.newick'
#
# leaf_node_file = '/Users/songweizhi/Desktop/node_list.txt'
#
# leaf_node_list = []
# for node in open(leaf_node_file):
#     leaf_node_list.append(node.strip())
#
#
# subset_tree(tree_file_in, leaf_node_list, tree_file_out)
#
#

from distutils.spawn import find_executable

print(find_executable('blastn'))
print(find_executable('fasttree'))

print(find_executable('fasttree') == None)