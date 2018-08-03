# atari-breakout-ML
Use reinforcement learning to train computer to play Atari Breakout.

# DQN with Experience Replay algorithm from DeepMind
Initialize replay memory D to capacity N </br>
&nbsp;&nbsp;Initialize action-value function Q with random weights </br>
    for episode = 1, M do </br>
      Initialise sequence s1 = {x1} and preprocessed sequenced φ1 = φ(s1) </br>
      for t = 1, T do </br>
        With probability  select a random action at </br>
        otherwise select at = maxa Q∗(φ(st), a; θ) </br>
        Execute action at in emulator and observe reward rt and image xt+1 </br>
        Set st+1 = st, at, xt+1 and preprocess φt+1 = φ(st+1) </br>
        Store transition (φt, at, rt, φt+1) in D </br>
        Sample random minibatch of transitions (φj , aj , rj , φj+1) from D </br>
        Set yj = rj for terminal φj+1 </br>
        Set yj = rj + γ maxa0 Q(φj+1, a0; θ) for non-terminal φj+1 </br>
        Perform a gradient descent step on (yj − Q(φj , aj ; θ))2 </br>
        according to equation 3 </br>
  end for </br>
end for </br>
