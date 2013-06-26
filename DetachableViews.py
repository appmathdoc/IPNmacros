## Firefox, Chrome,  

from IPython.display import HTML

class DetachableView:
    
    def __init__(my, PostType = "OneWay" ): #PostType is for later
        my.framecntr = 0 
        #HTML( """  """)
                 
    def HTMLView( my, HTMLview, toggle = True, width=None, height=None):
        my.framecntr += 1
        HtmlString  = ""
        if( toggle):
            HtmlString += """

                    <script type="text/javascript"> 
                
                function LaunchView%s( ) {
                    var iFrame = document.getElementById('IframeView%s');
                    var iFcont = "%s"
                    var DetachedName = "Detached%s";
                    if( iFrame.style.display === "block") {
                        var win = window.open('about:blank', DetachedName ,'height=500,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');
                        
                        var win_doc = win.document;
                        win_doc.open();
                        win_doc.write("<!DOCTYPE html><htm" + "l><head><body>"+ iFcont +"</body></ht" + "ml>");
                        win_doc.close();
                        iFrame.style.display = "none"
                    } else { 
                        iFrame.style.display = "block"
                    };
                }
                
            </script>  
      
                <input type="button" value="toggle view" onclick="LaunchView%s()"> <br>
        
            """ % ( my.framecntr, my.framecntr, HTMLview, my.framecntr,my.framecntr ) 
        
        if( width == None):
            width = "95%"
        elif( type(width) != type( "500px" )):
            width = "%spx" % width
            
        if( height == None):
            height = "24em"
        elif( type(height) != type( "500px" )):
            height = "%spx" % height
            
        HtmlString += """
            <iframe id = 'IframeView%s' src = "javascript: '%s' "  style = 'width:%s;height:%s;display:block;' > 
                Your browser does not support iframes </iframe> 
            """ % ( my.framecntr, HTMLview, width, height)
        return HTML(HtmlString)
        
FramesAndArrays = DetachableView( )

try:
    cround
except:
    def cround(z,n=5): return complex(round(z.real,n), round(z.imag,n)) 


def View( tmp ):
    "array or dataframe ->  Detachable View in Notebook"
    
    try:
        tmp.shape
    except:
        print( "View cannot create a display for an object %s " % type(tmp) )
        return 
    
    nme = "Name(s): "
    for nm in get_ipython().magic(u'who_ls'): 
        if( eval(nm) is tmp ):
            nme += nm + str(" ")

    IsDF = False
    try:
        tmp.index
        IsDF = True
    except:
        pass 
    
    if( len(tmp.shape) == 1 ):
        if( tmp.dtype.names ):
            nrows = len(tmp)
            ncols = len( tmp.dtype.names ) 
        else:
            ncols = len(tmp)
            nrows = 1
    else:
        nrows, ncols = tmp.shape
        
    hght = "%sem" % max(  8, min( 2*nrows+8, 40 ))
    wdth = "%sem" % max( 40, min( 4*ncols+4, 80 ))
    
    if( IsDF ):
        typ = "DataFrame: Entries via  Name[col][row] "
        shp = ( len( tmp.index), len(tmp.columns) )
        dtp = ""
        for tp in tmp.dtypes:
            dtp += "%s, " % tp
    elif( tmp.dtype.names ):
        typ = "Structured Array: Entries via  Name[col][row] "
        shp = ( tmp.shape[0], len(tmp.dtype.names) )
        dtp = ""
        for tp in tmp.dtype.descr:
            dtp += "%s, " % tp[1]
        dtp = dtp.replace("<","&amp;lt;")
        dtp = dtp.replace(">","&amp;gt;")
    elif( nrows == 1 ):
        typ = "Numpy 1D Array: Entries via  Name[index] "
        shp = tmp.shape
        dtp = tmp.dtype
    else:
        typ = "Numpy Array: Entries via  Name[row, col] "
        shp = tmp.shape
        dtp = tmp.dtype
    
    HtmlString  = "<style>"
    HtmlString += "  table   { width:95%;border:1px solid LightGray;border-spacing:0;border-collapse: collapse;margin-left: 0; }"
    HtmlString += "  th      { border:1px solid LightGray;padding:2px 4px; } "
    HtmlString += "  td      { border:1px solid LightGray;padding:2px 4px;text-align:center; } "
    HtmlString += "  caption { text-align:left; } "
    HtmlString += "  bcap   { font-size:larger; } "
    HtmlString += "</style>"
    
    HtmlString += "<div> <b id = &quot; #bcap &quot;> %s  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | </b>" % nme
    HtmlString += "&nbsp; &nbsp; &nbsp; &nbsp; %s  <sub> &nbsp; </sub> <br>  <table border=1 ><caption> " % typ
    HtmlString += " Size: %s  &nbsp;&nbsp;&nbsp;&nbsp Type(s): %s   </caption>" % ( shp, dtp ) 
    
    if( IsDF ):
        HtmlString += "<tr> <th> &nbsp; </th>"
        for nme in tmp.columns:
            HtmlString += '<th> %s </th> ' % nme 
        HtmlString += "</tr>" 
        for idx in tmp.index:
            HtmlString += '<tr><td><b> %s </b></td> ' % idx
            for col in tmp.columns:
                entry = tmp[col][idx]
                if(type(entry) in [ float, numpy.float16, numpy.float32, numpy.float64 ]  ): 
                    entry = round(entry,5)
                elif(type(entry)==complex):
                    entry = cround(entry,5)
                HtmlString += '<td> %s </td>  ' % entry
            HtmlString += "</tr>"
    elif( tmp.dtype.names ):
        HtmlString += "<tr> "
        for nme in tmp.dtype.names:
            HtmlString += '<th> %s </th> ' % nme 
        HtmlString += "</tr>  "
        for row in range(ncols):
            HtmlString += "<tr>"
            for nme in tmp.dtype.names:
                entry = tmp[nme][row]
                if( type(entry)  in [ float, numpy.float16, numpy.float32, numpy.float64 ] ):
                    entry = round(entry,5)
                elif(type(entry)==complex):
                    entry = cround(entry,5)
                HtmlString += '<td> %s </td>  ' % entry
            HtmlString += "</tr>  "
    else:
        for row in range(nrows):
            HtmlString += "<tr>"
            for col in range(ncols):
                if(len(tmp.shape) > 1 ):
                    entry = tmp[row,col]
                    if(type(entry)  in [ float, numpy.float16, numpy.float32, numpy.float64 ] ):
                        entry = round(entry,5)
                    elif(type(entry)==complex):
                        entry = cround(entry,5)
                    HtmlString += '<td> %s </td> ' % entry
                else:
                    entry = tmp[col]
                    if( type(entry) in [ float, numpy.float16, numpy.float32, numpy.float64  ] ):
                        entry = round(entry,5)
                    elif(type(entry)==complex):
                        entry = cround(entry,5)
                    HtmlString += '<td> %s </td> ' % entry
            HtmlString += "</tr>  "
    
    HtmlString += "  </table></div> " 
    return  FramesAndArrays.HTMLView(HtmlString, width = wdth, height=hght)
            

