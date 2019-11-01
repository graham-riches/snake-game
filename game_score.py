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
import os
from datetime import datetime

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
        with totally different dict structures to the class
        """
        def attach_score(self, *args, **kwargs):
            _tag, _score = func(self, *args, **kwargs)
            self.scores[_tag] = _score
        return attach_score

    @register
    def simple_score(self, _tag):
        """
        create a new single valued score
        with a name.
        """ 
        _score = {'score':0} # simple score only has one value
        return _tag, _score
    
    @register
    def simple_score_with_highscore(self, _tag, filepath=''):
        """
        simple score with highscore and an optional
        filepath argument, which loads the
        historic highscore
        """
        if filepath == '':
            _path = os.path.join(os.getcwd(), '{}.json'.format(_tag))
        else:
            _path = os.path.join(filepath, '{}'.format(_tag))
        _score = {'score':0, 'path':_path}
        return _tag, _score

    def add(self, value, _tag):
        """
        increment a score in the score dict indexed
        at _tag by value
        """
        self.scores[_tag]['score'] = self.scores[_tag]['score'] + value
        return
    
    def get_score(self, _tag):
        """
        get the score value from entry _tag
        """
        return self.scores[_tag]['score']
    
    def get_path(self, _tag):
        """
        get the filepath from a score object if it
        exists
        """
        try:
            _path = self.scores[_tag]['path']
            return _path
        except Exception:
            print('{}   ERROR: score object does not have a path property'.format(datetime.now()))
       


