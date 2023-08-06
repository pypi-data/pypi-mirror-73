# LR_exploration_tf
HTD, Cyclic, and Other basic LR callback implementation 

Paper Implementation 
1) Stochastic Gradient Descent with Hyperbolic-Tangent Decay on Classification
Download link https://arxiv.org/pdf/1806.01593.pdf
2) Cyclical Learning Rates for Training Neural Networks
Download link https://arxiv.org/pdf/1506.01186.pdf
3) LipschitzLR: Using theoretically computed adaptivelearning rates for fast convergence

Algo. implementation as classes:
1) Hyperbolic-Tangent Decay
2) Two-stage exponential decay
3) Cosine scheduler
4) Exponential decay scheduler
5) Step decay schedule
6) Cyclical Learning Rates

####### Innovation : Combained Hyperbolic-Tangent Decay and Cyclical Learning Rates #######
In this algorithm I have combained just like how two modulation signals are added ; High frequency(lr will change in every batch in a epoch) + Low frequency(lr range  will change in every epoch)
####### Results: Small implementation check in fashion_mnist dataset ########
