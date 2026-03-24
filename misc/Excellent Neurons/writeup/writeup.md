1. Note Hidden2 has a single output node, a2, therefore the Output Layer is entirely determined by that node.
2. The weights of the Output Layer are of such magnitude (+/- 300), the bias is irrelevant if a2 is large.
3. Notably, the Output Layer biases are a valid solution to the neural network. So if a2 was 0, the large Output Layer weights wouldn't matter (W3*a2 = 0) and output would be FLAG. Even if a2 was near 0, this could work.
4. Since the bias in H2 is so small, a2 would be near 0 if a1 was all zeros. Similarly, (W1*a1 = 0) so we could ignore the weights, and just get the small bias.
5. a1 would be all 0s if x*W1 + b1 = 0. Fortunately, W1 is all 0s, 1s, or -1s with only 1 non-zero value for each H1 neuron. So we need to find +/- x + b1 = 0. This means that the biases in H1 directly correspond to the desired input.
6. Using Weights=1 in W1 and the corresponding biases, we can compute ASCII(Bias * 127) (to undo normalization) to get the letters, but they're scrambled
7. Use the index of the weights to unscramble and reveal the flag.