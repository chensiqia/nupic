# ----------------------------------------------------------------------
#  Copyright (C) 2011, 2012 Numenta Inc, All rights reserved,
#
#  The information and source code contained herein is the
#  exclusive property of Numenta Inc, No part of this software
#  may be used, reproduced, stored or distributed in any form,
#  without explicit written authorization from Numenta Inc.
# ----------------------------------------------------------------------

"""
Template file used by ExpGenerator to generate the actual
permutations.py file by replacing $XXXXXXXX tokens with desired values.

This permutations.py file was generated by:
'/Users/ronmarianetti/nta/eng/lib/python2.6/site-packages/nupic/frameworks/opf/expGenerator/ExpGenerator.py'
"""

import os

from nupic.swarming.permutationhelpers import *

# The name of the field being predicted.  Any allowed permutation MUST contain
# the prediction field.
# (generated from PREDICTION_FIELD)
predictedField = 'consumption'

permutations = {
  
  'modelParams': {
    'sensorParams': {
      'encoders': {
        'consumption': PermuteEncoder(fieldName='consumption', 
                                      encoderClass='ScalarEncoder',
                                       maxval=PermuteInt(100, 300, 1), 
                                       n=PermuteInt(13, 500, 1), 
                                       w=7, 
                                       minval=0),
      },
    },
  
  
    'tpParams': {
      'minThreshold': PermuteInt(9, 12),
      'activationThreshold': PermuteInt(12, 16),
    },
  
  
    }
}


# Fields selected for final hypersearch report;
# NOTE: These values are used as regular expressions by RunPermutations.py's
#       report generator
# (fieldname values generated from PERM_PREDICTED_FIELD_NAME)
report = [
          '.*consumption.*',
         ]

# Permutation optimization setting: either minimize or maximize metric
# used by RunPermutations.
# NOTE: The value is used as a regular expressions by RunPermutations.py's
#       report generator
# (generated from minimize = 'prediction:rmse:field=consumption')
minimize = 'prediction:rmse:field=consumption'


#############################################################################
def dummyModelParams(perm):
  """ This function can be used for Hypersearch algorithm development. When
  present, Hypersearch doesn't actually run the CLA model in the OPF, but instead run
  a dummy model. This function returns the dummy model params that will be
  used. See the OPFDummyModelRunner class source code (in
  nupic.swarming.ModelRunner) for a description of the schema for
  the dummy model params.
  """

  errScore = 50

  #errScore += abs(perm['modelParams']['sensorParams']['encoders']\
  #                ['consumption']['maxval'] - 250)
  #errScore += abs(perm['modelParams']['sensorParams']['encoders']\
  #                ['consumption']['n'] - 53)


  # Make models that contain the __timestamp_timeOfDay encoder run a bit
  #  slower so we can test that we successfully kill running models
  waitTime = 0.01

  dummyModelParams = dict(
                metricValue = errScore,
                iterations = int(os.environ.get('NTA_TEST_numIterations', '5')),
                waitTime = waitTime,
                sysExitModelRange = os.environ.get('NTA_TEST_sysExitModelRange',
                                                   None),
                delayModelRange = os.environ.get('NTA_TEST_delayModelRange',
                                                   None),
                errModelRange = os.environ.get('NTA_TEST_errModelRange',
                                               None),
                jobFailErr = bool(os.environ.get('NTA_TEST_jobFailErr', False))
                )
  return dummyModelParams



#############################################################################
def permutationFilter(perm):
  """ This function can be used to selectively filter out specific permutation
  combinations. It is called by RunPermutations for every possible permutation
  of the variables in the permutations dict. It should return True for valid a
  combination of permutation values and False for an invalid one.

  Parameters:
  ---------------------------------------------------------
  perm: dict of one possible combination of name:value
        pairs chosen from permutations.
  """

  # An example of how to use this
  limit = int(os.environ.get('NTA_TEST_maxvalFilter', 300))
  if perm['modelParams']['sensorParams']['encoders']['consumption']['maxval'] > limit:
    return False;

  return True

