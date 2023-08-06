import gym
import numpy as np
from gym.envs.registration import register

from griddly import GriddlyLoader, gd


class GymWrapper(gym.Env):

    def __init__(self, yaml_file, level=0, global_observer_type=gd.ObserverType.SPRITE_2D,
                 player_observer_type=gd.ObserverType.SPRITE_2D, image_path=None, shader_path=None):
        """
        Currently only supporting a single player (player 1 as defined in the environment yaml
        :param yaml_file:
        :param level:
        :param global_observer_type: the render mode for the global renderer
        :param player_observer_type: the render mode for the players
        """

        # Set up multiple render windows so we can see what the AIs see and what the game environment looks like
        self._renderWindow = {}

        loader = GriddlyLoader(image_path, shader_path)

        self._grid = loader.load_game(yaml_file)
        self._grid.load_level(level)

        self.action_input_mappings = self._grid.get_action_input_mappings()

        self.available_action_input_mappings = {}
        self.action_names = []
        for k, mapping in sorted(self.action_input_mappings.items()):
            if not mapping['Internal']:
                self.available_action_input_mappings[k] = mapping
                self.action_names.append(k)

        self.available_actions_count = len(self.action_names)

        self.avatar_object = self._grid.get_avatar_object()

        self._has_avatar = self.avatar_object is not None and len(self.avatar_object) > 0

        self._num_actions = 0
        for action, action_ids in self.action_input_mappings.items():
            if len(action_ids) > self._num_actions:
                self._num_actions = len(action_ids) + 1

        self._players = []
        self.player_count = self._grid.get_player_count()

        self.game = self._grid.create_game(global_observer_type)

        for p in range(1, self.player_count + 1):
            self._players.append(self.game.register_player(f'Player {p}', player_observer_type))

        self._last_observation = {}

        self.game.init()



    def step(self, action):
        """
        Step for a particular player in the environment
        action can be in the format:

        ...actionData - if there is a single player and a single action definition, the action parameter can just be an integer

        [playerId, ...actionData] - If there is a single action definiton but multiple players

        [actionDefinitionId, ...actionData] - If there is a single player but multiple action definitions

        [playerId, actionDefinitionId, ...actionData] - if there are multiple players and multiple defined actions
        (like move, push, punch..)

        The ...actionData parameter refers to a list of integers that define the parameters of the action.
        in SELECTIVE* action control schemes this is 3 parameters [x, y, actionId]
        in DIRECT* action control schemes this is just the single actionId parameter

        :param action:
        :return:
        """

        # TODO: support more than 1 action at at time
        # TODO: support batches for parallel environment processing

        defined_action_id = 0
        player_id = 0
        action_data = []

        if isinstance(action, int):
            assert self._has_avatar, "The environment expects x and y coordinates as well as an action Id"
            assert self.available_actions_count == 1, "when there are multiple defined actions, an array of ints need to be supplied as an action"
            assert self.player_count == 1, "when there are multiple players, an array of ints need to be supplied as an action: []"
            action_data = [action]
        elif isinstance(action, list) or isinstance(action, np.ndarray):

            if (len(action) == 2 and self._has_avatar) or (len(action) == 4 and not self._has_avatar):
                if self.available_actions_count == 1:
                    assert self.player_count > 1, "There is only a single player and a single action definition. Action should be supplied as a single integer"
                    player_id = action[0]
                    action_data = action[1:]
                elif self.player_count == 1:
                    assert self.available_actions_count > 1, "There is only a single player and a single action definition. Action should be supplied as a single integer"
                    defined_action_id = action[0]
                    action_data = action[1:]
            elif (len(action) == 3 and self._has_avatar) or (len(action) == 5 and not self._has_avatar):
                player_id = action[0]
                defined_action_id = action[1]
                action_data = action[2:]
                assert player_id < self.player_count, "Unknown player Id"
                assert defined_action_id < self.available_actions_count, "Unknown defined action Id"
            elif len(action) == 1:
                action_data = action
            else:
                raise RuntimeError("action must be a single integer, a list of integers or a numpy array of integers")
        else:
            return

        action_name = self.action_names[defined_action_id]
        reward, done = self._players[player_id].step(action_name, action_data)
        self._last_observation[player_id] = np.array(self._players[player_id].observe(), copy=False)
        return self._last_observation[player_id], reward, done, None

    def reset(self, level_id=None, level_string=None):

        if level_string is not None:
            self._grid.load_level_string(level_string)
        elif level_id is not None:
            self._grid.load_level(level_id)

        self.game.reset()
        player_observation = np.array(self._players[0].observe(), copy=False)
        global_observation = np.array(self.game.observe(), copy=False)

        self._last_observation[0] = player_observation

        self._grid_width = self._grid.get_width()
        self._grid_height = self._grid.get_height()

        self.player_observation_shape = player_observation.shape
        self.global_observation_shape = global_observation.shape

        self._observation_shape = player_observation.shape
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=self._observation_shape, dtype=np.uint8)

        if self._has_avatar:
            self.action_space = gym.spaces.MultiDiscrete([self._num_actions])
        else:
            self.action_space = gym.spaces.MultiDiscrete([self._grid_width, self._grid_height, self._num_actions])

        return self._last_observation[0]

    def render(self, mode='human', observer=0):

        if observer == 'global':
            observation = np.array(self.game.observe(), copy=False)
        else:
            observation = self._last_observation[observer]

        if mode == 'human':
            if self._renderWindow.get(observer) is None:
                from griddly.RenderTools import RenderWindow
                self._renderWindow[observer] = RenderWindow(observation.shape[1], observation.shape[2])
            self._renderWindow[observer].render(observation)

        return np.array(observation, copy=False).swapaxes(0, 2)

    def get_keys_to_action(self):
        keymap = {
            (ord('a'),): 1,
            (ord('w'),): 2,
            (ord('d'),): 3,
            (ord('s'),): 4,
            (ord('e'),): 5
        }

        return keymap


class GymWrapperFactory():

    def build_gym_from_yaml(self, environment_name, yaml_file, global_observer_type=gd.ObserverType.SPRITE_2D,
                            player_observer_type=gd.ObserverType.SPRITE_2D, level=None):
        register(
            id=f'GDY-{environment_name}-v0',
            entry_point='griddly:GymWrapper',
            kwargs={
                'yaml_file': yaml_file,
                'level': level,
                'global_observer_type': global_observer_type,
                'player_observer_type': player_observer_type
            }
        )
