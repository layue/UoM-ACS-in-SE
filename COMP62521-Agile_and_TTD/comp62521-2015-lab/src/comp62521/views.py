from comp62521 import app
from database import database
from flask import (render_template, request)


def format_data(data):
    fmt = "%.2f"
    result = []
    for item in data:
        if type(item) is list:
            result.append(", ".join([(fmt % i).rstrip('0').rstrip('.') for i in item]))
        else:
            result.append((fmt % item).rstrip('0').rstrip('.'))
    return result


@app.route("/averages")
def showAverages(debug=None, db=None):
    if debug is None:
        dataset = app.config['DATASET']
        db = app.config['DATABASE']
    else:
        dataset = "debug.xml"

    args = {"dataset": dataset, "id": "averages"}
    args['title'] = "Averaged Data"
    tables = []
    averages = [database.Stat.MEAN, database.Stat.MEDIAN, database.Stat.MODE]

    col1 = 0
    col2 = 0
    col3 = 0
    col4 = 0

    order1 = "a"
    order2 = "a"
    order3 = "a"
    order4 = "a"

    if debug is None and "field" in request.args:
        column = request.args.get("field")
        print(column[1:2])
        if (column[1:2] == "1"):
            col1 = int(column[:1])
            order1 = column[-1:]
        elif (column[1:2] == "2"):
            col2 = int(column[:1])
            order2 = column[-1:]
        elif (column[1:2] == "3"):
            col3 = int(column[:1])
            order3 = column[-1:]
        elif (column[1:2] == "4"):
            col4 = int(column[:1])
            order4 = column[-1:]

    if (order1 == "d"):
        headers = ["AVERAGE01a", "CONFERENCE PAPER11a", "JOURNAL21a", "BOOK31a", "BOOK CHAPTER41a",
                   "ALL PUBLICATIONS51a"]
    else:
        headers = ["AVERAGE01d", "CONFERENCE PAPER11d", "JOURNAL21d", "BOOK31d", "BOOK CHAPTER41d",
                   "ALL PUBLICATIONS51d"]

    tables.append({
        "id": 1,
        "title": "Average Authors per Publication",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_per_publication(i)[1])
            for i in averages]})

    if (order1 == "d"):
        tables[0]['rows'].sort(key=lambda x: x[col1], reverse=True)
    else:
        tables[0]['rows'].sort(key=lambda x: x[col1], reverse=False)

    if (order2 == "d"):
        headers = ["AVERAGE02a", "CONFERENCE PAPER12a", "JOURNAL22a", "BOOK32a", "BOOK CHAPTER42a",
                   "ALL PUBLICATIONS52a"]
    else:
        headers = ["AVERAGE02d", "CONFERENCE PAPER12d", "JOURNAL22d", "BOOK32d", "BOOK CHAPTER42d",
                   "ALL PUBLICATIONS52d"]

    tables.append({
        "id": 2,
        "title": "Average Publications per Author",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_per_author(i)[1])
            for i in averages]})

    if (order2 == "d"):
        tables[1]['rows'].sort(key=lambda x: x[col2], reverse=True)
    else:
        tables[1]['rows'].sort(key=lambda x: x[col2], reverse=False)

    if (order3 == "d"):
        headers = ["AVERAGE03a", "CONFERENCE PAPER13a", "JOURNAL23a", "BOOK33a", "BOOK CHAPTER43a",
                   "ALL PUBLICATIONS53a"]
    else:
        headers = ["AVERAGE03d", "CONFERENCE PAPER13d", "JOURNAL23d", "BOOK33d", "BOOK CHAPTER43d",
                   "ALL PUBLICATIONS53d"]

    tables.append({
        "id": 3,
        "title": "Average Publications in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_publications_in_a_year(i)[1])
            for i in averages]})

    if (order3 == "d"):
        tables[2]['rows'].sort(key=lambda x: x[col3], reverse=True)
    else:
        tables[2]['rows'].sort(key=lambda x: x[col3], reverse=False)

    if (order4 == "d"):
        headers = ["AVERAGE04a", "CONFERENCE PAPER14a", "JOURNAL24a", "BOOK34a", "BOOK CHAPTER44a",
                   "ALL PUBLICATIONS54a"]
    else:
        headers = ["AVERAGE04d", "CONFERENCE PAPER14d", "JOURNAL24d", "BOOK34d", "BOOK CHAPTER44d",
                   "ALL PUBLICATIONS54d"]

    tables.append({
        "id": 4,
        "title": "Average Authors in a Year",
        "header": headers,
        "rows": [
            [database.Stat.STR[i]]
            + format_data(db.get_average_authors_in_a_year(i)[1])
            for i in averages]})

    if (order4 == "d"):
        tables[3]['rows'].sort(key=lambda x: x[col4], reverse=True)
    else:
        tables[3]['rows'].sort(key=lambda x: x[col4], reverse=False)

    args['tables'] = tables
    args["url"] = "averages"

    if debug is not None:
        return "OK"

    return render_template("averages.html", args=args)


