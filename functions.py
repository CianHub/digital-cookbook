def getPages(count, limit):
    #Get Number of Pages to Paginate
    pages = count / limit
    if count % limit > 0:
        if count % limit <= limit:
            pages += 1
            return pages
        else:
            pages += 2
    else:
        return pages

def generatePaginationLinks(offset, limit, pages, webpage, search):
    #Generates Pagination Links
    if webpage == 'search':
        url_list = ['/' + webpage + '/' + search  + '?limit=' + str(limit) + '&offset=0']
        for i in range(pages):
            url_list.append('/' + webpage + '/' + search  + '?limit=' + str(limit) + '&offset=' + str(offset + limit))
            offset += limit
    else:
        url_list = ['/' + webpage + '?limit=' + str(limit) + '&offset=0']
        for i in range(pages):
            url_list.append('/' + webpage  + '?limit=' + str(limit) + '&offset=' + str(offset + limit))
            offset += limit
    return url_list
        
    