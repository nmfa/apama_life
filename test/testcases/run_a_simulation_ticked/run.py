from pysys.constants import *
from pysys.basetest import BaseTest
from pysys.utils.filereplace import *
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
        
        correlator.send(filenames=['start_conditions.evt'])

        correlator.flush()
        
        for i in range(22):
            correlator.setApplicationLogFile('application' + str(i+1) + '.log')
            correlator.send(filenames=['tick.evt'])
            correlator.flush()
            self.assertDiff(file1='application' + str(i+1) + '.log', file2='unscaled_application' + str(i+1) + '.log', \
                            ignores=['Spawned cell', 'Killed cell'], \
                            sort=True, \
                            replace=[(r'^.*INFO  \[.*\] -','INFO -'), \
                                     (r'Cell \[.*\]','Cell [X]'), \
                                     (r'"Arena:.*"','"Arena:X"')])        
        
               
        
    def validate(self):
        self.assertTrue(True)