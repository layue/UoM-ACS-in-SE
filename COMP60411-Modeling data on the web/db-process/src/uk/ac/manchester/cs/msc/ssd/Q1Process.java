package uk.ac.manchester.cs.msc.ssd;

import java.io.*;
import java.sql.*;
import java.util.*;

//import com.sun.tools.internal.xjc.reader.xmlschema.bindinfo.BIConversion;
import org.apache.commons.csv.*;

import uk.ac.manchester.cs.msc.ssd.core.*;

//
// THIS CLASS IS A TEMPLATE WHOSE IMPLEMENTATION SHOULD BE PROVIDED
// BY THE STUDENT IN ORDER TO PROVIDE A SOLUTION TO PROBLEM 1.
//
// THE "ExampleProcess" CLASS SHOULD BE USED AS A GUIDE IN CREATING
// THE IMPLEMENTATION.
//
class Q1Process extends DatabaseProcess {

	static private final File ATTEMPTS_IN_FILE = getInputFile("attempts");
    static private final File PEOPLE_IN_FILE = getInputFile("people");

    static private final String ATTEMPTS_TABLE_NAME = "ATTEMPTS";
    static private final String PEOPLE_TABLE_NAME = "PEOPLE";

    static private final String ATTEMPTS_PERSONID_NAME = "PERSONID";
    static private final String ATTEMPTS_PROBLEMID_NAME = "PROBLEMID";
    static private final String ATTEMPTS_ANSWER_NAME = "ANSWER";

    static private final String PEOPLE_PERSONID_NAME = "ID";
    static private final String PEOPLE_FIRST_NAME = "FIRSTNAME";
    static private final String PEOPLE_LAST_NAME = "LASTNAME";
    static private final String PEOPLE_COMPANY_NAME = "COMPANYNAME";
    static private final String PEOPLE_ADDRESS_NAME = "ADDRESS";
    static private final String PEOPLE_CITY_NAME = "CITY";
    static private final String PEOPLE_COUNTRY_NAME = "COUNTRY";
    static private final String PEOPLE_POSTAL_NAME = "POSTAL";
    static private final String PEOPLE_PHONE1_NAME = "PHONE1";
    static private final String PEOPLE_PHONE2_NAME = "PHONE2";
    static private final String PEOPLE_EMAIL_NAME = "EMAIL";
    static private final String PEOPLE_WEB_NAME = "WEB";

    static private final String ATTEMPTS_TABLE_CREATION_ARGS
                                    = ATTEMPTS_PERSONID_NAME + " integer NOT NULL, "
                                    + ATTEMPTS_PROBLEMID_NAME + " integer NOT NULL, "
                                    + ATTEMPTS_ANSWER_NAME + " integer NOT NULL";

    static private final String PEOPLE_TABLE_CREATION_ARGS
                                    = PEOPLE_PERSONID_NAME + " integer NOT NULL, "
                                    + PEOPLE_FIRST_NAME + " varchar(255), "
                                    + PEOPLE_LAST_NAME + " varchar(255), "
                                    + PEOPLE_COMPANY_NAME + " varchar(255), "
                                    + PEOPLE_ADDRESS_NAME + " varchar(255), "
                                    + PEOPLE_CITY_NAME + " varchar(255), "
                                    + PEOPLE_COUNTRY_NAME + " varchar(255), "
                                    + PEOPLE_POSTAL_NAME + " varchar(255), "
                                    + PEOPLE_PHONE1_NAME + " varchar(255), "
                                    + PEOPLE_PHONE2_NAME + " varchar(255), "
                                    + PEOPLE_EMAIL_NAME + " varchar(255), "
                                    + PEOPLE_WEB_NAME + " varchar(255)";

    static private final String SELECT_NUMBERS_QUERY
            = "SELECT PEOPLE.LASTNAME, PEOPLE.FIRSTNAME, ATT.NUM "
            + "FROM PEOPLE JOIN (SELECT PERSONID, COUNT(DISTINCT PROBLEMID) AS NUM FROM ATTEMPTS GROUP BY PERSONID) AS ATT "
            + "ON PEOPLE.ID = ATT.PERSONID";

//            = "SELECT PEOPLE.LASTNAME, PEOPLE.FIRSTNAME, ATTEMPTS.PROBLEMID AS NUM "
//            + "FROM PEOPLE JOIN ATTEMPTS "
//            + "ON PEOPLE.ID = ATTEMPTS.PERSONID";

//            = "(SELECT PERSONID, COUNT(PROBLEMID) "
//            + "FROM ATTEMPTS "
//            + "GROUP BY PERSONID)";


	private Database database;
	private CSVHandler csvHandler;

    private InputTable attemptsInputTable = new InputTable();
    private InputTable peopleInputTable = new InputTable();

    private List<Number> Numbers = new ArrayList<Number>();

    private class Number
    {
        private String lName;
        private String fName;
        private int num;

        Number(ResultSet results) throws SQLException
        {

            lName = results.getString(PEOPLE_LAST_NAME);
            fName = results.getString(PEOPLE_FIRST_NAME);
            num = results.getInt("NUM");
            Numbers.add(this);
        }

        void print(CSVPrinter printer) throws IOException
        {
            printer.printRecord(lName,fName,num);
        }

    }
	// Implementation of the "readInput" method as specified by the base-class.
	protected void readInput() throws IOException {

        attemptsInputTable.readFromFile(csvHandler, ATTEMPTS_IN_FILE);
        peopleInputTable.readFromFile(csvHandler, PEOPLE_IN_FILE);

//		System.out.println("readInput(): Method to be implemented");
	}

	// Implementation of the "runCoreProcess" method as specified by the base-class.
	protected void runCoreProcess() throws SQLException {

        database.createTable(ATTEMPTS_TABLE_NAME, ATTEMPTS_TABLE_CREATION_ARGS);
        database.createTable(PEOPLE_TABLE_NAME, PEOPLE_TABLE_CREATION_ARGS);

        attemptsInputTable.writeToDatabase(database, ATTEMPTS_TABLE_NAME);
        peopleInputTable.writeToDatabase(database, PEOPLE_TABLE_NAME);

        System.out.println("XUBING:" + SELECT_NUMBERS_QUERY);

        ResultSet results = database.executeQuery(SELECT_NUMBERS_QUERY);

        while (results.next())
        {
            new Number(results);
        }
//        System.out.println("runCoreProcess(): Method to be implemented");
	}

	// Implementation of the "writeOutput" method as specified by the base-class.
	protected void writeOutput() throws IOException {


        File outCSVFile = getOutputFile();

        CSVPrinter printer = csvHandler.createPrinter(outCSVFile);

        for (Number number : Numbers)
        {
            number.print(printer);
        }
// System.out.println("writeOutput(): Method to be implemented");
	}

	// Constructor.
	Q1Process(Database database, CSVHandler csvHandler) {

		this.database = database;
		this.csvHandler = csvHandler;
	}
}
