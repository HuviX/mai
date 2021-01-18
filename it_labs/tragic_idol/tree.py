import pandas as pd
import numpy as np
import pydot
from typing import List, Optional, Dict, Any
import pickle5 as pickle


class tree:
    def __init__(self):
        self.tree = None


    @staticmethod
    def entropy(p: List[float]) -> float:
        return -sum([np.log2(x) * x for x in p])


    @staticmethod
    def leaf_df(df: pd.DataFrame, col: str, value: object) -> pd.DataFrame:
        return df[df[col] == value].reset_index(drop=True)


    def _get_tree(self, df: pd.DataFrame, target: str, tree=None) -> dict:
        get = self._max_gain(df, target)
        ent = get[1]
        col_to_split = get[0]

        unique_values = df[col_to_split].unique()
        tree = dict()
        tree[col_to_split] = dict()

        for val in unique_values:
            sub_df = self.leaf_df(df, col_to_split, val)
            vals, counts = np.unique(sub_df[target], return_counts=True)
            if ent == 0:
                tree[col_to_split][val] = vals
            elif len(counts) == 1:
                tree[col_to_split][val] = vals[0]
            else:
                tree[col_to_split][val] = self._get_tree(sub_df, target)
        return tree


    def _max_gain(self, df: pd.DataFrame, target: str) -> str:
        target_entropy = self.entropy((df[target].value_counts()/df.shape[0]).values)
        gains = {}
        #здесь считается Information gain для каждого признака.
        for col in df.columns:
            if col != target:
                vals = df[col].unique()
                sub = 0
                for val in vals:
                    probs = df[df[col] == val][target].value_counts()/df[df[col] == val].shape[0]
                    entropy_ = self.entropy(probs)
                    freq = df[df[col] == val].shape[0]/df.shape[0]
                    sub += entropy_ * freq
                gains[col] = target_entropy - sub
        #необходимо выбрать максимальный Information Gain, чтобы разбить по нему
        return sorted(gains.items(), key=lambda item: item[1], reverse=True)[0]


    def fit(self, df: pd.DataFrame, target: str) -> str:
        self.tree = self._get_tree(df, target)
        return "Done"


    def _plot_tree(self, graph: pydot.Dot, tree: Dict, parent_node=None) -> None:

        for k in tree:
            if parent_node is not None:

                from_name = parent_node.get_name().replace("\"", "") + '_' + str(k)
                from_label = str(k)

                node_from = pydot.Node(from_name, label=from_label)
                graph.add_node(node_from)
                graph.add_edge(pydot.Edge(parent_node, node_from))

                if isinstance(tree[k], dict):
                    self._plot_tree(graph, tree[k], node_from)

                else: # if leaf node
                    to_name = str(k) + '_' + str(tree[k]) # unique name
                    to_label = str(tree[k])
                    node_to = pydot.Node(to_name, label=to_label, shape='box')
                    graph.add_node(node_to)
                    graph.add_edge(pydot.Edge(node_from, node_to))

            else:
                from_name =  str(k)
                from_label = str(k)
                node_from = pydot.Node(from_name, label=from_label)
                graph.add_node(node_from)
                self._plot_tree(graph, tree[k], node_from)


    def to_png(self, path: str) -> None:
        """
        Allow to save decision tree graph as png file
        """
        assert (self.tree), "No tree created for this class instance"

        self.graph = pydot.Dot(graph_type='graph')
        self._plot_tree(self.graph, self.tree)
        self.graph.write_png(path)


    def save(self, path: str) -> None:
        """
        Allow to dump tree to pickle.
        .pkl file extension should be specified

        tree.save("path.pkl")
        """
        assert (self.tree), "No tree created for this class instance"

        with open(path, 'wb') as handle:
            pickle.dump(self.tree, handle)
    

    def load(self, path: str) -> None:
        """
        Allow to load tree from pickle file.
        .pkl file extenstion should be specified

        tree.load("path.pkl")
        """
        with open(path, 'rb') as handle:
            self.tree = pickle.load(handle)


    def predict(self, data: Dict) -> str:
        node = self.tree
        while isinstance(node, dict):
            field = list(node.keys())[0]
            key = data[field]
            node = node[field][key]
        return node
