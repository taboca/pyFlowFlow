import os
import webapp2
import logging

import stateFlow

class state_test_1(stateFlow.stateBase):

    state = {
        "success" : 'state_test_1',
        "error"   : 'state_test_1_FAIL',
        "depends" : [
        ],
        "yields"  : [
            {'true': 'state_test_2'}
        ]
    }

    def execute(self, webSelf):
        self.debug('executing...' + self.state['success'])
        self.flow(self, True, True)

stateFlow.export("state_test_1",state_test_1)

class state_test_2(stateFlow.stateBase):

    state = {
        "success" : 'state_test_2',
        "error"   : 'state_test_2_FAIL',
        "depends" : [
            {"true": 'state_test_1'}
        ],
    }

    def execute(self, webSelf):

        webSelf.response.out.write("state_test_2")

        self.debug('executing...' + self.state['success'])
        self.flow(self, True, False)

stateFlow.export("state_test_2",state_test_2)

# Call from web = webapp.RequestHandler
class web_test_states_1_2(webapp2.RequestHandler):
  def get(self):

      # We do this because this is asynchronous,
      # So this is like trying to recover a state sequence
      # If passes, pass self, and aims states chained  or exits
      a = state_test_1()
      a.run(None, self, True)

app = webapp2.WSGIApplication([

    ('/test', web_test_states_1_2)

], debug=True)
