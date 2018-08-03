# atari-breakout-ML
Use reinforcement learning to train computer to play Atari Breakout.

# DQN with Experience Replay algorithm from DeepMind
Initialize replay memory D to capacity N</br>
  Initialize action-value function Q with random weights
    for episode = 1, M do
      Initialise sequence s1 = {x1} and preprocessed sequenced φ1 = φ(s1)
      for t = 1, T do
        With probability  select a random action at
        otherwise select at = maxa Q∗
        (φ(st), a; θ)
        Execute action at in emulator and observe reward rt and image xt+1
        Set st+1 = st, at, xt+1 and preprocess φt+1 = φ(st+1)
        Store transition (φt, at, rt, φt+1) in D
        Sample random minibatch of transitions (φj , aj , rj , φj+1) from D
        Set yj =
        
        rj for terminal φj+1
        rj + γ maxa0 Q(φj+1, a0
        ; θ) for non-terminal φj+1
        Perform a gradient descent step on (yj − Q(φj , aj ; θ))2
        according to equation 3
  end for
end for
