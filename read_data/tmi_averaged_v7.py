#	This routine reads version-7.1 RSS TMI time-averaged files 
#	The time-averaged files include:
#   3-day	(average of 3 days ending on file date),  satname_yyyymmddv7.1_d3d.gz
#   weekly	(average of 7 days ending on Saturday of file date),  satname_yyyymmddv7.1.gz
#   monthly	(average of all days in month),  satname_yyyymmv7.1.gz
#	 	where satname   = name of satellite (tmi)
#	              yyyy	= year
#		        mm	= month
#		        dd	= day of month
#
#   missing = fill value used for missing data;
#                  if None, then fill with byte codes (251-255)

#	the output values correspond to:
#	sst		sea surface temperature in deg Celsius
#	windLF		10m surface wind, low frequency, in meters/second
#	windMF		10m surface wind, medium frequency, in meters/second
#	vapor		columnar or integrated water vapor in millimeters
#	cloud		cloud liquid water in millimeters
#	rain		rain rate in millimeters/hour
#   longitude	Grid Cell Center Longitude', LON = 0.25*x_grid_location - 0.125 degrees east
#   latitude	Grid Cell Center Latitude',  LAT = 0.25*y_grid_location - 90.125
#   land		Is this land?
#   ice			Is this ice?
#   nodata		Is there no data

from read_data.bytemaps import sys
from read_data.bytemaps import Dataset
from read_data.bytemaps import Verify

from read_data.bytemaps import _get_latitude


class TMIaveraged(Dataset):
    """ Read averaged TMI bytemaps. """
    """
    Public data:
        filename = name of data file
        missing = fill value used for missing data;
                  if None, then fill with byte codes (251-255)
        dimensions = dictionary of dimensions for each coordinate
        variables = dictionary of data for each variable
    """

    def __init__(self, filename, missing=None):
        """
        Required arguments:
            filename = name of data file to be read (string)
                
        Optional arguments:
            missing = fill value for missing data,
                      default is the value used in verify file
        """       
        self.filename = filename
        self.missing = missing
        Dataset.__init__(self)

    # Dataset:

    def _attributes(self):
        return ['coordinates','long_name','units','valid_min','valid_max']

    def _coordinates(self):
        return ('variable','latitude','longitude')

    def _shape(self):
        return (6,720,1440)

    def _variables(self):
        return ['sst','w11','w37','vap','cld','rain',
                'longitude','latitude','land','ice','nodata']                

    # _default_get():
    
    def _get_index(self,var):
        return {'sst' : 0,
                'w11' : 1,
                'w37' : 2,
                'vap' : 3,
                'cld' : 4,
                'rain': 5,
                }[var]

    def _get_scale(self,var):
        return {'sst' : 0.15,
                'w11' : 0.2,
                'w37' : 0.2,
                'vap' : 0.3,
                'cld' : 0.01,
                'rain': 0.1,
                }[var]

    def _get_offset(self,var):
        return {'sst' : -3.0,
                'cld' : -0.05,
                }[var]

    # _get_ attributes:
    
    def _get_long_name(self,var):
        return {'sst' : 'Sea Surface Temperature',
                'w11' : '10m surface wind using 11 GHz channel algorithm',
                'w37' : '10m surface wind, using 37 GHz channel algorithm',
                'vap' : 'Columnar Water Vapor',
                'cld' : 'Cloud Liquid Water',
                'rain' : 'Surface Rain Rate',
                'longitude' : 'Grid Cell Center Longitude',
                'latitude' : 'Grid Cell Center Latitude',
                'land' : 'Is this land?',
                'ice' : 'Is this ice?',
                'nodata' : 'Is there no data?',
                }[var]

    def _get_units(self,var):
        return {'sst' : 'deg C',
                'w11' : 'm/s',
                'w37' : 'm/s',                
                'vap' : 'mm',
                'cld' : 'mm',
                'rain' : 'mm/hr',
                'longitude' : 'degrees east',
                'latitude' : 'degrees north',
                'land' : 'True or False',
                'ice' : 'True or False',
                'nodata' : 'True or False',
                }[var]

    def _get_valid_min(self,var):
        return {'sst' : -3.0,
                'w11' : 0.0,
                'w37' : 0.0,
                'vap' : 0.0,
                'cld' : -0.05,
                'rain' : 0.0,
                'longitude' : 0.0,
                'latitude' : -90.0,
                'land' : False,
                'ice' : False,
                'nodata' : False,
                }[var]

    def _get_valid_max(self,var):
        return {'sst' : 34.5,
                'w11' : 50.0,
                'w37' : 50.0,
                'vap' : 75.0,
                'cld' : 2.45,
                'rain' : 25.0,
                'longitude' : 360.0,
                'latitude' : 90.0,
                'land' : True,
                'ice' : True,
                'nodata' : True,
                }[var]

    # _get_ variables:

    def _get_latitude(self,var,bmap):
        return _get_latitude(var,bmap,nlat=720,lat0=-89.875)
    

