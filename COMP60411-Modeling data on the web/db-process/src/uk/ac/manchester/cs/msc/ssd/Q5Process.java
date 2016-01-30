package uk.ac.manchester.cs.msc.ssd;

import java.io.*;
import java.sql.*;
import java.util.*;

import org.apache.commons.csv.*;

import uk.ac.manchester.cs.msc.ssd.core.*;

//
// THIS CLASS IS A TEMPLATE WHOSE IMPLEMENTATION SHOULD BE PROVIDED
// BY THE STUDENT IN ORDER TO PROVIDE A SOLUTION TO PROBLEM 1.
//
// THE "ExampleProcess" CLASS SHOULD BE USED AS A GUIDE IN CREATING
// THE IMPLEMENTATION.
//
class Q5Process extends DatabaseProcess {

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


	private Database database;
	private CSVHandler csvHandler;


	private InputTable attemptsInputTable = new InputTable();
	private InputTable peopleInputTable = new InputTable();


	private List<Attempt> attempts = new ArrayList<Attempt>();

	private class Attempt
	{
		private int AID;
		private int BID;

		Attempt(ResultSet results) throws SQLException
		{
			AID = results.getInt("A");
			BID = results.getInt("B");

			attempts.add(this);
		}
	}

	private List<People> people = new ArrayList<People>();

	private class People
	{
		private int id;
		private String lastName;
		private String firstName;
		private int m;

		People(ResultSet results) throws SQLException
		{
			id = results.getInt("ID");
			lastName = results.getString("LASTNAME");
			firstName = results.getString("FIRSTNAME");
			m = results.getInt("M");

			people.add(this);
		}

	}

	private List<SameAnswer> sameAnswers = new ArrayList<SameAnswer>();

	private class SameAnswer
	{
		private int AID;
		private int BID;
		private int count;
		private int m;
		private String ALN;
		private String AFN;
		private String BLN;
		private String BFN;

		SameAnswer(ResultSet results) throws SQLException
		{
			AID = -1;

			sameAnswers.add(this);
		}

		void print(CSVPrinter printer) throws IOException
		{
			if(AID != -1)
				printer.printRecord(ALN, AFN, BLN, BFN, m, count);
		}

	}


	// Implementation of the "readInput" method as specified by the base-class.
	protected void readInput() throws IOException {

		attemptsInputTable.readFromFile(csvHandler, ATTEMPTS_IN_FILE);
		peopleInputTable.readFromFile(csvHandler, PEOPLE_IN_FILE);

	}

	// Implementation of the "runCoreProcess" method as specified by the base-class.
	protected void runCoreProcess() throws SQLException {

		database.createTable(ATTEMPTS_TABLE_NAME, ATTEMPTS_TABLE_CREATION_ARGS);
		database.createTable(PEOPLE_TABLE_NAME, PEOPLE_TABLE_CREATION_ARGS);


		attemptsInputTable.writeToDatabase(database, ATTEMPTS_TABLE_NAME);
		peopleInputTable.writeToDatabase(database, PEOPLE_TABLE_NAME);


		String SELECT_ALL_PEOPLE = "SELECT ID, PEOPLE.LASTNAME, PEOPLE.FIRSTNAME, ATT.NUM AS M "
				+ "FROM PEOPLE LEFT JOIN (SELECT PERSONID, COUNT(DISTINCT PROBLEMID) AS NUM FROM ATTEMPTS GROUP BY PERSONID) AS ATT "
				+ "ON PEOPLE.ID = ATT.PERSONID";
		ResultSet results = database.executeQuery(SELECT_ALL_PEOPLE);

		while (results.next())
		{
			new People(results);
		}


		String GET_ATTEMPT_SAME = "SELECT ATTEMPTS.PERSONID AS A, AB.PERSONID AS B "
									+ "FROM ATTEMPTS JOIN ATTEMPTS AS AB "
									+ "ON ATTEMPTS.PROBLEMID = AB.PROBLEMID AND ATTEMPTS.ANSWER = AB.ANSWER AND "
									+ "ATTEMPTS.PERSONID != AB.PERSONID "
									+ "ORDER BY A, B";


		results = database.executeQuery(GET_ATTEMPT_SAME);

		while (results.next())
		{
			new Attempt(results);
			new SameAnswer(results);
		}


		sameAnswers.get(0).AID = attempts.get(0).AID;
		sameAnswers.get(0).BID = attempts.get(0).BID;
		sameAnswers.get(0).count = 1;
		int j = 0;
		for(int i = 1; i < attempts.size(); i++)
		{
			if(attempts.get(i).AID < attempts.get(i).BID)
			{
				if ((attempts.get(i).AID == attempts.get(i - 1).AID)
						&& (attempts.get(i).BID == attempts.get(i - 1).BID) )
				{
					sameAnswers.get(j).count ++;
				}
				else
				{
					j ++;
					sameAnswers.get(j).AID = attempts.get(i).AID;
					sameAnswers.get(j).BID = attempts.get(i).BID;
					sameAnswers.get(j).count ++;
				}
			}
		}


		for (int i = 0; i < j + 1; i ++)
		{
			int aID;
			int bID;
			int am;
			int bm;

			aID = sameAnswers.get(i).AID - 1;
			bID = sameAnswers.get(i).BID - 1;
			am = people.get(aID).m;
			bm = people.get(bID).m;

			sameAnswers.get(i).m = am <= bm ? am : bm;

			if(sameAnswers.get(i).count > sameAnswers.get(i).m / 2)
			{
				sameAnswers.get(i).ALN = people.get(aID).lastName;
				sameAnswers.get(i).AFN = people.get(aID).firstName;
				sameAnswers.get(i).BLN = people.get(bID).lastName;
				sameAnswers.get(i).BFN = people.get(bID).firstName;
			}
			else
				sameAnswers.get(i).AID = -1;
		}

	}

	// Implementation of the "writeOutput" method as specified by the base-class.
	protected void writeOutput() throws IOException {

		File outCSVFile = getOutputFile();

		CSVPrinter printer = csvHandler.createPrinter(outCSVFile);

		for (SameAnswer sameAnswer : sameAnswers)
		{
			sameAnswer.print(printer);
		}
	}

	// Constructor.
	Q5Process(Database database, CSVHandler csvHandler) {

		this.database = database;
		this.csvHandler = csvHandler;
	}
}
