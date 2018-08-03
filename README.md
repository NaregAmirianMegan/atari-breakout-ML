# atari-breakout-ML
Use reinforcement learning to train computer to play Atari Breakout.

# DQN with Experience Replay algorithm from DeepMind
Initialize replay memory D to capacity N </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Initialize action-value function Q with random weights </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for episode = 1, M do </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Initialise sequence s1 = {x1} and preprocessed sequenced φ1 = φ(s1) </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for t = 1, T do </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With probability &#949; select a random action at </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;otherwise select at = maxa Q∗(φ(st), a; θ) </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Execute action at in emulator and observe reward rt and image xt+1 </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set st+1 = st, at, xt+1 and preprocess φt+1 = φ(st+1) </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Store transition (φt, at, rt, φt+1) in D </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sample random minibatch of transitions (φj , aj , rj , φj+1) from D </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set yj = rj for terminal φj+1 </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set yj = rj + γ maxa0 Q(φj+1, a0; θ) for non-terminal φj+1 </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Perform a gradient descent step on (yj − Q(φj , aj ; θ))2 according to equation 3 </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end for </br>
end for </br>
