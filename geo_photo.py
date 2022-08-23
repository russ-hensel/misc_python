# -*- coding: utf-8 -*-

#    Some code for:
#
#          (4) GPS Location From Image Metadata in Python - YouTube
#         https://www.youtube.com/watch?v=BpE9mk1FeJ4
#
#    Complete with minimal testing
#        some debug prints still active



import geopy
import gmplot
from   gmplot import gmplot
from   geopy.geocoders import Nominatim
import webbrowser


import PIL.Image
import PIL.ExifTags


# ----------------------------------------
def ex_photo_gmplot():
    """
    code from youtube
    """
    # constants to make code have fewer magic values
    filename        = "window.png"
    zoom_level      = 12
    filename_html   = "location.html"

    # -----
    img     = PIL.Image.open(  filename )
    exif    = { PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS }

    gps_info     = exif['GPSInfo']
    north        = gps_info[2]
    east         = gps_info[4]
    print( gps_info )
    print( north, east )

    lat      =  ((( north[0] * 60 + north[1] ) * 60 + north[2]) / (60 * 60.) )
    long     =  ((( east[0] * 60 + east[1] ) * 60 + east[2]) / (60 * 60.) )
    long     = -long    # else I got to afganastan
    print( lat, long )

    # an equivalent calc  ?
    # lat2    = north[0] + north[1]/60 + north[2]/3600.
    # long2   = east[0]+east[1]/60+east[2]/3600.
    # print( lat2, long2 )

    gmap       = gmplot.GoogleMapPlotter( lat, long, zoom_level )
    gmap.marker( lat, long, "cornflowerblue" )
    gmap.draw( filename_html )   # a file name for the html
    webbrowser.open( filename_html, new = 2 )        # auto open file above in new tab

    geoloc     = Nominatim( user_agent = "GetLoc")
    locname    = geoloc.reverse( f"{lat}, {long}")
    print( locname.address )


#ex_photo_gmplot()    # comment out this line to stop example from running


# ----------------------------------------
class GeoPhoto( ):
    """
    above code as an object, a bit overdone
    """

    # ----------------------------------------
    def __init__(self, filename ):
        self.filename               = None
        self.set_filename( filename )
        self.filename_html_default  = "photo_loc.html"
        self.zoom_level_default     = 12

    # ----------------------------------------
    def set_filename( self, filename ):
        """
        set the file name to be input
        """
        self.get_long_lat( filename )
        self.filename_html          = None
        self.location               = None
        self.zoom_level             = None

        return

    # ----------------------------------------
    def get_long_lat( self, filename   ):
        """
        compute the longitude and lat

        Return mutates object, sets file name if changed, computes long, lat
        """
        # -----
        if self.filename != filename:

            self.filename   = filename
            img             = PIL.Image.open( self.filename )
            exif            = { PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS }

            gps_info        = exif['GPSInfo']
            north           = gps_info[2]
            east            = gps_info[4]

            print( gps_info )
            print( north, east )

            self.lat         =  ((( north[0] * 60 + north[1] ) * 60 + north[2]) / (60 * 60.) )
            self.long        =  ((( east[0]  * 60 + east[1] )  * 60 + east[2])  / (60 * 60.) )
            self.long        = -self.long    # else I got to afganastan

            print( self.lat, self.long )

    # ----------------------------------------
    def html_location( self, filename_html = None, zoom_level = None, open_browser  = False ):
        """
        create an html location file and optionally open it

        Returns: a file name
        """
        if zoom_level is None:
            zoom_level = self.zoom_level_default

        if filename_html is None:
            filename_html  = self.filename_html_default

        #self.get_long_lat( self.filename )  # not required

        if self.zoom_level  != zoom_level or self.filename_html != filename_html:
            self.zoom_level      = zoom_level
            self.filename_html   = filename_html

            gmap       = gmplot.GoogleMapPlotter( self.lat, self.long, self.zoom_level )
            gmap.marker( self.lat, self.long, "cornflowerblue" )
            gmap.draw( filename_html )   # a file name for the html map

        if open_browser:
             webbrowser.open( self.filename_html, new = 2 )        # open file in new browser tab

        return self.filename_html

    # ----------------------------------------
    def get_address( self,   ):
        """
        Returns: a physical address
        """
        geoloc     = Nominatim( user_agent = "GetLoc")
        locname    = geoloc.reverse( f"{self.lat}, {self.long}")
        address     = locname.address
        print( address )   # debug/test
        return address

    # ----------------------------------------
    def to_debug_string( self,   ):
        """
        create and retrun debug string

        return: debug string
        """
        line_begin  ="\n"
        a_str = ""
        a_str = f"{a_str}\n>>>>>>>>>>* debug values (some) *<<<<<<<<<<<<"
        a_str = f"{a_str}{line_begin}   self.filename            {self.filename}"
        a_str = f"{a_str}{line_begin}   self.filename_html       {self.filename_html}"
        a_str = f"{a_str}{line_begin}   self.location            {self.location}"
        a_str = f"{a_str}{line_begin}   self.zoom_level          {self.zoom_level}"
        #-------+-----------------------+------------------------+------------------

        return a_str

# ----------------------------------------
def ex_test_GePhoto():
    """
    test GeoPhoto object

    """
    filename        = "window.png"
    geo_photo      = GeoPhoto( filename )

    print( geo_photo.to_debug_string() )

    print( geo_photo.get_address( ) )
    # a few test calls
    geo_photo.html_location( open_browser  = True )

    geo_photo.html_location( zoom_level= 12, open_browser  = True )

    geo_photo.html_location( filename_html  = "photo_loc_b.html", zoom_level= 5, open_browser  = True )

    print( geo_photo.get_address( ) )

ex_test_GePhoto()



