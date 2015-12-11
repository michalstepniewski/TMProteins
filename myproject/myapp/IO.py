def readpath(path):

    InFile = open (path, 'r')
    InLines = InFile. readlines ()
    InFile. close ()

    return InLines
