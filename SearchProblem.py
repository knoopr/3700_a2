from bisect import insort

class SearchProblem:
  """
  This class represents the superclass for a search problem.

  Programmers should subclass this superclass filling in specific
  versions of the methods that are stubbed below.
  """

  def __init__( self, state=None ):
    """
    Stub
    Constructor function for a search problem.

    Each subclass should supply a constructor method that can operate with
    no arguments other than the implicit "self" argument to create the
    start state of a problem.

    It should also supply a constructor method that accepts a "state"
    argument containing a string that represents an arbitrary state in
    the given search problem.

    It should also initialize the "path" member variable to a string.
    """
    raise NotImplementedError("__init__");

  # class variable holding a set of strings representing states of the
  # problem that have been visited by the search algorithm
  #visited = set();

  def edges( self ):
    """
    Stub
    This method must supply a list or iterator for the Edges leading out 
    of the current state.
    """
    raise NotImplementedError("edges");

  def is_target( self ):
    """
    Stub
    This method must return True if the current state is a goal state and
    False otherwise.
    """

    raise NotImplementedError("is_target");

  def __repr__( self ):
    """
    This method must return a string representation of the current state
    which can be "eval"ed to generate an instance of the current state.
    """

    return self.__class__.__name__ + "( " + repr(self.state) + ")";

  def Wrong_place(self, input_Array):
    """
    Stub
    This method must return the number of pieces that are currently in the correct place
    """
    raise NotImplementedError("Wrong_place");

  def target_found( self ):
    """
    This method is called when the target is found.

    By default it prints out the path that was followed to get to the 
    current state.
    """
    print "Depth = " + str(len(self.path)),
    print "Total States = " + str(self.total_States[0]),
    print "- Solution: " + self.path


  def continue_search( self ):
    """
    This method should return True if the search algorithm is to continue
    to search for more solutions after it has found one, or False if it
    should not.
    """
    return False;

  def dfs( self ):
    """
    Perform a depth first search originating from the node, "self".
    Recursive method.
    """
  
  #self.visited.add( repr(self ) );	# add current node to class variable
					# visited
    for action in self.edges(): # consider each edge leading out of this node
      action.destination.path = self.path + str(action.label);	
					# get the label associated with the
					# action and append it to the path
					# string
      if action.destination.is_target(): 
				# check if destination of edge is target node
        action.destination.target_found();	# perform target found action
        if not self.continue_search():	# stop searching if not required
          return 1
      #if repr(action.destination) in self.visited:
      #continue;		# skip if we've visited this one before
      if action.destination.dfs() == 1:   # resume recursive search
        return 1


  def bfs(self, level=0, queue = []):
    if not queue:               #if nothing in the queue yet, assume that we are just starting
      queue.append(Edge( "", "", self))
    
    while queue and not len(queue[0].destination.path) == level:
      queue_Node = queue.pop(0)        #Remove the top node from the queue
      for action in queue_Node.destination.edges():
        action.destination.path = queue_Node.destination.path + str(action.label);
        queue.append(action)

    #Once all of the queue is the given depth
    for action in queue:
        if action.destination.is_target():
          action.destination.target_found()
          if not self.continue_search():
            break


  def h1_Search(self):
      greatest = 0
      the_Queue = [self]
      first_Item = 1
      
      while len(the_Queue) > 0:
          if first_Item == 1:
              next_Search = the_Queue.pop(0)
              current_Edges = next_Search.edges()
              the_Path = ""
              first_Item = 0
          else:
              next_Search = the_Queue.pop(0)
              current_Edges = next_Search[1].destination.edges()
              the_Path = next_Search[1].destination.path
          for action in current_Edges:
              action.destination.path = the_Path + str(action.label);
              result = action.destination.Wrong_place()
              result += len(action.destination.path)
              if (result,action) not in the_Queue:
                  insort(the_Queue,(result,action))
              if action.destination.is_target(): # check if destination of edge is target node
                  action.destination.target_found();	# perform target found action
                  if not self.continue_search():	# stop searching if not required
                      return 1

  def h2_Search(self):
    greatest = 0
    the_Queue = [self]
    first_Item = 1
    
    while len(the_Queue) > 0:
        if first_Item == 1:
            next_Search = the_Queue.pop(0)
            current_Edges = next_Search.edges()
            the_Path = ""
            first_Item = 0
        else:
            next_Search = the_Queue.pop(0)
            current_Edges = next_Search[1].destination.edges()
            the_Path = next_Search[1].destination.path
        for action in current_Edges:
            action.destination.path = the_Path + str(action.label);
            result = action.destination.Places_to()
            result += len(action.destination.path)
            if (result,action) not in the_Queue:
                insort(the_Queue,(result,action))
            if action.destination.is_target(): # check if destination of edge is target node
                action.destination.target_found();	# perform target found action
                if not self.continue_search():	# stop searching if not required
                    return 1

class Edge:
  """
  This class represents an edge between two nodes in a SearchProblem.
  Each edge has a "source" (which is a subclass of SearchProblem), a
  "destination" (also a subclass of SearchProblem) and a text "label".
  """

  def __init__( self, source, label, destination ):
    """
    Constructor function assigns member variables "source", "label" and
    "destination" as specified.
    """
    self.source = source;
    self.label = label;
    self.destination = destination;

  def __repr__( self ):
    return "Edge(" + repr( self.source ) + "," + \
                     repr( self.label ) + "," + \
                     repr( self.destination ) + ")";
