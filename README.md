# GraphAutoencoder
Embedding the graph nodes using a deep fully connected autoencoder 

Consider the graph G(V,E). The embedding starts from the graph incidence matrix with each column (equivalently row) representing the local neighborhood for each graph vertex. Each vertex is then represented with a column of size |V|, that is mapped to a code of size d, where d << |V|.

For more details look at "Representation Learning on Graphs: Methods and Applications" by William L. Hamilton, Rex Ying, Jure Leskovec, that is avaialble at https://arxiv.org/abs/1709.05584

files:

--data.txt: includes the incidence matrix
--incidence_data.ods: lists the graph 
--autoencode_toy.py: main file

to run:

go to the source code directory and run --- python autoencoder_toy.py
