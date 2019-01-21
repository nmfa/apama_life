from pysys.constants import *
from pysys.basetest import BaseTest
from progress.apama.correlator import CorrelatorHelper

class PySysTest(BaseTest):

    def execute(self):
        # create the correlator helper, start the correlator 
        correlator = CorrelatorHelper(self)
        correlator.start(logfile='correlator.log')
        correlator.setApplicationLogFile('application.log')
        correlator.applicationEventLogging(True)
                           
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
                                   '3x3_square.evt'])
        
        # Check the number of monitors after each tick.
        
        # 0
        correlator.toStringAll(filename='state.log')
        self.assertLineCount(file='state.log', expr='xPos = ', condition='==26')
        
        for i in range(7):
            correlator.send(filenames=['time.evt'])
            correlator.toStringAll(filename='state.log')
            # Remember i starts at zero, so is one less than tick count.
            if (i == 0 or i == 1):
                self.assertLineCount(file='state.log', expr='xPos = ', condition='==38')
            if (i == 2):
                self.assertLineCount(file='state.log', expr='xPos = ', condition='==46')
            if (i == 3):
                self.assertLineCount(file='state.log', expr='xPos = ', condition='==58')
            if (i == 4):
                self.assertLineCount(file='state.log', expr='xPos = ', condition='==66')
            if (i == 5 or i == 6):
                self.assertLineCount(file='state.log', expr='xPos = ', condition='==77')
        
        
    def validate(self):
        self.assertDiff(file1='application.log', file2='application.log', \
                        replace=[(r'^.*INFO  \[.*\] -','INFO -')])