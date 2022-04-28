import os

from cartpole.env import Cartpole
from unreal.mladapter.utils import random_action, ArgumentParser
from unreal.mladapter.runner import UE4Params
import unreal.mladapter.logger as logger

project = "/media/setepenre/Games/UE4RL/UE4RL.uproject"
project = "E:/cartpole/UE4RL.uproject"
map = "Game/CartPole/CartPole.umap"

parser = ArgumentParser()
parser.add_argument("--iter", type=int, default=3, help="number of games to play")

parser.add_argument("--project", type=str, default=project, help="Path to the uproject")

parser.add_argument("--level", type=str, default=map, help="Path to the level to load")

parser.add_argument(
    "--launch",
    action="store_true",
    default=False,
    help="If true the game will be launched by python",
)

args = parser.parse_args()

if os.environ.get("UE-DevBinaries") is None and args.exec is None:
    raise RuntimeError("UE4 binaries not found")

logger.set_level(logger.DEBUG)

env = Cartpole(
    args.project,
    UE4Params() if args.launch else None,
    server_port=15151,
)

print("Starting Environment")

for i in range(args.iter):
    obs = env.reset()

    reward = 0
    done = False
    print("Environment initialized")

    while not env.game_over:
        a = random_action(env)
        # print(obs, a, reward, done)
        print(reward)
        obs, reward, done, _ = env.step(a)

    print("{}: Score: {}".format(i, reward))

env.close()
