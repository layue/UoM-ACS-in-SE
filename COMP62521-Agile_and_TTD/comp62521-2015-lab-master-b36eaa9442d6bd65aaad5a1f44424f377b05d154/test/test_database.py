from os import path
from comp62521 import app
import unittest
from comp62521.database import database
from comp62521.views import format_data, showAverages, showCoAuthors, showPublicationSummary, showsearch


class TestDatabase(unittest.TestCase):
    def setUp(self):
        dir, _ = path.split(__file__)
        self.data_dir = path.join(dir, "..", "data")

    def test_read(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        self.assertEqual(len(db.publications), 1)

    def test_read_invalid_xml(self):
        db = database.Database()
        self.assertFalse(db.read(path.join(self.data_dir, "invalid_xml_file.xml")))

    def test_read_missing_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_year.xml")))
        self.assertEqual(len(db.publications), 0)

    def test_read_missing_title(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "missing_title.xml")))
        # publications with missing titles should be added
        self.assertEqual(
            len(db.publications), 1)

    def test_get_average_authors_per_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-1.xml")))
        _, data = db.get_average_authors_per_publication(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.3, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 2, places=1)
        _, data = db.get_average_authors_per_publication(database.Stat.MODE)
        self.assertEqual(data[0], [2])

    def test_get_average_publications_per_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-2.xml")))
        _, data = db.get_average_publications_per_author(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 1.5, places=1)
        _, data = db.get_average_publications_per_author(database.Stat.MODE)
        self.assertEqual(data[0], [0, 1, 2, 3])

    def test_get_average_publications_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-3.xml")))
        _, data = db.get_average_publications_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.5, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_publications_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [3])

    def test_get_average_authors_in_a_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        _, data = db.get_average_authors_in_a_year(database.Stat.MEAN)
        self.assertAlmostEqual(data[0], 2.8, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MEDIAN)
        self.assertAlmostEqual(data[0], 3, places=1)
        _, data = db.get_average_authors_in_a_year(database.Stat.MODE)
        self.assertEqual(data[0], [0, 2, 4, 5])
        # additional test for union of authors
        self.assertEqual(data[-1], [0, 2, 4, 5])

    def test_get_publication_summary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data[0]), 6,
                         "incorrect number of columns in data")
        self.assertEqual(len(data), 2,
                         "incorrect number of rows in data")
        self.assertEqual(data[0][1], 1,
                         "incorrect number of publications for conference papers")
        self.assertEqual(data[1][1], 2,
                         "incorrect number of authors for conference papers")

    def test_get_average_authors_per_publication_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "three-authors-and-three-publications.xml")))
        header, data = db.get_average_authors_per_publication_by_author(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
                         "incorrect average of number of conference papers")
        self.assertEqual(data[0][1], 1.5,
                         "incorrect mean journals for author1")
        self.assertEqual(data[1][1], 2,
                         "incorrect mean journals for author2")
        self.assertEqual(data[2][1], 1,
                         "incorrect mean journals for author3")

    def test_get_publications_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
                         "incorrect number of authors")
        self.assertEqual(data[0][-1], 1,
                         "incorrect total")

    def test_get_average_publications_per_author_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_average_publications_per_author_by_year(database.Stat.MEAN)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
                         "incorrect year in result")

    def test_get_publications_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
                         "incorrect year in result")

    def test_get_author_totals_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect number of rows")
        self.assertEqual(data[0][0], 9999,
                         "incorrect year in result")
        self.assertEqual(data[0][1], 2,
                         "incorrect number of authors in result")

    ####################################################################################################################
    #                                                     VIEWS TESTS                                                  #
    ####################################################################################################################

    def test_format_data(self):
        list = [3.1416, 1.1693]
        numList = [[10.9999, 11.9999, 12.9999]]
        result = format_data(list)
        self.assertEqual(['3.14', '1.17'], result, "Data wrong formatted!")
        result = format_data(numList)
        self.assertEqual(['11, 12, 13'], result, "Data wrong formatted!")

    def test_showAverages(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        self.assertEqual("OK", showAverages("Y", db), "The Averages page run failed...")

    def test_showCoAuthors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        self.assertEqual("OK", showCoAuthors("Y", db), "The Co-Authors page run failed...")

    def test_showPublicationSummary(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        self.assertEqual("OK", showPublicationSummary("publication_summary", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("publication_author", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("publication_year", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("author_year", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("author_summary", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("conf_paper_summary", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("journals_summary", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("books_summary", "Y", db),
                         "Publication Summary page failed")
        self.assertEqual("OK", showPublicationSummary("book_chapters_summary", "Y", db),
                         "Publication Summary page failed")

    def test_showsearch_v(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        self.assertEqual("OK", showsearch("Y", db), "The Search page run failed...")

    ####################################################################################################################
    #                                                    SPRINT TESTS                                                  #
    ####################################################################################################################

    def test_get_numbers_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        header, data = db.get_numbers_by_author()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 7,
                         "incorrect number of rows")
        self.assertEqual([data[6][1]] + [data[6][2]], [2, 2],
                         "incorrect numbers of times in result")

    def test_get_numbers_by_author_2(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_numbers_by_author()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 6,
                         "incorrect number of authors")
        self.assertEqual(data[0][-2], 2,
                         "incorrect amount normal!")
        header, data = db.get_numbers_by_author("0", "d")
        self.assertEqual(data[0][-2], 1,
                         "incorrect amount descending sort!")
        header, data = db.get_numbers_by_author("0", "a")
        self.assertEqual(data[0][-2], 2,
                         "incorrect amount ascending sort!")
        header, data = db.get_numbers_by_author("1", "d")
        self.assertEqual(data[0][-2], 1,
                         "incorrect amount descending sort!")
        header, data = db.get_numbers_by_author("1", "a")
        self.assertEqual(data[0][-2], 1,
                         "incorrect amount ascending sort!")

    def test_get_publications_by_author_s1(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_publications_by_author()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 6,
                         "incorrect number of authors")
        self.assertEqual(data[0][-1], 3,
                         "incorrect amount")
        header, data = db.get_publications_by_author("0", "d")
        self.assertEqual(data[0][-1], 1,
                         "incorrect amount")
        header, data = db.get_publications_by_author("0", "a")
        self.assertEqual(data[0][-1], 3,
                         "incorrect amount")
        header, data = db.get_publications_by_author("1", "d")
        self.assertEqual(data[0][-1], 3,
                         "incorrect amount")
        header, data = db.get_publications_by_author("1", "a")
        self.assertEqual(data[0][-1], 1,
                         "incorrect amount")

    def test_get_publication_summary_s1(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_publication_summary()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 2,
                         "incorrect table structure")
        self.assertEqual(data[0][-1], 5,
                         "incorrect amount")
        header, data = db.get_publication_summary("0", "a")
        self.assertEqual(data[0][-1], 6,
                         "incorrect amount")
        header, data = db.get_publication_summary("0", "d")
        self.assertEqual(data[0][-1], 5,
                         "incorrect amount")

    def test_get_publication_summary_average(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_publication_summary_average(2)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")

    def test_get_average_authors_per_publication_by_year(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_average_authors_per_publication_by_year(2)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")

    def test_get_publications_by_year_s1(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple3.xml")))
        header, data = db.get_publications_by_year()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 1,
                         "incorrect table structure")
        self.assertEqual(data[0][-1], 5,
                         "incorrect amount")
        header, data = db.get_publications_by_year("0", "a")
        self.assertEqual(data[0][-1], 5,
                         "incorrect amount")
        header, data = db.get_publications_by_year("0", "d")
        self.assertEqual(data[0][-1], 5,
                         "incorrect amount")

    def test_get_author_totals_by_year_s1(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple4.xml")))
        header, data = db.get_author_totals_by_year()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 3,
                         "incorrect table structure")
        self.assertEqual(data[0][-1], 2,
                         "incorrect amount")
        header, data = db.get_author_totals_by_year("0", "a")
        self.assertEqual(data[0][-1], 2,
                         "incorrect amount")
        header, data = db.get_author_totals_by_year("0", "d")
        self.assertEqual(data[0][-1], 6,
                         "incorrect amount")

    def test_get_network_data(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple4.xml")))
        nodes, links = db.get_network_data()
        self.assertEquals(len(nodes), 6,
                          "incorrect amount of nodes")
        self.assertEquals(len(links), 3,
                          "incorrect amount of links")

    ## MODIFIED FOR SPRINT 2 ##

    def test_get_coauthor_details(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        details = db.get_coauthor_details("AUTHOR1 F")
        self.assertEqual(details[-1][0], "AUTHOR6 A",
                         "incorrect data of coauthors")

    def test_get_coauthor_data(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        header, data = db.get_coauthor_data(100, 10000, 4)
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        header, data = db.get_coauthor_data(100, 10000, 4, "0", "d")
        self.assertEqual(len(data), 6,
                         "incorrect number of authors")
        header, data = db.get_coauthor_data(100, 10000, 4, "1", "d")
        self.assertEqual(len(data), 6,
                         "incorrect number of authors")
        header, data = db.get_coauthor_data(100, 10000, 4, "0", "a")
        self.assertEqual(len(data), 6,
                         "incorrect number of authors")
        header, data = db.get_coauthor_data(100, 10000, 4, "1", "a")
        self.assertEqual(len(data), 6,
                         "incorrect number of authors")

    def test_get_all_authors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        keys = db.get_all_authors()
        self.assertEqual(len(keys), 6,
                         "incorrect number of authors")

    ## MODIFIED FOR SPRINT 2 ##

    def test_get_numbers_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "sprint-2-acceptance-4.xml")))
        header, data = db.get_numbers_by_author()
        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(len(data), 7,
                         "incorrect number of rows")
        self.assertEqual(data[0][-1], 2,
                         "incorrect numbers of times in result2")

    def test_search_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_sample.xml")))
        header, data = db.search_by_author("Piero Fraternali")
        header, data2 = db.search_by_author("sfdsgjfdgdfgfd")
        self.assertEqual(len(data), 1, "incorrect number of rows")
        self.assertEqual(data, [["Piero Fraternali"]])
        self.assertEqual(data2, [["Nothing found"]])

    ## TEST FOR SPRINT 3 - STORY 1 ##

    def test_get_numbers_by_author_ordered(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        header, data = db.get_numbers_by_author("1", "d")
        self.assertEqual(data[1], ["AUTHOR6 A", 1, 1, 0])

    ## TEST FOR SPRINT 3 - STORY 2 ##

    def test_get_numbers_by_author_by_publication(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "simple5.xml")))
        header, data = db.get_numbers_by_author_type(0, "0", "a")
        self.assertEqual(data[-1], ["AUTHOR1 F", 1, 5, 0], "Error in ascending by name")
        header, data = db.get_numbers_by_author_type(0, "0", "d")
        self.assertEqual(data[-1], ["AUTHOR6 A", 1, 1, 0], "Error in descending by name")
        header, data = db.get_numbers_by_author_type(0, "1", "a")
        self.assertEqual(data[-1], ["AUTHOR2 E", 4, 1, 0], "Error in ascending not by name")
        header, data = db.get_numbers_by_author_type(0, "1", "d")
        self.assertEqual(data[-1], ["AUTHOR4 C", 0, 1, 0], "Error in descending not by name")

    ## TEST FOR SPRINT 3 - STORY 4 ##

    def test_get_search_results(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "search-tester.xml")))
        header, data = db.search_by_author("")
        self.assertEqual(len(data), 21, "Wrong number of authors in search result. Should be 19")
        header, data = db.search_by_author("sam")
        self.assertEqual(len(data), 17, "Wrong number of authors in search result. Should be 15")
        header, data = db.search_by_author("sam")
        self.assertEqual(data[0], ["Alice Sam"], "Wrong order of results in search,"
                                                 " found data from: " + data[0][0])

    def test_get_stats_by_author(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_2000_2005_114_papers.xml")))
        header, data, coAuthorNamesKeys = db.get_stats_by_author("Alon Y. Halevy")

        self.assertEqual(len(header), len(data[0]),
                         "header and data column size doesn't match")
        self.assertEqual(data[0], ["Number of publications", 71, 39, 31, 0, 1],
                         "Wrong result for number of publications")
        self.assertEqual(data[1], ["Number of times first author", 9, 5, 4, 0, 0],
                         "Wrong result for number of times first author")
        self.assertEqual(data[2], ["Number of times last author", 21, 12, 8, 0, 1],
                         "Wrong result for number of times last author")
        self.assertEqual(data[3], ["Number of times sole author", 9, 3, 6, 0, 0],
                         "Wrong result for number of times sole author")
        self.assertEqual(data[4], ["Number of co-authors", 80, '-', '-', '-', '-'],
                         "Wrong result for number of co-authors")

    def test_get_seperation_degree_between_two_authors(self):
        db = database.Database()
        self.assertTrue(db.read(path.join(self.data_dir, "dblp_curated_separations.xml")))
        header, degree = db.get_seperation_degree_between_two_authors("Caroline Jay", "Robert Haines")
        self.assertEqual(len(header), len(degree),
                         "header and data column size doesn't match")
        self.assertEqual(degree[-1], 2,
                         "Wrong result for degrees of separation")
        header, degree = db.get_seperation_degree_between_two_authors("Alan R. Williams", "Roger J. Hubbold")
        self.assertEqual(degree[-1], 3,
                         "Wrong result for degrees of separation")

if __name__ == '__main__':
    unittest.main()
