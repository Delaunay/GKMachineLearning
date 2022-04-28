import random
import math
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import gym.spaces

from torch.distributions import Categorical
from torchvision.utils import save_image
import unreal.mladapter.logger as logger
from unreal.mladapter.utils import random_action

from cartpole.env import Cartpole
from cartpole.model import MLP, LeNet
from cartpole.replay import ReplayMemory, Transition


logger.set_level(logger.DEBUG)

project = "E:/cartpole/UE4RL.uproject"


def space_size(x):
    def prod(lst):
        n = 1
        for i in lst:
            n *= i
        return n

    if isinstance(x, gym.spaces.Discrete):
        return x.n

    if isinstance(x, gym.spaces.MultiDiscrete):
        return sum([n for n in x.nvec])

    if isinstance(x, gym.spaces.Box):
        return prod([n for n in x.shape])

    if isinstance(x, gym.spaces.Dict):
        n = 0
        for _, item in x.spaces.items():
            n += space_size(item)
        return n

    if isinstance(x, gym.spaces.Tuple):
        n = 0
        for item in x.spaces:
            n += space_size(item)
        return n


def space_shape(x):
    if isinstance(x, gym.spaces.Box):
        return x.shape


def flatten_obs(obs, size):
    t = torch.zeros((size,))

    s = 0
    e = 0
    for ob in obs:
        v = torch.flatten(torch.Tensor(ob))
        e = v.shape[0]
        t[s : s + e] = v
        s = s + e

    return t


def swap_channel(x):
    return torch.from_numpy(x).permute(2, 0, 1)[0:3, :, :]


BATCH_SIZE = 128
GAMMA = 0.999
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 200
TARGET_UPDATE = 10


def select(cond, a, b):
    return a if cond else b


