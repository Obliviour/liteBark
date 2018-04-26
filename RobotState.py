from state import State

class Idle(State):
    """
    The state which indicates the robot is idle. Use
    This state as a 'menu' to choose between following
    a human, using voice control, or quitting the app.
    """
    
    def on_event(self, event):
        if event == 'left':
            return FollowHumanIdle()
        elif event == 'down':
            return VoiceControlIdle()
        elif event == 'stop' or event == 'up':
            return QuitApp()
        return self


class FollowHumanIdle(State):
    """
    The state which indicates the robot is idle, waiting
    to be told to start following a human.
    """
    
    def on_event(self, event):
        if event == 'go':
            return FollowHuman()
        elif event == 'stop' or event == 'up':
            return Idle()
        return self

class FollowHuman(State):
    """
    The state which indicates the robot is following a
    human.
    """
    
    def on_event(self, event):
        if event == 'stop':
            return FollowHumanIdle()
        return self

class VoiceControlIdle(State):
    """
    The state which indicates the robot idle, waiting to
    be told to listen to human voice for control.
    """
    
    def on_event(self, event):
        if event == 'go':
            return Forward()
        elif event == 'left':
            return RotateLeft()
        elif event == 'right':
            return RotateRight()
        elif event == 'stop' or event == 'up':
            return Idle()
        return self


class Forward(State):
    """
    The state which indicates the robot is moving forward
    when using human voice control.
    """

    def on_event(self, event):
        if event == 'stop' or event == 'up':
            return VoiceControlIdle()
        return self

class RotateLeft(State):
    """
    The state which indicates the robot is rotating left
    when using human voice control.
    """
    
    def on_event(self, event):
        if event == 'stop' or event == 'up':
            return VoiceControlIdle()
        return self

class RotateRight(State):
    """
    The state which indicates the robot is rotating right
    when using human voice control.
    """
    
    def on_event(self, event):
        if event == 'stop' or event == 'up':
            return VoiceControlIdle()
        return self


class QuitApp(State):
    """
    The state which indicates the app has quit.
    """

    def on_event(self, event):
        return self
    
