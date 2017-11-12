import uuid
import logging

exportFunctionMap = {}

def export(functionStr, functionRef):
    exportFunctionMap[functionStr] = functionRef

# Base class
class stateBase():

    historyStack = []

    currentSessionWebSelf = None
    sessionFlowID         = None

    strDebug = ""

    def debug(self, str):
        logging.info(self.strDebug + str)

    def run(self, refParent, webSelf, newFlow):

        if(refParent):
            self.strDebug+='    '

        self.debug('run')

        if(newFlow is True):
            self.sessionFlowID = uuid.uuid4()
            self.currentSessionWebSelf = webSelf
        else:
            self.sessionFlowID = refParent.sessionFlowID
            self.currentSessionWebSelf = refParent.currentSessionWebSelf
            webSelf = self.currentSessionWebSelf

        self.debug('Initializing : flow session : ' + str(self.sessionFlowID))
        self.debug('Initializing : state        : ' + self.state['success'])

        if(refParent):
            #print(refParent.historyStack[len(refParent.historyStack)-1])
            #priorContext = refParent.historyStack[len(refParent.historyStack)-1]
            if(self.state['depends'][0]['true']==refParent.state['success']):
            #if(self.state['depends'][0]['true']==priorContext['state']):
                self.execute(webSelf)
            else:
                self.debug('end...')
        else:
            self.execute(webSelf)

    def flow(self, stateSelf, returnState, sameFlow):

        if(returnState):
            self.historyStack.append({'state': stateSelf.state['success']})
            self.debug("Success : pushing "+stateSelf.state['success']+" into stack history..")
        else:
            self.historyStack.append({'state': stateSelf.state['error']})
            self.debug("Error : pushing "+stateSelf.state['success']+" into stack history..")

        if (sameFlow):

            # Search in whole tree for parent state
            currentState = self.historyStack[len(self.historyStack)-1]['state']
            self.debug('sameFlow is true : checking last state : ' + currentState)
            self.debug('.. yields for ' + stateSelf.state['success'] + ' is ' + stateSelf.state['yields'][0]['true'])

#            if(stateSelf.state['yields'][0]['true']=='state_facebook_fetch'):
#                a = state_facebook_fetch()
            a=exportFunctionMap[stateSelf.state['yields'][0]['true']]()
            a.run(self, None, False)

        else:
            currentState = self.historyStack[len(self.historyStack)-1]['state']
            self.debug('..reflow : checking last state : ' + currentState)

        self.debug('State exited..')
