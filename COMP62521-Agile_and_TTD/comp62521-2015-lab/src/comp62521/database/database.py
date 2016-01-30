from comp62521.statistics import average
import itertools
import numpy as np
from xml.sax import handler, make_parser, SAXException

PublicationType = [
    "Conference Paper", "Journal", "Book", "Book Chapter"]


class Publication:
    CONFERENCE_PAPER = 0
    JOURNAL = 1
    BOOK = 2
    BOOK_CHAPTER = 3

    def __init__(self, pub_type, title, year, authors):
        self.pub_type = pub_type
        self.title = title
        if year:
            self.year = int(year)
        else:
            self.year = -1
        self.authors = authors


class Author:
    def __init__(self, name):
        n = name
        self.name = name
        lastname = n.split()
        self.lastname = lastname[-1]
        firstname = n.split()
        del firstname[-1]
        self.firstname = " ".join(firstname)


class Stat:
    STR = ["Mean", "Median", "Mode"]
    FUNC = [average.mean, average.median, average.mode]
    MEAN = 0
    MEDIAN = 1
    MODE = 2


class Database:
    def read(self, filename):
        self.publications = []
        self.authors = []
        self.author_idx = {}
        self.min_year = None
        self.max_year = None

        handler = DocumentHandler(self)
        parser = make_parser()
        parser.setContentHandler(handler)
        infile = open(filename, "r")
        valid = True
        try:
            parser.parse(infile)
        except SAXException as e:
            valid = False
            print
            "Error reading file (" + e.getMessage() + ") File: " + filename
        infile.close()

        for p in self.publications:
            if self.min_year == None or p.year < self.min_year:
                self.min_year = p.year
            if self.max_year == None or p.year > self.max_year:
                self.max_year = p.year

        return valid

    def get_all_authors(self):
        return self.author_idx.keys()

    def get_coauthor_data(self, start_year, end_year, pub_type, column=None, order=None):
        coauthors = {}
        for p in self.publications:
            if ((start_year == None or p.year >= start_year) and
                    (end_year == None or p.year <= end_year) and
                    (pub_type == 4 or pub_type == p.pub_type)):
                for a in p.authors:
                    for a2 in p.authors:
                        if a != a2:
                            try:
                                coauthors[a].add(a2)
                            except KeyError:
                                coauthors[a] = set([a2])

        def display(db, coauthors, author_id):
            return "%s (%d)" % (db.authors[author_id].name, len(coauthors[author_id]))

        if (order == "d"):
            header = ("AUTHOR0a", "CO-AUTHORS1a")
        else:
            header = ("AUTHOR0d", "CO-AUTHORS1d")

        data = []
        for a in coauthors:
            data.append([display(self, coauthors, a),
                         ", ".join([
                                       display(self, coauthors, ca) for ca in coauthors[a]])])

        if (column is not None):
            column = int(column)
            if (order == "d" and column == 0):
                data.sort(key=lambda x: x[column].split()[-2], reverse=True)
            elif (order == "d" and column != 0):
                data.sort(key=lambda x: x[column], reverse=True)
            elif (order == "a" and column == 0):
                data.sort(key=lambda x: x[column].split()[-2], reverse=False)
            else:
                data.sort(key=lambda x: x[column], reverse=False)

        return (header, data)

    def get_average_authors_per_publication(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [func(auth_per_pub[i]) for i in np.arange(4)] + [func(list(itertools.chain(*auth_per_pub)))]
        return (header, data)

    def get_average_publications_per_author(self, av):
        header = ("Conference Paper", "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))

        for p in self.publications:
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [func(pub_per_auth[:, i]) for i in np.arange(4)] + [func(pub_per_auth.sum(axis=1))]
        return (header, data)

    def get_average_publications_in_a_year(self, av):
        header = ("Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        ystats = np.zeros((int(self.max_year) - int(self.min_year) + 1, 4))

        for p in self.publications:
            ystats[p.year - self.min_year][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [func(ystats[:, i]) for i in np.arange(4)] + [func(ystats.sum(axis=1))]
        return (header, data)

    def get_average_authors_in_a_year(self, av):
        header = ("Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        yauth = [[set(), set(), set(), set(), set()] for _ in range(int(self.min_year), int(self.max_year) + 1)]

        for p in self.publications:
            for a in p.authors:
                yauth[p.year - self.min_year][p.pub_type].add(a)
                yauth[p.year - self.min_year][4].add(a)

        ystats = np.array([[len(S) for S in y] for y in yauth])

        func = Stat.FUNC[av]

        data = [func(ystats[:, i]) for i in np.arange(5)]
        return (header, data)

    def get_publication_summary_average(self, av):
        header = ("Details", "Conference Paper",
                  "Journal", "Book", "Book Chapter", "All Publications")

        pub_per_auth = np.zeros((len(self.authors), 4))
        auth_per_pub = [[], [], [], []]

        for p in self.publications:
            auth_per_pub[p.pub_type].append(len(p.authors))
            for a in p.authors:
                pub_per_auth[a, p.pub_type] += 1

        name = Stat.STR[av]
        func = Stat.FUNC[av]

        data = [
            [name + " authors per publication"]
            + [func(auth_per_pub[i]) for i in np.arange(4)]
            + [func(list(itertools.chain(*auth_per_pub)))],
            [name + " publications per author"]
            + [func(pub_per_auth[:, i]) for i in np.arange(4)]
            + [func(pub_per_auth.sum(axis=1))]]
        return (header, data)

    def get_publication_summary(self, column=None, order=None):

        if (order == "d"):
            header = ("DETAILS0a", "CONFERENCE PAPER1a",
                      "JOURNAL2a", "BOOK3a", "BOOK CHAPTER4a", "TOTAL5a")
        else:
            header = ("DETAILS0d", "CONFERENCE PAPER1d",
                      "JOURNAL2d", "BOOK3d", "BOOK CHAPTER4d", "TOTAL5d")

        plist = [0, 0, 0, 0]
        alist = [set(), set(), set(), set()]

        for p in self.publications:
            plist[p.pub_type] += 1
            for a in p.authors:
                alist[p.pub_type].add(a)
        # create union of all authors
        ua = alist[0] | alist[1] | alist[2] | alist[3]

        data = [
            ["Number of publications"] + plist + [sum(plist)],
            ["Number of authors"] + [len(a) for a in alist] + [len(ua)]]

        if (column is not None):
            column = int(column)
            if (order == "d"):
                data.sort(key=lambda x: x[column], reverse=True)
            else:
                data.sort(key=lambda x: x[column], reverse=False)

        return (header, data)

    def get_average_authors_per_publication_by_author(self, av):
        header = ("Author", "Number of conference papers",
                  "Number of journals", "Number of books",
                  "Number of book chapers", "All publications")

        astats = [[[], [], [], []] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [[self.authors[i].name]
                + [func(L) for L in astats[i]]
                + [func(list(itertools.chain(*astats[i])))]
                for i in range(len(astats))]

        return (header, data)

    def get_publications_by_author(self, column=None, order=None):

        if (order == "d"):
            header = ("AUTHOR0a", "NUMBER OF CONFERENCE PAPERS1a",
                      "NUMBER OF JOURNALS2a", "NUMBER OF BOOKS3a",
                      "NUMBER OF BOOK CHAPTERS4a", "TOTAL5a")
        else:
            header = ("AUTHOR0d", "NUMBER OF CONFERENCE PAPERS1d",
                      "NUMBER OF JOURNALS2d", "NUMBER OF BOOKS3d",
                      "NUMBER OF BOOK CHAPTERS4d", "TOTAL5d")

        astats = [[0, 0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])]
                for i in range(len(astats))]

        if (column is not None):
            column = int(column)
            if (order == "d" and column == 0):
                data.sort(key=lambda x: x[column].split()[-1], reverse=True)
            elif (order == "d" and column != 0):
                data.sort(key=lambda x: (-x[column], x[0].split()[-1]), reverse=False)
            elif (order == "a" and column == 0):
                data.sort(key=lambda x: x[column].split()[-1], reverse=False)
            else:
                data.sort(key=lambda x: (x[column], x[0].split()[-1]), reverse=False)

        return (header, data)

    def get_numbers_by_author(self, column=None, order=None):

        if (order == "d"):
            header = (
                "AUTHOR0a", "NUMBER OF TIMES FIRST AUTHOR1a", "NUMBER OF TIMES LAST AUTHOR2a",
                "NUMBERS FOR SOLE AUTHOR3a")
        else:
            header = (
                "AUTHOR0d", "NUMBER OF TIMES FIRST AUTHOR1d", "NUMBER OF TIMES LAST AUTHOR2d",
                "NUMBERS FOR SOLE AUTHOR3d")

        astats = [[0, 0, 0] for _ in range(len(self.authors))]
        i = 0
        for p in self.publications:
            if (len(p.authors) == 1):
                astats[p.authors[0]][2] += 1
            else:
                astats[p.authors[0]][0] += 1
                astats[p.authors[-1]][1] += 1

        data = [[self.authors[i].name] + astats[i] for i in range(len(astats))]

        if (column is not None):
            column = int(column)
            if (order == "d" and column == 0):
                data.sort(key=lambda x: x[column].split()[-1], reverse=True)
            elif (order == "d" and column != 0):
                data.sort(key=lambda x: (-x[column], x[0].split()[-1]), reverse=False)
            elif (order == "a" and column == 0):
                data.sort(key=lambda x: x[column].split()[-1], reverse=False)
            else:
                data.sort(key=lambda x: (x[column], x[0].split()[-1]), reverse=False)

        # print data

        return (header, data)

    def get_numbers_by_author_type(self, pType, column=None, order=None):

        if (order == "d"):
            header = ("AUTHOR0a", "NUMBER OF TIMES FIRST AUTHOR1a", "NUMBER OF TIMES LAST AUTHOR2a",
                      "NUMBERS FOR SOLE AUTHOR3a")
        else:
            header = ("AUTHOR0d", "NUMBER OF TIMES FIRST AUTHOR1d", "NUMBER OF TIMES LAST AUTHOR2d",
                      "NUMBERS FOR SOLE AUTHOR3d")

        astats = [[0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            if (p.pub_type == pType):

                if (len(p.authors) == 1):
                    astats[p.authors[0]][2] += 1
                else:
                    astats[p.authors[0]][0] += 1
                    astats[p.authors[-1]][1] += 1

        data = [[self.authors[i].name] + astats[i] for i in range(len(astats))]

        if (column is not None):
            column = int(column)
            if (order == "d" and column == 0):
                data.sort(key=lambda x: x[column].split()[-1], reverse=True)
            elif (order == "d" and column != 0):
                data.sort(key=lambda x: (-x[column], x[0].split()[-1]), reverse=False)
            elif (order == "a" and column == 0):
                data.sort(key=lambda x: x[column].split()[-1], reverse=False)
            else:
                data.sort(key=lambda x: (x[column], x[0].split()[-1]), reverse=False)

        # print data

        return (header, data)

    def get_average_authors_per_publication_by_year(self, av):
        header = ("Year", "Conference papers",
                  "Journals", "Books",
                  "Book chapers", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type].append(len(p.authors))
            except KeyError:
                ystats[p.year] = [[], [], [], []]
                ystats[p.year][p.pub_type].append(len(p.authors))

        func = Stat.FUNC[av]

        data = [[y]
                + [func(L) for L in ystats[y]]
                + [func(list(itertools.chain(*ystats[y])))]
                for y in ystats]
        return (header, data)

    def get_publications_by_year(self, column=None, order=None):

        if (order == "d"):
            header = ("YEAR0a", "NUMBER OF CONFERENCE PAPERS1a",
                      "NUMBER OF JOURNALS2a", "NUMBER OF BOOKS3a",
                      "NUMBER OF BOOK CHAPTERS4a", "TOTAL5a")
        else:
            header = ("YEAR0d", "NUMBER OF CONFERENCE PAPERS1d",
                      "NUMBER OF JOURNALS2d", "NUMBER OF BOOKS3d",
                      "NUMBER OF BOOK CHAPTERS4d", "TOTAL5d")

        ystats = {}
        for p in self.publications:
            try:
                ystats[p.year][p.pub_type] += 1
            except KeyError:
                ystats[p.year] = [0, 0, 0, 0]
                ystats[p.year][p.pub_type] += 1

        data = [[y] + ystats[y] + [sum(ystats[y])] for y in ystats]

        if (column is not None):
            column = int(column)
            if (order == "d"):
                data.sort(key=lambda x: x[column], reverse=True)
            else:
                data.sort(key=lambda x: x[column], reverse=False)

        return (header, data)

    def get_average_publications_per_author_by_year(self, av):
        header = ("Year", "Conference papers",
                  "Journals", "Books",
                  "Book chapters", "All publications")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year]
            except KeyError:
                s = np.zeros((len(self.authors), 4))
                ystats[p.year] = s
            for a in p.authors:
                s[a][p.pub_type] += 1

        func = Stat.FUNC[av]

        data = [[y]
                + [func(ystats[y][:, i]) for i in np.arange(4)]
                + [func(ystats[y].sum(axis=1))]
                for y in ystats]
        return (header, data)

    def get_author_totals_by_year(self, column=None, order=None):

        if (order == "d"):
            header = ("YEAR0a", "NUMBER OF CONFERENCE PAPERS1a",
                      "NUMBER OF JOURNALS2a", "NUMBER OF BOOKS3a",
                      "NUMBER OF BOOK CHAPTERS4a", "TOTAL5a")
        else:
            header = ("YEAR0d", "NUMBER OF CONFERENCE PAPERS1d",
                      "NUMBER OF JOURNALS2d", "NUMBER OF BOOKS3d",
                      "NUMBER OF BOOK CHAPTERS4d", "TOTAL5d")

        ystats = {}
        for p in self.publications:
            try:
                s = ystats[p.year][p.pub_type]
            except KeyError:
                ystats[p.year] = [set(), set(), set(), set()]
                s = ystats[p.year][p.pub_type]
            for a in p.authors:
                s.add(a)
        data = [[y] + [len(s) for s in ystats[y]] + [len(ystats[y][0] | ystats[y][1] | ystats[y][2] | ystats[y][3])]
                for y in ystats]

        if (column is not None):
            column = int(column)
            if (order == "d"):
                data.sort(key=lambda x: x[column], reverse=True)
            else:
                data.sort(key=lambda x: x[column], reverse=False)

        return (header, data)

    def add_publication(self, pub_type, title, year, authors):
        if year == None or len(authors) == 0:
            print
            "Warning: excluding publication due to missing information"
            print
            "    Publication type:", PublicationType[pub_type]
            print
            "    Title:", title
            print
            "    Year:", year
            print
            "    Authors:", ",".join(authors)
            return
        if title == None:
            print
            "Warning: adding publication with missing title [ %s %s (%s) ]" % (
                PublicationType[pub_type], year, ",".join(authors))
        idlist = []
        for a in authors:
            try:
                idlist.append(self.author_idx[a])
            except KeyError:
                a_id = len(self.authors)
                self.author_idx[a] = a_id
                idlist.append(a_id)
                self.authors.append(Author(a))
        self.publications.append(
            Publication(pub_type, title, year, idlist))
        if (len(self.publications) % 100000) == 0:
            print
            "Adding publication number %d (number of authors is %d)" % (len(self.publications), len(self.authors))

        if self.min_year == None or year < self.min_year:
            self.min_year = year
        if self.max_year == None or year > self.max_year:
            self.max_year = year

    def _get_collaborations(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[a] += 1
                    except KeyError:
                        data[a] = 1
        if not include_self:
            del data[author_id]
        return data

    # get a list of coauthors for author_id, [coauthor id, collaboration pubs]

    def get_coauthor_names(self, author_id, include_self):
        data = {}
        for p in self.publications:
            if author_id in p.authors:
                for a in p.authors:
                    try:
                        data[str(self.authors[a].name)] += 1
                    except KeyError:
                        data[str(self.authors[a].name)] = 1
        if not include_self:
            del data[str(self.authors[author_id].name)]
        return data

    # get a list of coauthors for author_name, [coauthor id, collaboration pubs]

    def get_coauthor_details(self, name):
        author_id = self.author_idx[name]
        data = self._get_collaborations(author_id, True)
        return [(self.authors[key].name, data[key])
                for key in data]

    def get_network_data(self):
        na = len(self.authors)

        nodes = [[self.authors[i].name, -1] for i in range(na)]
        links = set()
        for a in range(na):
            collab = self._get_collaborations(a, False)
            nodes[a][1] = len(collab)
            for a2 in collab:
                if a < a2:
                    links.add((a, a2))
        return (nodes, links)

    def search_by_author(self, name):
        # header = ("AUTHOR", "CONFERENCE PAPERS", "JOURNALS", "BOOKS", "BOOK CHAPTERS", "TOTAL PUBLICATIONS",
        #          "CO-AUTHORS", "FIRST APPEAR", "LAST APPEAR", "SOLE AUTHOR")

        header = ""

        coauthors = {}
        for p in self.publications:
            for a in p.authors:
                coauthors[a] = set([])
        for p in self.publications:
            for a in p.authors:
                for a2 in p.authors:
                    if a != a2:
                        try:
                            coauthors[a].add(a2)
                        except KeyError:
                            coauthors[a] = set([a2])

        astats = [[0, 0, 0, 0] for _ in range(len(self.authors))]

        for p in self.publications:
            for a in p.authors:
                astats[a][p.pub_type] += 1

        astats2 = [[0, 0, 0] for _ in range(len(self.authors))]
        for p in self.publications:
            if (len(p.authors) == 1):
                astats2[p.authors[0]][2] += 1
            else:
                astats2[p.authors[0]][0] += 1
                astats2[p.authors[-1]][1] += 1

        data = [[self.authors[i].name] + astats[i] + [sum(astats[i])] for i in range(len(astats))]

        index = []
        k = 0
        for y in range(len(data)):
            p = data[y]
            if name.upper() in p[0].upper():
                index.append(y)
                k += 1

        # print(index)
        # LIST OF SELECTED AUTHOR NAMES #

        authNames = []
        authNamesAux = []

        for e in range(len(index)):
            aName = data[index[e]]
            authNames.append([index[e], aName[0]])

        # FOUR ORDERING CONDITIONS #

        lastList = []
        firstList = []
        middleList = []
        keyList = []

        # LAST NAME BEGINS WITH KEY WORD #

        for e in range(len(authNames)):
            if authNames[e][1].split()[-1].upper().startswith(name.upper()):
                lastList.append(authNames[e])
            else:
                authNamesAux.append(authNames[e])

        lastList.sort(key=lambda x: x[1].split()[-1])

        authNames = authNamesAux
        authNamesAux = []

        # FIRST NAME BEGINS WITH KEY WORD #

        for e in range(len(authNames)):
            if authNames[e][1].upper().startswith(name.upper()):
                firstList.append(authNames[e])
            else:
                authNamesAux.append(authNames[e])

        firstList.sort(key=lambda x: x[1])

        authNames = authNamesAux
        authNamesAux = []

        # MIDDLE NAME BEGINS WITH KEY WORD #

        for e in range(len(authNames)):
            if len(authNames[e][1].split()) > 2 and authNames[e][1].split()[1].upper().startswith(name.upper()):
                middleList.append(authNames[e])
            else:
                authNamesAux.append(authNames[e])

        middleList.sort(key=lambda x: x[1].split()[-1])

        authNames = authNamesAux
        authNamesAux = []

        # LAST NAME CONTAINS KEY WORD BUT NOT BEGINS WITH IT #

        for e in range(len(authNames)):
            if len(authNames[e][1].split()) > 1 and name.upper() in authNames[e][1].split()[-1].upper():
                keyList.append(authNames[e])
            else:
                authNamesAux.append(authNames[e])

        keyList.sort(key=lambda x: x[1].split()[-1])

        authNames = authNamesAux
        authNamesAux = []

        authNames.sort(key=lambda x: x[1].split()[-1])

        authNamesAux.extend(lastList)
        authNamesAux.extend(firstList)
        authNamesAux.extend(middleList)
        authNamesAux.extend(keyList)
        authNamesAux.extend(authNames)

        # print(lastList)
        # print(firstList)
        # print(middleList)
        # print(keyList)
        # print(authNames)

        index = []

        for x in range(len(authNamesAux)):
            index.append(authNamesAux[x][0])

        data2 = []
        # if (index != []):
        #    for m in range(len(index)):
        #        data2.append([self.authors[index[m]].name] + astats[index[m]] + [sum(astats[index[m]])] +
        #                     [len(coauthors[index[m]])] + astats2[index[m]])

        if (index != []):
            for m in range(len(index)):
                data2.append([self.authors[index[m]].name])

        else:
            header = ("")
            data2 = [["Nothing found"]]

        return (header, data2)

    def get_stats_by_author(self, name):

        astats = [[0, 0, 0, 0] for _ in range(4)]

        header = ("CATEGORY", "OVERALL", "CONFERENCE PAPERS", "JOURNAL ARTICLES", "BOOKS", "BOOK CHAPTERS")

        for p in self.publications:

            if (self.author_idx[name] in p.authors):
                astats[0][p.pub_type] += 1
                if (len(p.authors) == 1):
                    astats[3][p.pub_type] += 1
                else:
                    if (self.author_idx[name] == p.authors[0]):
                        astats[1][p.pub_type] += 1
                    if (self.author_idx[name] == p.authors[-1]):
                        astats[2][p.pub_type] += 1

        coauthorDic = self._get_collaborations(self.author_idx[name], False)

        data = []
        data.append(["Number of publications"] + [sum(astats[0])] + astats[0])
        data.append(["Number of times first author"] + [sum(astats[1])] + astats[1])
        data.append(["Number of times last author"] + [sum(astats[2])] + astats[2])
        data.append(["Number of times sole author"] + [sum(astats[3])] + astats[3])
        data.append(["Number of co-authors"] + [len(coauthorDic), "-", "-", "-", "-"])

        coauthorNamesDic = self.get_coauthor_names(self.author_idx[name], False)

        coAuthorNamesKeys = coauthorNamesDic.keys()

        return (header, data, coAuthorNamesKeys)

    def get_seperation_degree_between_two_authors(self, name1, name2):
        # input two authors' name, return the path of collaboration,
        # e.g. Pub 1: Author1, Author2, Pub 2: Author1, Author 3
        # input Author 1, Author 3, return id of Author2(if is 2) ->  [2]

        id1 = self.author_idx[name1]
        id2 = self.author_idx[name2]

        inf = 99999
        header = ("Author1", "Author2", "Degrees of separation")

        nodes, links = self.get_network_data()

        network = [[inf for _ in range(len(self.authors))] for _ in range(len(self.authors))]
        for l in links:
            a1 = l[0]
            a2 = l[1]
            network[a1][a2] = 1
            network[a2][a1] = 1
        for i in range(len(self.authors)):
            network[i][i] = 0

        for k in range(len(network)):
            for i in range(len(network)):
                for j in range(len(network)):
                    if network[i][j] > network[i][k] + network[k][j]:
                        network[i][j] = network[i][k] + network[k][j]

        degree = []

        if network[id1][id2] == inf:
            degree.append(name1)
            degree.append(name2)
            degree.append("X")

        else:
            degree.append(name1)
            degree.append(name2)
            degree.append(network[id1][id2] - 1)

        return header, degree

    def get_visualization_for_degrees_of_separation(self):
        header = []
        return header
            # t = id2
            # P = [ "*" for _ in range(len(self.authors))]
            # D = [network[id1][i] for i in range(len(self.authors))]
            # final = [0 for _ in range(len(self.authors))]
            # final[id1] = 1
            #
            # for _ in range(len(self.authors)):
            #     min = inf
            #     for w in range(len(self.authors)):
            #         if final[w] == 0 and D[w] < min:
            #             id2 = w
            #             min = D[w]
            #     final[id2] = 1
            #     for w in range(len(self.authors)):
            #         if final[w] == 0 and min + network[id2][w] < D[w]:
            #             D[w] = min + network[id2][w]
            #             P[w] = id2
            #
            # print P
            # print D
            # print final

            # pathes = [[[] for _ in range(len(self.authors))] for _ in range(len(self.authors)) ]

            # for i in range(len(network)):
            #     for j in range(len(network)):
            #         if network[i][j] == 1:
            #             pathes[i][j] = [i]
            #         elif network[i][j] == inf:
            #             pathes[i][j] == [-1]
            # # print pathes
            # # pathes = {}
            # for k in range(len(network)):
            #     for i in range(len(network)):
            #         for j in range(len(network)):
            #             if network[i][j] > network[i][k] + network[k][j]:
            #                 network[i][j] = network[i][k] + network[k][j]
            #                 pathes[i][k] = [i]
            #                 pathes[i][j] = pathes[k][j]
                            # print network[i][k] , "*" , network[k][j]
                            # pathes[i][j] = pathes[i][k] + [k] + pathes[k][j]
                            # try:
                            #     pathes[(i, j)] = pathes[(i, k)] + [k] + pathes[(k, j)]
                            # except:
                            #     pathes[(i, j)] = [k]
                            # if pathes.has_key((i, j)):
                            #     if network[i][j] > network[i][k] + network[k][j]:
                            #         pathes[(i, j)] = pathes[(i, k)] + [k] + pathes[(k, j)]
                            #     elif i != k and j != k :
                            #         pathes[(i, j)] = [pathes[(i, j)]] + [pathes[(i, k)] + [k] + pathes[(k, j)]]
                            # else:
                            #     pathes[(i, j)] = [k]

                                # elif network[i][j] == network[i][k] + network[k][j] and k != i and k != j:
                                #     # pathes[(i, j)] = [pathes[(i, j)]] + [pathes[(i, k)] + [k] + pathes[(k, j)]]
                                #     print [pathes[(i, j)]]
                                #     print [pathes[(i, k)] + [k] + pathes[(k, j)]]

                                # pathes[i][j] = [pathes[i][j][-1]] + [k]
                                # print pathes[i][j]
                                # print k
                                # if i == id1 and j == id2:
                                #      print k
                                # if network[i][j] == network[i][k] + network[k][j]:
                                #
                                # else:
                                #     path[i][j] = path[i][k] + [k] + path[k][j]

        # t = id2
        # P = [ "*" for _ in range(len(self.authors))]
        # D = [network[id1][i] for i in range(len(self.authors))]
        # final = [0 for _ in range(len(self.authors))]
        # final[id1] = 1
        #
        # for _ in range(len(self.authors)):
        #     min = inf
        #     for w in range(len(self.authors)):
        #         if final[w] == 0 and D[w] < min:
        #             id2 = w
        #             min = D[w]
        #     final[id2] = 1
        #     for w in range(len(self.authors)):
        #         if final[w] == 0 and min + network[id2][w] < D[w]:
        #             D[w] = min + network[id2][w]
        #             P[w] = id2
        #
        # print P
        # print D
        # print final

        # pathes = [[[] for _ in range(len(self.authors))] for _ in range(len(self.authors)) ]

        # for i in range(len(network)):
        #     for j in range(len(network)):
        #         if network[i][j] == 1:
        #             pathes[i][j] = [i]
        #         elif network[i][j] == inf:
        #             pathes[i][j] == [-1]
        # # print pathes
        # # pathes = {}
        # for k in range(len(network)):
        #     for i in range(len(network)):
        #         for j in range(len(network)):
        #             if network[i][j] > network[i][k] + network[k][j]:
        #                 network[i][j] = network[i][k] + network[k][j]
        #                 pathes[i][k] = [i]
        #                 pathes[i][j] = pathes[k][j]
        # print network[i][k] , "*" , network[k][j]
        # pathes[i][j] = pathes[i][k] + [k] + pathes[k][j]
        # try:
        #     pathes[(i, j)] = pathes[(i, k)] + [k] + pathes[(k, j)]
        # except:
        #     pathes[(i, j)] = [k]
        # if pathes.has_key((i, j)):
        #     if network[i][j] > network[i][k] + network[k][j]:
        #         pathes[(i, j)] = pathes[(i, k)] + [k] + pathes[(k, j)]
        #     elif i != k and j != k :
        #         pathes[(i, j)] = [pathes[(i, j)]] + [pathes[(i, k)] + [k] + pathes[(k, j)]]
        # else:
        #     pathes[(i, j)] = [k]

        # elif network[i][j] == network[i][k] + network[k][j] and k != i and k != j:
        #     # pathes[(i, j)] = [pathes[(i, j)]] + [pathes[(i, k)] + [k] + pathes[(k, j)]]
        #     print [pathes[(i, j)]]
        #     print [pathes[(i, k)] + [k] + pathes[(k, j)]]

        # pathes[i][j] = [pathes[i][j][-1]] + [k]
        # print pathes[i][j]
        # print k
        # if i == id1 and j == id2:
        #      print k
        # if network[i][j] == network[i][k] + network[k][j]:
        #
        # else:
        #     path[i][j] = path[i][k] + [k] + path[k][j]
        # except KeyError:
        #     # pathes[id1, id2)] = []
        #     # P = []

class DocumentHandler(handler.ContentHandler):
    TITLE_TAGS = ["sub", "sup", "i", "tt", "ref"]
    PUB_TYPE = {
        "inproceedings": Publication.CONFERENCE_PAPER,
        "article": Publication.JOURNAL,
        "book": Publication.BOOK,
        "incollection": Publication.BOOK_CHAPTER}

    def __init__(self, db):
        self.tag = None
        self.chrs = ""
        self.clearData()
        self.db = db

    def clearData(self):
        self.pub_type = None
        self.authors = []
        self.year = None
        self.title = None

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        if name in self.TITLE_TAGS:
            return
        if name in DocumentHandler.PUB_TYPE.keys():
            self.pub_type = DocumentHandler.PUB_TYPE[name]
        self.tag = name
        self.chrs = ""

    def endElement(self, name):
        if self.pub_type == None:
            return
        if name in self.TITLE_TAGS:
            return
        d = self.chrs.strip()
        if self.tag == "author":
            self.authors.append(d)
        elif self.tag == "title":
            self.title = d
        elif self.tag == "year":
            self.year = int(d)
        elif name in DocumentHandler.PUB_TYPE.keys():
            self.db.add_publication(
                self.pub_type,
                self.title,
                self.year,
                self.authors)
            self.clearData()
        self.tag = None
        self.chrs = ""

    def characters(self, chrs):
        if self.pub_type != None:
            self.chrs += chrs
