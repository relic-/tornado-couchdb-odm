#! /usr/bin/python

__author__="Igor Krestov"
__date__ ="$26-Jul-2012 15:36:42$"


from odm import Manager
from tornado import gen

class CouchManager(Manager):
        
    @gen.engine
    def create(self, **kwargs):
        """
        Create and save new Model object based on passed keyword arguments
        """
        try: callback = kwargs.pop('callback')
        except KeyError: callback = None
        obj = self._model_class(kwargs)
        res = yield gen.Task(obj.save)
        if hasattr(callback, '__call__'):
            callback(obj)
    
    @gen.engine
    def get(self, pk):
        """
        Function fetches/ loads only **one** record, returns instance of class *Model*
        """
        res = yield gen.Task(self.db.get_doc, pk)
        callback(self._model_class(res))
        
    @gen.engine
    def fetch(self, design, view, callback, *args, **kwargs):
        """
        Loads a list of objects, returns *Iterable*.
        Each value is instance of class *Model*.
        """
        res = yield gen.Task(self.db.view,design, view, *args, **kwargs)
        callback(self._view_to_iterable(res))
        
    def _view_to_iterable(self, res):
        """
        Transforms CouchDB's *view* result into generator that produces **Model** instances
        """
        return (self._model_class(row['value']) for row in res['rows'])