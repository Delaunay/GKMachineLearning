from unreal.mladapter import UnrealEnv
from unreal.mladapter.core import AgentConfig
from unreal.mladapter.socket import NoActiveSession
from unreal.mladapter import logger

import pkg_resources
import time


def load_exec(name):
    try:
        return pkg_resources.resource_filename(__name__, name)
    except Exception:
        return None


cartpole_linux = load_exec("Cooked/LinuxNoEditor/Cartpole.sh")
cartpole_windows = load_exec("Cooked/WindowsNoEditor/Cartpole.exe")


class Cartpole(UnrealEnv):
    """
    Parameters
    ----------
    path: str
        path to the project file (.uproject), leave to None to use the packaged version

    ue_params: UEParams
        Unreal Engine additional parameters, leave to None to connect to a running instance

    """

    MAP = "/Game/CartPole/CartPole.umap"
    PROJECT_NAME = None
    USE_IMAGE = True

    def __init__(self, path=None, ue_params=None, **kwargs):
        if path is None:
            path = cartpole_windows

        Cartpole.PROJECT_NAME = path

        if ue_params is not None:
            ue_params.set_default_map_name(Cartpole.MAP)

        super().__init__(
            ue_params=ue_params, timeout=180, **kwargs # standalone=cartpole_windows is not None
        )

    def reset(self, wait_action=None, skip_time=1):
        """Specialize reset to reset our agents after each reset.
        We need to do that because 
        
        """
        if not self.is_connected():
            raise NotConnected
        logger.debug('{}: reset'.format(self._debug_id))

        self.conn.reset()

        # wait until game says it's not over
        start = time.time()
        try:
            while not self.conn.is_ready():
                if time.time() - start > self._timeout:
                    raise TimeoutError(f"Waited more than {self._timeout} s for reset")

                if self.action_space is not None:
                    self.conn.act(self._agent_id, self.wrap_action(
                        self.action_space.sample() if wait_action is None else wait_action))
                self.skip(skip_time)

        except NoActiveSession:
            self._setup_agents(True)

        self._steps_performed = 0
        return self._get_observation()

    @staticmethod
    def default_agent_config():
        agent_config = AgentConfig()

        # Our pawn that the agent is controlling
        agent_config.avatarClassName = "Pawn_Cart_C"

        # Actuators define the action space
        agent_config.add_actuator(
            "InputKey", dict(ignore_keys="esc", ignore_actions="Quit")
        )

        # Sensors define the observation space
        if Cartpole.USE_IMAGE:
            agent_config.add_sensor(
                "Camera",
                {
                    "width": "32",
                    "height": "32",

                    # Note that value does not matter
                    "tick_every_frame": "1",

                    # tick_every_n_frames
                    # tick_every_x_seconds
                },
            )
            return agent_config

        # Add our pawn movement (i.e cart movement)
        agent_config.add_sensor(
            "Movement", {"location": "absolute", "velocity": "absolute"}
        )

        # Add sight so we can see the pole
        agent_config.add_sensor(
            "AIPerception",
            {
                "count": "2",  # Number of actors it can see
                "sort": "distance",  # how the actors are sorted `distance`` or `in_front`
                "peripheral_angle": 180,  # sight cone
                "mode": "rotator",  # vector (HeadingVector) or rotator
                # max_age
            },
        )

        return agent_config
