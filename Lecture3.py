## Doesn't yet work in Firefox for every possible argument (waiting for srcdoc -- Probably Oct 2013 in Firefox 25) 

## Tested on Chrome 28, Firefox 22, and Safari 5.1.7 on Windows 7 Home, Professional

from __future__ import division
from IPython.display import HTML
from pandas import DataFrame


class DetachableView:
    "ONLY DOUBLE QUOTES PERMITTED IN HTMLview -- use &apos; for single quotes"
    def __init__(my, PostType = "OneWay" ): #PostType is for later
        my.framecntr = 0 
        lttrs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
        
        my.frameSig = ""
        for i in range(20):
            my.frameSig += lttrs[ randint(len(lttrs)) ]

    def URLView( my, URL, width=None, height=None, toggle = True,  message = None):
        """ URLView(URL) -> Detachable View of the page at URL
        
            if message != None, then postMessage API used to send message to Views"""
        
        # Each LaunchView is unique -- probably could have one LaunchView + arguments, 
        # but the data to be displayed (i.e., the would-be argument) is the lion's 
        # share of the definition
        my.framecntr += 1
        fcntr = my.frameSig + str(my.framecntr)
        
        HtmlString = ""
        # toggle = False suppresses the popup window
        if( toggle):
            HtmlString += """

                <script type='text/javascript'>
                    var win;
                    var messageHandler%s ;
                    var MessageRepeater%s ;
                    function LaunchView%s( ) {
                        var iFrame = document.getElementById('IframeView%s');
                        if( iFrame.style.display == 'block') {
                            win = window.open( '%s', 'Detached%s' ,'height=500,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');
                    """ % (fcntr, fcntr, fcntr, fcntr, URL, fcntr ) 
            if( message != None):
                HtmlString += """
                            messageHandler%s = function(event){
                                if( event.data == 'ready' ) { 
                                    win.postMessage('%s', '*' ) ;
                                }
                                if( event.data == 'done'  ) {
                                    window.removeEventListener('message',arguments.callee,false)
                                }
                            }
                            window.addEventListener('message',messageHandler%s, false);
                  """ %(fcntr, message, fcntr )

            HtmlString += """
                        iFrame.style.display = 'none'
                    } else { 
                        iFrame.style.display = 'block'
                    };

                }
                
                </script>  
      
                <input type='button' value='toggle view' onclick='LaunchView%s()'> <br>
                
            """ % fcntr 
        
        # Set width, height
        if( width == None):
            width = "95%"
        elif( type(width) != type( "500px" )):
            width = "%spx" % width
            
        if( height == None):
            height = "24em"
        elif( type(height) != type( "500px" )):
            height = "%spx" % height
           
        # Create an Iframe (BTW, HTML() is fantastic! 
        HtmlString += """
            <iframe id = 'IframeView%s' src = '%s' style = 'width:%s;height:%s;display:block;' > 
                Your browser does not support iframes </iframe> 
            """ % ( fcntr, URL, width, height)

        if( message != None):
            HtmlString += """
                <script type="text/javascript">

                    var MessageHandler%s = function(event){
                        if( event.data == 'ready' ) {
                            document.getElementById('IframeView%s').contentWindow.postMessage('%s', '*' ) ;
                        }
                        if( event.data == 'done'  ) {
                            window.removeEventListener('message',arguments.callee,false)
                        }
                    }
            
                    window.addEventListener('message',MessageHandler%s, false);
            
                </script> """ %(fcntr, fcntr, message, fcntr)
        return HTML(HtmlString)
        

    def HTMLView( my, HTMLCode, width=None, height=None, toggle = True):
        """        HTMLCode  -> Detachable View of the Code
        
        ONLY DOUBLE QUOTES PERMITTED IN HTMLview -- use &apos; for single quotes"""
        
        # Each LaunchView is unique -- probably could have one LaunchView + arguments, 
        # but the data to be displayed (i.e., the would-be argument) is the lion's 
        # share of the definition
        my.framecntr += 1
        fcntr = my.frameSig + str(my.framecntr)
        
        #Javascript is weird
        HTMLJS = HTMLCode.replace('</script>', '<\/script>' )
        HTMLlist = HTMLJS.split('\n')
        
        #Split into lines for the win_doc.writeln commands
        HTMLtext = "' '"
        for line in HTMLlist:
            HTMLtext += ", '%s' " % line
 
        HtmlString  = ""
        
        # toggle = False suppresses the popup window
        if( toggle):
            HtmlString += """

           <script type='text/javascript'> 
                
                function LaunchView%s( ) {
                    var iFrame = document.getElementById('IframeView%s');
                    var iStringArray = [ %s ];
                    var DetachedName = 'Detached%s';
                    if( iFrame.style.display == 'block') {
                        var win = window.open('about:blank', DetachedName ,'height=500,width=800,left=100,top=100,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no, status=yes');
                        
                        var win_doc = win.document;
                        win_doc.open();
                        win_doc.writeln('<!DOCTYPE html><htm' + 'l><head><body>');
                        for (var i = 0; i < iStringArray.length; i++) {
                            win_doc.writeln( iStringArray[i] );
                        };
                        win_doc.writeln('</body></ht' + 'ml>');
                        win_doc.close();
                        iFrame.style.display = 'none'
                    } else { 
                        iFrame.style.display = 'block'
                    };
                }
                
            </script>  
      
                <input type='button' value='toggle view' onclick='LaunchView%s()'> <br>
                
            """ % ( fcntr, fcntr, HTMLtext, fcntr, fcntr ) 
        
        # Set width, height
        if( width == None):
            width = "95%"
        elif( type(width) != type( "500px" )):
            width = "%spx" % width
            
        if( height == None):
            height = "24em"
        elif( type(height) != type( "500px" )):
            height = "%spx" % height
           
        HTMLJS = HTMLJS.replace('"','&quot;' )
        
        # Create an Iframe (BTW, HTML() is fantastic! 
        HtmlString += """
            <iframe id = 'IframeView%s' srcdoc = '%s'  src = "javascript: '%s' " style = 'width:%s;height:%s;display:block;' > 
                Your browser does not support iframes </iframe> 
            """ % ( fcntr, HTMLCode, HTMLJS, width, height)
        return HTML(HtmlString)
        

## View -- for tables, etc. 

FramesAndArrays = DetachableView( )

Precision = 5
ComplexUnitString = "j"

try:
    cround
except:
    def cround(z,n=5): return complex(round(z.real,n), round(z.imag,n)) 


def FormatForView( entry ): 
    "entry -> nice representation for this object"
    
    try:
        if(entry.dtype.kind in typecodes['AllFloat'] ):
            entry = round(entry,Precision)
        elif( entry.imag != 0):
            if( entry.real == 0):
                entry = " %s %s " % (round( entry.imag,Precision), ComplexUnitString )
            else:
                entry = cround(entry,Precision)
                entry = " %s + %s %s" % (entry.real, entry.imag, ComplexUnitString)
        elif( entry.dtype.kind in typecodes['Complex']+'c' ):
            entry = round(entry.real,Precision)
        return entry
    except:
        try:
            if( entry.imag != 0):
                if( entry.real == 0):
                    entry = " %s %s " % (round( entry.imag,Precision), ComplexUnitString )
                else:
                    entry = cround(entry,Precision)
                    entry = " %s + %s %s" % (entry.real, entry.imag, ComplexUnitString)
            return entry
        except:
            return entry


def View( DataFrameOrArray ):
    """array or dataframe ->  Detachable View in Notebook
    
    If DataFrameOrArray is either a Pandas Dataframe or a Numpy array 
    (anything which has a .shape), then View creates a custom view with
    relevant information and places it in a detachable view.  Otherwise, 
    View returns a detachable view of the standard representation. 
    
    Clicking on the [toggle view] button detaches the View and places
    it in a popup.  Clicking again restores the original inline view. 
    
    NOTE:  DESIGNED TO WORK WITH PYLAB!
    
    Examples: 
    
    In [ ]: A = array( [ [1,2],[3,4] ] )
            View(A)
    
    Out[ ]: [toggle view]
            Formatted table with scrollbars if necessary
    
    
    
    In [ ]: from pandas import DataFrame
            B = DataFrame( A , index = [1,2], columns = ["A","B"] )
            View(B)   
            
    Out[ ]: [toggle view]
            Formatted table with scrollbars if necessary
            and with Column/Row headings


    In [ ]: C = randn( 50, 50) # Gaussian random sampled 50x50 array
            View(C)
            
    Out[ ]: [toggle view]
            Scrolled View of Large Matrix
    
    """
    
    # Is this a data frame (based on existence of column/index lists 
    IsDF = False
    try: 
        DataFrameOrArray[DataFrameOrArray.columns[0]][DataFrameOrArray.index[0]]
        len( DataFrameOrArray.columns )
        len( DataFrameOrArray.index )
        IsDF = True
    except:
        pass 

    # Standard Rep if not a DataFrame or an Array
    try:
        DataFrameOrArray.shape
        if( not IsDF ):
            DataFrameOrArray.dtype.names
    except:
        return FramesAndArrays.HTMLView(str(DataFrameOrArray) )
    
    # Find all names that instance is bound to
    nme = "Name(s): "
    for nm in get_ipython().magic(u'who_ls'): 
        if( eval(nm) is DataFrameOrArray ):
            nme += nm + str(", ")
    nme = nme[0:-2]

    
    # Establish values for nrows and ncols
    if( len(DataFrameOrArray.shape) == 1 ):
        if( DataFrameOrArray.dtype.names ):
            nrows = len(DataFrameOrArray)
            ncols = len( DataFrameOrArray.dtype.names ) 
        else:
            ncols = len(DataFrameOrArray)
            nrows = 1
    else:
        nrows, ncols = DataFrameOrArray.shape
        
    # Not too small, but after height = 40em, wdth = 80 em, scrollbars
    hght = "%sem" % max(  8, min( 2*nrows+8, 40 ))
    wdth = "%sem" % max( 40, min( 4*ncols+4, 80 ))
    
    # Create header info for the 3 types -- array, Structured Array, DataFrame
    if( IsDF ):
        typ = "DataFrame: Entries via  Name[col][row] "
        shp = ( len( DataFrameOrArray.index), len(DataFrameOrArray.columns) )
        dtp = ""
        for tp in DataFrameOrArray.dtypes:
            dtp += "%s, " % tp
    elif( DataFrameOrArray.dtype.names ):
        typ = "Structured Array: Entries via  Name[col][row] "
        shp = ( DataFrameOrArray.shape[0], len(DataFrameOrArray.dtype.names) )
        dtp = ""
        for tp in DataFrameOrArray.dtype.descr:
            dtp += "%s, " % tp[1]
        dtp = dtp.replace("<","&amp;lt;")
        dtp = dtp.replace(">","&amp;gt;")
    elif( nrows == 1 ):
        typ = "Numpy 1D Array: Entries via  Name[index] "
        shp = DataFrameOrArray.shape
        dtp = DataFrameOrArray.dtype
    else:
        typ = "Numpy Array: Entries via  Name[row, col] "
        shp = DataFrameOrArray.shape
        dtp = DataFrameOrArray.dtype
    
    # Style and Header Info
    HtmlString   = """
    <style>
        table   { width:95%;border:1px solid LightGray;border-spacing:0;border-collapse: collapse; }
        th      { border:1px solid LightGray;padding:2px 4px; white-space:nowrap; } 
        td      { border:1px solid LightGray;padding:2px 4px;text-align:center;white-space:nowrap; } 
        caption { text-align:left; } 
        #bcap   { font-size:larger; } 
    </style>
    """
    
    HtmlString  += """
    <div> <b id =  "bcap" > %s  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | </b>
            &nbsp; &nbsp; &nbsp; &nbsp; %s  <sub> &nbsp; </sub> <br>  
        <table border=1 >
            <caption> shape: %s  &nbsp;&nbsp;&nbsp;&nbsp; Type(s): %s   </caption>
    """  % ( nme, typ, shp, dtp ) 
    
    # Create HTML5 table of given structure -- lots of details, but mainly iterating over rows and
    # columns to insert <tr>, <th>, and <td> tags as appropriate
    if( IsDF ):
        HtmlString += "<tr> <th> &nbsp; </th>"
        for nme in DataFrameOrArray.columns:
            HtmlString += '<th> %s </th> ' % nme 
        HtmlString += "</tr>" 
        for idx in DataFrameOrArray.index:
            HtmlString += '<tr><td><b> %s </b></td> ' % idx
            for col in DataFrameOrArray.columns:
                HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[col][idx]) 
            HtmlString += "</tr>"
    elif( DataFrameOrArray.dtype.names ):
        HtmlString += "<tr> "
        for nme in DataFrameOrArray.dtype.names:
            HtmlString += '<th> %s </th> ' % nme 
        HtmlString += "</tr>  "
        for row in range(nrows):
            HtmlString += "<tr>"
            for nme in DataFrameOrArray.dtype.names:
                HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[nme][row]) 
            HtmlString += "</tr>  "
    else:
        for row in range(nrows):
            HtmlString += "<tr>"
            for col in range(ncols):
                if(len(DataFrameOrArray.shape) > 1 ):
                    HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[row,col])
                else:
                    HtmlString += '<td> %s </td> ' %  FormatForView(DataFrameOrArray[col])
            HtmlString += "</tr>  "
    
    HtmlString += "  </table></div> " 
    return  FramesAndArrays.HTMLView(HtmlString, width = wdth, height=hght)
    
## The APM random Generator
try:
    prod
    array
except:
    from numpy import prod, array

class LcgRand:
    def __init__(my, seed):
        my.seed = seed
        my.state = seed
        
    def lcg(my):
        my.state = 16807*my.state % 2147483647
        return my.state
    
    def rand(my):
        return my.lcg() / 2147483647.0
    
    def _randint( my, low, high):
        return ( my.lcg() % (high - low) )  + low
    
    def randint(my,low, high = None, size = None ):
        if( high == None ): 
            high = low
            low = 0
        if( size == None and type(high) == tuple):
            size = high
            high = low
            low = 0        
        if( size == None ):
            return my._randint(low, high)
        else:
            if( type(size) != tuple ):
                size = ( size, )
            tmp = array( [ my._randint(low, high) for i in range( prod( size) ) ] )   
            return tmp.reshape( size )
            
            
    def _choose( my, low, high, number):
        if( number > high-low ):
            raise "Number of choices %s exceeds difference between %s and %s" % ( number, high, low )
        result = []
        
        for i in xrange(number):
            tmp = my.randint(low,high)
            for j in xrange(1000*number):
                if( not ( tmp in result ) ):
                    result.append(tmp)
                    break
                tmp = my.randint(low,high)
            else:
                raise Exception("Failed to generate choose.  Please execute again")
            
        return array(result)
            
    def choose( my, low, high = None, size = None ):
        if( high == None ): 
            high = low
            low = 0
        if( size == None and type(high) == tuple):
            size = high
            high = low
            low = 0        
        if( size == None ):
            return my._choose(low, high, 1)
        else:
            if( type(size) != tuple ):
                size = ( size, )
            tmp = my._choose(low, high, prod( size) )   
            return tmp.reshape( size )

    def sample(my, seq, number, with_replacement = True):
        "sample(seq, number) -> number of samples from seq"
        if( with_replacement ):
            return array([ seq[j] for j in my.randint(0,len(seq), number ) ] )
        else:
            if( len(seq) < number ):
                raise Exception( "number must be no greater than the length of %s" % seq )
            inds = my.choose(0,len(seq), number)
            tmp = array(seq)
            return tmp[inds]

 


HouseholdNames = [  "SMITH","JOHNSON","WILLIAMS","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE","TAYLOR","ANDERSON","THOMAS","JACKSON","WHITE",
                    "HARRIS","MARTIN","THOMPSON","GARCIA","MARTINEZ","ROBINSON","CLARK","RODRIGUEZ","LEWIS","LEE","WALKER","HALL","ALLEN","YOUNG",
                    "HERNANDEZ","KING","WRIGHT","LOPEZ","HILL","SCOTT","GREEN","ADAMS","BAKER","GONZALEZ","NELSON","CARTER","MITCHELL","PEREZ","ROBERTS",
                    "TURNER","PHILLIPS","CAMPBELL","PARKER","EVANS","EDWARDS","COLLINS","STEWART","SANCHEZ","MORRIS","ROGERS","REED","COOK","MORGAN","BELL",
                    "MURPHY","BAILEY","RIVERA","COOPER","RICHARDSON","COX","HOWARD","WARD","TORRES","PETERSON","GRAY","RAMIREZ","JAMES","WATSON","BROOKS","KELLY",
                    "SANDERS","PRICE","BENNETT","WOOD","BARNES","ROSS","HENDERSON","COLEMAN","JENKINS","PERRY","POWELL","LONG","PATTERSON","HUGHES","FLORES",
                    "WASHINGTON","BUTLER","SIMMONS","FOSTER","GONZALES","BRYANT","ALEXANDER","RUSSELL","GRIFFIN","DIAZ","HAYES","MYERS","FORD","HAMILTON",
                    "GRAHAM","SULLIVAN","WALLACE","WOODS","COLE","WEST","JORDAN","OWENS","REYNOLDS","FISHER","ELLIS","HARRISON","GIBSON","MCDONALD","CRUZ",
                    "MARSHALL","ORTIZ","GOMEZ","MURRAY","FREEMAN","WELLS","WEBB","SIMPSON","STEVENS","TUCKER","PORTER","HUNTER","HICKS","CRAWFORD","HENRY",
                    "BOYD","MASON","MORALES","KENNEDY","WARREN","DIXON","RAMOS","REYES","BURNS","GORDON","SHAW","HOLMES","RICE","ROBERTSON","HUNT","BLACK",
                    "DANIELS","PALMER","MILLS","NICHOLS","GRANT","KNIGHT","FERGUSON","ROSE","STONE","HAWKINS","DUNN","PERKINS","HUDSON","SPENCER","GARDNER",
                    "STEPHENS","PAYNE","PIERCE","BERRY","MATTHEWS","ARNOLD","WAGNER","WILLIS","RAY","WATKINS","OLSON","CARROLL","DUNCAN","SNYDER","HART",
                    "CUNNINGHAM","BRADLEY","LANE","ANDREWS","RUIZ","HARPER","FOX","RILEY","ARMSTRONG","CARPENTER","WEAVER","GREENE","LAWRENCE","ELLIOTT",
                    "CHAVEZ","SIMS","AUSTIN","PETERS","KELLEY","FRANKLIN","LAWSON","FIELDS","GUTIERREZ","RYAN","SCHMIDT","CARR","VASQUEZ","CASTILLO","WHEELER",
                    "CHAPMAN","OLIVER","MONTGOMERY","RICHARDS","WILLIAMSON","JOHNSTON","BANKS","MEYER","BISHOP","MCCOY","HOWELL","ALVAREZ","MORRISON","HANSEN",
                    "FERNANDEZ","GARZA","HARVEY","LITTLE","BURTON","STANLEY","NGUYEN","GEORGE","JACOBS","REID","KIM","FULLER","LYNCH","DEAN","GILBERT","GARRETT",
                    "ROMERO","WELCH","LARSON","FRAZIER","BURKE","HANSON","DAY","MENDOZA","MORENO","BOWMAN","MEDINA","FOWLER"]

AnimalNames = [ "aardvark","alligator","alpaca","anteater","antelope","aoudad","ape","argali","armadillo","baboon","badger","basilisk","bat","bear","beaver",
                "bighorn","bison","boar","budgerigar","buffalo","bull","bunny","burro","camel","canary","capybara","cat","chameleon","chamois","cheetah",
                "chimpanzee","chinchilla","chipmunk","civet","coati","colt","cony","cougar","cow","coyote","crocodile","crow","deer","dingo","doe","dog",
                "donkey","dormouse","dromedary","duckbill","dugong","eland","elephant","elk","ermine","ewe","fawn","ferret","finch","fish","fox","frog",
                "gazelle","gemsbok","gila","monster","giraffe","gnu","goat","gopher","gorilla","grizzly","groundhog","guanaco","guineapig","hamster","hare",
                "hartebeest","hedgehog","hippopotamus","hog","horse","hyena","ibex","iguana","impala","jackal","jaguar","jerboa","kangaroo","kid","kinkajou",
                "kitten","koala","koodoo","lamb","lemur","leopard","lion","lizard","llama","lovebird","lynx","mandrill","mare","marmoset","marten","mink","mole",
                "mongoose","monkey","moose","mouse","mule","muskrat","mustang","mynah","bird","newt","ocelot","okapi","opossum","orangutan","oryx","otter","ox",
                "panda","panther","parakeet","parrot","peccary","pig","platypus","pony","porcupine","porpoise","prairie","pronghorn","puma","puppy","rabbit",
                "raccoon","ram","rat","reindeer","reptile","rhinoceros","roebuck","salamander","seal","sheep","shrew","silver","skunk","sloth","snake","springbok",
                "squirrel","stallion","steer","tapir","tiger","toad","turtle","vicuna","walrus","warthog","waterbuck","weasel","whale","wildcat","wolf","wolverine",
                "wombat","woodchuck","yak","zebra"]

                
