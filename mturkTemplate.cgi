#!/usr/bin/python
#^DO NOT MOVE^

import mturkGenerator

DEFINE_TURK={
    'folderName':'mturk',
    'skipAtStart':2,
    'skipAtEnd':2,
    'exclusionList':["TML-30"],
    'experimentCode':"TML-30"
}
   
mturkGenerator.generateTurk(DEFINE_TURK)