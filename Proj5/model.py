import controller, sys
import model   # Pass a reference to model to each update call in update_all

#Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter
from special import Special


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=
running = False
cycle_count = 0
simultons = set()
selected_object = ""


#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global running, cycle_count, simultons
    running = False
    cycle_count = 0
    simultons = set()

#start running the simulation
def start ():
    global running
    running = True


#stop running the simulation (freezing it)
def stop ():
    global running
    running = False


#step just one update in the simulation
def step ():
    if running:
        update_all()
        display_all()
        stop()
    else:
        start()
        update_all()
        display_all()
        stop()

#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    global selected_object
    selected_object = kind


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    if selected_object == 'Remove':
        to_remove = set()
        for sim in simultons:
            coords = sim.get_location()
            if x - 10 <= coords[0] <= x + 10 and y - 10 <= coords[1] <= y + 10:
                to_remove.add(sim)
        for sim in to_remove:
            remove(sim)
    elif selected_object is not "":
        add(eval(str(selected_object) + "(" + str(x) + "," + str(y) + ")"))
    else:
        pass


#add simulton s to the simulation
def add(s):
    global simultons
    simultons.add(s)
    

# remove simulton s from the simulation    
def remove(s):
    global simultons
    simultons.remove(s)
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    sim_set = set()
    for sim in simultons:
        if isinstance(sim, p):
            sim_set.add(sim)
    return sim_set


#call update for each simulton in the simulation (passing model as an argument)
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    global cycle_count
    to_remove = set()
    if running:
        cycle_count += 1
        for sim in simultons:
            rem = sim.update(model)
            if type(rem) is set:
                to_remove.update(rem)
        for sim in to_remove:
            remove(sim)




#delete from the canvas each simulton being simulated; afterward call display on each
#  simulton being simulated to add it back to the canvas, possibly in a new location, to
#  animate it; also, update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    for sim in simultons:
        sim.display(controller.the_canvas)
    controller.the_progress.config(text=str(len(simultons))+" balls/"+str(cycle_count)+" cycles")
