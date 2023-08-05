# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 15:05:51 2020

     ------ Time-stamp: <2020-07-07 10:38:11 cws2> ------
     
@author: Carl Schmiedekamp

2020-04-14 /CS/ adding 'mine()' to list what has been setup by handies.py
                adding atan2P(y,x) to return positive angle.
2020-04-17 /CS/ adding astropy.units as '_'
"""
'''
Handy Functions and variables/constants for use at iPython prompt
   call mine() for full list of functions and variables.
   
    cdbn( dirname, sub=[subdirectory])
      for Windows, after setmyapps.bat
      does CD to directory specified by contents of env.var. 'dirname')
    cdpy1d()
      does CD to OneDrive
    cdWD()
      does CD to workingdirectory for giant pulses
    nowMJD()
      returns mjd of current time
    mjd2date( mjd)
      returns date strings (utc) for mjd
'''

## Shortcuts etc. functions.
from math import pi, sqrt, cos, sin, tan
from math import acos, asin, atan, atan2, degrees, radians
from math import log, log10, exp
import astropy
from astropy import units as u

import math
## math.comb is in Python 3.8 
if hasattr( math, "comb" ):
    from math import comb
    from math import comb as nCr
else:
    def nCr(n,r):
        ''' calculate number of combinations of r from n items.'''
        f = math.factorial
        return f(n) // f(r) // f(n-r)
    comb = nCr    

from platform import python_version
import sys, os.path, time


def hostname():
    '''Returns 'fully qualified domain name' '''
    import socket
    return socket.getfqdn()

print( "Loading Carl's handies.py updated {}; Python {}".format( 
    time.ctime(os.path.getmtime( __file__)), python_version())) 

def call( cmd):
    import subprocess
    '''Modeled after call function in NANOGrav Sprinng 2020 workshop.
    call() just executes the command in the shell and displays output,
    while runCatch( cmd) tries to catch all errors and output and only returns
    True of False to indicate success or failure.'''
    subprocess.call( cmd, shell=True)

def mine():

    '''List the functions and variables defined in handies.py'''
    print('\n handies.py modified {}'.format(
        time.ctime(os.path.getmtime( __file__)) ))
    print(' Python {},  path to handies.py:   \n{}'.format( python_version(), __file__))
    print('Defining:\n     nowMJD(); mjd2date(), date2mjd()\n     cdbn(); cdWD(), cdpy1d(),')
    print('     osname(), hostname(), call(), select_file( timeout=65)')
    print('     rad(), deg(), sinD(), cosD(), tanD(), asinD(),\n     acosD(), atanD(), atan2D(), atan2P()')
    print("       'D' and 'P' functions work with degrees.")
    print("       'P' inverse functions return only positive angles.")
    print("Defines nCr AKA comb or imports from math if available.")
    print('     greek  ➞ a string with greek alphabet.')
    print('     pltsize( w, h) ➞ resizes plots in matplotlib, units are inches')
    print('     mine() ➞ lists what handies.py defines.')

    print('From math imports:\n     pi, sqrt, degrees, radians,\n     cos, sin, tan, atan2, asin, acos, atan, and\n' + 
      '     log, log10, exp')

    print( 'From astropy units as "u", i.e. u.cm or u.GHz')
    
##Ref: https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-precision
    prhints = ('Hint:\n' + 
          '     "%precision %g" or %.6g for better number formats.')
    print(prhints)


def cosD( ang):
    '''Return cosine of angle in degrees.'''
    import math as m
    return m.cos( m.radians( ang))

def sinD( ang):
    '''Return sine of angle in degrees.'''
    import math as m
    return m.sin( m.radians( ang))

def tanD( ang):
    '''Return tangent of angle in degrees.'''
    import math as m
    return m.tan( m.radians( ang))

def asinD( val):
    '''Return inverse sine, in degrees, of val.'''
    import math as m
    return  m.degrees( m.asin( val))

def acosD( val):
    '''Return inverse consine, in degrees, of val.'''
    import math as m
    return m.degrees( m.acos( val))


def atanD( val):
    '''Return inverse tangent, in degrees, of val.'''
    import math as m
    return m.degrees( m.atan( val))


def atan2D( y, x):
    '''Return inverse tangent, in degrees, of y/x. (-180 ... 180)'''
    import math as m
    return m.degrees( m.atan2( y, x))

def atan2P( y, x):
    '''Return inverse tangent, in degrees, of y/x. (0 .. 360)'''
    ang = atan2D( y, x)
    if ang <0:
        ang = ang + 360
    return ang

rad = radians  ## alias the conversion functions
deg = degrees

greek = ' Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω  α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω '

def cdbn( dirname, sub=None):
    '''cd to directory (or subdirectory) who's path is in Env.Var. who's name is passed as
       first argument.  2nd argument specifies a subdirectory relative to
       that named directory.'''
    import os
    """ Does cd to directory named in specified environment
        variable.
        Returns True if no error.
        If Error, returns False and prints msg.
        --
        If sub is specified, tries to cd to that subdirectory
        after the cd to the contents of env. var.
    """
    try:
        dir = os.environ[ dirname]
    except KeyError:
        print( dirname, ': not an env. var.')
        return False
    else:
        if os.access( dir, os.R_OK):
            os.chdir( dir)
            if sub==None:
                return True
            else:
                if os.access( sub, os.R_OK):
                    os.chdir( sub)
                    return True
                else:
                    print( '{}: No access!'.format( 
                            os.path.join(dir,sub), dir))
            return False

        else:
            print('[{}] --> {} : No access!'.format( dirname, dir))
            return False

def cdpy1d():
    '''cd to Pythonista dir. in OneDrive'''
    return cdbn('MYonedrivepsu', 'Pythonista')

def cdWD():
    '''cd to SinglePulse/WorkingDir.'''
    ##os.chdir( r'C:\Users\hedfp\OneDrive - The Pennsylvania State University\InProgress\ACURA-Radio-Astro-class-stuff\SinglePulse-GiantPulses\WorkingDir')
    return cdbn('MYonedrivepsu', 'InProgress\ACURA-Radio-Astro-class-stuff\SinglePulse-GiantPulses\WorkingDir' )
        
def nowMJD():
    '''Convert current time to MJD'''
    from astropy.time import Time
    return Time.now().to_value( 'mjd')

def mjd2date( mjd):
    '''Convert MJD to a civil date/time'''
    
    from astropy.time import Time
    time = Time( mjd, format='mjd')
    return time.to_datetime()

def date2mjd_( civildate):
    '''Convert specified time to MJD.
    The string in civildate must be recognized by astropy.time.Time,
    and is assumed to be UCT time.

    Value returned is float
    
    Usage:
        date2mjd( '2020-05-16T14:10') returns 58985.59027777777778'''
    
    from astropy.time import Time
    return Time( civildate).to_value( 'mjd', 'long')
    
def date2mjd( civildate):
    '''Convert specified time to MJD.
    The string in civildate must be recognized by astropy.time.Time,
    and is assumed to be UCT time.
    As a special case, if the date/time is followed by UTC offset
    then that is used to shift the date/time to UTC.
    Example: 2019-09-30 20:54:54-04:00 corresponds to 
    UTC of 2019-10-01 00:54:54

    Value returned is float
    
    Usage:
        date2mjd( '2020-05-16T14:10') returns 58985.59027777777778
        or
        date2mjd( '2020-05-16T14:10-04:00') returns 58985.756944444444446
        '''
    
    cd = civildate
    offset = 0
    ## check for special case:
    if cd[-3]==':' and ( cd[-6]=='-' or cd[-6]=='+') :
        offset = (int( cd[-5:-3]) + int( cd[-2:])/60 )/24
        if cd[-6]=='+':
            offset = -offset
        cd = cd[:-6]
    
    from astropy.time import Time
    return Time( cd).to_value( 'mjd', 'long')+offset
    


def pltsize( w, h):
    '''set plot size (matplotlib), units are inches.'''
    import matplotlib
    matplotlib.rc('figure', figsize=[w,h])

def osname():
    '''Returns name of operating system that Python is running on.'''
    import os
    return os.uname().sysname

def select_file( timeout=65):
    ''' Uses fdtest.py to browse for file and return its path.
    If the fdtest call takes longer than 'timeout' seconds,
    the attempt is cancelled and an exception raised.
    The keyword argument, timeout, sets the number of seconds before time out,
    and raising an exception.
    Note: fdtest.py needs to be in directory or on PYTHONPATH'''
    from fdtest import gui_fname
    from func_timeout import func_timeout, FunctionTimedOut
    
    try:
        filename = func_timeout( timeout, gui_fname, args=()).decode("utf-8")
    except FunctionTimedOut as e:
        outstr = 'select_file cound not complete within '
        outstr += '{} seconds and was terminated.\n'.format( timeout)
        print( outstr)
        raise e
    ## handle other exceptions if needed
    # except Exception as e:
        
    return filename


if __name__ == "__main__":
    mine()
    
    
