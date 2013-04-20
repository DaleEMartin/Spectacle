# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import unittest
import time
from spectacle.main import PygameDisplayConfig
import ConfigParser

class TestDisplayConfig(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadConfig1(self):
        configParser = ConfigParser.ConfigParser()
        configParser.read('mockConfigDir/testDisplayConfig1.cfg')
        displayConfig = PygameDisplayConfig.constructWithConfig(True, configParser)
        self.assertEquals(displayConfig.cacheDirectory(), 'mockCacheDirectory')
        self.assertEquals(displayConfig.displayOnCommand(), 'mockDisplayOnCommand')
        self.assertEquals(displayConfig.displayOffCommand(), 'mockDisplayOffCommand')
