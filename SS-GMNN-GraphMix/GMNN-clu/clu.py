import numpy as np
from sklearn.cluster import KMeans

# from utils import load_data
import loader


dataset = '../data/pubmed'
net_file = dataset + '/net.txt'
label_file = dataset + '/label.txt'
feature_file = dataset + '/feature.txt'
train_file = dataset + '/train.txt'

vocab_node = loader.Vocab(net_file, [0, 1])
vocab_label = loader.Vocab(label_file, [1])
vocab_feature = loader.Vocab(feature_file, [1])

label = loader.EntityLabel(file_name=label_file, entity=[vocab_node, 0], label=[vocab_label, 1])
labels = np.array(label.itol)
# print(len(labels), labels)
# assert False

feature = loader.EntityFeature(file_name=feature_file, entity=[vocab_node, 0], feature=[vocab_feature, 1])
feature.to_one_hot(binary=True)
features = np.array(feature.one_hot)
# print(features.shape)
# assert False

with open(train_file, 'r') as fi:
    idx_train = [vocab_node.stoi[line.strip()] for line in fi]

# _, features, labels, idx_train, _, _, _ = load_data(dataset)

class_num = labels.max() + 1
feat_dim = features.shape[1]

centroids_labeled = np.zeros((class_num, feat_dim))
for cn in range(class_num):
    lf = features[idx_train]
    ll = labels[idx_train]
    centroids_labeled[cn] = lf[ll == cn].mean(axis=0)

cluster_labels = np.ones(labels.shape) * -1
cluster_labels[idx_train] = labels[idx_train]
kmeans = KMeans(n_clusters=200, random_state=0).fit(features)

for cn in range(200):
    centroids_unlabeled = features[kmeans.labels_==cn].mean(axis=0)
    label_for_cluster = np.linalg.norm(centroids_labeled - centroids_unlabeled, axis=1).argmin()
    for node in np.where(kmeans.labels_==cn)[0]:
        if node in idx_train:
            continue
        cluster_labels[node] = label_for_cluster

# print(len(idx_train))
# print(cluster_labels[:50])
# print(cluster_labels[cluster_labels > 6])
cluster_labels_file = './cluster_labels/' + dataset[7:] +'.npy'
np.save(cluster_labels_file, cluster_labels)

