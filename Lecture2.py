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

try: 
    DataFrame
except:
    from pandas import DataFrame
    
def MakeSmallTownData(Username):
    'Returns Subeconomy Problem Data'
    
    APM = LcgRand( hash( Username.lower() ) )
    Data = APM.randint(0,2,(250,20))
    
    ## Make a Subeconomy
    
    SubEconomy = APM.randint(0,250,APM.randint(20,80))
    
    Se = SubEconomy[0]
    
    for j in SubEconomy:
        Data[j,1:21] = Data[Se,1:21]
        
    ## Two Income Households
    
    for i in range(250):
        inds = []
        for j in range(20):
           if( Data[i,j] == 1 ): 
                inds.append(j)
        if( len(inds) == 0):
            tmp = APM.randint(1,21)
            Data[i,tmp] = 1
            Data[i, 2 ] = 1
            inds.append(2)
            inds.append(tmp)
         
        TwoIncome = APM.rand() <= 0.4
        
        earn = [ inds.pop( APM.randint( len(inds ) ) ) ]
        if(TwoIncome):
            earn.append( inds.pop( APM.randint( len(inds ) ) ) )
        else:
            earn.append( 40 )
        acc = 0
        for j in inds:
            if( j != earn[0] and j != earn[1] ):
                Data[i,j] = -APM.randint(5,21)*50
                acc += -Data[i,j]
        if( TwoIncome ):
            Data[i,earn[0]] = APM.randint( floor( acc / 40 ), floor( acc / 20 ) )*10
            Data[i,earn[1]] = acc - Data[i,earn[0]]  
        else:
            Data[i,earn[0]] = acc
    
    ## Add small transactions
    
    Smalltrans = 50
    
    for i in range(250):
        if( i in SubEconomy): 
            continue
        inds = []
        for j in range(2,20): #no grocery store changes
           if( Data[i,j] < 0 ): 
              inds.append(j)
        if( Data[i,1]==0 and Data[i,2] == 0 ):
            ind = inds.pop( APM.randint( len(inds) ) )
            Data[i,APM.randint(1,3)] = Data[i, ind ]
            Data[i, ind ] = 0
        if( 100*rand() < Smalltrans and len(inds) > 1 ):
            A = inds.pop( APM.randint( len(inds) ) )
            B = inds.pop( APM.randint( len(inds) ) )
            tmp = -10*APM.randint(1,10)
            Data[i,A] = Data[i,A] + Data[i,B] -  tmp
            Data[i,B] = tmp
     
    # Including Subeconomy threshold corruption
         
    for i in SubEconomy:
        inds = []
        for j in range(20):
           if( Data[i,j] == 0 ): 
                inds.append(j) 
           if( Data[i,j] > 0 ):
                inc = j
        tmp1 = -10*APM.randint(1,4)
        tmp2 = -10*APM.randint(1,4)
        Data[i,inds.pop( APM.randint(len(inds) ) ) ] = tmp1  
        Data[i,inds.pop( APM.randint(len(inds) ) ) ] = tmp2
        Data[i,inc] += -(tmp1+tmp2)
        
    return Data
    
Businesses = ['ThriftyFoods', 'TownFoods', 'RiversAuto', 'ClothesInc', 'SmartMart', 'Acme', 'AceAuto', 'BigDeals', 'SavingsBank', 
              'TownTools', 'BestDeals', 'Wyres', 'JanesPlace', 'Bhardware', 'Biddles', 'Macs', 'Plumbers', 'LendersCU', 'FillerUp', 'GetItToGo']

HouseholdNames = ["SMITH","JOHNSON","WILLIAMS","JONES","BROWN","DAVIS","MILLER","WILSON","MOORE","TAYLOR","ANDERSON","THOMAS","JACKSON","WHITE","HARRIS","MARTIN","THOMPSON","GARCIA","MARTINEZ","ROBINSON","CLARK","RODRIGUEZ","LEWIS","LEE","WALKER","HALL","ALLEN","YOUNG","HERNANDEZ","KING","WRIGHT","LOPEZ","HILL","SCOTT","GREEN","ADAMS","BAKER","GONZALEZ","NELSON","CARTER","MITCHELL","PEREZ","ROBERTS","TURNER","PHILLIPS","CAMPBELL","PARKER","EVANS","EDWARDS","COLLINS","STEWART","SANCHEZ","MORRIS","ROGERS","REED","COOK","MORGAN","BELL","MURPHY","BAILEY","RIVERA","COOPER","RICHARDSON","COX","HOWARD","WARD","TORRES","PETERSON","GRAY","RAMIREZ","JAMES","WATSON","BROOKS","KELLY","SANDERS","PRICE","BENNETT","WOOD","BARNES","ROSS","HENDERSON","COLEMAN","JENKINS","PERRY","POWELL","LONG","PATTERSON","HUGHES","FLORES","WASHINGTON","BUTLER","SIMMONS","FOSTER","GONZALES","BRYANT","ALEXANDER","RUSSELL","GRIFFIN","DIAZ","HAYES","MYERS","FORD","HAMILTON","GRAHAM","SULLIVAN","WALLACE","WOODS","COLE","WEST","JORDAN","OWENS","REYNOLDS","FISHER","ELLIS","HARRISON","GIBSON","MCDONALD","CRUZ","MARSHALL","ORTIZ","GOMEZ","MURRAY","FREEMAN","WELLS","WEBB","SIMPSON","STEVENS","TUCKER","PORTER","HUNTER","HICKS","CRAWFORD","HENRY","BOYD","MASON","MORALES","KENNEDY","WARREN","DIXON","RAMOS","REYES","BURNS","GORDON","SHAW","HOLMES","RICE","ROBERTSON","HUNT","BLACK","DANIELS","PALMER","MILLS","NICHOLS","GRANT","KNIGHT","FERGUSON","ROSE","STONE","HAWKINS","DUNN","PERKINS","HUDSON","SPENCER","GARDNER","STEPHENS","PAYNE","PIERCE","BERRY","MATTHEWS","ARNOLD","WAGNER","WILLIS","RAY","WATKINS","OLSON","CARROLL","DUNCAN","SNYDER","HART","CUNNINGHAM","BRADLEY","LANE","ANDREWS","RUIZ","HARPER","FOX","RILEY","ARMSTRONG","CARPENTER","WEAVER","GREENE","LAWRENCE","ELLIOTT","CHAVEZ","SIMS","AUSTIN","PETERS","KELLEY","FRANKLIN","LAWSON","FIELDS","GUTIERREZ","RYAN","SCHMIDT","CARR","VASQUEZ","CASTILLO","WHEELER","CHAPMAN","OLIVER","MONTGOMERY","RICHARDS","WILLIAMSON","JOHNSTON","BANKS","MEYER","BISHOP","MCCOY","HOWELL","ALVAREZ","MORRISON","HANSEN","FERNANDEZ","GARZA","HARVEY","LITTLE","BURTON","STANLEY","NGUYEN","GEORGE","JACOBS","REID","KIM","FULLER","LYNCH","DEAN","GILBERT","GARRETT","ROMERO","WELCH","LARSON","FRAZIER","BURKE","HANSON","DAY","MENDOZA","MORENO","BOWMAN","MEDINA","FOWLER"]

SmallTownData = DataFrame( MakeSmallTownData('FirstExample'), index = HouseholdNames, columns = Businesses)
Assignment1 = DataFrame( MakeSmallTownData(_margv[0]), index = HouseholdNames, columns = Businesses)



