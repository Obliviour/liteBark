from state import State

class WaitingForKeywordState(State):
    """
    The state which indicates that there the robot is waiting
    to be told a command.
    """
    
    def on_event(self, event):
        if event == 'follow_me':
            return FollowState()
        return self


class FollowState(State):
    """
    The state which indicates that the robot is following a
    light.
    """
    
    def on_event(self, event):
        if event == 'stop'
            return WaitingForKeywordState()
        return self