def AnimalIndex(animal):
    animal = animal.strip()
    for i in range(len(AnimalNames)):
        if( AnimalNames[i] == animal.lower() ):
            return i
    return False

def HouseholdIndex(household):
    household = household.strip()
    for i in range(len(HouseholdNames)):
        if( HouseholdNames[i] == household.upper() ):
            return i
    return False
                
def String2Int(strng):
    'StrToNum(strng) -> integer'
    val = ""
    for i in range(len(strng)):
        val += str( ord( strng[i] ) )
    return eval(val)

APM = LcgRand( String2Int( username.lower() ) )

def ImputationProblem(Username, nr = 25, nc = 10, ne = 50 ):
    "Returns an imputation problem"
    APM = LcgRand( String2Int( Username.lower() ) )
    
    dta = APM.randint( 0, 10, ( 3, nc ) )
    dta = dta.astype(float)
    DataKey = zeros( (nr,nc) )
    for i in range(nr):
        DataKey[i] = dta[ APM.randint(3) ]
        for j in range(nc):
            if( APM.rand() < 0.1 ):
                DataKey[i,j] += 3*cos(APM.randint(1,3)*pi)
        
    DataKey = DataKey.astype(int)
    
    # create data
    
    DataKey = DataKey.astype(float)
    Data = DataKey.copy()
    
    # replace entries with nan
    
    rows = APM.randint(0,nr,ne)
    #cols = APM.randint(0,nc,ne)
    cols = array( [ i % nc for i in range(ne) ] )
    
    for i in range(ne):
        Data[rows[i], cols[i]] = nan
    
    return Data, DataKey, ne

Data, AssnImputeKey, AssnImpCnt = ImputationProblem(username)    

def Score(Candidate):
    'Score(Candidate) -> score for Candidate as a percentage'
    
    Tmp = Candidate - AssnImputeKey
    Errors = Tmp[ Tmp != 0].flatten()
    
    Scre = AssnImpCnt - len(Errors)
    
    for er in Errors:
        if( abs(er) <= 1 ):
            Scre += 0.8
        elif( abs(er) <= 2):
            Scre += 0.4
            
    return Scre/AssnImpCnt
    
def RecommenderProblem(Username):
    'Returns Recommender Problem Data'
    
    APM = LcgRand( String2Int( Username.lower() ) )
    PreData = APM.randint(0,7,(25,177))
    for i in range(25):
        for j in range(177):
            if( not (1 <= PreData[i,j] <= 5 ) ):
                PreData[i,j] = 0
            if( j in [130] and PreData[i,j] > 0 ):
                PreData[i,j] = APM.randint(4,6) #Everyone Loves the Penguins
                
    Data = zeros( (250,177) )
    
    inds = APM.choose(0,250,250)
    ic = 0
    for i in range(25):
        for ii in range(10):
            for j in range(177):
                if( APM.rand( ) < 0.10 ): # change 10% of the entries
                    Data[ inds[ic], j] = APM.randint(0,6)
                else:
                    Data[ inds[ic], j] = PreData[i,j]
            ic += 1
            
 
    Df = DataFrame( array(Data, dtype=float), index = HouseholdNames, columns = AnimalNames)
                
    # Replace some ratings with zeros 
    REinds = []
    REcnt  = 0
    Key = []
    Prb = []
    for i in range(250):
        for j in range(177):
           if( Data[i,j] > 0  ):
                if( APM.rand() < 0.05 and REcnt < 100 ):
                    REinds.append( [i,j] )
                    REcnt += 1
                    
    for rind in REinds:
        Hh = HouseholdNames[ rind[0] ]
        An = AnimalNames[ rind[1] ]
        Key.append( (Hh, An, Df[An][Hh]) )
        Prb.append( (Hh, An, 0 ) )
        Df[ An ][ Hh ] = 0
                    
    # Add the NA's 
    NAinds = []
    NAcnt  = 0
    for i in range(250):
        for j in range(177):
           if( Data[i,j] > 0  ):
                if( APM.rand() < 0.05 and NAcnt < 500 ):
                    NAinds.append( [i,j] )
                    NAcnt += 1

    #print(len(NAinds))
    
    for nind in NAinds:
        Hh = HouseholdNames[ nind[0] ]
        An = AnimalNames[ nind[1] ]
        Df[ An ][ Hh ] = NaN
        
    return Df, Prb, Key


try:
    if( username == "Replace with Your Username"):
        raise 
    SmallTownZoo, Unrated, FstExkey = RecommenderProblem(username)
except:
    print("Unable to produce the SmallTownZoo data.  Did you enter your username?")



def Grade(Candidate):
    "Grade(Candidate) -> CandidatePercentageCorrect"
    
    Key = FstExkey
    Cand = SmallTownZoo.copy()
    
    if( Cand.shape[0] == 250 ):
        for cnd in Candidate:
            Cand[ cnd[1]][cnd[0]] = cnd[2]
        Cand = Cand.T
    else:
        for cnd in Candidate:
            Cand[ cnd[0]][cnd[1]] = cnd[2]
    Score = 0
    for ky in Key:
        if( Cand[ky[0]][ky[1]] == ky[2] ):
            Score += 1
        elif( abs(Cand[ky[0]][ky[1]] - ky[2]) <= 1  ):
            Score += 0.5
    Score = round(Score)
            
    msgString =  """<div style="border:solid black 2px;width:500px;padding:5px;"><b>Current Score: </b> %s percent  <p>&nbsp;</p>""" % round(Score,2) 
    if( Score < 50): 
        msgString += """<p>You might want to refine your methods.  </p> 

                Be sure that you remove na's first, and it needs to be solid.  Poor handling of na 
                will result in poor cosine similarity step."""
    elif( Score < 70):
        msgString += """<p>You're making progress. </p> 

                  You may still have issues in the na removal step.  Don't be afraid to tweak there also."""
    elif( Score < 90): 
        msgString += """<p>You're almost there.  Probably is <i>k</i> or the method in either Impute or Predict.</p>""" 
    else:
        msgString += """<p>Good Job!</p>""" 
    return HTML(msgString+"</div>")

from scipy import stats

class IG: 
    def norm( my, x, order = 2):
        tmp = logical_not( isnan(x)  ) 
        return norm( x[tmp], order )

    def correlation(my, x, y):
        tmp = logical_not( logical_or(isnan(x), isnan(y) ) ) 
        return corrcoef(x[tmp],y[tmp])[1,0]

    def mean( my, x ):
        tmp = logical_not( isnan(x)  ) 
        return mean( x[tmp] )
    
    def median( my, x):
        tmp = logical_not( isnan(x)  ) 
        return median( x[tmp] )
    
    def mode( my, x):
        tmp = logical_not( isnan(x)  ) 
        return stats.mode( x[tmp], axis=None)[0][0]

IgnoringNan = IG()

figsize(8,6)

def DisplayData2D( ClassData, kNNGraph = None ):
    "DisplayData2D( ClassData ) -> Scatter plot of Classifier 2D Data"
    
    m,n = ClassData.shape
    C0inds = []
    C1inds = []
    CUinds = {}
    ucnt = 0
    
    for i in range(m):
        if( isnan(ClassData[i,2]) ):
            CUinds[i] = chr( ord('A') + ucnt )
            ucnt += 1
        elif( ClassData[i,2] == 0 ):
            C0inds.append(i)
        else:
            C1inds.append(i)
     
    scatter( ClassData[C0inds,0], ClassData[C0inds,1], marker = '$0$', color='g', s=50)
    scatter( ClassData[C1inds,0], ClassData[C1inds,1], marker = '$1$', color='k', s=50)
    for i in CUinds.keys(): 
        scatter( ClassData[i,0], ClassData[i,1], marker = '$%s$' % CUinds[i], color='r', s=100)
    
    if( kNNGraph != None ):
        print("Scores for Unclassified based on mean class of k-nearest neighbors")
        for v in kNNGraph.nodes():
            for r in kNNGraph.neighbors(v):
                dx =  ClassData[r,0] - ClassData[v,0]
                dy =  ClassData[r,1] - ClassData[v,1]
                if( dx**2 + dy**2 > 0):
                    arrow( ClassData[v,0], ClassData[v,1],dx,dy, color='k', alpha=0.2, head_width=0.25, length_includes_head=True)
        for v in CUinds.keys():
            acc = 0
            cnt = 0
            for r in kNNGraph.neighbors(v):
                if(not isnan(ClassData[r,2]) ):
                    cnt += 1
                    acc += ClassData[r,2]
            if(cnt != 0 ):
                print( "kNN prediction of %s for unclassified point %s at (%s, %s)" % ( round(acc/cnt,2), CUinds[v], ClassData[v,0], ClassData[v,1] ) )
            else:
                print( "kNN makes no prediction for unclassified point %s at (%s, %s)" % ( CUinds[v], ClassData[v,0], ClassData[v,1] ) )
             
n0 = 10
n1 = 10
nu =  5

