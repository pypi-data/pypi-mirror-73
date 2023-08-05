import nep
import threading
from transitions import Machine, State
import time


class ActionEngine:


    def __init__(self, robot_name, robot_type="ros"):

        class Matter(object):
            def say_hello(self): print("hello, new state!")
            pass

        self.robot_type = robot_type
        self.lump = Matter()
        self.robot_name = robot_name
        self.node = nep.node(robot_name)
        self.rize = self.node.new_pub("rize_event", "json")
        self.sharo = self.node.new_pub("action_state", "json")
        self.sub_action = self.node.new_callback("robot_action", "json", self.nep_action)
        self.robot_actions ={}
        self.action2do = {"bt":{}, "id":0}
        self.multiple = False

        self.states = ['running','idle', 'new_execution', 'new_action']
        

        self.transitions = [
        { 'trigger': 'new_request', 'source': 'idle', 'dest': 'new_action' },
        { 'trigger': 'new_execution', 'source': 'new_action', 'dest': 'running' },
        { 'trigger': 'new_request', 'source': 'running', 'dest': 'running' },
        { 'trigger': 'execution_finished', 'source': 'running', 'dest': 'idle' },
        { 'trigger': 'cancel', 'source': 'running', 'dest': 'idle' }]

        self.machine = Machine(self.lump, states=self.states, transitions=self.transitions, initial='idle')
        print("Robot state: " + self.lump.state)
        self.running = True

        # ------------------------- Action thread ------------------------------------
        self.action_thread = threading.Thread(target = self.onActionLoop)
        self.action_thread.start()
        time.sleep(.1)
        
        # ------------------------- Stop thread ------------------------------------
        self.cancel_thread = threading.Thread(target = self.onCancelLoop)
        self.cancel_thread.start()
        time.sleep(.1)
        

    def onActionLoop(self):
        print("Action loop started")
        while self.running:  # While in execution
            if(self.lump.state == "new_action"):
                self.lump.trigger('new_execution')
                if self.robot_type == "aldebaran":
                    self.runNAOAction(self.action2do)
                else:
                    self.runAction(self.action2do)
                    
                print("Execution finished: " + self.action2do["id"])  
                self.lump.trigger('execution_finished')

    def runAction(self, message, cancel = False):
            """ Run an action
                
                Parameters
                ----------

                message : dictionary
                    Use the Action description
                cancel : bool
                    Use the Cancel action description

            """

            action = message["primitives"]                                                                                         # Get list of concatenated primitives
            if(type(action) == list):
                
                n_primitives = len(action)                                                                                             # How many actions are?
                in_parallel = True                                                                                                     # Start variable           
                # Perform all the actions in parallel
                for i in range(n_primitives):                                                                                          # Run primitives in parallel until the last one
                            
                    # Except the last one
                    if (i == n_primitives-1):
                        in_parallel = False
                        
                    primitive = action[i]                                                                                              # Get parameters 
                    primitive_name = primitive["primitive"] #Name of the primitive
                    input_ = primitive["input"]
                    options = primitive["options"]

                    if primitive_name in self.robot_actions:
                        # Execute function
                        if cancel:                                                                                                     # Cancel each action
                            try:
                                self.robot_cancel_actions[primitive_name]()
                            except Exception as e:
                                nep.logError(e)
                                pass
                        else:                                                                                                          # Run each action
                            try:
                                if (self.multiple):
                                    self.robot_actions[primitive_name](input_, options, in_parallel)                                    # Execute robot action
                                else:
                                    self.robot_actions[primitive_name](input_, options)
                            except Exception as e:
                                nep.logError(e)
                                nep.printError(" primitive " + str(primitive_name) + " was not executed")
                    else:
                        nep.printError(" primitive " + str(primitive_name) + " is not registered")

                    message["state"] = "success"
                    print("Return state: " + message["id"]) + " - " + message["state"] 
                    self.sharo.publish(message)

                    
            else:
                primitive_name = action["primitive"] 
                input_ = action["input"]
                options = action["options"]
                
                if primitive_name in self.robot_actions:                                                                                                         # Run each action
                    self.robot_actions[primitive_name](input_, options)
                    message["state"] = "success"
                    print("Return state: " + message["id"]) + " - " + message["state"]
                    self.sharo.publish(message)  

                else:
                    nep.printError(" primitive " + str(primitive_name) + " is not registered")


                    

    def onCancelLoop(self):
        print("Cancel loop started")
        while self.running:  # While in execution
            time.sleep(1)


    def isValidRequest(self, action_request):
        try:
            if 'robots' in action_request and "id" in action_request:                                          # Chech if the request specify that this robot need to do the action
                if  (type(action_request['robots']) is list):                       # Is a list of robots
                    if self.robot_name in action_request['robots']:                 # Is this robot in the list
                        return  True
                    else:
                        return  False
                else:                                                               # Is this robot in the same that the string value "robots"
                    if self.robot_name == action_request['robots']: 
                        return  True
                    else:
                        return  False
        except Exception as e:
            nep.logError(e)
            print ("Invalid action_request: " + str(type(action_request)))
            return False




    def setRobotActions(self,robot_actions):
        """ Set a python dictionary with all the functions which the node can execute
            Parameters
            ----------

            robot_actions : dictionary
                Dictionary of functions
            
        """
        try:
            self.robot_actions = robot_actions                                                  # Set robot actions (functions)
        except Exception as e:
            nep.logError(e)
            print ("Error setting actions, exit...")
            self.onConnectError()                                                               # Send error message to RIZE
            time.sleep(.1)                                                                      # Wait to see the message 
            os.system('kill %d' % os.getpid())                                                  # Kill this process
            sys.exit(0)


    def nep_action(self, action_request):
        is_valid = self.isValidRequest(action_request)
        print("--- Action request--- ")
        print ("ID: " + action_request["id"])
        if(self.lump.state == "idle"):
            self.action2do = action_request
        self.lump.trigger('new_request')
        print("Robot state: " + self.lump.state)
