import osgeo

ref1 = osgeo.osr.SpatialReference()
ref2 = osgeo.osr.SpatialReference()

ref1.ImportFromEPSG( 2249 )
ref2.SetWellKnownGeogCS( "WGS84" )
trans = osgeo.osr.CoordinateTransformation( ref1, ref2 )
#example point conversion
(x,y,z) = trans.TransformPoint( 773488.33782, 2953009.85636 )

