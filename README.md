# atari-breakout-ML
Use reinforcement learning to train computer to play Atari Breakout.

## DQN with Experience Replay algorithm from DeepMind
Initialize replay memory D to capacity N </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Initialize action-value function Q with random weights </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for episode = 1, M do </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Initialise sequence s<sub>1</sub> = {x<sub>1</sub>} and preprocessed sequenced φ<sub>1</sub> = φ(s<sub>1</sub>) </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for t = 1, T do </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With probability &#949; select a random action a<sub>t</sub> </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;otherwise select a<sub>t</sub> = max<sub>a</sub> Q<sup>∗</sup>(φ(s<sub>t</sub>), a; θ) </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Execute action a<sub>t</sub> in emulator and observe reward r<sub>t</sub> and image x<sub>t+1</sub> </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set s<sub>t+1</sub> = s<sub>t</sub>, a<sub>t</sub>, x<sub>t+1</sub> and preprocess φ<sub>t+1</sub> = φ(s<sub>t+1</sub>) </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Store transition (φ<sub>t</sub>, a<sub>t</sub>, r<sub>t</sub>, φ<sub>t+1</sub>) in D </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sample random minibatch of transitions (φ<sub>j</sub> , a<sub>j</sub> , r<sub>j</sub> , φ<sub>j+1</sub>) from D </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set y<sub>j</sub> = r<sub>j</sub> for terminal φ<sub>j+1</sub> </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set y<sub>j</sub> = r<sub>j</sub> + γ * max<sub>a</sub> Q(φ<sub>j+1</sub>, a<sup>'</sup>; θ) for non-terminal φ<sub>j+1</sub> </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Perform a gradient descent step on (y<sub>j</sub> − Q(φ<sub>j</sub> , a<sub>j</sub> ; θ))<sup>2</sup> according to equation 3 </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;end for </br>
end for </br>
