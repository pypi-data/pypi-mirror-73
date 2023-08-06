import collections
import gc

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import networkx as nx
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm


class DeepTopologicalClustering():
    def __init__(self, kmodel=None, optimizer=None, verbose=True, lmb=0.01, N=30, num_epochs=200, lr=0.001):
        self.kmodel = kmodel
        self.optimizer = optimizer
        self.verbose = verbose
        self.lmb = lmb
        self.N = N
        self.num_epochs = num_epochs
        self.lr = lr

    def fit(self, X):
        # X_rand = np.random.normal(np.mean(X, axis=1), np.var(X, axis=1), X.T.shape).T
        # self.random_matrix_ = tf.convert_to_tensor(X_rand.T, np.float32)
        self.input_matrix_ = tf.convert_to_tensor(X.T, np.float32)
        self.adjacency_matrix_ = np.zeros((self.N, self.N))

        if self.optimizer is None:
            self.optimizer_ = tf.keras.optimizers.Adam(learning_rate=self.lr)
        else:
            self.optimizer_ = self.optimizer

        if self.kmodel is None:
            y_idx = np.random.choice(range(X.shape[0]), size=self.N, replace=False)
            y = X[y_idx]
            input = tf.keras.layers.Input(shape=(X.shape[0],))
            x = tf.keras.layers.BatchNormalization()(input)
            # x = tf.keras.layers.Dense(10, activation='relu')(x)
            # x = tf.keras.layers.Dense(10, activation='relu')(x)
            output = tf.keras.layers.Dense(self.N)(x)
            self.kmodel_ = tf.keras.Model(inputs=input, outputs=output)
            self.kmodel_.compile(optimizer=self.optimizer_, loss="mse")
            # self.kmodel_.fit(X.T, y.T, epochs=20, verbose=0)

        self.loss_value_ = np.inf
        self.loss_vals = []
        self.loss_Q_ = []
        self.loss_E_ = []
        self.node_list_ = []
        pbar = tqdm(range(self.num_epochs+1))
        for epoch in pbar:
            loss_value, grads, adjacency_matrix = self._grad()
            self.loss_vals.append(loss_value.numpy())
            self.optimizer_.apply_gradients(zip(grads, self.kmodel_.trainable_variables))
            if loss_value < self.loss_value_:
                self.adjacency_matrix_ = adjacency_matrix
                self.loss_value_ = loss_value
                self.centroids_ = self.output_
            self.compute_graph()
            self.node_list_.append(len(self.G_.nodes))
            pbar.set_description(f"Epoch: {epoch} - Loss: {loss_value:.2f}")
        return self

    def _grad(self):
        with tf.GradientTape() as tape:
            loss_value, adjacency_matrix_ = self._loss(self.kmodel_(self.input_matrix_))
            # loss_value, adjacency_matrix_ = self._loss(self.kmodel_(self.random_matrix_))
        return loss_value, tape.gradient(loss_value, self.kmodel_.trainable_variables), adjacency_matrix_

    def _loss(self, output):
        self.output_ = output

        adjacency_matrix = np.zeros((self.N, self.N))
        A = tf.transpose(self.input_matrix_)
        D = _squared_dist(A, tf.transpose(output))
        d_min = tf.math.reduce_min(D, axis=1)

        s = tf.argsort(D.numpy(), axis=1)[:, :2].numpy()
        # min_inside = tf.Variable(tf.zeros((self.N,), dtype=np.float32))
        # max_outside = tf.Variable(tf.zeros((self.N,), dtype=np.float32))
        # d_max = tf.Variable(tf.zeros((self.N,), dtype=np.float32))
        for i in range(self.N):
            idx = s[:, 0] == i
            si = s[idx]
            if len(si) > 0:
                # a = A[idx]
                # b = A[~idx]
                # d_max[i].assign(tf.math.reduce_max(_squared_dist(a, tf.expand_dims(output[:, i], axis=0))))
                # min_inside[i].assign(tf.reduce_max(_squared_dist(a, a)))
                # max_outside[i].assign(tf.reduce_min(_squared_dist(a, b)))
                for j in set(si[:, 1]):
                    k = sum(si[:, 1] == j)
                    adjacency_matrix[i, j] += k
                    adjacency_matrix[j, i] += k

        E = tf.convert_to_tensor(adjacency_matrix, np.float32)

        # Fn = tf.reduce_max(min_inside)
        # Fd = tf.reduce_max(max_outside)
        # Eq2 = tf.norm(d_max)
        Eq = tf.norm(d_min)
        El = tf.norm(E, 2)
        # cost = Fn / Fd + Eq + Eq2 + El
        cost = Eq + self.lmb * El

        self.loss_Q_.append(Eq.numpy())
        self.loss_E_.append(El.numpy())

        return cost, adjacency_matrix

    def compute_graph(self):
        has_samples = []
        input_matrix = tf.transpose(self.input_matrix_)
        D = _squared_dist(input_matrix, tf.transpose(self.centroids_))
        s = tf.argsort(D.numpy(), axis=1)[:, :2].numpy()
        for i in range(self.N):
            idx = s[:, 0] == i
            if sum(idx) > 0:
                has_samples.append(True)
            else:
                has_samples.append(False)

        self.G_ = nx.Graph()
        we = []
        for i in range(0, self.adjacency_matrix_.shape[0]):
            for j in range(i + 1, self.adjacency_matrix_.shape[1]):
                if self.adjacency_matrix_[i, j] > 0 and has_samples[i] and has_samples[j]:
                    we.append((i, j, self.adjacency_matrix_[i, j]))
        self.G_.add_weighted_edges_from(we)

    def compute_sample_graph(self):
        self.centroids_ = self.kmodel_.predict(self.input_matrix_)
        n = self.input_matrix_.shape[1]
        self.adjacency_samples_ = np.zeros((n, n))
        has_samples = []
        input_matrix = tf.transpose(self.input_matrix_)
        D = _squared_dist(input_matrix, tf.transpose(self.centroids_))
        s = tf.argsort(D.numpy(), axis=1)[:, :2].numpy()
        for i in range(len(s)):
            w2 = s[i, 1]
            idx = np.argwhere(s[:, 0]==w2)
            if len(idx) > 0:
                for q in idx:
                    self.adjacency_samples_[i, q[0]] += 1
                    self.adjacency_samples_[q[0], i] += 1
        for i in range(self.N):
            idx = s[:, 0] == i
            if sum(idx) > 0:
                has_samples.append(True)
            else:
                has_samples.append(False)
            idx = np.argwhere(idx)
            if len(idx) > 0:
                for j, q in enumerate(idx):
                    for w in idx[j+1:]:
                        self.adjacency_samples_[q[0], w[0]] += 1
                        self.adjacency_samples_[w[0], q[0]] += 1

        self.G_samples_ = nx.Graph()
        we = []
        for i in range(0, self.adjacency_samples_.shape[0]):
            for j in range(i + 1, self.adjacency_samples_.shape[1]):
                if self.adjacency_samples_[i, j] > 0:
                    we.append((i, j, self.adjacency_samples_[i, j]))
        self.G_samples_.add_weighted_edges_from(we)

    def plot_adjacency_matrix(self, file_name=None, figsize=[5, 5]):
        plt.figure(figsize=figsize)
        sns.heatmap(self.adjacency_samples_, cbar=False, xticklabels=False, yticklabels=False)
        plt.tight_layout()
        if file_name is not None:
            plt.savefig(file_name)
        plt.show()
        plt.clf()
        plt.close()
        gc.collect()

    def plot_sample_graph(self, y, file_name=None, figsize=[5, 4]):
        if len(self.G_samples_.edges) == 0:
            return

        cmap = sns.color_palette(sns.color_palette("hls", len(set(y))))

        w = []
        for e in self.G_samples_.edges:
            w.append(self.adjacency_samples_[e[0], e[1]])
        wd = np.array(w)
        widths = MinMaxScaler(feature_range=(0.1, 1)).fit_transform(wd.reshape(-1, 1)).squeeze().tolist()

        node_colors_list = []
        for node in self.G_samples_.nodes:
            node_colors_list.append(cmap[y[node]])

        pos = nx.drawing.layout.spring_layout(self.G_samples_, seed=42)
        plt.figure(figsize=figsize)
        fig, ax = plt.subplots()
        c = '#00838F'
        nx.draw_networkx_nodes(self.G_samples_, pos=pos, node_size=10, node_color=node_colors_list)
        nx.draw_networkx_edges(self.G_samples_, pos=pos, width=widths, edge_color=c)
        ax.axis('off')
        plt.tight_layout()
        if file_name is not None:
            plt.savefig(file_name)
        plt.show()
        plt.clf()
        plt.close()
        gc.collect()

    def plot_graph(self, y, file_name=None, figsize=[5, 4]):

        if len(self.G_.nodes) == 0:
            return

        X = self.input_matrix_.numpy().T
        if X.shape[1] > 2:
            tsne = TSNE(n_components=2, random_state=42)
            M_list = [X]
            nodes_idx = []
            nodes_number = []
            for i, node in enumerate(self.G_.nodes):
                nodes_idx.append(i)
                nodes_number.append(node)
                M_list.append(self.centroids_[:, node].numpy().reshape(1, -1))
            M = np.concatenate(M_list)
            Mp = tsne.fit_transform(M)
            Xp = Mp[:X.shape[0]]
            Wp = Mp[X.shape[0]:]
            pos = {}
            for i in range(len(Wp)):
                pos[nodes_number[i]] = Wp[nodes_idx[i]].reshape(1, -1)[0]
        else:
            Xp = X
            pos = {}
            for i in self.G_.nodes:
                pos[i] = self.centroids_[:, i]
        w = []
        for e in self.G_.edges:
            w.append(self.adjacency_matrix_[e[0], e[1]])
        wd = np.array(w)
        widths = MinMaxScaler(feature_range=(0, 5)).fit_transform(wd.reshape(-1, 1)).squeeze().tolist()

        plt.figure(figsize=figsize)
        fig, ax = plt.subplots()
        if y is not None:
            cmap = sns.color_palette(sns.color_palette("hls", len(set(y))))
            sns.scatterplot(Xp[:, 0], Xp[:, 1], hue=y, palette=cmap, hue_order=set(y), alpha=0.3, legend=False)
        else:
            sns.scatterplot(Xp[:, 0], Xp[:, 1])
        c = '#00838F'
        nx.draw_networkx_nodes(self.G_, pos=pos, node_size=200, node_color=c)
        # nx.draw_networkx(self.G_, pos=pos, node_size=0, width=0, font_color='white', font_weight="bold")
        nx.draw_networkx(self.G_, pos=pos, node_size=0, width=0, with_labels=False)
        nx.draw_networkx_edges(self.G_, pos=pos, width=widths, edge_color=c)
        ax.axis('off')
        plt.tight_layout()
        if file_name is not None:
            plt.savefig(file_name)
        plt.show()
        plt.clf()
        plt.close()
        gc.collect()


def _squared_dist(A, B):
    row_norms_A = tf.reduce_sum(tf.square(A), axis=1)
    row_norms_A = tf.reshape(row_norms_A, [-1, 1])  # Column vector.

    row_norms_B = tf.reduce_sum(tf.square(B), axis=1)
    row_norms_B = tf.reshape(row_norms_B, [1, -1])  # Row vector.

    return row_norms_A - 2 * tf.matmul(A, tf.transpose(B)) + row_norms_B
