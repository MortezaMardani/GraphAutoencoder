import tensorflow as tf
import numpy as np
import math
#import pandas as pd
#import sys


# graph: data structure is a dictionary
# each node has a name and the single-hop neighbors are saved as a list
graph = {'a': ['b','c'], 'b': ['d'], ...}


# graph to incidence matrix
input = np.loadtxt('data.txt')

#print input
#print input.shape
#print type(input)


noisy_input = input #+ .2 * np.random.random_sample((input.shape)) - .1
output = input

# Scale to [0,1]
scaled_input_1 = np.divide((noisy_input-noisy_input.min()), (noisy_input.max()-noisy_input.min()))
scaled_output_1 = np.divide((output-output.min()), (output.max()-output.min()))

# Scale to [-1,1]
scaled_input_2 = (scaled_input_1*2)-1
scaled_output_2 = (scaled_output_1*2)-1

input_data = scaled_input_2
output_data = scaled_output_2

# Autoencoder with 1 hidden layer
n_samp, n_input = input_data.shape 
n_hidden = 10

x = tf.placeholder("float", [None, n_input])
# Weights and biases to hidden layer
Wh = tf.Variable(tf.random_uniform((n_input, n_hidden), -1.0 / math.sqrt(n_input), 1.0 / math.sqrt(n_input)))
bh = tf.Variable(tf.zeros([n_hidden]))
h = tf.nn.tanh(tf.matmul(x,Wh) + bh)
# Weights and biases to hidden layer
Wo = tf.transpose(Wh) # tied weights
bo = tf.Variable(tf.zeros([n_input]))
y = tf.nn.tanh(tf.matmul(h,Wo) + bo)
# Objective functions
y_ = tf.placeholder("float", [None,n_input])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
meansq = tf.reduce_mean(tf.square(y_-y))

# constraints: k-hop neighbors are in k-th arc with \theta_k = 2*pi/k. 
# constraints are applied per mini-batch

def regularizer_arc(graph, list_batch_nodes=[]):

    constraint = 0
    ind_a = 0
    ind_b = 0

    for a in list_batch_nodes: #need to define batch_nodes

        ind_a = ind_a + 1

        for b in list_batch_nodes:
            ind_b = ind_b + 1

            if a not b:

                 shortest_path_ab = find_shortest_path(graph, a, b, path=[])
                 shortest_dist_ab = len(shortest_path_ab)
                 h_a = h[ind_a,:]
                 h_b = h[ind_b,:]
                 cos_ab = tf.multiply(h_a,h_b)
                 constraint = constraint + tf.abs(tf.minimum(0,cos_ab - math.cos((2*pi/num_arcs)*(shortest_dist_ab+1)))) ...
                          + tf.abs(tf.maximum(0,cos_ab - math.cos((2*pi/num_arcs)*(shortest_dist_ab)))) 

    return constraint



def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest




penalty_weight = 10
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(meansq + penalty_weight*constriant)

init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

n_rounds = 100000
batch_size = min(5, n_samp)
list_nodes = graph.keys()

for i in range(n_rounds):

    sample = np.random.randint(n_samp, size=batch_size)
    list_batch_nodes = list_nodes[sample] #name of nodes in the minibatch#
    batch_xs = input_data[sample][:]
    batch_ys = output_data[sample][:]
    sess.run(train_step, feed_dict={x: batch_xs, y_:batch_ys})

    if i % 100 == 0:
        print i, sess.run(cross_entropy, feed_dict={x: batch_xs, y_:batch_ys}), sess.run(meansq, feed_dict={x: batch_xs, y_:batch_ys})

print "Target:"
print output_data
print "Final activations:"
print sess.run(y, feed_dict={x: input_data})
print "Final weights (input => hidden layer)"
print sess.run(Wh)
print "Final biases (input => hidden layer)"
print sess.run(bh)
print "Final biases (hidden layer => output)"
print sess.run(bo)
print "Final activations of hidden layer"
print sess.run(h, feed_dict={x: input_data})