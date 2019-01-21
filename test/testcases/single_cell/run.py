from pysys.constants import *
from pysys.basetest import BaseTest
from progress.apama.correlator import CorrelatorHelper

class PySysTest(BaseTest):

    def execute(self):
        # create the correlator helper, start the correlator 
        correlator = CorrelatorHelper(self)
        correlator.start(logfile='correlator.log')
        correlator.setApplicationLogFile('application.log')
                           
        # inject the monitors (directory defaults to the testcase input)
        correlator.injectMonitorscript(filenames=['ScenarioService.mon',
                                                  'DataViewService_Interface.mon', \
                                                  'DataViewService_Impl_Dict.mon'], \
                                       filedir=os.path.join(self.project.APAMA_HOME, 'monitors'))        
       
        correlator.injectMonitorscript(filenames=['ArenaEvents.mon', \
                                                  'CellEvents.mon'], \
                                       filedir=os.path.join(self.project.root, 'eventdefinitions'))
        correlator.injectMonitorscript(filenames=['Arena.mon', \
                                                  'Cell.mon'], \
                                       filedir=os.path.join(self.project.root, 'monitors'))
        
        correlator.send(filenames=['setup.evt', \
                                   'single_cell.evt'])

        correlator.toStringAll(filename='state.log')
        
        
    def validate(self):
        # Check there is only the master Cell monitor still in existence.
        self.assertLineCount(file='state.log', expr='xPos = ', condition='==1')
        self.assertDiff(file1='application.log', file2='application.log', \
                        replace=[(r'^.*INFO  \[.*\] -','INFO -')])