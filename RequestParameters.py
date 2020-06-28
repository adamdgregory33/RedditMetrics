#parameter class - stores the information about the request to 
#Reddit for the submission information


class RequestParameters:
    
    subName =''
    limit = 0
    sortBy = ''
    queryString = ''
    timeFilter = ''
    
    def __init__(self, sub,limit, sortBy, queryString ='',timeFilter =''):
        self.subName=sub
        self.limit= limit
        self.sortBy = sortBy
        self.queryString = queryString
        self.timeFilter = timeFilter
        