@app.route("/coauthors")
def showCoAuthors(debug=None, db=None):
    if debug is None:
        dataset = app.config['DATASET']
        db = app.config['DATABASE']
    else:
        dataset = "debug.xml"

    PUB_TYPES = ["Conference Papers", "Journals", "Books", "Book Chapters", "All Publications"]
    args = {"dataset": dataset, "id": "coauthors"}
    args["title"] = "Co-Authors"

    column = "0a"

    if debug is None and "field" in request.args:
        column = request.args.get("field")

    start_year = db.min_year
    if debug is None and "start_year" in request.args:
        start_year = int(request.args.get("start_year"))

    end_year = db.max_year
    if debug is None and "end_year" in request.args:
        end_year = int(request.args.get("end_year"))

    pub_type = 4
    if debug is None and "pub_type" in request.args:
        pub_type = int(request.args.get("pub_type"))

    args["data"] = db.get_coauthor_data(start_year, end_year, pub_type, column[:1], column[-1:])
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_type"] = pub_type
    args["min_year"] = db.min_year
    args["max_year"] = db.max_year
    args["start_year"] = start_year
    args["end_year"] = end_year
    args["pub_str"] = PUB_TYPES[pub_type]

    if debug is not None:
        return "OK"

    return render_template("coauthors.html", args=args)


@app.route("/")
def showStatisticsMenu():
    dataset = app.config['DATASET']
    args = {"dataset": dataset}
    return render_template('statistics.html', args=args)


@app.route("/statisticsdetails/<status>")
def showPublicationSummary(status, debug=None, db=None):
    if debug is None:
        dataset = app.config['DATASET']
        db = app.config['DATABASE']
    else:
        dataset = "debug.xml"

    args = {"dataset": dataset, "id": status}
    column = "0a"

    if debug is None and "field" in request.args:
        column = request.args.get("field")

    if (status == "publication_summary"):
        args["title"] = "Publication Summary"
        args["data"] = db.get_publication_summary(column[:1], column[-1:])
        args["url"] = "publication_summary"

    if (status == "publication_author"):
        args["title"] = "Author Publication"
        args["data"] = db.get_publications_by_author(column[:1], column[-1:])
        args["url"] = "publication_author"

    if (status == "publication_year"):
        args["title"] = "Publication by Year"
        args["data"] = db.get_publications_by_year(column[:1], column[-1:])
        args["url"] = "publication_year"

    if (status == "author_year"):
        args["title"] = "Author by Year"
        args["data"] = db.get_author_totals_by_year(column[:1], column[-1:])
        args["url"] = "author_year"

    if (status == "author_summary"):
        args["title"] = "Author Summary"
        args["data"] = db.get_numbers_by_author(column[:1], column[-1:])
        args["url"] = "author_summary"

    if (status == "conf_paper_summary"):
        args["title"] = "Conference Papers Summary"
        args["data"] = db.get_numbers_by_author_type(0, column[:1], column[-1:])
        args["url"] = "conf_paper_summary"

    if (status == "journals_summary"):
        args["title"] = "Journals Summary"
        args["data"] = db.get_numbers_by_author_type(1, column[:1], column[-1:])
        args["url"] = "journals_summary"

    if (status == "books_summary"):
        args["title"] = "Books Summary"
        args["data"] = db.get_numbers_by_author_type(2, column[:1], column[-1:])
        args["url"] = "books_summary"

    if (status == "book_chapters_summary"):
        args["title"] = "Book Chapters Summary"
        args["data"] = db.get_numbers_by_author_type(3, column[:1], column[-1:])
        args["url"] = "book_chapters_summary"

    if debug is not None:
        return "OK"

    return render_template('statistics_details.html', args=args)


@app.route("/search")
def showsearch(debug=None, db=None):
    if debug is None:
        dataset = app.config['DATASET']
        db = app.config['DATABASE']
    else:
        dataset = "debug.xml"

    args = {"dataset": dataset, "id": "search"}
    args["title"] = "Search"
    args["data"] = []

    name = ""

    if debug is None and "author_name" in request.args:
        name = request.args.get("author_name")
        args["data"] = db.search_by_author(name)

    if debug is not None:
        return "OK"

    data = db.search_by_author(name)

    if len(data[1]) == 1:
        args = {"dataset": dataset, "id": data[1][0][0]}
        args["title"] = data[1][0][0]
        args["data"] = []
        args["data"] = db.get_stats_by_author(data[1][0][0])
        return render_template('stats_author.html', args=args)


    return render_template('search.html', args=args)


@app.route("/stats_author/<name>")
def showStatsByAuthor(name, debug=None, db=None):
    if debug is None:
        dataset = app.config['DATASET']
        db = app.config['DATABASE']
    else:
        dataset = "debug.xml"

    args = {"dataset": dataset, "id": name}
    args["title"] = name
    args["data"] = []

    args["data"] = db.get_stats_by_author(name)

    if debug is not None:
        return "OK"

    return render_template('stats_author.html', args=args)

@app.route("/separationDegrees")
def showSeparationDegrees(debug=None, db=None):

    if debug is None:
        dataset = app.config['DATASET']
        db = app.config['DATABASE']
    else:
        dataset = "debug.xml"

    args = {"dataset": dataset, "id": "separationDegrees"}

    authors = db.get_all_authors()
    auth = []

    for a in range(len(authors)):
        auth.append(authors[a])
        auth.sort()

    args["authors"] = auth
    args["title"] = "Separation Degrees between two Authors"
    args["url"] = "separationDegrees"

    args["data"] = []

    if debug is None and "author1" in request.args and "author2" in request.args:
        author1 = request.args.get("author1")
        author2 = request.args.get("author2")
        args["data"] = db.get_seperation_degree_between_two_authors(author1, author2)

    print(args["data"])

    if debug is not None:
        return "OK"

    return render_template('separationDegrees.html', args=args)