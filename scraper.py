from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import requests

# Helper functions here

def getTableAsList(soup):
    """
        Scrapes the html document and searches for the second table by
        using the class attribute `leftfloat`. We use find() method
        of BeautifulSoup

        To iterate over the <td> tags, we use find_all() method

        Returns the scrape as a list.
    """

    #find the table
    table = soup.find('table', class_="leftfloat")

    # initialize list to store table cells
    lTable = []

    # scrape the table
    for row in table.find_all('tr'):
        #initialize a row list
        lRow = []
        #check if the row is a header and pass
        if row.find('th'):
            pass
        else:
            for column in row.find_all('td'):
                lRow.append(column.string)

            #append the row list to the table list
            lTable.append(lRow)

    print("The table of Rubik cube positions is ")
    print(lTable)

    return lTable


def pruneTheTable(lTable):
    """
        Prunes the list and returns 2D lists...
        (cells which are not numbers are omitted!!!)
    """
    #initialize an empty list
    lNumbers = []
    for row in lTable:
        #initialize row
        lRow = []
        for column in row:

            #remove the commas in numbers
            numString = ''.join( [ char for char in column if char.isdigit() ] )

            #try if it is not a number
            try:
                int(numString)
                #append the number
                lRow.append(int(numString))
            except:
                print("not a number... proceed")
                lRow.append('nan')

        lNumbers.append(lRow)

    print("The pruned table of Rubik cube's positions is:")
    print(lNumbers)

    return lNumbers

def properFormat(lNumbers):
    """
        Return properly ordered 2D arrays
    """
    nRows = len(lNumbers)

    nDistance = np.zeros( 2 * nRows )
    nPosition = np.zeros( 2 * nRows )

    for i in range( nRows ):
        nDistance[ i ] = lNumbers[ i ][ 0 ]
        nPosition[ i ] = lNumbers[ i ][ 1 ]
        nDistance[ i + nRows ] = lNumbers[ i ][ 2 ]
        nPosition[ i + nRows ] = lNumbers[ i ][ 3 ]

    nProperTable = np.zeros( [2 * nRows, 2 ])
    nProperTable = [ nDistance, nPosition ]

    print("The properly ordered data is:")
    print(nProperTable)

    return nProperTable

def saveTableToCSV(nProperTable, sFilename):
    """
        Save the 2D list as CSV file with proper header
    """
    sHeader = 'distance, positions'
    np.savetxt(sFilename, nProperTable, delimiter=',', header = sHeader)

def plotRubikPositions(nProperTable):
    """Takes as input the 2D array of data and plots the positions
        with the distance
    """
    #Get the data
    distance = nProperTable[ 0 ]
    position = nProperTable[ 1 ]

    #Plot the data
    fig = plt.figure( figsize = ( 6, 6 ) )
    ax = fig.add_subplot( 111 )
    ax.plot(distance, position,'ko--',label="positions")
    ax.set_yscale('log')
    plt.legend(loc='best')
    plt.title('Rubik cube 3x3x3', fontsize =24)
    plt.xlabel('Distance', fontsize=18)
    plt.ylabel('Positions', fontsize=18)
    plt.savefig('rubikCubePositions.png')

def getHTML( online, filename ):
    """
        If online flag is set, fetch the website using `requests` module
        else read the offline saved HTMl page
    """
    if online:
        r = requests.get("https://cube20.org/qtm/")

        #check for success of requests
        fetch = r.status_code == requests.codes.ok

        if fetch:
            soup = BeautifulSoup(r.text, features="html.parser")
    else:
        #read the html document
        with open(filename) as f:
            soup = BeautifulSoup(f, features="html.parser")

    return soup

if __name__ == '__main__':

    #read online flag
    online = False

    filename = "rubikCubeGodNumber.html"

    sFilename = "positions.csv"

    #get the soup
    soup = getHTML(online, filename)

    #scrape the soup
    lTable = getTableAsList(soup)

    #prune the table
    lNumbers = pruneTheTable(lTable)

    #order the data
    nProperTable = properFormat(lNumbers)

    #save the scrape to csv
    saveTableToCSV(nProperTable, sFilename)

    #plot the scrape
    plotRubikPositions(nProperTable)
