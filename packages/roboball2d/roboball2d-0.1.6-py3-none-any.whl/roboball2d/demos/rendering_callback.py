import math,random,time
from copy import deepcopy

from roboball2d.physics import B2World
from roboball2d.rendering import PygletRenderer
from roboball2d.rendering import RenderingConfig
from roboball2d.robot import DefaultRobotConfig
from roboball2d.robot import DefaultRobotState
from roboball2d.ball import BallConfig
from roboball2d.ball_gun import DefaultBallGun
from roboball2d.rendering import pyglet_utils


# this demo is similar to roboball2d_demo,
# but with supplementary rendering managed via a user callback

# callback for drawing a permanent ball
# at places the ball bounced on the floor
class _BouncePlaces:

    def __init__(self,
                 ball_config,
                 visual_height,
                 color=[0,1,1]):
        self._bounces = []
        self._visual_height = visual_height
        self._radius = ball_config.radius
        self._color = color

    def reset(self):
        self._bounces = []
        
    # callback function to be called
    # by the renderer
    def __call__(self,world_state):

        # each time the ball hits the floor,
        # saving the corresponding x position
        if world_state.ball_hits_floor :
            self._bounces.append(world_state.ball_hits_floor)

        # drawing
        for x in self._bounces:
            pyglet_utils.draw_ball([x,self._visual_height],
                                   0,
                                   self._radius,
                                   16,
                                   self._color,
                                   self._color)
            

# callback for drawing the robot in a given state with a specified
# color and z coordinate
class _Robot:

    def __init__(self, color, z_coordinate):
        self._color = color
        self._z_coordinate = z_coordinate
        self._robot_state = None

    def reset(self):
        self._robot_state = None

    def update_state(self, new_state):
        self._robot_state = new_state

    # callback function to be called
    # by the renderer
    def __call__(self,world_state):
        if self._robot_state is not None:
            self._robot_state.render(self._color, self._z_coordinate)

def run(rendering=True):

    """
    Runs the balls demo, in which the robot moves according to random
    torques as 1 ball bounce around. A rendering callback is used to 
    display the position the ball touched the ground.
    You may run the executable roboball2d_rendering_demo after install
    to see it in action.

    Parameters
    ----------

    rendering : 
        renders the environment if True
    
    """
    
    # configurations
    robot_config = DefaultRobotConfig()
    ball_config = BallConfig()
    visible_area_width = 6.0
    visual_height = 0.05

    # physics engine
    # physical engine
    world = B2World(robot_config,
                    ball_config,
                    visible_area_width)

    # graphics renderer

    # callback to draw permanent balls at bounce positions
    bounce_callback = _BouncePlaces(ball_config,visual_height)

    # callback for rendering of robot state with specified 
    # color and depth
    # Note that due to the nagative z coordinate the 
    # additional robot is drawn behind the simulated robot.
    robot_callback = _Robot(
            color = (0., .5, 0.), 
            z_coordinate = -0.1)

    if rendering:
        renderer_config = RenderingConfig(visible_area_width,
                                          visual_height)

        renderer = PygletRenderer(renderer_config,
                                  robot_config,
                                  ball_config,
                                  callbacks=[bounce_callback, 
                                      robot_callback])

    # ball gun : specifies the reset of
    # the ball (by shooting a new one)
    ball_gun = DefaultBallGun(ball_config)

    # robot init : specifies the reinit of the robot
    # (e.g. angles of the rods and rackets, etc)
    robot_init = DefaultRobotState(robot_config)

    # the ball and the robot will be reinit
    # when this is true
    reinit = True

    # tracking the number of times the ball bounced
    n_bounced = 0

    # we add a fixed goal
    # starting at x=3 and finishing at x=6
    goal = (2,4)
    goal_color = (0,0.7,0)
    goal_activated_color = (0,1,0)

    # running 5 episodes
    n_episodes = 0

    for episode in range(5):

        episode_end = False

        # resetting the robot and shooting
        # the ball gun
        world.reset(robot_init,
                    ball_gun)

        # resetting the permanent drawn balls
        bounce_callback.reset()

        # keeping track of the number of times the
        # ball bounced
        n_bounced = 0

        while not episode_end:


            # random policy
            torques = [random.randrange(-1.0,1.0) for _ in range(3)]

            #
            # running the physics
            #

            # returns a snapshot of all the data computed
            # and updated by the physics engine at this
            # iteration (see below for all information managed)
            # relative=True : torques are not given in absolute value,
            # but as values in [-1,1] that will be mapped to
            # [-max_torque,+max_torque]
            world_state = world.step(torques,relative_torques=True)


            # keeping track number of times the ball bounced
            if world_state.ball_hits_floor :
                n_bounced += 1
            if n_bounced >= 2 :
                # if bounced more than 2 : end of episode
                episode_end = True

            # update the robot state that is to be drawn behind the simulated 
            # robot from time to time
            if random.random() <= 0.01:
                robot_callback.update_state(deepcopy(world_state.robot))


            #
            # rendering
            #

            if rendering:
            
                # was the goal hit ?

                color = goal_color
                if world_state.ball_hits_floor :
                    p = world_state.ball_hits_floor
                    if p>goal[0] and p<goal[1]:
                        # yes, using activated color
                        color = goal_activated_color

                # the renderer can take in an array of goals
                # to display

                goals = [(goal[0],goal[1],color)]

                # render based on the information provided by
                # the physics engined
                renderer.render(world_state,goals,time_step=1.0/60.0)
