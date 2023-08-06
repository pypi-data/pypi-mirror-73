import pytest
import theseus_growth
import numpy as np
import random

def test_retention_profile():
	th = theseus_growth.theseus()

	x_data = [ 1, 14, 60 ]
	y_data = [ 40, 22, 15 ]

	new_x = []
	for i, x in enumerate( x_data ):
	    this_x = x
	    for z in np.arange( 1, 1000 ):
	        this_y = float( y_data[ i ] * ( 1 + ( random.randint( -20, 20 ) / 100 ) ) )
	        y_data.append( this_y )
	        new_x.append( this_x )

	x_data.extend( new_x )

	prof = th.create_profile( days = x_data, retention_values = y_data, profile_max = 180 )

	assert( isinstance( prof, dict ) )

	assert( 'retention_projection' in prof )

	assert( len( prof[ 'retention_projection' ][ 0 ] ) == 180 )