Class0 = array( [ APM.randint(0,10, n0),    randint(0,10,n0), [0 for i in range(n0) ] ] )
Class1 = array( [ APM.randint(0,10, n1)+10, randint(0,10,n1), [1 for i in range(n1) ] ] )
ClassU = array( [ APM.randint(5,15,nu), randint(0,10,nu), [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+n1)] = Class1
Exdat[:,(n0+n1):] = ClassU

Example1 = DataFrame( Exdat.T, columns = ['x','y','class'] )

n0 = 20
n1 = 20
nu =  5

Class0 = array( [ APM.randint(0,15, n0),    randint(0,10,n0), [0 for i in range(n0) ] ] )
Class1 = array( [ sqrt(APM.randint(0,100, n1)+100), randint(0,10,n1), [1 for i in range(n1) ] ] )
ClassU = array( [ APM.randint(5,15,nu), APM.randint(0,10,nu), [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+n1)] = Class1
Exdat[:,(n0+n1):] = ClassU

Example2 = DataFrame( Exdat.T, columns = ['x','y','class'] )


n0 = 50
n1 = 50
nu =  5

DoubleDensity1 = APM.randint(8,20, 2*n1)-0.5
DoubleDensity1[n1:] = APM.randint( 8,15,n1 )
DDy = [ APM.randint(0,9)+ APM.rand() for i in range(2*n1)]

Class0 = array( [ APM.randint(4,13, n0),    randint(4,9,n0)-0.5, [0 for i in range(n0) ] ] )
Class1 = array( [ DoubleDensity1, DDy, [1 for i in range(2*n1) ] ] )
ClassU = array( [ APM.randint(8,12,nu), APM.randint(3,6,nu) + APM.randint(0,5,nu)*0.2 , [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+2*n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+2*n1)] = Class1
Exdat[:,(n0+2*n1):] = ClassU

Example3 = DataFrame( Exdat.T, columns = ['x','y','class'] )
Example3Data = Example3.as_matrix()

n0 = 50
n1 = 200
nu =  5

Class0 = array( [ [ (APM.rand()+ 7)*cos(2*pi*i/n0) for i in range(n0)], [ (APM.rand()+ 7)*sin(2*pi*i/n0) for i in range(n0)], [0 for i in range(n0) ] ] )
Class1 = array( [ [ (4*APM.rand()+ 2)*cos(2*pi*i/n1) for i in range(n1)], [ (4*APM.rand()+ 2)*sin(2*pi*i/n1) for i in range(n1)], [1 for i in range(n1) ] ] )
ClassU = array( [ [ (6.1+i/nu)*cos(2*pi*i/nu) for i in range(nu)], [ (6.1+i/nu)*sin(2*pi*i/nu) for i in range(nu)], [nan for i in range(nu) ]] )

Exdat = zeros( (3,n0+n1+nu)  )

Exdat[:,:n0] = Class0
Exdat[:,n0:(n0+n1)] = Class1
Exdat[:,(n0+n1):] = ClassU

Exercise = DataFrame( Exdat.T, columns = ['x','y','class'] )
ExerciseData = Exercise.as_matrix()

    
def NormkNN(Data, k = 5, order = 2 ):
    """NormkNN(Data) -> norm distance k Nearest Neighbors directed graph with uniform outdegree of k

    Parameters are 

    k:  number of neighbors

    order: order of the norm"""
    
    m,n = Data.shape
    DistanceMatrix = zeros( shape = (m,m)  )  
    
    for i in range(m):
        for j in range(m):
            DistanceMatrix[i,j] = IgnoringNan.norm(  Data[i] - Data[j], order )
    
    DistanceData = [ (i,j,DistanceMatrix[i,j] )  for i in range(m) for j in range(i+1,m) ] 
    DistanceData = array( DistanceData, dtype = [ ('row1', int), ('row2', int), ( 'distance', float ) ] )
    ndarray.sort( DistanceData, order='distance' )
    
    ImputekNN = networkx.DiGraph()
    ImputekNN.add_nodes_from( list(range(m)) )
    
    for distdat in DistanceData:
        if ImputekNN.out_degree(distdat[0]) < k:
            ImputekNN.add_edge(distdat[0], distdat[1] )
        if ImputekNN.out_degree(distdat[1]) < k:   
            ImputekNN.add_edge(distdat[1], distdat[0] )
            
    return ImputekNN

def CosinekNN(Data, k = 5 ):
    """CosinekNN(Data) -> Cosine similarity k Nearest Neighbors directed graph with uniform outdegree of k

    Parameters are 

    k:  number of neighbors

    """
    
    m,n = Data.shape
    DistanceMatrix = zeros( shape = (m,m)  )  
    
    for i in range(m):
        for j in range(m):
            DistanceMatrix[i,j] = 1 - dot( Data[i],  Data[j] ) / norm(Data[i])/norm(Data[j])
    
    DistanceData = [ (i,j,DistanceMatrix[i,j] )  for i in range(m) for j in range(i+1,m) ] 
    DistanceData = array( DistanceData, dtype = [ ('row1', int), ('row2', int), ( 'distance', float ) ] )
    ndarray.sort( DistanceData, order='distance' )
    
    kNN = networkx.DiGraph()
    kNN.add_nodes_from( list(range(m)) )
    
    for distdat in DistanceData:
        if kNN.out_degree(distdat[0]) < k:
            kNN.add_edge(distdat[0], distdat[1] )
        if kNN.out_degree(distdat[1]) < k:   
            kNN.add_edge(distdat[1], distdat[0] )
            
    return kNN
 
def Impute(Data, kNNGraph, Method = IgnoringNan.mean):
    "Impute(Data,Graph) -> Data with nan's replaced using Graph Neighborhoods"
    
    Data = Data.copy()
    
    m,n = Data.shape
    for i in range(m):
        nbrs = kNNGraph.neighbors(i)
        for j in range(n):
            if( isnan( Data[i,j] ) ):
                Data[i,j] = int( Method( array( [Data[nbr,j] for nbr in nbrs] ) ) )
    return Data    

    
def Predict(ImputedData, Unrated, kNNGraph, Method = mean, PrintPredictions = 0 ):
    """Predict(Data, Unrated, kNNGraph) -> Data with Unrated replaced by predictions from using Graph Neighborhoods
    
    Method: Any method which returns a number given an array
    """
    apd = False
    if( ImputedData.shape[0] == 250  ):
        apd = True
     
    Ratings = []
    
    for unr in Unrated:
        unh = HouseholdIndex( unr[0] )
        una = AnimalIndex( unr[1] )
        
        nbrs = kNNGraph.neighbors( unh );
        if(apd):
            pred =  int( Method( array( [ ImputedData[nbr,una] for nbr in nbrs] ) ) )
            if(PrintPredictions > 0):
                PrintPredictions += -1
                print( "Household %s is predicted give animal exhibit %s a rating of %s" %(unr[0], unr[1], pred ) )
            Ratings.append( (unr[0], unr[1], pred ) )
        else:
            pred =  int( Method( array( [ ImputedData[una,nbr] for nbr in nbrs] ) ) )
            if(PrintPredictions > 0 ):
                PrintPredictions += -1
                print( "Household %s is predicted give animal exhibit %s a rating of %s" %(unr[0], unr[1], pred ) )
            Ratings.append( (unr[0], unr[1], pred ) )
        
    return Ratings
        
UserID = list(range(1,6041))
Movies = ["Toy Story (1995)","Jumanji (1995)","Grumpier Old Men (1995)","Waiting to Exhale (1995)","Father of the Bride Part II (1995)","Heat (1995)","Sabrina (1995)","Tom and Huck (1995)","Sudden Death (1995)","GoldenEye (1995)","American President, The (1995)","Dracula: Dead and Loving It (1995)","Balto (1995)","Nixon (1995)","Cutthroat Island (1995)","Casino (1995)","Sense and Sensibility (1995)","Four Rooms (1995)","Ace Ventura: When Nature Calls (1995)","Money Train (1995)","Get Shorty (1995)","Copycat (1995)","Assassins (1995)","Powder (1995)","Leaving Las Vegas (1995)","Othello (1995)","Now and Then (1995)","Persuasion (1995)","City of Lost Children, The (1995)","Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)","Dangerous Minds (1995)","Twelve Monkeys (1995)","Wings of Courage (1995)","Babe (1995)","Carrington (1995)","Dead Man Walking (1995)","Across the Sea of Time (1995)","It Takes Two (1995)","Clueless (1995)","Cry, the Beloved Country (1995)","Richard III (1995)","Dead Presidents (1995)","Restoration (1995)","Mortal Kombat (1995)","To Die For (1995)","How to Make an American Quilt (1995)","Seven (Se7en) (1995)","Pocahontas (1995)","When Night Is Falling (1995)","Usual Suspects, The (1995)","Guardian Angel (1994)","Mighty Aphrodite (1995)","Lamerica (1994)","Big Green, The (1995)","Georgia (1995)","Kids of the Round Table (1995)","Home for the Holidays (1995)","Postino, Il (The Postman) (1994)","Confessional, The (Le Confessionnal) (1995)","Indian in the Cupboard, The (1995)","Eye for an Eye (1996)","Mr. Holland`s Opus (1995)","Don`t Be a Menace to South Central While Drinking Your Juice in the Hood (1996)","Two if by Sea (1996)","Bio-Dome (1996)","Lawnmower Man 2: Beyond Cyberspace (1996)","Two Bits (1995)","French Twist (Gazon maudit) (1995)","Friday (1995)","From Dusk Till Dawn (1996)","Fair Game (1995)","Kicking and Screaming (1995)","Misérables, Les (1995)","Bed of Roses (1996)","Big Bully (1996)","Screamers (1995)","Nico Icon (1995)","Crossing Guard, The (1995)","Juror, The (1996)","White Balloon, The (Badkonake Sefid ) (1995)","Things to Do in Denver when You`re Dead (1995)","Antonia`s Line (Antonia) (1995)","Once Upon a Time... When We Were Colored (1995)","Last Summer in the Hamptons (1995)","Angels and Insects (1995)","White Squall (1996)","Dunston Checks In (1996)","Black Sheep (1996)","Nick of Time (1995)","Journey of August King, The (1995)","Mary Reilly (1996)","Vampire in Brooklyn (1995)","Beautiful Girls (1996)","Broken Arrow (1996)","In the Bleak Midwinter (1995)","Hate (Haine, La) (1995)","Shopping (1994)","Heidi Fleiss: Hollywood Madam (1995)","City Hall (1996)","Bottle Rocket (1996)","Mr. Wrong (1996)","Unforgettable (1996)","Happy Gilmore (1996)","Bridges of Madison County, The (1995)","Nobody Loves Me (Keiner liebt mich) (1994)","Muppet Treasure Island (1996)","Catwalk (1995)","Headless Body in Topless Bar (1995)","Braveheart (1995)","Taxi Driver (1976)","Rumble in the Bronx (1995)","Before and After (1996)","Margaret`s Museum (1995)","Happiness Is in the Field (1995)","Anne Frank Remembered (1995)","Young Poisoner`s Handbook, The (1995)","If Lucy Fell (1996)","Steal Big, Steal Little (1995)","Race the Sun (1996)","Boys of St. Vincent, The (1993)","Boomerang (1992)","Chungking Express (1994)","Star Maker, The (Uomo delle stelle, L`) (1995)","Flirting With Disaster (1996)","NeverEnding Story III, The (1994)","Silence of the Palace, The (Saimt el Qusur) (1994)","Jupiter`s Wife (1994)","Pie in the Sky (1995)","Angela (1995)","Frankie Starlight (1995)","Jade (1995)","Nueba Yol (1995)","Sonic Outlaws (1995)","Down Periscope (1996)","From the Journals of Jean Seberg (1995)","Man of the Year (1995)","Neon Bible, The (1995)","Target (1995)","Up Close and Personal (1996)","Birdcage, The (1996)","Shadows (Cienie) (1988)","Gospa (1995)","Brothers McMullen, The (1995)","Bad Boys (1995)","Amazing Panda Adventure, The (1995)","Basketball Diaries, The (1995)","Awfully Big Adventure, An (1995)","Amateur (1994)","Apollo 13 (1995)","Rob Roy (1995)","Addiction, The (1995)","Batman Forever (1995)","Belle de jour (1967)","Beyond Rangoon (1995)","Blue in the Face (1995)","Canadian Bacon (1994)","Casper (1995)","Clockers (1995)","Congo (1995)","Crimson Tide (1995)","Crumb (1994)","Desperado (1995)","Devil in a Blue Dress (1995)","Die Hard: With a Vengeance (1995)","Doom Generation, The (1995)","Feast of July (1995)","First Knight (1995)","Free Willy 2: The Adventure Home (1995)","Hackers (1995)","Jeffrey (1995)","Johnny Mnemonic (1995)","Judge Dredd (1995)","Jury Duty (1995)","Kids (1995)","Living in Oblivion (1995)","Lord of Illusions (1995)","Love & Human Remains (1993)","Mad Love (1995)","Mallrats (1995)","Mighty Morphin Power Rangers: The Movie (1995)","Moonlight and Valentino (1995)","Mute Witness (1994)","Nadja (1994)","Net, The (1995)","Nine Months (1995)","Party Girl (1995)","Prophecy, The (1995)","Reckless (1995)","Safe (1995)","Scarlet Letter, The (1995)","Show, The (1995)","Showgirls (1995)","Smoke (1995)","Something to Talk About (1995)","Species (1995)","Stars Fell on Henrietta, The (1995)","Strange Days (1995)","Umbrellas of Cherbourg, The (Parapluies de Cherbourg, Les) (1964)","Tie That Binds, The (1995)","Three Wishes (1995)","Total Eclipse (1995)","To Wong Foo, Thanks for Everything! Julie Newmar (1995)","Under Siege 2: Dark Territory (1995)","Unstrung Heroes (1995)","Unzipped (1995)","Walk in the Clouds, A (1995)","Waterworld (1995)","White Man`s Burden (1995)","Wild Bill (1995)","Browning Version, The (1994)","Bushwhacked (1995)","Burnt By the Sun (Utomlyonnye solntsem) (1994)","Before the Rain (Pred dozhdot) (1994)","Before Sunrise (1995)","Billy Madison (1995)","Babysitter, The (1995)","Boys on the Side (1995)","Cure, The (1995)","Castle Freak (1995)","Circle of Friends (1995)","Clerks (1994)","Don Juan DeMarco (1995)","Disclosure (1994)","Dream Man (1995)","Drop Zone (1994)","Destiny Turns on the Radio (1995)","Death and the Maiden (1994)","Dolores Claiborne (1994)","Dumb & Dumber (1994)","Eat Drink Man Woman (1994)","Exotica (1994)","Exit to Eden (1994)","Ed Wood (1994)","French Kiss (1995)","Forget Paris (1995)","Far From Home: The Adventures of Yellow Dog (1995)","Goofy Movie, A (1995)","Hideaway (1995)","Fluke (1995)","Farinelli: il castrato (1994)","Gordy (1995)","Gumby: The Movie (1995)","Glass Shield, The (1994)","Hoop Dreams (1994)","Heavenly Creatures (1994)","Houseguest (1994)","Immortal Beloved (1994)","Heavyweights (1994)","Hunted, The (1995)","I.Q. (1994)","Interview with the Vampire (1994)","Jefferson in Paris (1995)","Jerky Boys, The (1994)","Junior (1994)","Just Cause (1995)","Kid in King Arthur`s Court, A (1995)","Kiss of Death (1995)","Star Wars: Episode IV - A New Hope (1977)","Little Women (1994)","Little Princess, A (1995)","Ladybird Ladybird (1994)","Enfer, L` (1994)","Like Water for Chocolate (Como agua para chocolate) (1992)","Legends of the Fall (1994)","Major Payne (1994)","Little Odessa (1994)","My Crazy Life (Mi vida loca) (1993)","Love Affair (1994)","Losing Isaiah (1995)","Madness of King George, The (1994)","Mary Shelley`s Frankenstein (1994)","Man of the House (1995)","Mixed Nuts (1994)","Milk Money (1994)","Miracle on 34th Street (1994)","Miami Rhapsody (1995)","My Family (1995)","Murder in the First (1995)","Nobody`s Fool (1994)","Nell (1994)","New Jersey Drive (1995)","New York Cop (1996)","Beyond Bedlam (1993)","Nemesis 2: Nebula (1995)","Nina Takes a Lover (1994)","Natural Born Killers (1994)","Only You (1994)","Once Were Warriors (1994)","Poison Ivy II (1995)","Outbreak (1995)","Professional, The (a.k.a. Leon: The Professional) (1994)","Perez Family, The (1995)","Pyromaniac`s Love Story, A (1995)","Pulp Fiction (1994)","Panther (1995)","Pushing Hands (1992)","Priest (1994)","Quiz Show (1994)","Picture Bride (1995)","Queen Margot (La Reine Margot) (1994)","Quick and the Dead, The (1995)","Roommates (1995)","Ready to Wear (Pret-A-Porter) (1994)","Three Colors: Red (1994)","Three Colors: Blue (1993)","Three Colors: White (1994)","Red Firecracker, Green Firecracker (1994)","Rent-a-Kid (1995)","Relative Fear (1994)","Stuart Saves His Family (1995)","Swan Princess, The (1994)","Secret of Roan Inish, The (1994)","Specialist, The (1994)","Stargate (1994)","Santa Clause, The (1994)","Shawshank Redemption, The (1994)","Shallow Grave (1994)","Suture (1993)","Strawberry and Chocolate (Fresa y chocolate) (1993)","Swimming with Sharks (1995)","Sum of Us, The (1994)","National Lampoon`s Senior Trip (1995)","To Live (Huozhe) (1994)","Tank Girl (1995)","Tales From the Crypt Presents: Demon Knight (1995)","Star Trek: Generations (1994)","Tales from the Hood (1995)","Tom & Viv (1994)","Village of the Damned (1995)","Tommy Boy (1995)","Vanya on 42nd Street (1994)","Underneath, The (1995)","Walking Dead, The (1995)","What`s Eating Gilbert Grape (1993)","Virtuosity (1995)","While You Were Sleeping (1995)","War, The (1994)","Double Happiness (1994)","Muriel`s Wedding (1994)","Baby-Sitters Club, The (1995)","Ace Ventura: Pet Detective (1994)","Adventures of Priscilla, Queen of the Desert, The (1994)","Backbeat (1993)","Bitter Moon (1992)","Bullets Over Broadway (1994)","Clear and Present Danger (1994)","Client, The (1994)","Corrina, Corrina (1994)","Crooklyn (1994)","Crow, The (1994)","Cobb (1994)","Flintstones, The (1994)","Forrest Gump (1994)","Four Weddings and a Funeral (1994)","Higher Learning (1995)","I Like It Like That (1994)","I Love Trouble (1994)","It Could Happen to You (1994)","Jungle Book, The (1994)","Wonderful, Horrible Life of Leni Riefenstahl, The (Die Macht der Bilder) (1993)","Lion King, The (1994)","Little Buddha (1993)","Wes Craven`s New Nightmare (1994)","Mask, The (1994)","Maverick (1994)","Mrs. Parker and the Vicious Circle (1994)","Naked Gun 33 1/3: The Final Insult (1994)","Paper, The (1994)","Reality Bites (1994)","Red Rock West (1992)","Richie Rich (1994)","Safe Passage (1994)","River Wild, The (1994)","Speed (1994)","Speechless (1994)","Timecop (1994)","True Lies (1994)","When a Man Loves a Woman (1994)","Wolf (1994)","Wyatt Earp (1994)","Bad Company (1995)","Man of No Importance, A (1994)","S.F.W. (1994)","Low Down Dirty Shame, A (1994)","Boys Life (1995)","Colonel Chabert, Le (1994)","Faster Pussycat! Kill! Kill! (1965)","Jason`s Lyric (1994)","Secret Adventures of Tom Thumb, The (1993)","Street Fighter (1994)","Coldblooded (1995)","Desert Winds (1995)","Fall Time (1995)","Fear, The (1995)","Frank and Ollie (1995)","Girl in the Cadillac (1995)","Homage (1995)","Mirage (1995)","Open Season (1996)","Two Crimes (1995)","Brother Minister: The Assassination of Malcolm X (1994)","Highlander III: The Sorcerer (1994)","Federal Hill (1994)","In the Mouth of Madness (1995)","8 Seconds (1994)","Above the Rim (1994)","Addams Family Values (1993)","You So Crazy (1994)","Age of Innocence, The (1993)","Airheads (1994)","Air Up There, The (1994)","Another Stakeout (1993)","Bad Girls (1994)","Barcelona (1994)","Being Human (1993)","Beverly Hillbillies, The (1993)","Beverly Hills Cop III (1994)","Black Beauty (1994)","Blink (1994)","Blown Away (1994)","Blue Chips (1994)","Blue Sky (1994)","Body Snatchers (1993)","Boxing Helena (1993)","Bronx Tale, A (1993)","Cabin Boy (1994)","Calendar Girl (1993)","Carlito`s Way (1993)","City Slickers II: The Legend of Curly`s Gold (1994)","Clean Slate (1994)","Cliffhanger (1993)","Coneheads (1993)","Color of Night (1994)","Cops and Robbersons (1994)","Cowboy Way, The (1994)","Dangerous Game (1993)","Dave (1993)","Dazed and Confused (1993)","Demolition Man (1993)","Endless Summer 2, The (1994)","Even Cowgirls Get the Blues (1993)","Fatal Instinct (1993)","Farewell My Concubine (1993)","Favor, The (1994)","Fearless (1993)","Fear of a Black Hat (1993)","With Honors (1994)","Flesh and Bone (1993)","Widows` Peak (1994)","For Love or Money (1993)","Firm, The (1993)","Free Willy (1993)","Fresh (1994)","Fugitive, The (1993)","Geronimo: An American Legend (1993)","Getaway, The (1994)","Getting Even with Dad (1994)","Go Fish (1994)","Good Man in Africa, A (1994)","Guilty as Sin (1993)","Hard Target (1993)","Heaven & Earth (1993)","Hot Shots! Part Deux (1993)","Live Nude Girls (1995)","Englishman Who Went Up a Hill, But Came Down a Mountain, The (1995)","House of the Spirits, The (1993)","House Party 3 (1994)","Hudsucker Proxy, The (1994)","I`ll Do Anything (1994)","In the Army Now (1994)","In the Line of Fire (1993)","In the Name of the Father (1993)","Inkwell, The (1994)","What`s Love Got to Do with It? (1993)","Jimmy Hollywood (1994)","Judgment Night (1993)","Jurassic Park (1993)","Kalifornia (1993)","Killing Zoe (1994)","King of the Hill (1993)","Lassie (1994)","Last Action Hero (1993)","Life with Mikey (1993)","Lightning Jack (1994)","M. Butterfly (1993)","Made in America (1993)","Malice (1993)","Man Without a Face, The (1993)","Manhattan Murder Mystery (1993)","Menace II Society (1993)","Executive Decision (1996)","In the Realm of the Senses (Ai no corrida) (1976)","What Happened Was... (1994)","Much Ado About Nothing (1993)","Mr. Jones (1993)","Mr. Wonderful (1993)","Mrs. Doubtfire (1993)","Naked (1993)","Next Karate Kid, The (1994)","New Age, The (1994)","No Escape (1994)","North (1994)","Orlando (1993)","Perfect World, A (1993)","Philadelphia (1993)","Piano, The (1993)","Poetic Justice (1993)","Program, The (1993)","Robert A. Heinlein`s The Puppet Masters (1994)","Radioland Murders (1994)","Ref, The (1994)","Remains of the Day, The (1993)","Renaissance Man (1994)","Rising Sun (1993)","Road to Wellville, The (1994)","Robocop 3 (1993)","Robin Hood: Men in Tights (1993)","Romeo Is Bleeding (1993)","Romper Stomper (1992)","Ruby in Paradise (1993)","Rudy (1993)","Saint of Fort Washington, The (1993)","Savage Nights (Nuits fauves, Les) (1992)","Schindler`s List (1993)","Scout, The (1994)","Searching for Bobby Fischer (1993)","Second Best (1994)","Secret Garden, The (1993)","Serial Mom (1994)","Shadow, The (1994)","Shadowlands (1993)","Short Cuts (1993)","Simple Twist of Fate, A (1994)","Sirens (1994)","Six Degrees of Separation (1993)","Sleepless in Seattle (1993)","Sliver (1993)","Blade Runner (1982)","Son in Law (1993)","So I Married an Axe Murderer (1993)","Striking Distance (1993)","Harlem (1993)","Super Mario Bros. (1993)","Surviving the Game (1994)","Terminal Velocity (1994)","Thirty-Two Short Films About Glenn Gould (1993)","Threesome (1994)","Nightmare Before Christmas, The (1993)","Three Musketeers, The (1993)","Tombstone (1993)","Trial by Jury (1994)","True Romance (1993)","War Room, The (1993)","Mamma Roma (1962)","Pagemaster, The (1994)","Paris, France (1993)","Beans of Egypt, Maine, The (1994)","Killer (Bulletproof Heart) (1994)","Welcome to the Dollhouse (1995)","Germinal (1993)","Chasers (1994)","Cronos (1992)","Naked in New York (1994)","Kika (1993)","Bhaji on the Beach (1993)","Little Big League (1994)","Slingshot, The (Kådisbellan ) (1993)","Wedding Gift, The (1994)","Foreign Student (1994)","Ciao, Professore! (Io speriamo che me la cavo ) (1993)","Spanking the Monkey (1994)","Little Rascals, The (1994)","Fausto (1993)","Andre (1994)","Hour of the Pig, The (1993)","Scorta, La (1993)","Princess Caraboo (1994)","Celluloid Closet, The (1995)","Metisse (Café au Lait) (1993)","Dear Diary (Caro Diario) (1994)","I Don`t Want to Talk About It (De eso no se habla) (1993)","Brady Bunch Movie, The (1995)","Home Alone (1990)","Ghost (1990)","Aladdin (1992)","Terminator 2: Judgment Day (1991)","Dances with Wolves (1990)","Tough and Deadly (1995)","Batman (1989)","Silence of the Lambs, The (1991)","Snow White and the Seven Dwarfs (1937)","Beauty and the Beast (1991)","Pinocchio (1940)","Pretty Woman (1990)","Window to Paris (1994)","Wild Bunch, The (1969)","Love and a .45 (1994)","Wooden Man`s Bride, The (Wu Kui) (1994)","Great Day in Harlem, A (1994)","Bye Bye, Love (1995)","Criminals (1996)","One Fine Day (1996)","Candyman: Farewell to the Flesh (1995)","Century (1993)","Fargo (1996)","Homeward Bound II: Lost in San Francisco (1996)","Heavy Metal (1981)","Hellraiser: Bloodline (1996)","Pallbearer, The (1996)","Jane Eyre (1996)","Loaded (1994)","Bread and Chocolate (Pane e cioccolata) (1973)","Aristocats, The (1970)","Flower of My Secret, The (La Flor de Mi Secreto) (1995)","Two Much (1996)","Ed (1996)","Scream of Stone (Schrei aus Stein) (1991)","My Favorite Season (1993)","Modern Affair, A (1995)","Condition Red (1995)","Asfour Stah (1990)","Thin Line Between Love and Hate, A (1996)","Last Supper, The (1995)","Primal Fear (1996)","Rude (1995)","Carried Away (1996)","All Dogs Go to Heaven 2 (1996)","Land and Freedom (Tierra y libertad) (1995)","Denise Calls Up (1995)","Theodore Rex (1995)","Family Thing, A (1996)","Frisk (1995)","Sgt. Bilko (1996)","Jack and Sarah (1995)","Girl 6 (1996)","Diabolique (1996)","Little Indian, Big City (Un indien dans la ville) (1994)","Roula (1995)","Peanuts - Die Bank zahlt alles (1996)","Happy Weekend (1996)","Nelly & Monsieur Arnaud (1995)","Courage Under Fire (1996)","Mission: Impossible (1996)","Cold Fever (Á köldum klaka) (1994)","Moll Flanders (1996)","Superweib, Das (1996)","301, 302 (1995)","Dragonheart (1996)","Und keiner weint mir nach (1996)","Mutters Courage (1995)","Eddie (1996)","Yankee Zulu (1994)","Billy`s Holiday (1995)","Purple Noon (1960)","August (1996)","James and the Giant Peach (1996)","Fear (1996)","Kids in the Hall: Brain Candy (1996)","Faithful (1996)","Underground (1995)","All Things Fair (1996)","Bloodsport 2 (1995)","Pather Panchali (1955)","Aparajito (1956)","World of Apu, The (Apur Sansar) (1959)","Mystery Science Theater 3000: The Movie (1996)","Tarantella (1995)","Space Jam (1996)","Barbarella (1968)","Hostile Intentions (1994)","They Bite (1996)","Some Folks Call It a Sling Blade (1993)","Run of the Country, The (1995)","Alphaville (1965)","Clean Slate (Coup de Torchon) (1981)","Tigrero: A Film That Was Never Made (1994)","Eye of Vichy, The (Oeil de Vichy, L`) (1993)","Windows (1980)","It`s My Party (1995)","Country Life (1994)","Operation Dumbo Drop (1995)","Promise, The (Versprechen, Das) (1994)","Mrs. Winterbourne (1996)","Solo (1996)","Under the Domin Tree (Etz Hadomim Tafus) (1994)","Substitute, The (1996)","True Crime (1995)","Butterfly Kiss (1995)","Feeling Minnesota (1996)","Delta of Venus (1994)","To Cross the Rubicon (1991)","Angus (1995)","Daens (1992)","Faces (1968)","Boys (1996)","Quest, The (1996)","Cosi (1996)","Sunset Park (1996)","Mulholland Falls (1996)","Truth About Cats & Dogs, The (1996)","Oliver & Company (1988)","Celtic Pride (1996)","Flipper (1996)","Captives (1994)","Of Love and Shadows (1994)","Dead Man (1995)","Horseman on the Roof, The (Hussard sur le toit, Le) (1995)","Switchblade Sisters (1975)","Mouth to Mouth (Boca a boca) (1995)","Visitors, The (Les Visiteurs) (1993)","Multiplicity (1996)","Wallace & Gromit: The Best of Aardman Animation (1996)","Halfmoon (Paul Bowles - Halbmond) (1995)","Haunted World of Edward D. Wood Jr., The (1995)","Two Friends (1986)","Craft, The (1996)","Great White Hype, The (1996)","Last Dance (1996)","War Stories (1995)","Cold Comfort Farm (1995)","Institute Benjamenta, or This Dream People Call Human Life (1995)","Low Life, The (1994)","Heaven`s Prisoners (1996)","Original Gangstas (1996)","Rock, The (1996)","Getting Away With Murder (1996)","Cemetery Man (Dellamorte Dellamore) (1994)","Twister (1996)","Barb Wire (1996)","Garcu, Le (1995)","Honigmond (1996)","Ghost in the Shell (Kokaku kidotai) (1995)","Thinner (1996)","Spy Hard (1996)","Brothers in Trouble (1995)","Close Shave, A (1995)","Force of Evil (1948)","Stupids, The (1996)","Arrival, The (1996)","Man from Down Under, The (1943)","Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb (1963)","Careful (1992)","Vermont Is For Lovers (1992)","Month by the Lake, A (1995)","Gold Diggers: The Secret of Bear Mountain (1995)","Kim (1950)","Carmen Miranda: Bananas Is My Business (1994)","Ashes of Time (1994)","Jar, The (Khomreh) (1992)","Maya Lin: A Strong Clear Vision (1994)","Stalingrad (1993)","Phantom, The (1996)","Striptease (1996)","Last of the High Kings, The (a.k.a. Summer Fling) (1996)","Heavy (1995)","Jack (1996)","I Shot Andy Warhol (1996)","Grass Harp, The (1995)","Someone Else`s America (1995)","Marlene Dietrich: Shadow and Light (1996)","Costa Brava (1946)","Vie est belle, La (Life is Rosey) (1987)","Quartier Mozart (1992)","Touki Bouki (Journey of the Hyena) (1973)","Wend Kuuni (God`s Gift) (1982)","Spirits of the Dead (Tre Passi nel Delirio) (1968)","Babyfever (1994)","Pharaoh`s Army (1995)","Trainspotting (1996)","`Til There Was You (1997)","Independence Day (ID4) (1996)","Stealing Beauty (1996)","Fan, The (1996)","Hunchback of Notre Dame, The (1996)","Cable Guy, The (1996)","Kingpin (1996)","Eraser (1996)","Gate of Heavenly Peace, The (1995)","Nutty Professor, The (1996)","I, Worst of All (Yo, la peor de todas) (1990)","An Unforgettable Summer (1994)","Last Klezmer: Leopold Kozlowski, His Life and Music, The (1995)","Hungarian Fairy Tale, A (1987)","My Life and Times With Antonin Artaud (En compagnie d`Antonin Artaud) (1993)","Midnight Dancers (Sibak) (1994)","Somebody to Love (1994)","Very Natural Thing, A (1974)","Old Lady Who Walked in the Sea, The (Vieille qui marchait dans la mer, La) (1991)","Daylight (1996)","Frighteners, The (1996)","Lone Star (1996)","Harriet the Spy (1996)","Phenomenon (1996)","Walking and Talking (1996)","She`s the One (1996)","Time to Kill, A (1996)","American Buffalo (1996)","Rendezvous in Paris (Rendez-vous de Paris, Les) (1995)","Alaska (1996)","Fled (1996)","Kazaam (1996)","Bewegte Mann, Der (1994)","Magic Hunter (1994)","Larger Than Life (1996)","Boy Called Hate, A (1995)","Power 98 (1995)","Two Deaths (1995)","Very Brady Sequel, A (1996)","Stefano Quantestorie (1993)","Death in the Garden (Mort en ce jardin, La) (1956)","Crude Oasis, The (1995)","Hedd Wyn (1992)","Collectionneuse, La (1967)","Kaspar Hauser (1993)","Echte Kerle (1996)","Diebinnen (1995)","Convent, The (Convento, O) (1995)","Adventures of Pinocchio, The (1996)","Joe`s Apartment (1996)","First Wives Club, The (1996)","Stonewall (1995)","Ransom (1996)","High School High (1996)","Phat Beach (1996)","Foxfire (1996)","Chain Reaction (1996)","Matilda (1996)","Emma (1996)","Crow: City of Angels, The (1996)","House Arrest (1996)","Eyes Without a Face (1959)","Tales from the Crypt Presents: Bordello of Blood (1996)","Lotto Land (1995)","Story of Xinghua, The (1993)","Day the Sun Turned Cold, The (Tianguo niezi) (1994)","Flirt (1995)","Big Squeeze, The (1996)","Spitfire Grill, The (1996)","Escape from L.A. (1996)","Cyclo (1995)","Basquiat (1996)","Tin Cup (1996)","Dingo (1992)","Ballad of Narayama, The (Narayama Bushiko) (1958)","Every Other Weekend (1990)","Mille bolle blu (1993)","Crows and Sparrows (1949)","Godfather, The (1972)","Hippie Revolution, The (1996)","Maybe, Maybe Not (Bewegte Mann, Der) (1994)","Supercop (1992)","Manny & Lo (1996)","Celestial Clockwork (1994)","Wife, The (1995)","Small Faces (1995)","Bound (1996)","Carpool (1996)","Death in Brunswick (1991)","Kansas City (1996)","Gone Fishin` (1997)","Lover`s Knot (1996)","Aiqing wansui (1994)","Shadow of Angels (Schatten der Engel) (1976)","Killer: A Journal of Murder (1995)","Nothing to Lose (1994)","Police Story 4: Project S (Chao ji ji hua) (1993)","Girls Town (1996)","Bye-Bye (1995)","Relic, The (1997)","Island of Dr. Moreau, The (1996)","First Kid (1996)","Trigger Effect, The (1996)","Sweet Nothing (1995)","Bogus (1996)","Bulletproof (1996)","Talk of Angels (1998)","Land Before Time III: The Time of the Great Giving (1995)","1-900 (1994)","Baton Rouge (1988)","Halloween: The Curse of Michael Myers (1995)","Twelfth Night (1996)","Mother Night (1996)","Liebelei (1933)","Venice/Venice (1992)","Wild Reeds (1994)","For Whom the Bell Tolls (1943)","Philadelphia Story, The (1940)","Singin` in the Rain (1952)","American in Paris, An (1951)","Funny Face (1957)","Breakfast at Tiffany`s (1961)","Vertigo (1958)","Rear Window (1954)","It Happened One Night (1934)","Gaslight (1944)","Gay Divorcee, The (1934)","North by Northwest (1959)","Apartment, The (1960)","Some Like It Hot (1959)","Charade (1963)","Casablanca (1942)","Maltese Falcon, The (1941)","My Fair Lady (1964)","Sabrina (1954)","Roman Holiday (1953)","Little Princess, The (1939)","Meet Me in St. Louis (1944)","Wizard of Oz, The (1939)","Gone with the Wind (1939)","My Favorite Year (1982)","Sunset Blvd. (a.k.a. Sunset Boulevard) (1950)","Citizen Kane (1941)","2001: A Space Odyssey (1968)","Golden Earrings (1947)","All About Eve (1950)","Women, The (1939)","Rebecca (1940)","Foreign Correspondent (1940)","Notorious (1946)","Spellbound (1945)","Affair to Remember, An (1957)","To Catch a Thief (1955)","Father of the Bride (1950)","Band Wagon, The (1953)","Ninotchka (1939)","Love in the Afternoon (1957)","Gigi (1958)","Reluctant Debutante, The (1958)","Adventures of Robin Hood, The (1938)","Mark of Zorro, The (1940)","Laura (1944)","Ghost and Mrs. Muir, The (1947)","Lost Horizon (1937)","Top Hat (1935)","To Be or Not to Be (1942)","My Man Godfrey (1936)","Giant (1956)","East of Eden (1955)","Thin Man, The (1934)","His Girl Friday (1940)","Around the World in 80 Days (1956)","It`s a Wonderful Life (1946)","Mr. Smith Goes to Washington (1939)","Bringing Up Baby (1938)","Penny Serenade (1941)","Scarlet Letter, The (1926)","Lady of Burlesque (1943)","Of Human Bondage (1934)","Angel on My Shoulder (1946)","Little Lord Fauntleroy (1936)","They Made Me a Criminal (1939)","Inspector General, The (1949)","Angel and the Badman (1947)","39 Steps, The (1935)","Walk in the Sun, A (1945)","Outlaw, The (1943)","Night of the Living Dead (1968)","African Queen, The (1951)","Beat the Devil (1954)","Cat on a Hot Tin Roof (1958)","Last Time I Saw Paris, The (1954)","Meet John Doe (1941)","Algiers (1938)","Something to Sing About (1937)","Farewell to Arms, A (1932)","Moonlight Murder (1936)","Blue Angel, The (Blaue Engel, Der) (1930)","Nothing Personal (1995)","In the Line of Duty 2 (1987)","Dangerous Ground (1997)","Picnic (1955)","Madagascar Skin (1995)","Pompatus of Love, The (1996)","Small Wonders (1996)","Fly Away Home (1996)","Bliss (1997)","Grace of My Heart (1996)","Schlafes Bruder (Brother of Sleep) (1995)","Maximum Risk (1996)","Michael Collins (1996)","Rich Man`s Wife, The (1996)","Infinity (1996)","Big Night (1996)","Last Man Standing (1996)","Caught (1996)","Set It Off (1996)","2 Days in the Valley (1996)","Curdled (1996)","Associate, The (L`Associe)(1982)","Ed`s Next Move (1996)","Extreme Measures (1996)","Glimmer Man, The (1996)","D3: The Mighty Ducks (1996)","Chamber, The (1996)","Apple Dumpling Gang, The (1975)","Davy Crockett, King of the Wild Frontier (1955)","Escape to Witch Mountain (1975)","Love Bug, The (1969)","Herbie Rides Again (1974)","Old Yeller (1957)","Parent Trap, The (1961)","Pollyanna (1960)","Homeward Bound: The Incredible Journey (1993)","Shaggy Dog, The (1959)","Swiss Family Robinson (1960)","That Darn Cat! (1965)","20,000 Leagues Under the Sea (1954)","Cool Runnings (1993)","Angels in the Outfield (1994)","Cinderella (1950)","Winnie the Pooh and the Blustery Day (1968)","Three Caballeros, The (1945)","Sword in the Stone, The (1963)","So Dear to My Heart (1949)","Robin Hood: Prince of Thieves (1991)","Mary Poppins (1964)","Dumbo (1941)","Pete`s Dragon (1977)","Bedknobs and Broomsticks (1971)","Alice in Wonderland (1951)","Fox and the Hound, The (1981)","Freeway (1996)","Sound of Music, The (1965)","Die Hard (1988)","Lawnmower Man, The (1992)","Unhook the Stars (1996)","Synthetic Pleasures (1995)","Secret Agent, The (1996)","Secrets & Lies (1996)","That Thing You Do! (1996)","To Gillian on Her 37th Birthday (1996)","Surviving Picasso (1996)","Love Is All There Is (1996)","Beautiful Thing (1996)","Long Kiss Goodnight, The (1996)","Ghost and the Darkness, The (1996)","Looking for Richard (1996)","Trees Lounge (1996)","Proprietor, The (1996)","Normal Life (1996)","Get on the Bus (1996)","Shadow Conspiracy (1997)","Jude (1996)","Everyone Says I Love You (1996)","Bitter Sugar (Azucar Amargo) (1996)","William Shakespeare`s Romeo and Juliet (1996)","Swingers (1996)","Sleepers (1996)","Sunchaser, The (1996)","Johns (1996)","Aladdin and the King of Thieves (1996)","Woman in Question, The (1950)","Shall We Dance? (1937)","Damsel in Distress, A (1937)","Crossfire (1947)","Murder, My Sweet (1944)","Macao (1952)","For the Moment (1994)","Willy Wonka and the Chocolate Factory (1971)","Sexual Life of the Belgians, The (1994)","Innocents, The (1961)","Sleeper (1973)","Bananas (1971)","Fish Called Wanda, A (1988)","Monty Python`s Life of Brian (1979)","Victor/Victoria (1982)","Candidate, The (1972)","Great Race, The (1965)","Bonnie and Clyde (1967)","Old Man and the Sea, The (1958)","Dial M for Murder (1954)","Madame Butterfly (1995)","Dirty Dancing (1987)","Reservoir Dogs (1992)","Platoon (1986)","Weekend at Bernie`s (1989)","Basic Instinct (1992)","Doors, The (1991)","Crying Game, The (1992)","Glengarry Glen Ross (1992)","Sophie`s Choice (1982)","E.T. the Extra-Terrestrial (1982)","Search for One-eye Jimmy, The (1996)","Christmas Carol, A (1938)","Days of Thunder (1990)","Top Gun (1986)","American Strays (1996)","Rebel Without a Cause (1955)","Streetcar Named Desire, A (1951)","Children of the Corn IV: The Gathering (1996)","Leopard Son, The (1996)","Loser (1991)","Prerokbe Ognja (1995)","Charm`s Incidents (1996)","Bird of Prey (1996)","Microcosmos (Microcosmos: Le peuple de l`herbe) (1996)","Palookaville (1996)","Associate, The (1996)","Funeral, The (1996)","Sleepover (1995)","Single Girl, A (La Fille Seule) (1995)","Eighth Day, The (Le Huitième jour ) (1996)","Tashunga (1995)","Drunks (1997)","People vs. Larry Flynt, The (1996)","Glory Daze (1996)","Plutonium Circus (1995)","Perfect Candidate, A (1996)","On Golden Pond (1981)","Return of the Pink Panther, The (1974)","Drop Dead Fred (1991)","Abyss, The (1989)","Fog, The (1980)","Escape from New York (1981)","Howling, The (1980)","Jean de Florette (1986)","Manon of the Spring (Manon des sources) (1986)","Talking About Sex (1994)","Johnny 100 Pesos (1993)","Private Benjamin (1980)","Monty Python and the Holy Grail (1974)","Hustler White (1996)","Dadetown (1995)","Everything Relative (1996)","Entertaining Angels: The Dorothy Day Story (1996)","Hoogste tijd (1995)","Get Over It (1996)","Three Lives and Only One Death (1996)","Line King: Al Hirschfeld, The (1996)","Snowriders (1996)","Curtis`s Charm (1995)","When We Were Kings (1996)","Wrong Trousers, The (1993)","JLG/JLG - autoportrait de décembre (1994)","Return of Martin Guerre, The (Retour de Martin Guerre, Le) (1982)","Faust (1994)","He Walked by Night (1948)","Raw Deal (1948)","T-Men (1947)","Invitation, The (Zaproszenie) (1986)","Children Are Watching us, The (Bambini ci guardano, I) (1942)","Symphonie pastorale, La (1946)","Here Comes Cookie (1935)","Love in Bloom (1935)","Six of a Kind (1934)","Tin Drum, The (Blechtrommel, Die) (1979)","Ruling Class, The (1972)","Mina Tannenbaum (1994)","Two or Three Things I Know About Her (1966)","Bloody Child, The (1996)","Farmer & Chase (1995)","Dear God (1996)","Bad Moon (1996)","American Dream (1990)","Best of the Best 3: No Turning Back (1995)","Bob Roberts (1992)","Cinema Paradiso (1988)","Cook the Thief His Wife & Her Lover, The (1989)","Grosse Fatigue (1994)","Delicatessen (1991)","Double Life of Veronique, The (La Double Vie de Véronique) (1991)","Enchanted April (1991)","Paths of Glory (1957)","Grifters, The (1990)","Hear My Song (1991)","Shooter, The (1995)","English Patient, The (1996)","Mediterraneo (1991)","My Left Foot (1989)","Sex, Lies, and Videotape (1989)","Passion Fish (1992)","Strictly Ballroom (1992)","Thin Blue Line, The (1988)","Tie Me Up! Tie Me Down! (1990)","Madonna: Truth or Dare (1991)","Paris Is Burning (1990)","One Flew Over the Cuckoo`s Nest (1975)","Up in Smoke (1978)","Star Wars: Episode V - The Empire Strikes Back (1980)","Princess Bride, The (1987)","Raiders of the Lost Ark (1981)","Brazil (1985)","Aliens (1986)","Good, The Bad and The Ugly, The (1966)","Withnail and I (1987)","12 Angry Men (1957)","Lawrence of Arabia (1962)","Transformers: The Movie, The (1986)","Clockwork Orange, A (1971)","To Kill a Mockingbird (1962)","Apocalypse Now (1979)","Once Upon a Time in the West (1969)","Star Wars: Episode VI - Return of the Jedi (1983)","Wings of Desire (Der Himmel über Berlin) (1987)","Third Man, The (1949)","GoodFellas (1990)","Alien (1979)","Army of Darkness (1993)","Big Blue, The (Le Grand Bleu) (1988)","Ran (1985)","Killer, The (Die xue shuang xiong) (1989)","Psycho (1960)","Blues Brothers, The (1980)","Godfather: Part II, The (1974)","Full Metal Jacket (1987)","Grand Day Out, A (1992)","Henry V (1989)","Amadeus (1984)","Quiet Man, The (1952)","Once Upon a Time in America (1984)","Raging Bull (1980)","Annie Hall (1977)","Right Stuff, The (1983)","Stalker (1979)","Boat, The (Das Boot) (1981)","Sting, The (1973)","Harold and Maude (1971)","Trust (1990)","Seventh Seal, The (Sjunde inseglet, Det) (1957)","Local Hero (1983)","Terminator, The (1984)","Braindead (1992)","Glory (1989)","Rosencrantz and Guildenstern Are Dead (1990)","Manhattan (1979)","Miller`s Crossing (1990)","Dead Poets Society (1989)","Graduate, The (1967)","Touch of Evil (1958)","Nikita (La Femme Nikita) (1990)","Bridge on the River Kwai, The (1957)","8 1/2 (1963)","Chinatown (1974)","Day the Earth Stood Still, The (1951)","Treasure of the Sierra Madre, The (1948)","Bad Taste (1987)","Duck Soup (1933)","Better Off Dead... (1985)","Shining, The (1980)","Stand by Me (1986)","M (1931)","Evil Dead II (Dead By Dawn) (1987)","Great Escape, The (1963)","Deer Hunter, The (1978)","Diva (1981)","Groundhog Day (1993)","Unforgiven (1992)","Manchurian Candidate, The (1962)","Pump Up the Volume (1990)","Arsenic and Old Lace (1944)","Back to the Future (1985)","Fried Green Tomatoes (1991)","Patton (1970)","Down by Law (1986)","Akira (1988)","Highlander (1986)","Cool Hand Luke (1967)","Cyrano de Bergerac (1990)","Young Frankenstein (1974)","Night on Earth (1991)","Raise the Red Lantern (1991)","Great Dictator, The (1940)","Fantasia (1940)","High Noon (1952)","Big Sleep, The (1946)","Heathers (1989)","Somewhere in Time (1980)","Ben-Hur (1959)","This Is Spinal Tap (1984)","Koyaanisqatsi (1983)","Some Kind of Wonderful (1987)","Indiana Jones and the Last Crusade (1989)","Being There (1979)","Gandhi (1982)","M*A*S*H (1970)","Unbearable Lightness of Being, The (1988)","Room with a View, A (1986)","Real Genius (1985)","Pink Floyd - The Wall (1982)","Killing Fields, The (1984)","My Life as a Dog (Mitt liv som hund) (1985)","Forbidden Planet (1956)","Field of Dreams (1989)","Man Who Would Be King, The (1975)","Butch Cassidy and the Sundance Kid (1969)","Paris, Texas (1984)","Until the End of the World (Bis ans Ende der Welt) (1991)","When Harry Met Sally... (1989)","I Shot a Man in Vegas (1995)","Parallel Sons (1995)","Hype! (1996)","Santa with Muscles (1996)","Female Perversions (1996)","Mad Dog Time (1996)","Breathing Room (1996)","Paris Was a Woman (1995)","Anna (1996)","I`m Not Rappaport (1996)","Blue Juice (1995)","Kids of Survival (1993)","Alien³ (1992)","American Werewolf in London, An (1981)","Amityville 1992: It`s About Time (1992)","Amityville 3-D (1983)","Amityville: Dollhouse (1996)","Amityville: A New Generation (1993)","Amityville II: The Possession (1982)","Amityville Horror, The (1979)","Amityville Curse, The (1990)","Blood For Dracula (Andy Warhol`s Dracula) (1974)","April Fool`s Day (1986)","Audrey Rose (1977)","Believers, The (1987)","Birds, The (1963)","Blob, The (1958)","Blood Beach (1981)","Body Parts (1991)","Body Snatcher, The (1945)","Bram Stoker`s Dracula (1992)","Bride of Frankenstein (1935)","Burnt Offerings (1976)","Candyman (1992)","Cape Fear (1991)","Cape Fear (1962)","Carrie (1976)","Cat People (1982)","Nightmare on Elm Street, A (1984)","Nosferatu (Nosferatu, eine Symphonie des Grauens) (1922)","Nosferatu a Venezia (1986)","Omen, The (1976)","Blood & Wine (1997)","Albino Alligator (1996)","Mirror Has Two Faces, The (1996)","Breaking the Waves (1996)","Nightwatch (1997)","Star Trek: First Contact (1996)","Shine (1996)","Sling Blade (1996)","Jingle All the Way (1996)","Identification of a Woman (Identificazione di una donna) (1982)","Paradise Lost: The Child Murders at Robin Hood Hills (1996)","Garden of Finzi-Contini, The (Giardino dei Finzi-Contini, Il) (1970)","Preacher`s Wife, The (1996)","Zero Kelvin (Kjærlighetens kjøtere) (1995)","Ridicule (1996)","Crucible, The (1996)","101 Dalmatians (1996)","Forbidden Christ, The (Cristo proibito, Il) (1950)","I Can`t Sleep (J`ai pas sommeil) (1994)","Die Hard 2 (1990)","Star Trek: The Motion Picture (1979)","Star Trek VI: The Undiscovered Country (1991)","Star Trek V: The Final Frontier (1989)","Star Trek: The Wrath of Khan (1982)","Star Trek III: The Search for Spock (1984)","Star Trek IV: The Voyage Home (1986)","Batman Returns (1992)","Young Guns (1988)","Young Guns II (1990)","Grease (1978)","Grease 2 (1982)","Marked for Death (1990)","Adrenalin: Fear the Rush (1996)","Substance of Fire, The (1996)","Under Siege (1992)","Terror in a Texas Town (1958)","Jaws (1975)","Jaws 2 (1978)","Jaws 3-D (1983)","My Fellow Americans (1996)","Mars Attacks! (1996)","Citizen Ruth (1996)","Jerry Maguire (1996)","Raising Arizona (1987)","Tin Men (1987)","Sneakers (1992)","Bastard Out of Carolina (1996)","In Love and War (1996)","Marvin`s Room (1996)","Somebody is Waiting (1996)","Ghosts of Mississippi (1996)","Night Falls on Manhattan (1997)","Beavis and Butt-head Do America (1996)","Cérémonie, La (1995)","Scream (1996)","Last of the Mohicans, The (1992)","Michael (1996)","Evening Star, The (1996)","Hamlet (1996)","Some Mother`s Son (1996)","Whole Wide World, The (1996)","Mother (1996)","Thieves (Voleurs, Les) (1996)","Evita (1996)","Portrait of a Lady, The (1996)","Walkabout (1971)","Message to Love: The Isle of Wight Festival (1996)","Grateful Dead (1995)","Murder at 1600 (1997)","Hearts and Minds (1996)","Inside (1996)","Fierce Creatures (1997)","Zeus and Roxanne (1997)","Turbulence (1997)","Angel Baby (1995)","Jackie Chan`s First Strike (1996)","Underworld (1997)","Beverly Hills Ninja (1997)","Metro (1997)","Machine, The (1994)","Stranger, The (1994)","Falling in Love Again (1980)","Cement Garden, The (1993)","Dante`s Peak (1997)","Meet Wally Sparks (1997)","Amos & Andrew (1993)","Benny & Joon (1993)","Prefontaine (1997)","Tickle in the Heart, A (1996)","Guantanamera (1994)","McHale`s Navy (1997)","Kolya (1996)","Gridlock`d (1997)","Fire on the Mountain (1996)","Waiting for Guffman (1996)","Prisoner of the Mountains (Kavkazsky Plennik) (1996)","Beautician and the Beast, The (1997)","SubUrbia (1997)","Hotel de Love (1996)","Pest, The (1997)","Fools Rush In (1997)","Touch (1997)","Absolute Power (1997)","That Darn Cat! (1997)","Vegas Vacation (1997)","Unforgotten: Twenty-Five Years After Willowbrook (1996)","That Old Feeling (1997)","Lost Highway (1997)","Rosewood (1997)","Donnie Brasco (1997)","Salut cousin! (1996)","Booty Call (1997)","Rhyme & Reason (1997)","Boys Life 2 (1997)","City of Industry (1997)","Best Men (1997)","Jungle2Jungle (a.k.a. Jungle 2 Jungle) (1997)","Kama Sutra: A Tale of Love (1996)","Private Parts (1997)","Love Jones (1997)","Saint, The (1997)","Smilla`s Sense of Snow (1997)","Van, The (1996)","Crash (1996)","Daytrippers, The (1996)","Liar Liar (1997)","Quiet Room, The (1996)","Selena (1997)","Devil`s Own, The (1997)","Cats Don`t Dance (1997)","B*A*P*S (1997)","Love and Other Catastrophes (1996)","Sixth Man, The (1997)","Turbo: A Power Rangers Movie (1997)","Anna Karenina (1997)","Double Team (1997)","Inventing the Abbotts (1997)","Anaconda (1997)","Grosse Pointe Blank (1997)","Keys to Tulsa (1997)","Kissed (1996)","8 Heads in a Duffel Bag (1997)","Hollow Reed (1996)","Paradise Road (1997)","Traveller (1997)","All Over Me (1997)","Brother`s Kiss, A (1997)","A Chef in Love (1996)","Romy and Michele`s High School Reunion (1997)","Temptress Moon (Feng Yue) (1996)","Volcano (1997)","Children of the Revolution (1996)","Austin Powers: International Man of Mystery (1997)","Breakdown (1997)","Broken English (1996)","Commandments (1997)","Ripe (1996)","Truth or Consequences, N.M. (1997)","Turning, The (1992)","Warriors of Virtue (1997)","Fathers` Day (1997)","Fifth Element, The (1997)","Intimate Relations (1996)","Nowhere (1997)","Losing Chase (1996)","Sprung (1997)","Promise, The (La Promesse) (1996)","Bonheur, Le (1965)","Love! Valour! Compassion! (1997)","Shall We Dance? (Shall We Dansu?) (1996)","Second Jungle Book: Mowgli & Baloo, The (1997)","Twin Town (1997)","Addicted to Love (1997)","Brassed Off (1996)","Designated Mourner, The (1997)","Lost World: Jurassic Park, The (1997)","Ponette (1996)","Schizopolis (1996)","Shiloh (1997)","War at Home, The (1996)","Rough Magic (1995)","Trial and Error (1997)","Buddy (1997)","Con Air (1997)","Late Bloomers (1996)","Pillow Book, The (1995)","To Have, or Not (1995)","Speed 2: Cruise Control (1997)","Squeeze (1996)","Sudden Manhattan (1996)","Next Step, The (1995)","Wedding Bell Blues (1996)","Batman & Robin (1997)","Dream With the Fishes (1997)","Roseanna`s Grave (For Roseanna) (1997)","Head Above Water (1996)","Hercules (1997)","Last Time I Committed Suicide, The (1997)","MURDER and murder (1996)","My Best Friend`s Wedding (1997)","Tetsuo II: Body Hammer (1992)","When the Cats Away (Chacun cherche son chat) (1996)","Contempt (Le Mépris) (1963)","Face/Off (1997)","Fall (1997)","Gabbeh (1996)","Mondo (1996)","Innocent Sleep, The (1995)","For Ever Mozart (1996)","Men in Black (1997)","Out to Sea (1997)","Wild America (1997)","Simple Wish, A (1997)","Contact (1997)","Love Serenade (1996)","G.I. Jane (1997)","Conan the Barbarian (1982)","George of the Jungle (1997)","Cop Land (1997)","Event Horizon (1997)","Spawn (1997)","Air Bud (1997)","Picture Perfect (1997)","In the Company of Men (1997)","Free Willy 3: The Rescue (1997)","Career Girls (1997)","Conspiracy Theory (1997)","Desperate Measures (1998)","Steel (1997)","She`s So Lovely (1997)","Hoodlum (1997)","Leave It to Beaver (1997)","Mimic (1997)","Money Talks (1997)","Excess Baggage (1997)","Kull the Conqueror (1997)","Air Force One (1997)","187 (1997)","Hunt for Red October, The (1990)","My Own Private Idaho (1991)","Kiss Me, Guido (1997)","Star Maps (1997)","In & Out (1997)","Edge, The (1997)","Peacemaker, The (1997)","L.A. Confidential (1997)","Seven Years in Tibet (1997)","Kiss the Girls (1997)","Soul Food (1997)","Kicked in the Head (1997)","Wishmaster (1997)","Thousand Acres, A (1997)","Game, The (1997)","Fire Down Below (1997)","U Turn (1997)","Locusts, The (1997)","MatchMaker, The (1997)","Lay of the Land, The (1997)","Assignment, The (1997)","Smile Like Yours, A (1997)","Ulee`s Gold (1997)","Ice Storm, The (1997)","Stag (1997)","Chasing Amy (1997)","How to Be a Player (1997)","Full Monty, The (1997)","Indian Summer (a.k.a. Alive & Kicking) (1996)","Mrs. Brown (Her Majesty, Mrs. Brown) (1997)","I Know What You Did Last Summer (1997)","Devil`s Advocate, The (1997)","Rocket Man (1997)","Playing God (1997)","House of Yes, The (1997)","Fast, Cheap & Out of Control (1997)","Washington Square (1997)","Telling Lies in America (1997)","Year of the Horse (1997)","Gattaca (1997)","FairyTale: A True Story (1997)","Phantoms (1998)","Swept from the Sea (1997)","Wonderland (1997)","Life Less Ordinary, A (1997)","Hurricane Streets (1998)","Eve`s Bayou (1997)","Switchback (1997)","Gang Related (1997)","Stripes (1981)","Nénette et Boni (1996)","Bean (1997)","Hugo Pool (1997)","Mad City (1997)","One Night Stand (1997)","Tango Lesson, The (1997)","Welcome To Sarajevo (1997)","Deceiver (1997)","Rainmaker, The (1997)","Boogie Nights (1997)","Witness (1985)","Incognito (1997)","Starship Troopers (1997)","Critical Care (1997)","Joy Luck Club, The (1993)","Chairman of the Board (1998)","Sliding Doors (1998)","Mortal Kombat: Annihilation (1997)","Truman Show, The (1998)","Wings of the Dove, The (1997)","Mrs. Dalloway (1997)","I Love You, I Love You Not (1996)","Red Corner (1997)","Jackal, The (1997)","Anastasia (1997)","Man Who Knew Too Little, The (1997)","Alien: Resurrection (1997)","Alien Escape (1995)","Amistad (1997)","Apostle, The (1997)","Artemisia (1997)","Bent (1997)","Big Bang Theory, The (1994)","Boys, Les (1997)","Butcher Boy, The (1998)","Deconstructing Harry (1997)","Flubber (1997)","For Richer or Poorer (1997)","Good Will Hunting (1997)","Guy (1996)","Harlem River Drive (1996)","Home Alone 3 (1997)","Ill Gotten Gains (1997)","Legal Deceit (1997)","Man of Her Dreams (1996)","Midnight in the Garden of Good and Evil (1997)","Mouse Hunt (1997)","Never Met Picasso (1996)","Office Killer (1997)","Other Voices, Other Rooms (1997)","Scream 2 (1997)","Stranger in the House (1997)","Sweet Hereafter, The (1997)","Time Tracers (1995)","Titanic (1997)","Tomorrow Never Dies (1997)","Twisted (1996)","Full Speed (1996)","Education of Little Tree, The (1997)","Postman, The (1997)","Horse Whisperer, The (1998)","Winter Guest, The (1997)","Jackie Brown (1997)","Kundun (1997)","Mr. Magoo (1997)","Big Lebowski, The (1998)","Afterglow (1997)","My Life in Pink (Ma vie en rose) (1997)","Great Expectations (1998)","Vermin (1998)","3 Ninjas: High Noon On Mega Mountain (1998)","Men of Means (1998)","Midaq Alley (Callejón de los milagros, El) (1995)","Caught Up (1998)","Arguing the World (1996)","Firestorm (1998)","Senseless (1998)","Wag the Dog (1997)","Dark City (1998)","Leading Man, The (1996)","Star Kid (1997)","Hard Rain (1998)","Half Baked (1998)","Fallen (1998)","Shooting Fish (1997)","Prophecy II, The (1998)","Duoluo tianshi (1995)","Dangerous Beauty (1998)","Four Days in September (1997)","Spice World (1997)","Deep Rising (1998)","Tainted (1998)","Letter From Death Row, A (1998)","Music From Another Room (1998)","Mat` i syn (1997)","Replacement Killers, The (1998)","B. Monkey (1998)","Night Flier (1997)","Blues Brothers 2000 (1998)","Tokyo Fist (1995)","Mass Transit (1998)","Ride (1998)","Wedding Singer, The (1998)","Sphere (1998)","Ayn Rand: A Sense of Life (1997)","Further Gesture, A (1996)","Little City (1998)","Palmetto (1998)","As Good As It Gets (1997)","King of New York (1990)","Paralyzing Fear: The Story of Polio in America, A (1998)","Men With Guns (1997)","Sadness of Sex, The (1995)","Twilight (1998)","U.S. Marshalls (1998)","Welcome to Woop-Woop (1997)","Love and Death on Long Island (1997)","Callejón de los milagros, El (1995)","In God`s Hands (1998)","Everest (1998)","Hush (1998)","Suicide Kings (1997)","Man in the Iron Mask, The (1998)","Newton Boys, The (1998)","Wild Things (1998)","Paulie (1998)","Cool Dry Place, A (1998)","Hana-bi (1997)","Primary Colors (1998)","Niagara, Niagara (1997)","Wide Awake (1998)","Price Above Rubies, A (1998)","Eden (1997)","Two Girls and a Guy (1997)","No Looking Back (1998)","Storefront Hitchcock (1997)","Proposition, The (1998)","Object of My Affection, The (1998)","Meet the Deedles (1998)","Homegrown (1998)","Player`s Club, The (1998)","Barney`s Great Adventure (1998)","Big One, The (1997)","Chinese Box (1997)","Follow the Bitch (1998)","Lost in Space (1998)","Heaven`s Burning (1997)","Mercury Rising (1998)","Spanish Prisoner, The (1997)","City of Angels (1998)","Last Days of Disco, The (1998)","Odd Couple II, The (1998)","My Giant (1998)","He Got Game (1998)","Gingerbread Man, The (1998)","Illtown (1996)","Slappy and the Stinkers (1998)","Live Flesh (1997)","Zero Effect (1998)","Nil By Mouth (1997)","Ratchet (1996)","Borrowers, The (1997)","Prince Valiant (1997)","I Love You, Don`t Touch Me! (1998)","Leather Jacket Love Story (1997)","Love Walked In (1998)","Alan Smithee Film: Burn Hollywood Burn, An (1997)","Kissing a Fool (1998)","Krippendorf`s Tribe (1998)","Kurt & Courtney (1998)","Real Blonde, The (1997)","Mr. Nice Guy (1997)","Taste of Cherry (1997)","Character (Karakter) (1997)","Junk Mail (1997)","Species II (1998)","Major League: Back to the Minors (1998)","Sour Grapes (1998)","Wild Man Blues (1998)","Big Hit, The (1998)","Tarzan and the Lost City (1998)","Truce, The (1996)","Black Dog (1998)","Dancer, Texas Pop. 81 (1998)","Friend of the Deceased, A (1997)","Go Now (1995)","Misérables, Les (1998)","Still Breathing (1997)","Clockwatchers (1997)","Deep Impact (1998)","Little Men (1998)","Woo (1998)","Hanging Garden, The (1997)","Lawn Dogs (1997)","Quest for Camelot (1998)","Godzilla (1998)","Bulworth (1998)","Fear and Loathing in Las Vegas (1998)","Opposite of Sex, The (1998)","I Got the Hook Up (1998)","Almost Heroes (1998)","Hope Floats (1998)","Insomnia (1997)","Little Boy Blue (1997)","Ugly, The (1997)","Perfect Murder, A (1998)","Beyond Silence (1996)","Six Days Seven Nights (1998)","Can`t Hardly Wait (1998)","Cousin Bette (1998)","High Art (1998)","Land Girls, The (1998)","Passion in the Desert (1998)","Children of Heaven, The (Bacheha-Ye Aseman) (1997)","Dear Jesse (1997)","Dream for an Insomniac (1996)","Hav Plenty (1997)","Henry Fool (1997)","Marie Baie Des Anges (1997)","Mr. Jealousy (1997)","Mulan (1998)","Resurrection Man (1998)","X-Files: Fight the Future, The (1998)","I Went Down (1997)","Doctor Dolittle (1998)","Out of Sight (1998)","Picnic at Hanging Rock (1975)","Smoke Signals (1998)","Voyage to the Beginning of the World (1997)","Buffalo 66 (1998)","Armageddon (1998)","Lethal Weapon 4 (1998)","Madeline (1998)","Small Soldiers (1998)","Pi (1998)","Whatever (1998)","There`s Something About Mary (1998)","Plan 9 from Outer Space (1958)","Wings (1927)","Broadway Melody, The (1929)","All Quiet on the Western Front (1930)","Cimarron (1931)","Grand Hotel (1932)","Cavalcade (1933)","Mutiny on the Bounty (1935)","Great Ziegfeld, The (1936)","Life of Émile Zola, The (1937)","You Can`t Take It With You (1938)","How Green Was My Valley (1941)","Mrs. Miniver (1942)","Going My Way (1944)","Lost Weekend, The (1945)","Best Years of Our Lives, The (1946)","Gentleman`s Agreement (1947)","Hamlet (1948)","All the King`s Men (1949)","Greatest Show on Earth, The (1952)","From Here to Eternity (1953)","On the Waterfront (1954)","Marty (1955)","West Side Story (1961)","Tom Jones (1963)","Man for All Seasons, A (1966)","In the Heat of the Night (1967)","Oliver! (1968)","Midnight Cowboy (1969)","French Connection, The (1971)","Rocky (1976)","Kramer Vs. Kramer (1979)","Ordinary People (1980)","Chariots of Fire (1981)","Terms of Endearment (1983)","Out of Africa (1985)","Last Emperor, The (1987)","Rain Man (1988)","Driving Miss Daisy (1989)","Take the Money and Run (1969)","Klute (1971)","Repo Man (1984)","Metropolitan (1990)","Labyrinth (1986)","Breakfast Club, The (1985)","Nightmare on Elm Street Part 2: Freddy`s Revenge, A (1985)","Nightmare on Elm Street 3: Dream Warriors, A (1987)","Nightmare on Elm Street 4: The Dream Master, A (1988)","Nightmare on Elm Street 5: The Dream Child, A (1989)","Freddy`s Dead: The Final Nightmare (1991)","Friday the 13th (1980)","Friday the 13th Part 2 (1981)","Friday the 13th Part 3: 3D (1982)","Friday the 13th: The Final Chapter (1984)","Friday the 13th Part V: A New Beginning (1985)","Friday the 13th Part VI: Jason Lives (1986)","Friday the 13th Part VII: The New Blood (1988)","Friday the 13th Part VIII: Jason Takes Manhattan (1989)","Halloween (1978)","Halloween II (1981)","Halloween III: Season of the Witch (1983)","Halloween 4: The Return of Michael Myers (1988)","Halloween 5: The Revenge of Michael Myers (1989)","Prom Night (1980)","Hello Mary Lou: Prom Night II (1987)","Prom Night III: The Last Kiss (1989)","Prom Night IV: Deliver Us From Evil (1992)","Child`s Play (1988)","Child`s Play 2 (1990)","Child`s Play 3 (1992)","Poltergeist (1982)","Poltergeist II: The Other Side (1986)","Poltergeist III (1988)","Exorcist, The (1973)","Exorcist II: The Heretic (1977)","Exorcist III, The (1990)","Lethal Weapon (1987)","Lethal Weapon 2 (1989)","Lethal Weapon 3 (1992)","Gremlins (1984)","Gremlins 2: The New Batch (1990)","Goonies, The (1985)","Mask of Zorro, The (1998)","Polish Wedding (1998)","This World, Then the Fireworks (1996)","Soylent Green (1973)","Metropolis (1926)","Back to the Future Part II (1989)","Back to the Future Part III (1990)","Poseidon Adventure, The (1972)","Freaky Friday (1977)","Absent Minded Professor, The (1961)","Apple Dumpling Gang Rides Again, The (1979)","Babes in Toyland (1961)","Bambi (1942)","Seven Samurai (The Magnificent Seven) (Shichinin no samurai) (1954)","Dangerous Liaisons (1988)","Dune (1984)","Last Temptation of Christ, The (1988)","Godfather: Part III, The (1990)","Rapture, The (1991)","Lolita (1997)","Disturbing Behavior (1998)","Mafia! (1998)","Saving Private Ryan (1998)","Billy`s Hollywood Screen Kiss (1997)","East Palace West Palace (Dong gong xi gong) (1997)","$1,000,000 Duck (1971)","Barefoot Executive, The (1971)","Black Cauldron, The (1985)","Black Hole, The (1979)","Blackbeard`s Ghost (1968)","Blank Check (1994)","Candleshoe (1977)","Cat from Outer Space, The (1978)","Cheetah (1989)","Computer Wore Tennis Shoes, The (1970)","Condorman (1981)","D2: The Mighty Ducks (1994)","Darby O`Gill and the Little People (1959)","Devil and Max Devlin, The (1981)","Far Off Place, A (1993)","Flight of the Navigator (1986)","Gnome-Mobile, The (1967)","Great Mouse Detective, The (1986)","Happiest Millionaire, The (1967)","Herbie Goes Bananas (1980)","Herbie Goes to Monte Carlo (1977)","Hocus Pocus (1993)","Honey, I Blew Up the Kid (1992)","Honey, I Shrunk the Kids (1989)","Hot Lead and Cold Feet (1978)","In Search of the Castaways (1962)","Incredible Journey, The (1963)","Negotiator, The (1998)","Parent Trap, The (1998)","BASEketball (1998)","Full Tilt Boogie (1997)","Governess, The (1998)","Seventh Heaven (Le Septième ciel) (1997)","Roger & Me (1989)","Purple Rose of Cairo, The (1985)","Out of the Past (1947)","Doctor Zhivago (1965)","Fanny and Alexander (1982)","Trip to Bountiful, The (1985)","Tender Mercies (1983)","And the Band Played On (1993)","`burbs, The (1989)","Fandango (1985)","Night Porter, The (Il Portiere di notte) (1974)","Mephisto (1981)","Blue Velvet (1986)","Journey of Natty Gann, The (1985)","Jungle Book, The (1967)","Kidnapped (1960)","Lady and the Tramp (1955)","Little Mermaid, The (1989)","Mighty Ducks, The (1992)","Muppet Christmas Carol, The (1992)","Newsies (1992)","101 Dalmatians (1961)","One Magic Christmas (1985)","Peter Pan (1953)","Popeye (1980)","Rescuers Down Under, The (1990)","Rescuers, The (1977)","Return from Witch Mountain (1978)","Return of Jafar, The (1993)","Return to Oz (1985)","Rocketeer, The (1991)","Shaggy D.A., The (1976)","Sleeping Beauty (1959)","Something Wicked This Way Comes (1983)","Son of Flubber (1963)","Song of the South (1946)","Splash (1984)","Squanto: A Warrior`s Tale (1994)","Steamboat Willie (1940)","Tall Tale (1994)","Tex (1982)","Tron (1982)","Swing Kids (1993)","Halloween: H20 (1998)","L.A. Story (1991)","Jerk, The (1979)","Dead Men Don`t Wear Plaid (1982)","Man with Two Brains, The (1983)","Grand Canyon (1991)","Graveyard Shift (1990)","Outsiders, The (1983)","Indiana Jones and the Temple of Doom (1984)","Lord of the Rings, The (1978)","Nineteen Eighty-Four (1984)","Dead Zone, The (1983)","Maximum Overdrive (1986)","Needful Things (1993)","Cujo (1983)","Children of the Corn (1984)","All Dogs Go to Heaven (1989)","Addams Family, The (1991)","Ever After: A Cinderella Story (1998)","Snake Eyes (1998)","First Love, Last Rites (1997)","Safe Men (1998)","Saltmen of Tibet, The (1997)","Atlantic City (1980)","Autumn Sonata (Höstsonaten ) (1978)","Who`s Afraid of Virginia Woolf? (1966)","Adventures in Babysitting (1987)","Weird Science (1985)","Doctor Dolittle (1967)","Nutty Professor, The (1963)","Charlotte`s Web (1973)","Watership Down (1978)","Secret of NIMH, The (1982)","Dark Crystal, The (1982)","American Tail, An (1986)","American Tail: Fievel Goes West, An (1991)","Legend (1985)","Sixteen Candles (1984)","Pretty in Pink (1986)","St. Elmo`s Fire (1985)","Clan of the Cave Bear, The (1986)","House (1986)","House II: The Second Story (1987)","Gods Must Be Crazy, The (1980)","Gods Must Be Crazy II, The (1989)","Air Bud: Golden Receiver (1998)","Avengers, The (1998)","How Stella Got Her Groove Back (1998)","Slums of Beverly Hills, The (1998)","Best Man, The (Il Testimone dello sposo) (1997)","Chambermaid on the Titanic, The (1998)","Henry: Portrait of a Serial Killer, Part 2 (1996)","Henry: Portrait of a Serial Killer (1990)","Rosemary`s Baby (1968)","NeverEnding Story, The (1984)","NeverEnding Story II: The Next Chapter, The (1990)","Attack of the Killer Tomatoes! (1980)","Surf Nazis Must Die (1987)","Your Friends and Neighbors (1998)","Return to Paradise (1998)","Blade (1998)","Dance with Me (1998)","Dead Man on Campus (1998)","Wrongfully Accused (1998)","Next Stop, Wonderland (1998)","Strike! (a.k.a. All I Wanna Do, The Hairy Bird) (1998)","Navigator: A Mediaeval Odyssey, The (1988)","Beetlejuice (1988)","Déjà Vu (1997)","Rope (1948)","Family Plot (1976)","Frenzy (1972)","Topaz (1969)","Torn Curtain (1966)","Marnie (1964)","Wrong Man, The (1956)","Man Who Knew Too Much, The (1956)","Trouble with Harry, The (1955)","I Confess (1953)","Strangers on a Train (1951)","Stage Fright (1950)","54 (1998)","I Married A Strange Person (1997)","Why Do Fools Fall In Love? (1998)","Merry War, A (1997)","See the Sea (Regarde la mer) (1997)","Willow (1988)","Untouchables, The (1987)","Dirty Work (1998)","Knock Off (1998)","Firelight (1997)","Modulations (1998)","Phoenix (1998)","Under Capricorn (1949)","Paradine Case, The (1947)","Lifeboat (1944)","Shadow of a Doubt (1943)","Saboteur (1942)","Mr. & Mrs. Smith (1941)","Suspicion (1941)","Jamaica Inn (1939)","Lady Vanishes, The (1938)","Young and Innocent (1937)","Sabotage (1936)","Secret Agent (1936)","Man Who Knew Too Much, The (1934)","Waltzes from Vienna (1933)","Number Seventeen (1932)","Rich and Strange (1932)","Skin Game, The (1931)","Elstree Calling (1930)","Juno and Paycock (1930)","Murder! (1930)","Manxman, The (1929)","Blackmail (1929)","Champagne (1928)","Farmer`s Wife, The (1928)","Downhill (1927)","Easy Virtue (1927)","Ring, The (1927)","Lodger, The (1926)","Mountain Eagle, The (1926)","Pleasure Garden, The (1925)","Always Tell Your Wife (1923)","Rounders (1998)","Cube (1997)","Digging to China (1998)","Let`s Talk About Sex (1998)","One Man`s Hero (1999)","Simon Birch (1998)","Without Limits (1998)","Seven Beauties (Pasqualino Settebellezze) (1976)","Swept Away (Travolti da un insolito destino nell`azzurro mare d`Agosto) (1975)","My Bodyguard (1980)","Class (1983)","Grandview, U.S.A. (1984)","Broadcast News (1987)","Allnighter, The (1987)","Working Girl (1988)","Stars and Bars (1988)","Married to the Mob (1988)","Say Anything... (1989)","My Blue Heaven (1990)","Men Don`t Leave (1990)","Cabinet of Dr. Ramirez, The (1991)","Hero (1992)","Toys (1992)","Choices (1981)","Young Doctors in Love (1982)","Parasite (1982)","No Small Affair (1984)","Master Ninja I (1984)","Blame It on Rio (1984)","Wisdom (1986)","One Crazy Summer (1986)","About Last Night... (1986)","Seventh Sign, The (1988)","We`re No Angels (1989)","Nothing But Trouble (1991)","Butcher`s Wife, The (1991)","Mortal Thoughts (1991)","Few Good Men, A (1992)","Indecent Proposal (1993)","Century of Cinema, A (1994)","Permanent Midnight (1998)","One True Thing (1998)","Rush Hour (1998)","Lilian`s Story (1995)","Six-String Samurai (1998)","Soldier`s Daughter Never Cries, A (1998)","Somewhere in the City (1997)","Ronin (1998)","Urban Legend (1998)","Clay Pigeons (1998)","Monument Ave. (1998)","Pecker (1998)","Sheltering Sky, The (1990)","Bandit Queen (1994)","If.... (1968)","Fiendish Plot of Dr. Fu Manchu, The (1980)","Them! (1954)","Thing, The (1982)","Player, The (1992)","Stardust Memories (1980)","Edward Scissorhands (1990)","Overnight Delivery (1996)","Shadrach (1998)","Antz (1998)","Impostors, The (1998)","Night at the Roxbury, A (1998)","What Dreams May Come (1998)","Strangeland (1998)","Battle of the Sexes, The (1959)","Producers, The (1968)","History of the World: Part I (1981)","My Cousin Vinny (1992)","Nashville (1975)","Love Is the Devil (1998)","Slam (1998)","Holy Man (1998)","One Tough Cop (1998)","Detroit 9000 (1973)","Inheritors, The (Die Siebtelbauern) (1998)","Mighty, The (1998)","2010 (1984)","Children of a Lesser God (1986)","Elephant Man, The (1980)","Beloved (1998)","Bride of Chucky (1998)","Practical Magic (1998)","Alarmist, The (1997)","Happiness (1998)","Reach the Rock (1997)","Apt Pupil (1998)","Pleasantville (1998)","Soldier (1998)","Cruise, The (1998)","Life Is Beautiful (La Vita è bella) (1997)","Orgazmo (1997)","Shattered Image (1998)","Tales from the Darkside: The Movie (1990)","Vampires (1998)","American History X (1998)","Hands on a Hard Body (1996)","Living Out Loud (1998)","Belly (1998)","Gods and Monsters (1998)","Siege, The (1998)","Waterboy, The (1998)","Elizabeth (1998)","Velvet Goldmine (1998)","I Still Know What You Did Last Summer (1998)","I`ll Be Home For Christmas (1998)","Meet Joe Black (1998)","Dancing at Lughnasa (1998)","Hard Core Logo (1996)","Naked Man, The (1998)","Runaway Train (1985)","Desert Bloom (1986)","Stepford Wives, The (1975)","Pope of Greenwich Village, The (1984)","Sid and Nancy (1986)","Mona Lisa (1986)","Heart Condition (1990)","Nights of Cabiria (Le Notti di Cabiria) (1957)","Big Chill, The (1983)","Enemy of the State (1998)","Rugrats Movie, The (1998)","Bug`s Life, A (1998)","Celebrity (1998)","Central Station (Central do Brasil) (1998)","Savior (1998)","Waking Ned Devine (1998)","Celebration, The (Festen) (1998)","Pink Flamingos (1972)","Glen or Glenda (1953)","Godzilla (Gojira) (1954)","Godzilla (Gojira) (1984)","King Kong vs. Godzilla (Kingukongu tai Gojira) (1962)","King Kong (1933)","King Kong (1976)","King Kong Lives (1986)","Desperately Seeking Susan (1985)","Emerald Forest, The (1985)","Fletch (1985)","Fletch Lives (1989)","Red Sonja (1985)","Gung Ho (1986)","Money Pit, The (1986)","View to a Kill, A (1985)","Lifeforce (1985)","Police Academy (1984)","Police Academy 2: Their First Assignment (1985)","Police Academy 3: Back in Training (1986)","Police Academy 4: Citizens on Patrol (1987)","Police Academy 5: Assignment: Miami Beach (1988)","Police Academy 6: City Under Siege (1989)","Babe: Pig in the City (1998)","Home Fries (1998)","Jerry Springer: Ringmaster (1998)","Very Bad Things (1998)","Steam: The Turkish Bath (Hamam) (1997)","Psycho (1998)","Little Voice (1998)","Simple Plan, A (1998)","Jack Frost (1998)","Star Trek: Insurrection (1998)","Prince of Egypt, The (1998)","Rushmore (1998)","Shakespeare in Love (1998)","Mass Appeal (1984)","Miracle on 34th Street (1947)","Santa Claus: The Movie (1985)","Prancer (1989)","Pale Rider (1985)","Rambo: First Blood Part II (1985)","First Blood (1982)","Rambo III (1988)","Jewel of the Nile, The (1985)","Romancing the Stone (1984)","Cocoon (1985)","Cocoon: The Return (1988)","Rocky II (1979)","Rocky III (1982)","Rocky IV (1985)","Rocky V (1990)","Clue (1985)","Young Sherlock Holmes (1985)","Violets Are Blue... (1986)","Back to School (1986)","Heartburn (1986)","Nothing in Common (1986)","Extremities (1986)","Karate Kid, The (1984)","Karate Kid, Part II, The (1986)","Karate Kid III, The (1989)","Christmas Vacation (1989)","You`ve Got Mail (1998)","General, The (1998)","Theory of Flight, The (1998)","Thin Red Line, The (1998)","Faculty, The (1998)","Mighty Joe Young (1998)","Mighty Joe Young (1949)","Patch Adams (1998)","Stepmom (1998)","Civil Action, A (1998)","Down in the Delta (1998)","Hurlyburly (1998)","Tea with Mussolini (1999)","Wilde (1997)","Outside Ozona (1998)","Affliction (1997)","Another Day in Paradise (1998)","Hi-Lo Country, The (1998)","Hilary and Jackie (1998)","Playing by Heart (1998)","24 7: Twenty Four Seven (1997)","At First Sight (1999)","In Dreams (1999)","Varsity Blues (1999)","Virus (1999)","Garbage Pail Kids Movie, The (1987)","Howard the Duck (1986)","Gate, The (1987)","Gate II: Trespassers, The (1990)","Boy Who Could Fly, The (1986)","Fly, The (1958)","Fly, The (1986)","Fly II, The (1989)","Running Scared (1986)","Armed and Dangerous (1986)","Texas Chainsaw Massacre, The (1974)","Texas Chainsaw Massacre 2, The (1986)","Leatherface: Texas Chainsaw Massacre III (1990)","Return of the Texas Chainsaw Massacre, The (1994)","Ruthless People (1986)","Trick or Treat (1986)","Deadly Friend (1986)","Belizaire the Cajun (1986)","Name of the Rose, The (1986)","Jumpin` Jack Flash (1986)","Peggy Sue Got Married (1986)","Crocodile Dundee (1986)","Crocodile Dundee II (1988)","Tough Guys (1986)","Soul Man (1986)","Color of Money, The (1986)","52 Pick-Up (1986)","Heartbreak Ridge (1986)","Firewalker (1986)","Three Amigos! (1986)","Gloria (1999)","Dry Cleaning (Nettoyage à sec) (1997)","My Name Is Joe (1998)","Still Crazy (1998)","Day of the Beast, The (El Día de la bestia) (1995)","Tinseltown (1998)","She`s All That (1999)","24-hour Woman (1998)","Blood, Guts, Bullets and Octane (1998)","Peeping Tom (1960)","Spanish Fly (1998)","Payback (1999)","Simply Irresistible (1999)","20 Dates (1998)","Harmonists, The (1997)","Last Days, The (1998)","Fantastic Planet, The (La Planète sauvage) (1973)","Blast from the Past (1999)","Message in a Bottle (1999)","My Favorite Martian (1999)","God Said `Ha!` (1998)","Jawbreaker (1999)","October Sky (1999)","Office Space (1999)","Apple, The (Sib) (1998)","200 Cigarettes (1999)","8MM (1999)","Other Sister, The (1999)","Breakfast of Champions (1999)","Breaks, The (1999)","Eight Days a Week (1997)","Just the Ticket (1999)","Long Goodbye, The (1973)","Ballad of Narayama, The (Narayama Bushiko) (1982)","Pet Sematary (1989)","Pet Sematary II (1992)","Children of the Corn II: The Final Sacrifice (1993)","Children of the Corn III (1994)","Christine (1983)","Night Shift (1982)","House on Haunted Hill (1958)","Airport (1970)","Airport 1975 (1974)","Airport `77 (1977)","Rollercoaster (1977)","Towering Inferno, The (1974)","Alligator (1980)","Meteor (1979)","Westworld (1973)","Logan`s Run (1976)","Planet of the Apes (1968)","Beneath the Planet of the Apes (1970)","Battle for the Planet of the Apes (1973)","Conquest of the Planet of the Apes (1972)","Escape from the Planet of the Apes (1971)","Avalanche (1978)","Earthquake (1974)","Concorde: Airport `79, The (1979)","Beyond the Poseidon Adventure (1979)","Dancemaker (1998)","Analyze This (1999)","Corruptor, The (1999)","Cruel Intentions (1999)","Lock, Stock & Two Smoking Barrels (1998)","Six Ways to Sunday (1997)","School of Flesh, The (L` École de la chair) (1998)","Relax... It`s Just Sex (1998)","Deep End of the Ocean, The (1999)","Harvest (1998)","Rage: Carrie 2, The (1999)","Wing Commander (1999)","Haunting, The (1963)","Dead Ringers (1988)","My Boyfriend`s Back (1993)","Village of the Damned (1960)","Children of the Damned (1963)","Baby Geniuses (1999)","Telling You (1998)","I Stand Alone (Seul contre tous) (1998)","Forces of Nature (1999)","King and I, The (1999)","Ravenous (1999)","True Crime (1999)","Bandits (1997)","Beauty (1998)","Empty Mirror, The (1999)","King and I, The (1956)","Doug`s 1st Movie (1999)","EDtv (1999)","Mod Squad, The (1999)","Among Giants (1998)","Walk on the Moon, A (1999)","Matrix, The (1999)","10 Things I Hate About You (1999)","Tango (1998)","Out-of-Towners, The (1999)","Dreamlife of Angels, The (La Vie rêvée des anges) (1998)","Love, etc. (1996)","Metroland (1997)","Sticky Fingers of Time, The (1997)","Following (1998)","Go (1999)","Never Been Kissed (1999)","Twin Dragons (Shuang long hui) (1992)","Cookie`s Fortune (1999)","Foolish (1999)","Lovers of the Arctic Circle, The (Los Amantes del Círculo Polar) (1998)","Goodbye, Lover (1999)","Life (1999)","Clubland (1998)","Friends & Lovers (1999)","Hideous Kinky (1998)","Jeanne and the Perfect Guy (Jeanne et le garçon formidable) (1998)","Joyriders, The (1999)","Monster, The (Il Mostro) (1994)","Open Your Eyes (Abre los ojos) (1997)","Photographer (Fotoamator) (1998)","SLC Punk! (1998)","Lost & Found (1999)","Pushing Tin (1999)","Election (1999)","eXistenZ (1999)","Little Bit of Soul, A (1998)","Mighty Peking Man (Hsing hsing wang) (1977)","Nô (1998)","Let it Come Down: The Life of Paul Bowles (1998)","Entrapment (1999)","Idle Hands (1999)","Get Real (1998)","Heaven (1998)","King of Masks, The (Bian Lian) (1996)","Three Seasons (1999)","Winslow Boy, The (1998)","Mildred Pierce (1945)","Night of the Comet (1984)","Chopping Mall (a.k.a. Killbots) (1986)","My Science Project (1985)","Dick Tracy (1990)","Mummy, The (1999)","Castle, The (1997)","Mascara (1999)","This Is My Father (1998)","Xiu Xiu: The Sent-Down Girl (Tian yu) (1998)","Midsummer Night`s Dream, A (1999)","Trippin` (1999)","After Life (1998)","Black Mask (Hak hap) (1996)","Edge of Seventeen (1998)","Endurance (1998)","Star Wars: Episode I - The Phantom Menace (1999)","Love Letter, The (1999)","Besieged (L` Assedio) (1998)","Frogs for Snakes (1998)","Saragossa Manuscript, The (Rekopis znaleziony w Saragossie) (1965)","Mummy, The (1932)","Mummy, The (1959)","Mummy`s Curse, The (1944)","Mummy`s Ghost, The (1944)","Mummy`s Hand, The (1940)","Mummy`s Tomb, The (1942)","Mommie Dearest (1981)","Superman (1978)","Superman II (1980)","Superman III (1983)","Superman IV: The Quest for Peace (1987)","Dracula (1931)","Dracula (1958)","House of Dracula (1945)","House of Frankenstein (1944)","Frankenstein (1931)","Son of Frankenstein (1939)","Ghost of Frankenstein, The (1942)","Frankenstein Meets the Wolf Man (1943)","Curse of Frankenstein, The (1957)","Son of Dracula (1943)","Wolf Man, The (1941)","Howling II: Your Sister Is a Werewolf (1985)","Tarantula (1955)","Rocky Horror Picture Show, The (1975)","Flying Saucer, The (1950)","It Came from Hollywood (1982)","Thing From Another World, The (1951)","It Came from Outer Space (1953)","War of the Worlds, The (1953)","It Came from Beneath the Sea (1955)","Invasion of the Body Snatchers (1956)","Earth Vs. the Flying Saucers (1956)","It Conquered the World (1956)","Mole People, The (1956)","Swamp Thing (1982)","Pork Chop Hill (1959)","Run Silent, Run Deep (1958)","Notting Hill (1999)","Thirteenth Floor, The (1999)","Eternity and a Day (Mia eoniotita ke mia mera ) (1998)","Loss of Sexual Innocence, The (1999)","Twice Upon a Yesterday (1998)","Instinct (1999)","Buena Vista Social Club (1999)","Desert Blue (1999)","Finding North (1999)","Floating (1997)","Free Enterprise (1998)","Limbo (1999)","Austin Powers: The Spy Who Shagged Me (1999)","Taxman (1999)","Red Dwarf, The (Le Nain rouge) (1998)","Red Violin, The (Le Violon rouge) (1998)","Tarzan (1999)","General`s Daughter, The (1999)","Get Bruce (1999)","Ideal Husband, An (1999)","Legend of 1900, The (Leggenda del pianista sull`oceano) (1998)","Run Lola Run (Lola rennt) (1998)","Trekkies (1997)","Big Daddy (1999)","Boys, The (1997)","Dinner Game, The (Le Dîner de cons) (1998)","My Son the Fanatic (1998)","Zone 39 (1997)","Arachnophobia (1990)","South Park: Bigger, Longer and Uncut (1999)","Wild Wild West (1999)","Summer of Sam (1999)","Broken Vessels (1998)","Lovers on the Bridge, The (Les Amants du Pont-Neuf) (1991)","Late August, Early September (Fin août, début septembre) (1998)","American Pie (1999)","Arlington Road (1999)","Autumn Tale, An (Conte d`automne) (1998)","Muppets From Space (1999)","Blair Witch Project, The (1999)","My Life So Far (1999)","Eyes Wide Shut (1999)","Lake Placid (1999)","Wood, The (1999)","Velocity of Gary, The (1998)","Ghostbusters (1984)","Ghostbusters II (1989)","Drop Dead Gorgeous (1999)","Haunting, The (1999)","Inspector Gadget (1999)","Trick (1999)","Deep Blue Sea (1999)","Mystery Men (1999)","Runaway Bride (1999)","Twin Falls Idaho (1999)","Killing, The (1956)","Killer`s Kiss (1955)","Spartacus (1960)","Lolita (1962)","Barry Lyndon (1975)","400 Blows, The (Les Quatre cents coups) (1959)","Jules and Jim (Jules et Jim) (1961)","Vibes (1988)","Mosquito Coast, The (1986)","Golden Child, The (1986)","Brighton Beach Memoirs (1986)","Assassination (1987)","Crimes of the Heart (1986)","Color Purple, The (1985)","Kindred, The (1986)","No Mercy (1986)","Ménage (Tenue de soirée) (1986)","Native Son (1986)","Otello (1986)","Mission, The (1986)","Little Shop of Horrors (1986)","Little Shop of Horrors, The (1960)","Allan Quartermain and the Lost City of Gold (1987)","Morning After, The (1986)","Radio Days (1987)","From the Hip (1987)","Outrageous Fortune (1987)","Bedroom Window, The (1987)","Deadtime Stories (1987)","Light of Day (1987)","Wanted: Dead or Alive (1987)","Frances (1982)","Plenty (1985)","Dick (1999)","Gambler, The (A Játékos) (1997)","Iron Giant, The (1999)","Sixth Sense, The (1999)","Thomas Crown Affair, The (1999)","Thomas Crown Affair, The (1968)","Acid House, The (1998)","Adventures of Sebastian Cole, The (1998)","Illuminata (1998)","Stiff Upper Lips (1998)","Yards, The (1999)","Bowfinger (1999)","Brokedown Palace (1999)","Detroit Rock City (1999)","Alice and Martin (Alice et Martin) (1998)","Better Than Chocolate (1999)","Head On (1998)","Marcello Mastroianni: I Remember Yes, I Remember (1997)","Cobra (1925)","Never Talk to Strangers (1995)","Heaven Can Wait (1978)","Raven, The (1963)","Tingler, The (1959)","Pit and the Pendulum (1961)","Tomb of Ligeia, The (1965)","Masque of the Red Death, The (1964)","Tales of Terror (1962)","Haunted Honeymoon (1986)","Cat`s Eye (1985)","And Now for Something Completely Different (1971)","Damien: Omen II (1978)","Final Conflict, The (a.k.a. Omen III: The Final Conflict) (1981)","Airplane! (1980)","Airplane II: The Sequel (1982)","American Werewolf in Paris, An (1997)","European Vacation (1985)","Vacation (1983)","Funny Farm (1988)","Big (1988)","Problem Child (1990)","Problem Child 2 (1991)","Little Nemo: Adventures in Slumberland (1992)","Oscar and Lucinda (a.k.a. Oscar & Lucinda) (1997)","Tequila Sunrise (1988)","Pelican Brief, The (1993)","Christmas Story, A (1983)","Mickey Blue Eyes (1999)","Teaching Mrs. Tingle (1999)","Universal Soldier: The Return (1999)","Universal Soldier (1992)","Love Stinks (1999)","Perfect Blue (1997)","With Friends Like These... (1998)","In Too Deep (1999)","Source, The (1999)","Bat, The (1959)","Iron Eagle (1986)","Iron Eagle II (1988)","Aces: Iron Eagle III (1992)","Iron Eagle IV (1995)","Three Days of the Condor (1975)","Hamlet (1964)","Male and Female (1919)","Medicine Man (1992)","Spiders, The (Die Spinnen, 1. Teil: Der Goldene See) (1919)","On the Ropes (1999)","Rosie (1998)","13th Warrior, The (1999)","Astronaut`s Wife, The (1999)","Dudley Do-Right (1999)","Muse, The (1999)","Cabaret Balkan (Bure Baruta) (1998)","Dog of Flanders, A (1999)","Lost Son, The (1999)","Lucie Aubrac (1997)","Very Thought of You, The (1998)","Chill Factor (1999)","Outside Providence (1999)","Bedrooms & Hallways (1998)","I Woke Up Early the Day I Died (1998)","West Beirut (West Beyrouth) (1998)","Stigmata (1999)","Stir of Echoes (1999)","Best Laid Plans (1999)","Black Cat, White Cat (Crna macka, beli macor) (1998)","Minus Man, The (1999)","White Boys (1999)","Adventures of Milo and Otis, The (1986)","Only Angels Have Wings (1939)","Othello (1952)","Queens Logic (1991)","Public Access (1993)","Saturn 3 (1979)","Soldier`s Story, A (1984)","Communion (a.k.a. Alice, Sweet Alice/Holy Terror) (1977)","Don`t Look in the Basement! (1973)","Nightmares (1983)","I Saw What You Did (1965)","Yellow Submarine (1968)","American Beauty (1999)","Stop Making Sense (1984)","Blue Streak (1999)","For Love of the Game (1999)","Caligula (1980)","Hard Day`s Night, A (1964)","Splendor (1999)","Sugar Town (1999)","Buddy Holly Story, The (1978)","Fright Night (1985)","Fright Night Part II (1989)","Separation, The (La Séparation) (1994)","Barefoot in the Park (1967)","Deliverance (1972)","Excalibur (1981)","Lulu on the Bridge (1998)","Pajama Game, The (1957)","Sommersby (1993)","Thumbelina (1994)","Tommy (1975)","Hell Night (1981)","Operation Condor (Feiying gaiwak) (1990)","Operation Condor 2 (Longxiong hudi) (1990)","Double Jeopardy (1999)","Jakob the Liar (1999)","Mumford (1999)","Dog Park (1998)","Guinevere (1999)","Adventures of Elmo in Grouchland, The (1999)","Simon Sez (1999)","Drive Me Crazy (1999)","Mystery, Alaska (1999)","Three Kings (1999)","Happy, Texas (1999)","New Rose Hotel (1998)","Plunkett & MaCleane (1999)","Romance (1999)","Napoleon and Samantha (1972)","Alvarez Kelly (1966)","And the Ship Sails On (E la nave va) (1984)","Dark Half, The (1993)","Gulliver`s Travels (1939)","Monkey Shines (1988)","Phantasm (1979)","Psycho II (1983)","Psycho III (1986)","Rain (1932)","Sanjuro (1962)","Random Hearts (1999)","Superstar (1999)","Boys Don`t Cry (1999)","Five Wives, Three Secretaries and Me (1998)","Ennui, L` (1998)","Grandfather, The (El Abuelo) (1998)","Limey, The (1999)","Mating Habits of the Earthbound Human, The (1998)","Molly (1999)","Risky Business (1983)","Total Recall (1990)","Body Heat (1981)","Ferris Bueller`s Day Off (1986)","Year of Living Dangerously (1982)","Children of Paradise (Les enfants du paradis) (1945)","High Plains Drifter (1972)","Hang `em High (1967)","Citizen`s Band (a.k.a. Handle with Care) (1977)","Drunken Master (Zui quan) (1979)","Conformist, The (Il Conformista) (1970)","Hairspray (1988)","Brief Encounter (1946)","Razor`s Edge, The (1984)","Reds (1981)","Return with Honor (1998)","Time of the Gypsies (Dom za vesanje) (1989)","Days of Heaven (1978)","Fire Within, The (Le Feu Follet) (1963)","Love Bewitched, A (El Amor Brujo) (1986)","Lady Eve, The (1941)","Sullivan`s Travels (1942)","Palm Beach Story, The (1942)","Man Facing Southeast (Hombre Mirando al Sudeste) (1986)","Niagara (1953)","Gilda (1946)","South Pacific (1958)","Flashdance (1983)","Indochine (1992)","Dirty Dozen, The (1967)","Mike`s Murder (1984)","Help! (1965)","Goldfinger (1964)","From Russia with Love (1963)","Dr. No (1962)","Blue Lagoon, The (1980)","Fistful of Dollars, A (1964)","Hard 8 (a.k.a. Sydney, a.k.a. Hard Eight) (1996)","Home Alone 2: Lost in New York (1992)","Penitentiary (1979)","Penitentiary II (1982)","Someone to Watch Over Me (1987)","Sparrows (1926)","Naturally Native (1998)","Fight Club (1999)","Beefcake (1999)","Story of Us, The (1999)","Fever Pitch (1997)","Joe the King (1999)","Julien Donkey-Boy (1999)","Omega Code, The (1999)","Straight Story, The (1999)","Bad Seed, The (1956)","Time Bandits (1981)","Man and a Woman, A (Un Homme et une Femme) (1966)","Fitzcarraldo (1982)","All That Jazz (1979)","Red Sorghum (Hong Gao Liang) (1987)","Crimes and Misdemeanors (1989)","Bats (1999)","Best Man, The (1999)","Bringing Out the Dead (1999)","Crazy in Alabama (1999)","Three to Tango (1999)","Body Shots (1999)","Men Cry Bullets (1997)","Brother, Can You Spare a Dime? (1975)","Guardian, The (1990)","Ipcress File, The (1965)","On Any Sunday (1971)","Robocop (1987)","Robocop 2 (1990)","Who Framed Roger Rabbit? (1988)","Melvin and Howard (1980)","For Your Eyes Only (1981)","Licence to Kill (1989)","Live and Let Die (1973)","Rawhead Rex (1986)","Thunderball (1965)","City, The (1998)","House on Haunted Hill, The (1999)","Music of the Heart (1999)","Being John Malkovich (1999)","Dreaming of Joseph Lees (1998)","Man of the Century (1999)","Princess Mononoke, The (Mononoke Hime) (1997)","Suburbans, The (1999)","My Best Fiend (Mein liebster Feind) (1999)","Train of Life (Train De Vie) (1998)","Bachelor, The (1999)","Bone Collector, The (1999)","Insider, The (1999)","American Movie (1999)","Last Night (1998)","Portraits Chinois (1996)","Rosetta (1999)","They Shoot Horses, Don`t They? (1969)","Battling Butler (1926)","Bride of Re-Animator (1990)","Bustin` Loose (1981)","Coma (1978)","Creepshow (1982)","Creepshow 2 (1987)","Re-Animator (1985)","Drugstore Cowboy (1989)","Falling Down (1993)","Funhouse, The (1981)","General, The (1927)","My Best Girl (1927)","Piranha (1978)","Rough Night in Jericho (1967)","Slaughterhouse (1987)","Slaughterhouse 2 (1988)","Taming of the Shrew, The (1967)","Nighthawks (1981)","Yojimbo (1961)","Repossessed (1990)","Omega Man, The (1971)","Spaceballs (1987)","Robin Hood (1973)","Mister Roberts (1955)","Quest for Fire (1981)","Little Big Man (1970)","Face in the Crowd, A (1957)","Trading Places (1983)","Meatballs (1979)","Meatballs Part II (1984)","Meatballs III (1987)","Meatballs 4 (1992)","Dead Again (1991)","Peter`s Friends (1992)","Incredibly True Adventure of Two Girls in Love, The (1995)","Experience Preferred... But Not Essential (1982)","Under the Rainbow (1981)","How I Won the War (1967)","Light It Up (1999)","Anywhere But Here (1999)","Dogma (1999)","Messenger: The Story of Joan of Arc, The (1999)","Pokémon: The First Movie (1998)","Felicia`s Journey (1999)","Oxygen (1999)","Where`s Marlowe? (1999)","Ape, The (1940)","British Intelligence (1940)","Commitments, The (1991)","Holiday Inn (1942)","Longest Day, The (1962)","Poison Ivy (1992)","Poison Ivy: New Seduction (1997)","Ten Benny (1997)","Tora! Tora! Tora! (1970)","Women on the Verge of a Nervous Breakdown (1988)","Verdict, The (1982)","Effect of Gamma Rays on Man-in-the-Moon Marigolds, The (1972)","Adventures of Buckaroo Bonzai Across the 8th Dimension, The (1984)","Stand and Deliver (1987)","Moonstruck (1987)","Sandpiper, The (1965)","Jeremiah Johnson (1972)","Repulsion (1965)","Irma la Douce (1963)","42 Up (1998)","Liberty Heights (1999)","Mansfield Park (1999)","Goodbye, 20th Century (Zbogum na dvadesetiot vek) (1998)","Sleepy Hollow (1999)","World Is Not Enough, The (1999)","All About My Mother (Todo Sobre Mi Madre) (1999)","Home Page (1999)","Living Dead Girl, The (La Morte Vivante) (1982)","March of the Wooden Soldiers (a.k.a. Laurel & Hardy in Toyland) (1934)","Scrooged (1988)","Harvey (1950)","Bicycle Thief, The (Ladri di biciclette) (1948)","Matewan (1987)","Kagemusha (1980)","Chushingura (1962)","McCabe & Mrs. Miller (1971)","Maurice (1987)","Grapes of Wrath, The (1940)","My Man Godfrey (1957)","Shop Around the Corner, The (1940)","Natural, The (1984)","Shampoo (1975)","River Runs Through It, A (1992)","Fatal Attraction (1987)","Jagged Edge (1985)","Stanley & Iris (1990)","Midnight Run (1988)","Awakenings (1990)","Come See the Paradise (1990)","Backdraft (1991)","Fisher King, The (1991)","River, The (1984)","Country (1984)","Places in the Heart (1984)","`Night Mother (1986)","End of Days (1999)","Toy Story 2 (1999)","Flawless (1999)","Miss Julie (1999)","Ride with the Devil (1999)","Tumbleweeds (1999)","Bay of Blood (Reazione a catena) (1971)","Distinguished Gentleman, The (1992)","Hitch-Hiker, The (1953)","Santa Fe Trail (1940)","Spring Fever USA (a.k.a. Lauderdale) (1989)","Agnes Browne (1999)","End of the Affair, The (1999)","End of the Affair, The (1955)","Holy Smoke (1999)","Map of the World, A (1999)","Sweet and Lowdown (1999)","Bonfire of the Vanities (1990)","Broadway Damage (1997)","Daddy Long Legs (1919)","Go West (1925)","Grand Illusion (Grande illusion, La) (1937)","Great Santini, The (1979)","James Dean Story, The (1957)","Sea Wolves, The (1980)","Stealing Home (1988)","Tarzan the Fearless (1933)","Three Ages, The (1923)","Two Jakes, The (1990)","U2: Rattle and Hum (1988)","Hell in the Pacific (1968)","Glass Bottom Boat, The (1966)","Cradle Will Rock, The (1999)","Deuce Bigalow: Male Gigolo (1999)","Green Mile, The (1999)","Cider House Rules, The (1999)","Diamonds (1999)","War Zone, The (1999)","Bat Whispers, The (1930)","Last Picture Show, The (1971)","7th Voyage of Sinbad, The (1958)","Blood on the Sun (1945)","Anna and the King (1999)","Bicentennial Man (1999)","Stuart Little (1999)","Emperor and the Assassin, The (Jing ke ci qin wang) (1999)","Fantasia 2000 (1999)","Magnolia (1999)","Onegin (1999)","Simpatico (1999)","Topsy-Turvy (1999)","Alley Cats, The (1968)","Boiling Point (1993)","Brenda Starr (1989)","Carnal Knowledge (1971)","Easy Rider (1969)","Falcon and the Snowman, The (1984)","Hi-Yo Silver (1940)","Room at the Top (1959)","Ulysses (Ulisse) (1954)","Any Given Sunday (1999)","Man on the Moon (1999)","Galaxy Quest (1999)","Talented Mr. Ripley, The (1999)","Next Friday (1999)","Hurricane, The (1999)","Angela`s Ashes (1999)","Play it to the Bone (1999)","Titus (1999)","Mr. Death: The Rise and Fall of Fred A. Leuchter Jr. (1999)","Third Miracle, The (1999)","Montana (1998)","Snow Falling on Cedars (1999)","Girl, Interrupted (1999)","Trans (1998)","Life and Times of Hank Greenberg, The (1998)","My Dog Skip (1999)","Supernova (2000)","Quarry, The (1998)","Terrorist, The (Malli) (1998)","Creature (1999)","Way We Were, The (1973)","Tess of the Storm Country (1922)","Stalag 17 (1953)","Presidio, The (1988)","Papillon (1973)","Pal Joey (1957)","Last Detail, The (1973)","Five Easy Pieces (1970)","Even Dwarfs Started Small (Auch Zwerge haben klein angefangen) (1971)","Dead Calm (1989)","Boys from Brazil, The (1978)","Black Sunday (La Maschera Del Demonio) (1960)","Against All Odds (1984)","Snows of Kilimanjaro, The (1952)","Loaded Weapon 1 (1993)","Loves of Carmen, The (1948)","Fast Times at Ridgemont High (1982)","Cry in the Dark, A (1988)","Born to Win (1971)","Batman: Mask of the Phantasm (1993)","American Flyers (1985)","Voyage of the Damned (1976)","Vampyros Lesbos (Las Vampiras) (1970)","Star Is Born, A (1937)","Poison (1991)","Pacific Heights (1990)","Night Tide (1961)","Draughtsman`s Contract, The (1982)","Carmen (1984)","Zed & Two Noughts, A (1985)","Woman in the Dunes (Suna no onna) (1964)","Down to You (2000)","Hellhounds on My Trail (1999)","Not Love, Just Frenzy (Más que amor, frenesí) (1996)","Wirey Spindell (1999)","Another Man`s Poison (1952)","Odessa File, The (1974)","Saphead, The (1920)","Seven Chances (1925)","Smashing Time (1967)","Train Ride to Hollywood (1978)","Where the Buffalo Roam (1980)","Zachariah (1971)","Kestrel`s Eye (Falkens öga) (1998)","Eye of the Beholder (1999)","Isn`t She Great? (2000)","Big Tease, The (1999)","Cup, The (Phörpa) (1999)","Santitos (1997)","Encino Man (1992)","Goodbye Girl, The (1977)","I Am Cuba (Soy Cuba/Ya Kuba) (1964)","Malcolm X (1992)","Sister Act (1992)","Sister Act 2: Back in the Habit (1993)","Hand That Rocks the Cradle, The (1992)","Alive (1993)","Agnes of God (1985)","Scent of a Woman (1992)","Wayne`s World (1992)","Wayne`s World 2 (1993)","League of Their Own, A (1992)","Patriot Games (1992)","Bodyguard, The (1992)","Death Becomes Her (1992)","Far and Away (1992)","Howards End (1992)","Singles (1992)","Twin Peaks: Fire Walk with Me (1992)","White Men Can`t Jump (1992)","Buffy the Vampire Slayer (1992)","Hard-Boiled (Lashou shentan) (1992)","Man Bites Dog (C`est arrivé près de chez vous) (1992)","Mariachi, El (1992)","Stop! Or My Mom Will Shoot (1992)","Forever Young (1992)","Cutting Edge, The (1992)","Of Mice and Men (1992)","Bad Lieutenant (1992)","Scream 3 (2000)","Single White Female (1992)","Boondock Saints, The (1999)","Gun Shy (2000)","Beloved/Friend (Amigo/Amado) (1999)","Gendernauts (1999)","Knockout (1999)","Baby, The (1973)","Brandon Teena Story, The (1998)","Different for Girls (1996)","Minnie and Moskowitz (1971)","They Might Be Giants (1971)","Beach, The (2000)","Snow Day (2000)","Tigger Movie, The (2000)","Cotton Mary (1999)","Not One Less (Yi ge dou bu neng shao) (1999)","Soft Toilet Seats (1999)","Trois (2000)","Big Combo, The (1955)","Conceiving Ada (1997)","Eaten Alive (1976)","Raining Stones (1993)","To Sir with Love (1967)","With Byrd at the South Pole (1930)","Boiler Room (2000)","Hanging Up (2000)","Pitch Black (2000)","Whole Nine Yards, The (2000)","Beautiful People (1999)","Black Tar Heroin: The Dark End of the Street (1999)","Blue Collar (1978)","Bluebeard (1944)","Circus, The (1928)","City Lights (1931)","Flamingo Kid, The (1984)","Dog`s Life, A (1920)","Kid, The (1921)","Man from Laramie, The (1955)","McCullochs, The (1975)","Class Reunion (1982)","Big Trees, The (1952)","Happy Go Lovely (1951)","Reindeer Games (2000)","Wonder Boys (2000)","Deterrence (1998)","Judy Berlin (1999)","Mifune (Mifunes sidste sang) (1999)","Waiting Game, The (2000)","3 Strikes (2000)","Chain of Fools (2000)","Drowning Mona (2000)","Next Best Thing, The (2000)","What Planet Are You From? (2000)","Beyond the Mat (2000)","Ghost Dog: The Way of the Samurai (1999)","Year My Voice Broke, The (1987)","Splendor in the Grass (1961)","My Tutor (1983)","Legend of Lobo, The (1962)","Killing of Sister George, The (1968)","Key Largo (1948)","Jail Bait (1954)","It Happened Here (1961)","I`ll Never Forget What`s `is Name (1967)","For All Mankind (1989)","Cross of Iron (1977)","Bride of the Monster (1956)","Born Yesterday (1950)","Birdy (1984)","And God Created Woman (1988)","Blood Feast (1963)","Charlie, the Lonesome Cougar (1967)","Color Me Blood Red (1965)","Never Cry Wolf (1983)","Night Visitor, The (1970)","Perils of Pauline, The (1947)","Raisin in the Sun, A (1961)","Two Thousand Maniacs! (1964)","Brown`s Requiem (1998)","Closer You Get, The (2000)","Mission to Mars (2000)","Ninth Gate, The (2000)","Condo Painting (2000)","East-West (Est-ouest) (1999)","Defending Your Life (1991)","Breaking Away (1979)","Hoosiers (1986)","Bull Durham (1988)","Dog Day Afternoon (1975)","American Graffiti (1973)","Asphalt Jungle, The (1950)","Searchers, The (1956)","Where Eagles Dare (1969)","Devil`s Brigade, The (1968)","Big Country, The (1958)","Any Number Can Win (Mélodie en sous-sol ) (1963)","Betrayed (1988)","Bound for Glory (1976)","Bridge at Remagen, The (1969)","Buck and the Preacher (1972)","Daughters of the Dust (1992)","Destination Moon (1950)","Fantastic Night, The (La Nuit Fantastique) (1949)","Hangmen Also Die (1943)","Ogre, The (Der Unhold) (1996)","On the Beach (1959)","Railroaded! (1947)","Slaves to the Underground (1997)","Song of Freedom (1936)","Big Fella (1937)","Taking of Pelham One Two Three, The (1974)","Volunteers (1985)","JFK (1991)","Who`s Harry Crumb? (1989)","Harry and the Hendersons (1987)","Let`s Get Harry (1986)","Shanghai Surprise (1986)","Who`s That Girl? (1987)","She-Devil (1989)","Date with an Angel (1987)","Blind Date (1987)","Nadine (1987)","Muppet Movie, The (1979)","Great Muppet Caper, The (1981)","Muppets Take Manhattan, The (1984)","Sesame Street Presents Follow That Bird (1985)","We`re Back! A Dinosaur`s Story (1993)","Baby... Secret of the Lost Legend (1985)","Turtle Diary (1985)","Raise the Titanic (1980)","Titanic (1953)","Night to Remember, A (1958)","Captain Horatio Hornblower (1951)","Carriers Are Waiting, The (Les Convoyeurs Attendent) (1999)","Erin Brockovich (2000)","Final Destination (2000)","Soft Fruit (1999)","Babymother (1998)","Bear, The (1988)","Impact (1949)","Love Is a Many-Splendored Thing (1955)","Mirror, The (Zerkalo) (1975)","Trial, The (Le Procès) (1963)","Crimson Pirate, The (1952)","Thelma & Louise (1991)","Something for Everyone (1970)","...And Justice for All (1979)","Animal House (1978)","She`s Gotta Have It (1986)","School Daze (1988)","Do the Right Thing (1989)","Mo` Better Blues (1990)","Jungle Fever (1991)","Coogan`s Bluff (1968)","Champ, The (1979)","Creature Comforts (1990)","Death Wish (1974)","Death Wish II (1982)","Death Wish 3 (1985)","Death Wish 4: The Crackdown (1987)","Death Wish V: The Face of Death (1994)","Double Indemnity (1944)","Dying Young (1991)","Cool as Ice (1991)","Teenage Mutant Ninja Turtles (1990)","Teenage Mutant Ninja Turtles II: The Secret of the Ooze (1991)","Teenage Mutant Ninja Turtles III (1993)","Red Dawn (1984)","Band of the Hand (1986)","Born American (1986)","Bloodsport (1988)","Eyes of Laura Mars (1978)","Funny Bones (1995)","Good Earth, The (1937)","Good Morning, Vietnam (1987)","Good Mother, The (1988)","Grumpy Old Men (1993)","Guess Who`s Coming to Dinner (1967)","Romeo Must Die (2000)","Here on Earth (2000)","Whatever It Takes (2000)","Buddy Boy (1999)","Color of Paradise, The (Rang-e Khoda) (1999)","Waking the Dead (1999)","Blood and Sand (Sangre y Arena) (1989)","Gothic (1986)","Hillbillys in a Haunted House (1967)","Lord of the Flies (1963)","Modern Times (1936)","Last Resort (1994)","Solar Crisis (1993)","That`s Life! (1986)","Heart and Souls (1993)","Hud (1963)","Hustler, The (1961)","Inherit the Wind (1960)","Dersu Uzala (1974)","Close Encounters of the Third Kind (1977)","Horror Hotel (a.k.a. The City of the Dead) (1960)","Jonah Who Will Be 25 in the Year 2000 (1976)","Retroactive (1997)","Place in the Sun, A (1951)","Jacob`s Ladder (1990)","Empire Records (1995)","Bamba, La (1987)","Ladyhawke (1985)","Lucas (1986)","High Fidelity (2000)","Price of Glory (2000)","Road to El Dorado, The (2000)","Skulls, The (2000)","Autopsy (Macchie Solari) (1975)","Devil Girl From Mars (1954)","Dorado, El (1967)","Hideous Sun Demon, The (1959)","Hook (1991)","Horror Express (1972)","My Chauffeur (1986)","Son of the Sheik, The (1926)","Torso (Corpi Presentano Tracce di Violenza Carnale) (1973)","True Grit (1969)","Roadside Prophets (1992)","Madame Sousatzka (1988)","Max Dugan Returns (1983)","Midnight Express (1978)","Misery (1990)","Mr. Saturday Night (1992)","Murphy`s Romance (1985)","My Life (1993)","Solaris (Solyaris) (1972)","Network (1976)","No Way Out (1987)","North Dallas Forty (1979)","Odd Couple, The (1968)","Outlaw Josey Wales, The (1976)","Black and White (1999)","Frequency (2000)","Ready to Rumble (2000)","Return to Me (2000)","Rules of Engagement (2000)","Joe Gould`s Secret (2000)","Me Myself I (2000)","Bell, Book and Candle (1958)","Bells, The (1926)","End of Violence, The (1997)","Force 10 from Navarone (1978)","How to Stuff a Wild Bikini (1965)","Mystery Train (1989)","Sacco and Vanzetti (Sacco e Vanzetti) (1971)","Taffin (1988)","Arthur (1981)","Bachelor Party (1984)","Parenthood (1989)","Predator (1987)","Prince of Tides, The (1991)","Postman Always Rings Twice, The (1981)","Smoking/No Smoking (1993)","All the Vermeers in New York (1990)","Freedom for Us (À nous la liberté ) (1931)","Actor`s Revenge, An (Yukinojo Henge) (1963)","28 Days (2000)","American Psycho (2000)","Keeping the Faith (2000)","Where the Money Is (2000)","East is East (1999)","Filth and the Fury, The (2000)","Passion of Mind (1999)","Third World Cop (1999)","Coming Apart (1969)","Diner (1982)","Shakes the Clown (1991)","Cabaret (1972)","What Ever Happened to Baby Jane? (1962)","Prick Up Your Ears (1987)","Auntie Mame (1958)","Guys and Dolls (1955)","Hunger, The (1983)","Marathon Man (1976)","Caddyshack (1980)","Gossip (2000)","Love and Basketball (2000)","U-571 (2000)","Virgin Suicides, The (1999)","Jennifer 8 (1992)","Law, The (Le Legge) (1958)","Limelight (1952)","Phantom Love (Ai No Borei) (1978)","Stacy`s Knights (1982)","Committed (2000)","Crow: Salvation, The (2000)","Flintstones in Viva Rock Vegas, The (2000)","Where the Heart Is (2000)","Big Kahuna, The (2000)","Bossa Nova (1999)","Smiling Fish and Goat on Fire (1999)","Idiots, The (Idioterne) (1998)","Last September, The (1999)","Time Code (2000)","Carnosaur (1993)","Carnosaur 2 (1995)","Carnosaur 3: Primal Species (1996)","Defying Gravity (1997)","Hidden, The (1987)","Two Moon Juction (1988)","Gladiator (2000)","I Dreamed of Africa (2000)","Up at the Villa (2000)","Human Traffic (1999)","Jails, Hospitals & Hip-Hop (2000)","Black Tights (Les Collants Noirs) (1960)","Breathless (1983)","Great Locomotive Chase, The (1956)","Idolmaker, The (1980)","Inferno (1980)","King of Marvin Gardens, The (1972)","Kill, Baby... Kill! (Operazione Paura) (1966)","Lords of Flatbush, The (1974)","Mr. Mom (1983)","Time Masters (Les Maîtres du Temps) (1982)","Battlefield Earth (2000)","Center Stage (2000)","Held Up (2000)","Screwed (2000)","Whipped (2000)","Hamlet (2000)","Anchors Aweigh (1945)","Blue Hawaii (1961)","Castaway Cowboy, The (1974)","G. I. Blues (1960)","Gay Deceivers, The (1969)","Gypsy (1962)","King Creole (1958)","On the Town (1949)","One Little Indian (1973)","Pee-wee`s Big Adventure (1985)","Regret to Inform (1998)","Roustabout (1964)","Saludos Amigos (1943)","Slipper and the Rose, The (1976)","Things Change (1988)","Honeymoon in Vegas (1992)","Dinosaur (2000)","Loser (2000)","Road Trip (2000)","Small Time Crooks (2000)","Hollywood Knights, The (1980)","Myth of Fingerprints, The (1997)","Possession (1981)","Twelve Chairs, The (1970)","Mission: Impossible 2 (2000)","Shanghai Noon (2000)","Better Living Through Circuitry (1999)","8 1/2 Women (1999)","Carnival of Souls (1962)","Flying Tigers (1942)","Gold Rush, The (1925)","House of Exorcism, The (La Casa dell`esorcismo) (1974)","It`s in the Water (1998)","Monsieur Verdoux (1947)","On Her Majesty`s Secret Service (1969)","Seven Days in May (1964)","Spy Who Loved Me, The (1977)","Those Who Love Me Can Take the Train (Ceux qui m`aiment prendront le train) (1998)","Vagabond (Sans toit ni loi) (1985)","Moonraker (1979)","Man with the Golden Gun, The (1974)","King in New York, A (1957)","Woman of Paris, A (1923)","In Old California (1942)","Fighting Seabees, The (1944)","Dark Command (1940)","Cleo From 5 to 7 (Cléo de 5 à 7) (1962)","Big Momma`s House (2000)","Running Free (2000)","Abominable Snowman, The (1957)","American Gigolo (1980)","Anguish (Angustia) (1986)","Blood Spattered Bride, The (La Novia Ensangrentada) (1972)","City of the Living Dead (Paura nella città dei morti viventi) (1980)","Endless Summer, The (1966)","Guns of Navarone, The (1961)","Blow-Out (La Grande Bouffe) (1973)","Lured (1947)","Pandora and the Flying Dutchman (1951)","Quatermass and the Pit (1967)","Quatermass II (1957)","Puppet Master (1989)","Puppet Master II (1990)","Puppet Master III: Toulon`s Revenge (1991)","Puppet Master 4 (1993)","Puppet Master 5: The Final Chapter (1994)","Curse of the Puppet Master (1998)","Retro Puppetmaster (1999)","Rent-A-Cop (1988)","Romeo and Juliet (1968)","Stay Tuned (1992)","Story of G.I. Joe, The (1945)","Blazing Saddles (1974)","Benji (1974)","Benji the Hunted (1987)","For the Love of Benji (1977)","White Christmas (1954)","Eraserhead (1977)","Baraka (1992)","Man with the Golden Arm, The (1955)","Decline of Western Civilization, The (1981)","Decline of Western Civilization Part II: The Metal Years, The (1988)","For a Few Dollars More (1965)","Magnum Force (1973)","Blood Simple (1984)","Fabulous Baker Boys, The (1989)","Prizzi`s Honor (1985)","Flatliners (1990)","Light Years (1988)","Porky`s (1981)","Porky`s II: The Next Day (1983)","Porky`s Revenge (1985)","Private School (1983)","Class of Nuke `Em High (1986)","Toxic Avenger, The (1985)","Toxic Avenger, Part II, The (1989)","Toxic Avenger Part III: The Last Temptation of Toxie, The (1989)","Night of the Creeps (1986)","Predator 2 (1990)","Running Man, The (1987)","Starman (1984)","Brother from Another Planet, The (1984)","Alien Nation (1988)","Mad Max (1979)","Mad Max 2 (a.k.a. The Road Warrior) (1981)","Mad Max Beyond Thunderdome (1985)","Bird on a Wire (1990)","Angel Heart (1987)","Nine 1/2 Weeks (1986)","Firestarter (1984)","Sleepwalkers (1992)","Action Jackson (1988)","Sarafina! (1992)","Soapdish (1991)","Long Walk Home, The (1990)","Clara`s Heart (1988)","Burglar (1987)","Fatal Beauty (1987)","Gone in 60 Seconds (2000)","American Pimp (1999)","Love`s Labour`s Lost (2000)","Sunshine (1999)","Trixie (1999)","Live Virgin (1999)","Hamlet (1990)","Coming Home (1978)","American Pop (1981)","Assault on Precinct 13 (1976)","Near Dark (1987)","One False Move (1991)","Shaft (1971)","Conversation, The (1974)","Cutter`s Way (1981)","Fury, The (1978)","Paper Chase, The (1973)","Prince of the City (1981)","Serpico (1973)","Big Carnival, The (1951)","Lonely Are the Brave (1962)","Sugarland Express, The (1974)","Trouble in Paradise (1932)","Big Trouble in Little China (1986)","Badlands (1973)","Battleship Potemkin, The (Bronenosets Potyomkin) (1925)","Boys and Girls (2000)","Shaft (2000)","Titan A.E. (2000)","Butterfly (La Lengua de las Mariposas) (2000)","Jesus` Son (1999)","Match, The (1999)","Time Regained (Le Temps Retrouvé) (1999)","Boricua`s Bond (2000)","Chicken Run (2000)","Me, Myself and Irene (2000)","Patriot, The (2000)","Adventures of Rocky and Bullwinkle, The (2000)","Perfect Storm, The (2000)","Golden Bowl, The (2000)","Asylum (1972)","Communion (1989)","Fun and Fancy Free (1947)","Kentucky Fried Movie, The (1977)","Blood In, Blood Out (a.k.a. Bound by Honor) (1993)","Daughter of Dr. Jeckyll (1957)","F/X (1986)","F/X 2 (1992)","Hot Spot, The (1990)","Missing in Action (1984)","Missing in Action 2: The Beginning (1985)","Braddock: Missing in Action III (1988)","Thunderbolt and Lightfoot (1974)","Dreamscape (1984)","Golden Voyage of Sinbad, The (1974)","Hatchet For the Honeymoon (Rosso Segno Della Follia) (1969)","House Party (1990)","House Party 2 (1991)","Make Mine Music (1946)","Melody Time (1948)","Nekromantik (1987)","On Our Merry Way (1948)","Project Moon Base (1953)","Rocketship X-M (1950)","Shaft in Africa (1973)","Shaft`s Big Score! (1972)","Croupier (1998)","Kid, The (2000)","Scary Movie (2000)","But I`m a Cheerleader (1999)","Shower (Xizhao) (1999)","Blowup (1966)","Pawnbroker, The (1965)","Groove (2000)","Footloose (1984)","Duel in the Sun (1946)","X-Men (2000)","Chuck & Buck (2000)","Five Senses, The (1999)","Wisdom of Crocodiles, The (a.k.a. Immortality) (2000)","In Crowd, The (2000)","What Lies Beneath (2000)","Pokémon the Movie 2000 (2000)","Criminal Lovers (Les Amants Criminels) (1999)","Anatomy of a Murder (1959)","Freejack (1992)","Greaser`s Palace (1972)","H.O.T.S. (1979)","Knightriders (1981)","MacKenna`s Gold (1969)","Sinbad and the Eye of the Tiger (1977)","Two Women (La Ciociara) (1961)","What About Bob? (1991)","White Sands (1992)","Breaker Morant (1980)","Everything You Always Wanted to Know About Sex (1972)","Interiors (1978)","Love and Death (1975)","Official Story, The (La Historia Oficial) (1985)","Other Side of Sunday, The (Søndagsengler) (1996)","Pot O` Gold (1941)","Tampopo (1986)","Thomas and the Magic Railroad (2000)","Nutty Professor II: The Klumps (2000)","Girl on the Bridge, The (La Fille sur le Pont) (1999)","Wonderland (1999)","Autumn in New York (2000)","Coyote Ugly (2000)","Hollow Man (2000)","Space Cowboys (2000)","Better Living (1998)","Mad About Mambo (2000)","Psycho Beach Party (2000)","Saving Grace (2000)","Black Sabbath (Tre Volti Della Paura, I) (1963)","Brain That Wouldn`t Die, The (1962)","Bronco Billy (1980)","Crush, The (1993)","Kelly`s Heroes (1970)","Phantasm II (1988)","Phantasm III: Lord of the Dead (1994)","Phantasm IV: Oblivion (1998)","Pumpkinhead (1988)","Air America (1990)","Make Them Die Slowly (Cannibal Ferox) (1980)","Sleepaway Camp (1983)","Steel Magnolias (1989)","And God Created Woman (Et Dieu&#8230;Créa la Femme) (1956)","Easy Money (1983)","Ilsa, She Wolf of the SS (1974)","Silent Fall (1994)","Spiral Staircase, The (1946)","Whatever Happened to Aunt Alice? (1969)","I`m the One That I Want (2000)","Tao of Steve, The (2000)","Tic Code, The (1998)","Aimée & Jaguar (1999)","Affair of Love, An (Une Liaison Pornographique) (1999)","Autumn Heart (1999)","Bless the Child (2000)","Cecil B. Demented (2000)","Eyes of Tammy Faye, The (2000)","Opportunists, The (1999)","Replacements, The (2000)","About Adam (2000)","Cell, The (2000)","Godzilla 2000 (Gojira ni-sen mireniamu) (1999)","Original Kings of Comedy, The (2000)","Sunset Strip (2000)","All the Rage (a.k.a. It`s the Rage) (1999)","Naked Gun: From the Files of Police Squad!, The (1988)","Naked Gun 2 1/2: The Smell of Fear, The (1991)","Our Town (1940)","Shane (1953)","Suddenly, Last Summer (1959)","Cat Ballou (1965)","Couch in New York, A (1996)","Devil Rides Out, The (1968)","Jerry & Tom (1998)","Supergirl (1984)","X: The Unknown (1956)","Art of War, The (2000)","Ballad of Ramblin` Jack, The (2000)","Bittersweet Motel (2000)","Bring It On (2000)","Catfish in Black Bean Sauce (2000)","Crew, The (2000)","Love & Sex (2000)","Steal This Movie! (2000)","Went to Coney Island on a Mission From God... Be Back by Five (1998)","Skipped Parts (2000)","Highlander: Endgame (2000)","Back Stage (2000)","Turn It Up (2000)","Anatomy (Anatomie) (2000)","Nurse Betty (2000)","Solas (1999)","Watcher, The (2000)","Way of the Gun, The (2000)","Almost Famous (2000)","Bait (2000)","Circus (2000)","Crime and Punishment in Suburbia (2000)","Duets (2000)","Goya in Bordeaux (Goya en Bodeos) (1999)","Urbania (2000)","Uninvited Guest, An (2000)","Specials, The (2000)","Under Suspicion (2000)","Prince of Central Park, The (1999)","Urban Legends: Final Cut (2000)","Woman on Top (2000)","Dancer in the Dark (2000)","Best in Show (2000)","Beautiful (2000)","Barenaked in America (1999)","Broken Hearts Club, The (2000)","Girlfight (2000)","Remember the Titans (2000)","Hellraiser (1987)","Hellbound: Hellraiser II (1988)","Hellraiser III: Hell on Earth (1992)","Faraway, So Close (In Weiter Ferne, So Nah!) (1993)","Beach Party (1963)","Bikini Beach (1964)","Return of the Fly (1959)","Pajama Party (1964)","Stranger Than Paradise (1984)","Voyage to the Bottom of the Sea (1961)","Fantastic Voyage (1966)","Abbott and Costello Meet Frankenstein (1948)","Bank Dick, The (1940)","Creature From the Black Lagoon, The (1954)","Giant Gila Monster, The (1959)","Invisible Man, The (1933)","Killer Shrews, The (1959)","Kronos (1957)","Kronos (1973)","Phantom of the Opera, The (1943)","Runaway (1984)","Slumber Party Massacre, The (1982)","Slumber Party Massacre II, The (1987)","Slumber Party Massacre III, The (1990)","Sorority House Massacre (1986)","Sorority House Massacre II (1990)","Bamboozled (2000)","Bootmen (2000)","Digimon: The Movie (2000)","Get Carter (2000)","Get Carter (1971)","Meet the Parents (2000)","Requiem for a Dream (2000)","Tigerland (2000)","Two Family House (2000)","Contender, The (2000)"]

HTML(""" 
    <p>Several commands and structures have been added, including the following:</p>
    <p>The __View__ command can be used to produce detachable views of data sets</p>
    <p><b>SmallTownZoo</b> data is now loaded <br/>
    <b>Assignment2</b> data is now loaded<br/>
    <b>HouseholdNames</b> and <b>AnimalNames</b> are loaded as lists of strings</p>
    <p>The <b>Grade</b> command allows you to determine the grade that your candidate <br/> solution would receive if submitted</p>
    <p>See course information (at course website) for details on grading</p>
    <p>More details on additional commands within the notebook as needed</p>
    """)
    