import unittest
import bridge_functions as f
from bridge_functions import *

example_bridge = [[1, 'Highway 24 Underpass at Highway 403',
                   '403', 43.167233, -80.275567, '1965', '2014', '2009', 4,
                   [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
                   [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
                     '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
                    [MISSING_BCI, 72.3, MISSING_BCI, 69.5, MISSING_BCI, 70.0, MISSING_BCI,
                     70.3, MISSING_BCI, 70.5, MISSING_BCI, 70.7, 72.9, MISSING_BCI]]],

                  [2, 'WEST STREET UNDERPASS',
                   '403', 43.164531, -80.251582, '1963', '2014', '2007', 4,
                   [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
                   [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
                     '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
                    [MISSING_BCI, 71.5, MISSING_BCI, 68.1, MISSING_BCI, 69.0, MISSING_BCI,
                     69.4, MISSING_BCI, 69.4, MISSING_BCI, 70.3, 73.3, MISSING_BCI]]
                   ],

                  [3, 'STOKES RIVER BRIDGE', '6',
                   45.036739, -81.33579, '1958', '2013', '', 1,
                   [16.0], 18.4, '08/28/2013',
                   [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
                     '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
                    [85.1, MISSING_BCI, 67.8, MISSING_BCI, 67.4, MISSING_BCI, 69.2,
                     70.0, 70.5, MISSING_BCI, 75.1, MISSING_BCI, 90.1, MISSING_BCI]]
                   ]
                  ]

class test_find_bridge_condition(unittest.TestCase):

    def normal_test(self):
        expected = f.get_bridge_condition(example_bridge, 3)
        actual = 85.1
        self.assertTrue(expected, actual)