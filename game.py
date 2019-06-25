"""Selenium interfacing between Python and Chrome Javascript

Authors:
    Ravi Munde
        project description on Medium: https://medium.com/acing-ai/how-i-build-an-ai-to-play-dino-run-e37f37bdf153
        starter code from: https://github.com/ravi72munde/Chrome-Dino-Reinforcement-Learning
    Gael Colas
"""

import time
import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from args import get_game_args


class Game:
    """'Game' class: interface between Python (AI agent) and Chrome Javascript (game)
    
    Attributes:
        '_drive' (selenium.webdriver): Chrome Webdriver 
    """
    def __init__(self, args):
        """Launch the browser window.
        
        Remarks:
            The display options can be modified.
        """
        # mute the infobars
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("disable-infobars")
        
        # launch the Chrome browser window
        self._driver = webdriver.Chrome(executable_path = args.chrome_driver_path, chrome_options=chrome_options)
        
        # size and position of the window
        #self._driver.set_window_position(x=-10,y=0)
        #self._driver.set_window_size(200, 300)
        
        # go to the game url
        self._driver.get(args.game_url)
        
        # set the simulation parameters
        self.set_config(args)
        
    def set_config(self, args):
        """Set the parameters of the simulation.
        
        Remarks:
            The settable parameters are: initial and maximum speed of the dino, acceleration of the dino.
        """
        # set the initial speed for the first and the next simulations
        self._driver.execute_script("Runner.instance_.currentSpeed = {}".format(args.initial_speed))
        self._driver.execute_script("Runner.instance_.config.SPEED = {}".format(args.initial_speed))
        # set the maximum speed
        self._driver.execute_script("Runner.instance_.config.MAX_SPEED = {}".format(args.max_speed))
        # set the acceleration
        self._driver.execute_script("Runner.instance_.config.ACCELERATION = {}".format(args.acceleration))
        # set the initial free time
        self._driver.execute_script("Runner.instance_.config.CLEAR_TIME = {}".format(args.clear_time))
        
        # set the game sprite
        if args.dino_sprite_1x:
            # open the image
            with open(args.dino_sprite_1x, 'rb') as image_file:
                # convert bytes to base64
                encoded_image = base64.b64encode(image_file.read())
            # add the header
            encoded_image = "data:image/png;base64," + str(encoded_image)[2:-1]
            
            # find corresponding html object
            element = self._driver.find_element_by_id("offline-resources-1x")
            # set the sprite
            self._driver.execute_script("arguments[0].setAttribute('src','{}')".format(encoded_image), element)
            
            # open the image
            with open(args.dino_sprite_2x, 'rb') as image_file:
                # convert bytes to base64
                encoded_image = base64.b64encode(image_file.read())
            # add the header
            encoded_image = "data:image/png;base64," + str(encoded_image)[2:-1]
            
            # find corresponding html object
            element = self._driver.find_element_by_id("offline-resources-2x")
            # set the sprite
            self._driver.execute_script("arguments[0].setAttribute('src','{}')".format(encoded_image), element)
            
            # force to use this sprite
            #self._driver.execute_script("IS_HIDPI = false")
            #self._driver.execute_script("Runner.instance_.loadImages()")            

    def get_crashed(self):
        """Check if the agent has crashed on an obstacle. 
        Gets the state of the agent from the game Javascript variable.
        
        Return:
            'hasCrashed' (bool): True if the agent has crashed
        """
        # send a Javascript signal to Chrome
        hasCrashed = self._driver.execute_script("return Runner.instance_.crashed")
        return hasCrashed
        
    def get_playing(self):
        """Check if the game is playing (ie not paused and not game over). 
        Gets the state of the agent from the game Javascript variable.
        
        Return:
            'isPlaying' (bool): True if the game is playing (not crashed and not game over)
        """
        # send a Javascript signal to Chrome
        isPlaying = self._driver.execute_script("return Runner.instance_.playing")
        return isPlaying
        
    def get_score(self):
        """Get the current score from the corresponding Javascript variable.
        
        Return:
            'score' (int): current score
            
        Remarks:
            The Javascript score variable is of type array. 
            Example: a score of 100 is stored in the format [1,0,0].
        """
        # send a Javascript signal to Chrome
        score_array = self._driver.execute_script("return Runner.instance_.distanceMeter.digits")
        score = int(''.join(score_array)) 
        return score
        
    def get_n_sim(self):
        """Get the number of simulations played.
        
        Return:
            'n_sim' (int): number of simulations played
        """
        # send a Javascript signal to Chrome
        n_sim = self._driver.execute_script("return Runner.instance_.playCount")
        return n_sim
        
    def restart(self):
        """Restart the game.
        """
        # send a Javascript signal to Chrome
        self._driver.execute_script("Runner.instance_.restart()")
        # sleep at the beginning because there is no obstacle
        #time.sleep(0.25)# no actions are possible for 0.25 sec after game starts, 
        
    def press_up(self):
        """Press the UP Arrow key.
        """
        # send a Javascript signal to Chrome
        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_UP)
        
    def press_down(self):
        """Press the DOWN Arrow key.
        """
        # send a Javascript signal to Chrome
        self._driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)
        
    def set_duck(self, duck_time):
        """Make the Dino duck for the specified amount of time.
        
        Args:
            'duck_time' (float): how long (in s) the Dino has to duck
        """
        # check if the Dino is currently jumping
        isJumping = self._driver.execute_script("return Runner.instance_.tRex.jumping")
        
        if isJumping:
            # if jumping: speed drop, activated only when jump key is not pressed
            self._driver.execute_script("return Runner.instance_.tRex.setSpeedDrop()")
        else:
            # otherwise duck
            self._driver.execute_script("return Runner.instance_.tRex.setDuck(true)")
            time.sleep(duck_time)
            self._driver.execute_script("return Runner.instance_.tRex.setDuck(false)")        

    def pause(self):
        """Pause the game.
        """
        return self._driver.execute_script("return Runner.instance_.stop()")
        
    def resume(self):
        """Resume the game if the agent has not crashed.
        """
        return self._driver.execute_script("return Runner.instance_.play()")
        
    def end(self):
        """Close the browser window and end the game.
        """
        self._driver.close()
        
    def get_obstacle(self):
        """Get the information about the next obstacle.
        
        Return:
            'obstacle_info' (dict): dictionary gathering the next obstacle information
            
        Remarks:
            The information gathered:
                - 'type' of obstacle: 'CACTUS_SMALL', 'CACTUS_LARGE' or 'PTERODACTYL'
                - 'config' of obstacle: number of consecutive cactuses for 'CACTUS' (1, 2 or 3) and flying level of 'PTERODACTYL' (100, 75 or 50)
                - 'width' of obstacle
                - 'dx': pixel x-distance between the dino and the next obstacle
        """
        # get list of generated obstacles
        obstacles = self._driver.execute_script("return Runner.instance_.horizon.obstacles")
        
        if not obstacles: # no obstacles have been generated yet
            return None
        
        next_obstacle = obstacles[0]
        
        # check if the obstacle has been passed
        dino_x_pos = self._driver.execute_script("return Runner.instance_.tRex['xPos']")
        if (len(obstacles) > 1) and next_obstacle['xPos'] < dino_x_pos:
            next_obstacle = obstacles[1]
        # REMARK: when ducking is allowed, a more thorough test may be useful to avoid landing on the obstacle
        #if (len(obstacles) > 1) and next_obstacle['xPos'] +  next_obstacle['width'] < dino_x_pos:
        
        # obstacle information
        obstacle_info = {'type': next_obstacle['typeConfig']['type']}
        
        if obstacle_info['type'] == 'PTERODACTYL':
            # flight level
            obstacle_info['config'] = next_obstacle['yPos']
            
        elif 'CACTUS' in obstacle_info['type']:
            # number of consecutive cactuses
            obstacle_info['config'] = next_obstacle['size']
            
        else: # UNHANDLED OBSTACLE TYPE
            return None
        
        obstacle_info['width'] = next_obstacle['width']
        obstacle_info['dx'] = next_obstacle['xPos']
        
        return obstacle_info

    def get_dino_state(self):
        """Get the information about the current state of the dino.
        
        Return:
            'dino_state' (dict): dictionary gathering the current dino state
            
        Remarks:
            The information gathered:
                - 'status' of dino: 'RUNNING', 'JUMPING' or 'DUCKING'
                - 'y' position of dino: only changes when jumping
                - 'speed': current speed of dino
        """
        # all the stored information on dino
        dino_info = self._driver.execute_script("return Runner.instance_.tRex")
        currentSpeed = self._driver.execute_script("return Runner.instance_.currentSpeed")
        
        # dino state
        dino_state = {'status': dino_info['status'], 'y': dino_info['yPos'], 'speed': currentSpeed}
        return dino_state
        
        
if __name__=='__main__':
    # get arguments needed to play the Game
    args = get_game_args()
    # create a game
    game = Game(args)
    # launch the game by jumping
    game.press_up()
    # wait
    time.sleep(2.)
    # dino jumps
    game.press_up()
    # wait
    time.sleep(1.)
    # pause game
    game.pause()
    print("The game is paused:", not game.get_playing())
    # wait 
    time.sleep(2.)
    # resume game 
    game.resume()
    # dino ducks until crash
    while game.get_playing():
        game.press_down()
    print("The Dino has crashed:", game.get_crashed())
    # wait
    time.sleep(2.)
    # restart game
    game.restart()
    # wait
    time.sleep(2.)
    # end game
    game.end()

    