import osgeo
import osgeo.osr
import urllib2
import json
import requests
import cPickle as pickle

#geo projection conversion
ref1 = osgeo.osr.SpatialReference()
ref2 = osgeo.osr.SpatialReference()
ref1.ImportFromEPSG( 2249 )
ref2.SetWellKnownGeogCS( "WGS84" )
global trans
trans = osgeo.osr.CoordinateTransformation( ref1, ref2 )
    

#coordinate point conversion
def reprojectCoord( x, y ):
    global trans
    (lon,lat,z) = trans.TransformPoint( x, y )
    return lat, lon


#get crime couch data (your fork):  
couchurl = "http://datacouch.com/api/couch/dc6aca92f2c00f747e6961abf4e7ecf537"     
response = urllib2.urlopen( str( "%s/_all_docs" % couchurl ) )
jsonstr  = response.read()
jarr     = json.loads( jsonstr )

#update the records
updateurl = "http://mytwitterhandle:mydatatoken@data.ic.ht/dc6aca92f2c00f747e6961abf4e7ecf537"
res = []
for i in jarr['rows']:
    response = urllib2.urlopen( str( "%s/%s" % ( couchurl, i['id']) ) )
    jsonstr = response.read()
    r = json.loads( jsonstr ) 
    k = r.keys()
    #you may have to replace the names of the coordinate fields in the data set
    if ' X' in k and ' Y' in k and len( r[' X'] ) > 0 and len( r[' Y'] ) > 0:
        lat, lon = reprojectCoord( float(r[' X']), float(r[' Y']) )
        r['geometry'] = {'type': 'Point', 'coordinates' : [lon, lat]}
        res.append( r )
        t = requests.post(updateurl, data=json.dumps(r), headers={"Content-Type" : "application/json"} )

#make a local copy    
pickle.dump( res, open( "boston_crime_latlon.pickle", "wb" ) )



