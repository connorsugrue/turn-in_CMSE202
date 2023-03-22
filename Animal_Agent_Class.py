import random 
import numpy as np
import math
import matplotlib.pyplot as plt
import itertools

class Animal_Agent():

    '''
    An Animal_Agent class. 
    '''
    
    def __init__(self,xmax=100,ymax=100,ptype="Prey",sex="M",age_limit=50,catch_radius=10,mate_range=5,gestation=8,shape="o",color="saddlebrown",saturation_pop=150):
        '''
        Initaliazes an animal agent object, an autonomous agent that can interact with other agents. Specifically, predators can hunt prey,
        prey can procreate, and both predator and prey can move around and age. 

        xmax (int): The (x) size of the habitat
        ymax (int): The (y) size of the habitat
        pytpe (string): Sets whether this is a predator or prey type of animal
        sex (string): Sets the sex of the animal
        age_limit (int): Sets the age at which the animal dies of old age
        catch_radius (int): Specifies how far away a predator can find/catch prey
        mate_range (int): Specifies how far away a prey can find a mate
        gestation (int): How long does an animal need to wait between mating cycles
        shape (string): Specifies the marker to use when visualizing the animal
        color (string): Specifies the color to use when visualizing the animal
        saturation_pop (int): The saturation population, where the environment can no longer support the prey
        is_caught (bool): Flag for determining whether prey has been caught by a predator
        '''
        self.x = random.randint(0, xmax)
        self.y = random.randint(0, ymax)
        self.age = 0 
        self.ptype = ptype
        self.age_limit = age_limit
        self.catch_radius = catch_radius
        self.xmax = xmax
        self.ymax = ymax
        self.sex = sex
        self.gestation = gestation
        self.last_litter_time = 1
        self.mate_range = mate_range 
        self.color = color
        self.shape = shape
        self.saturation_pop = saturation_pop
        self.is_caught = False

    def roaming(self,vx=7,vy=7): 
        '''
        Method to proceed random walk. Checks to make sure that the position it is trying to move into is within the bounds of 
        the environment. 
        '''
        dx = np.random.randint(-vx,vx)
        dy = np.random.randint(-vy,vy)

        if (self.x + dx > self.xmax) or (self.x + dx < 0):
            self.x -= dx
        else:
            self.x += dx

        if (self.y + dy > self.ymax) or (self.y + dy < 0):
            self.y -= dy
        else:
            self.y += dy
        # print(self.x,self.y)

    def set_allele(self, alle_d, alle_m):
        '''
        Method to set the alleles of this mouse: alle_d and alle_m from dad and mom, respectively.
        The values is either 0 or 1 for each allele. 
        0 and 1 are recessive and dominant gene expressions, respectively.
        This setup will result in three types of fur_color expressions: 
        type0 ==> (0,0): 0 = 0 + 0; recessive, dark color
        type1 ==> (0,1) or (1,0): 1 = 0 + 1 = 1 + 0; dominant, light color
        type2 ==> (1,1): 2 = 1 + 1; dominant, light color
        '''
        
        self.alle_d = alle_d
        self.alle_m = alle_m
        
        # Here we set light animal color to be dominant.
        if self.alle_d + self.alle_m >= 1:
            self.color = 'goldenrod'
            self.catch_probability = 0.95
            
        else:
            self.color = "saddlebrown" 


    def draw(self,ax):
        '''
        Method to draw the animal agent using an axis object ax.
        '''
        ax.scatter(self.x, self.y, s=24.0, c=self.color, marker=self.shape)   
    
    def aging(self):
        '''
        Method to increase the age of the animal agent by one.
        '''
        self.age += 1

    def check_if_dead(self):
        '''
        Method to check whether the animal agent has died of old age.
        '''
        if self.age > self.age_limit:
            return True
        else:
            return False


    def get_distance(self,agent):
        '''
        Get the distance between agents.

        agent (Animal_Agent): An animal agent object that we're finding the distance to.
        '''
        return math.sqrt((self.x-agent.x)**2 + (self.y-agent.y)**2)
    
    def hunt(self,all_agents):
        '''
        Method for a predator to find prey. If the predator finds prey, the method sets the is_caught flag 
        and returns the prey object so it can be removed from the environment. 


        all_agents (list): A list of all of the animal agent objects 
        '''
        for agent in all_agents:
            if (agent.ptype == "Prey") and (agent.age < agent.age_limit) and not (agent.is_caught):
                if self.get_distance(agent) < self.catch_radius:
                    agent.is_caught = True
                    return agent       
        return False
    
    def procreate(self,all_agents,time):
        '''
        Method to create new agents (procreate). There are three barriers to procreation:
        1. Has it been enough time between the last procreation? (I.e., more than the gestation time.)
        2. Is there a (male) agent within range?
        3. Is the population below the saturation point? This is modeled as a logistic function.
        If all of these conditions are met, then a new litter is created. Every member of the new litter is 
        randomly assigned genes from their parents. The last litter time is set to the current time and the
        list of children is returned. 

        all_agents (list): A list of all of the animal agent objects 
        time (int): The current time, used to determine if the Animal Agent has passed the gestation period.
        '''
        
        child_list = []
        val = random.random()
        if (self.sex == 'F') and (np.mod(abs(time-self.last_litter_time),self.gestation) == 0):
            for agent in all_agents:
                if (agent.ptype=="Prey") and (agent.sex == "M") and (self.get_distance(agent) <= self.mate_range) and (val > (1.0/(1.0+np.exp(-len(all_agents)/self.saturation_pop)))):
                    child_num = int(np.random.normal(7,1))
                    for jj in range(child_num):
                        mom_a = self.alle_d
                        if np.random.randint(0,2) == 1:
                            mom_a = self.alle_m
                        dad_a = agent.alle_d
                        if np.random.randint(0,2) == 1:
                            dad_a = agent.alle_m               
                        child = Animal_Agent(sex="F")
                        if np.random.randint(0,2) == 1:
                            child = Animal_Agent(sex="M")
                        child.set_allele(dad_a,mom_a)
                        child_list.append(child)
                    self.last_litter_time = time
                    break

        return child_list