class ThreedayVerify(Verify):
    """ Contains info for verification. """
    
    def __init__(self,dataset):
        self.filename = 'verify_TMI_v7.txt'
        self.ilon1 = 328
        self.ilon2 = 330
        self.ilat1 = 392
        self.ilat2 = 395       
        self.variables = ['sst','w11','w37','vap','cld','rain']
        self.startline = {'sst' : 110,
                          'w11' : 116,
                          'w37' : 122,
                          'vap' : 128,
                          'cld' : 134,
                          'rain': 140 }
        Verify.__init__(self,dataset)
        

class WeeklyVerify(Verify):
    """ Contains info for verification. """
    
    def __init__(self,dataset):
        self.filename = 'verify_TMI_v4.txt'
        self.ilon1 = 328
        self.ilon2 = 330
        self.ilat1 = 392
        self.ilat2 = 395       
        self.variables = ['sst','w11','w37','vap','cld','rain']
        self.startline = {'sst' : 151,
                          'w11' : 157,
                          'w37' : 163,
                          'vap' : 169,
                          'cld' : 175,
                          'rain': 181 }
        Verify.__init__(self,dataset)
        

class MonthlyVerify(Verify):
    """ Contains info for verification. """
    
    def __init__(self,dataset):
        self.filename = 'verify_TMI_v4.txt'
        self.ilon1 = 328
        self.ilon2 = 330
        self.ilat1 = 392
        self.ilat2 = 395       
        self.variables = ['sst','w11','w37','vap','cld','rain']
        self.startline = {'sst' : 193,
                          'w11' : 199,
                          'w37' : 205,
                          'vap' : 211,
                          'cld' : 217,
                          'rain': 223 }
        Verify.__init__(self,dataset)
        

if __name__ == '__main__':
    """ Automated testing. """    

    # read 3-day averaged:
    tmi = TMIaveraged('TMI_19990414v7.1_d3d.gz')
    if not tmi.variables: sys.exit('problem reading file')

    # verify 3-day:
    verify = ThreedayVerify(tmi)
    if verify.success: print ('successful verification for 3-day')
    else: sys.exit('verification failed for 3-day')
    print()

    # read weekly averaged:
    tmi = TMIaveraged('TMI_19990417v7.1.gz')
    if not tmi.variables: sys.exit('problem reading file')

    # verify weekly:
    verify = WeeklyVerify(tmi)
    if verify.success: print ('successful verification for weekly')
    else: sys.exit('verification failed for weekly')     
    print()
    
    # read monthly averaged:
    tmi = TMIaveraged('TMI_199904v7.1.gz')
    if not tmi.variables: sys.exit('problem reading file')
    
    # verify:
    verify = MonthlyVerify(tmi)
    if verify.success: print ('successful verification for monthly')
    else: sys.exit('verification failed for monthly')      
    print()
    
    print ('all tests completed successfully')