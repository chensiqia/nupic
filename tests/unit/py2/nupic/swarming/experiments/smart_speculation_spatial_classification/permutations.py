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
predictedField = 'attendance'

permutations = {
  
  'modelParams': {
    'sensorParams': {
      'encoders': {
        'A': PermuteEncoder(fieldName='daynight', encoderClass='SDRCategoryEncoder', w=7, n=100),
        'B': PermuteEncoder(fieldName='daynight', encoderClass='SDRCategoryEncoder', w=7, n=100),
        'C': PermuteEncoder(fieldName='precip', encoderClass='SDRCategoryEncoder', w=7, n=100),
        '_classifierInput': dict(fieldNname='attendance', 
                                 classifierOnly=True,
                                 type='AdaptiveScalarEncoder', 
                                 maxval=36067, 
                                 n=PermuteInt(13, 500, 25), 
                                 clipInput=True, w=7, minval=0),
      },
    },
  }
}


# Fields selected for final hypersearch report;
# NOTE: These values are used as regular expressions by RunPermutations.py's
#       report generator
# (fieldname values generated from PERM_PREDICTED_FIELD_NAME)
report = [
          '.*attendance.*',
         ]

# Permutation optimization setting: either minimize or maximize metric
# used by RunPermutations.
# NOTE: The value is used as a regular expressions by RunPermutations.py's
#       report generator
# (generated from minimize = 'nonprediction:aae:window=1000:field=attendance')
minimize = "multiStepBestPredictions:multiStep:errorMetric='aae':steps=\[0\]:window=1000:field=attendance"


#############################################################################
def dummyModelParams(perm):
  """ This function can be used for Hypersearch algorithm development. When
  present, we don't actually run the CLA model in the OPF, but instead run
  a dummy model. This function returns the dummy model params that will be
  used. See the OPFDummyModelRunner class source code (in
  nupic.swarming.ModelRunner) for a description of the schema for
  the dummy model params.
  """

  errScore = 500

  if not perm['modelParams']['sensorParams']['encoders']['A'] is None:
    errScore -= 40
  if not perm['modelParams']['sensorParams']['encoders']['B'] is None:
    errScore -= 30
  if not perm['modelParams']['sensorParams']['encoders']['C'] is None:
    errScore -= 20
  delay = 0
  
  # Make the best model in sprint 0 run slower so that we create more
  #  speculative models
  encoderCount = 0
  encoders = perm['modelParams']['sensorParams']['encoders']
  for field,encoder in encoders.items():
   	if encoder is not None:
   		encoderCount += 1

  # NOTE: The _classifierInput is always present. It seems that speculation
  #  favors fields that are not done yet, so make the worse fields take
  #  longer so that the speculative particles choose them in the second
  #  sprint. 
  if encoderCount == 2: 
    delay = 0.1
    
  # Make speculative swarms that should be killed take longer...
  elif encoderCount == 3 \
        and perm['modelParams']['sensorParams']['encoders']["A"] is None:
    delay = 0.2

  # Make the best possible combination take the longest so that we have
  #  an opportunity to kill other swarms before we finish 
  elif encoderCount == 3:
    delay = 0.3

  
  dummyModelParams = dict(
                metricValue = errScore,
                metricFunctions = None,
                delay=delay,
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
  #if perm['__consumption_encoder']['maxval'] > 300:
  #  return False;
  #
  return True