class DDQTrainer:
    def __init__(self, env) -> None:
        self.use_image = True
        self.env = env
        self.input_size = select(
            self.use_image,
            (3, 32, 32),
            space_size(env.observation_space),
        )
        self.output_size = space_size(env.action_space)  #  + 1

        self.device = "cuda"
        model = select(self.use_image, LeNet, MLP)
        self.policy = model(self.input_size, self.output_size).to(self.device)
        self.target = model(self.input_size, self.output_size).to(self.device)

        self.target.load_state_dict(self.policy.state_dict())
        self.target.eval()

        self.optimizer = optim.RMSprop(
            self.policy.parameters(),
            lr=1e-3,
            alpha=0.99,
            eps=1e-8,
            weight_decay=0.01,
            momentum=0.9,
        )
        self.memory = ReplayMemory(10000)
        self.loss = 0
        self.loss_count = 0
        self.steps_done = 0

    def select_action(self, state):
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(
            -1.0 * self.steps_done / EPS_DECAY
        )

        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                state = state.unsqueeze(0).to(self.device)

                # t.max(1) will return largest column value of each row.
                # second column on max result is index of where max element was
                # found, so we pick action with the larger expected reward.
                expected_reward = self.policy(state)
                action = expected_reward.max(1)[1]
                return action, 0, 0, 0
        else:
            return (
                torch.tensor(
                    [random.randrange(self.output_size)],
                    device=self.device,
                    dtype=torch.long,
                ),
                0,
                0,
                0,
            )

    def _select_action(self, state):
        """Our model does not return the action perse but the distribution of all the action"""

        with torch.no_grad():
            # Our batch is size=1 here
            state = state.unsqueeze(0).to(self.device)

            # without exploration
            # self.policy(state).max(1)[1].view(1, 1)

            # with exploration
            weights = self.policy.action_probs(state)
            dist = Categorical(weights)
            action = dist.sample()

            log_prob = dist.log_prob(action).unsqueeze(1)
            return action, log_prob, dist.entropy(), weights

    def optimize(self):
        if len(self.memory) < BATCH_SIZE:
            return

        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        # 128x1 = True if next_state exists
        non_final_mask = torch.tensor(
            tuple(map(lambda s: s is not None, batch.next_state)),
            device=self.device,
            dtype=torch.bool,
        )

        non_final_next_states = torch.stack(
            [s for s in batch.next_state if s is not None]
        ).to(self.device)

        # Shape is 128x11
        state_batch = torch.stack(batch.state).to(self.device)

        # Shape: 128x1
        action_batch = torch.stack(batch.action).to(self.device)

        # Shape: 128
        reward_batch = torch.cat(batch.reward).to(self.device)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net

        # Get the probability of the action given the action taken
        state_action_values = self.policy(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(BATCH_SIZE, device=self.device)

        # Get the largest action probability, shape: 128
        expected = self.target(non_final_next_states).max(1)[0].detach()
        next_state_values[non_final_mask] = expected

        # Compute the expected Q values
        expected_state_action_values = (
            (next_state_values * GAMMA) + reward_batch
        ).unsqueeze(1)

        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values)

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

        self.loss += loss.item()
        self.loss_count += 1

    def preprocess_obs(self, obs):
        if self.use_image:
            return swap_channel(obs)

        return flatten_obs(obs, self.input_size)

    def train(self, episodes):

        for i_episode in range(episodes):
            # Initialize the environment and state
            state = self.preprocess_obs(self.env.reset())
            envlog.write(f'{state.sum()}\n')

            for t in count():
                # Select and perform an action
                action, log_prob, entropy, weights = self.select_action(state)

                rpc_action = action.item()

                # values = ' '.join([f'{i: 8.2f}' for i in state.numpy()])
                msg = f"\r {t:4d} {rpc_action} {weights}"
                msg = f'{msg}{" " * (80 - len(msg))}'

                print(msg, end="")

                # We get a screenshot every 3 frames
                obs, reward, done, _ = self.env.step(rpc_action)
     
                envlog.write(f'{obs.sum()} {reward} {done}\n')
                reward = (t > 100) * reward

                obs = self.preprocess_obs(obs)

                reward = torch.tensor([reward], device=self.device)

                # Store the transition in memory
                self.memory.push(state, action, obs, reward)

                # Move to the next state
                state = obs

                # save_image(state, 'image.png')

                # Perform one step of the optimization (on the policy network)
                self.optimize()

                if done:
                    break

            if self.loss_count > 50:
                print(f"\n{i_episode} {t} Loss {self.loss / self.loss_count}")
                self.loss_count = 0
                self.loss = 0

            # Update the target network, copying all weights and biases in DQN
            if i_episode % TARGET_UPDATE == 0:
                self.memory = ReplayMemory(10000)
                self.target.load_state_dict(self.policy.state_dict())


def main():
    from unreal.mladapter.runner import UEParams
    from unreal.mladapter.utils import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--project", type=str, default=None, help="Path to the uproject"
    )
    parser.add_argument(
        "--launch",
        action="store_true",
        default=True,
        help="If true the game will be launched by python",
    )
    parser.add_argument(
        "--no-launch",
        action="store_false",
        dest="launch",
        help="Force the environment to connect to an already running instance of the game",
    )
    args = parser.parse_args()

    ueparams = None

    if args.launch:
        ueparams = UEParams(rendering=True, single_thread=True)

    with Cartpole(args.project, ue_params=ueparams, server_port=15151) as env:

        trainer = DDQTrainer(env)

        # print(env.action_space)
        # print(list(map(float, gym.spaces.flatten(env.action_space, 0))))
        # print(list(map(float, gym.spaces.flatten(env.action_space, 1))))
        # print(gym.spaces.Discrete(2).sample())

        trainer.train(500)


class SafeWrite():
    def __init__(self, file=None):
        self.file = file

    def write(self, msg):
        if self.file:
            self.file.write(msg)

envlog = SafeWrite()

if __name__ == "__main__":
    with open('env.log', 'w') as file:
        envlog.file = file

        #
        # python Source/python/cartpole/train.py --project E:/cartpole/Cartpole.uproject --exec E:/UnrealEngine/Engine/Binaries/Win64/UE4Editor.exe
        # python Source/python/cartpole/train.py --project /media/setepenre/Games/cartpole/Cartpole.uproject --exec /media/setepenre/Games/UnrealEngine/Engine/Binaries/Linux/UE4Editor
        main()
