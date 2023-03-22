import random 
import numpy as np
import math
import matplotlib.pyplot as plt
import time  
from IPython.display import display, clear_output
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data

class Environment():

    '''
    An Environment class. 
    '''
    
    def __init__(self, xsize=100, ysize=100):
        self.xsize = xsize
        self.ysize = ysize
        self.environ = np.zeros((self.xsize,self.ysize,3))
        self.environ[:,:,0] = 0.38
        self.environ[:,:,1] = 0.19
        self.environ[:,:,2] = 0.04
        self.animal_agents = []

    
    def add_agent(self,agent):
        self.animal_agents.append(agent)
    
    def simulate(self,tot_time):
        for dt in range(tot_time):
            clear_output(wait=True)
            plt.figure(figsize=(6, 6))    
            plt.imshow(self.environ) 
            ax = plt.gca()   
            
            # loop over each animal
            temp_agents = []
            temp_hunted_agents = []
            for agent in self.animal_agents:
                agent.roaming()
                agent.draw(ax)
                
                if agent.ptype == "Prey":
                    agent.aging()
                    
                    if agent.check_if_dead():
                        del agent
                    else:
                        temp_agents.append(agent)
                        temp_new_agents = agent.procreate(dt, self.animal_agents)
                        if len(temp_new_agents) > 0:
                            temp_agents.extend(temp_new_agents)
                else:
                    caught_prey = agent.hunt(self.animal_agents)
                    if caught_prey:
                        temp_hunted_agents.append(caught_prey)

            for agent in temp_hunted_agents:
                temp_agents.remove(agent)        
            self.animal_agents.clear
            self.animal_agents = temp_agents
            plt.xlim(0,self.xsize)
            plt.ylim(0,self.ysize)
            plt.show()   
            time.sleep(0.001)      

    def simulate_plot_populations(self,tot_time):
        self.light_brown_animals = []
        self.dark_brown_animals = []
        self.times = []
        for dt in range(tot_time):
            
            # loop over each animal agent
            temp_agents = []
            temp_hunted_agents = []
            for agent in self.animal_agents:
                agent.roaming()
                
                if agent.ptype == "Prey":
                    agent.aging()
                    
                    if agent.check_if_dead():
                        del agent
                    else:
                        temp_agents.append(agent)
                        temp_new_agents = agent.procreate(dt, self.animal_agents)
                        if len(temp_new_agents) > 0:
                            temp_agents.extend(temp_new_agents)
                elif agent.ptype == "Predator":
                    caught_prey = agent.hunt(self.animal_agents)
                    if caught_prey:
                        temp_hunted_agents.append(caught_prey)
                    temp_agents.append(agent)
            
            for agent in temp_hunted_agents:
                temp_agents.remove(agent)
            self.animal_agents.clear
            self.animal_agents = temp_agents

            self.times.append(dt)
            self.light_brown_animals.append(0)
            self.dark_brown_animals.append(0)
            for agent in self.animal_agents:
                if agent.color == 'goldenrod':
                    self.light_brown_animals[-1] += 1
                elif agent.color == "saddlebrown":
                    self.dark_brown_animals[-1] += 1

        plt.plot(self.times,self.light_brown_animals,label="Light Brown")   
        plt.plot(self.times,self.dark_brown_animals,label="Dark Brown")
        plt.legend(loc="best")
        plt.show()  
