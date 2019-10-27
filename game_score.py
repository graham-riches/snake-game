"""
@author Graham Riches
@brief A scoring class for use in games
@description
    GameScore is intended to be a singleton object
    where any number of score objects can be created and tracked.
    Process:
        1. Create a GameScore object
        2. Create a new score 
        3. Modify the score using score event handlers
"""
import json
import functools

class GameScore:
    """
    A class for keeping track of game scores, and 
    handling scoring events
    """
    def __init__(self, _filepath = 'score.json'):
        """
        Class constructor with optional filepath for score name.
        """
        self.scores = {}  # empty dict will hold dicts of score objects
        pass
    
    def register(func):
        """
        register decorator to add score objects to the 
        scores dict. This makes it easy to add scores
        with totally different dict structures
        """
        def attach_score(self, *args, **kwargs):
            _tag, _score = func(self, *args, **kwargs)
            self.scores[_tag] = _score
        return attach_score

    @register
    def new_simple_score(self, _tag):
        """
        create a new single valued score
        with a name.
        """ 
        _score = {'score':0} # simple score only has one value
        return _tag, _score
       


