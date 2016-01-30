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
class Q2Process extends DatabaseProcess {

	static private final File ATTEMPTS_IN_FILE = getInputFile("attempts");
	static private final File PEOPLE_IN_FILE = getInputFile("people");
	static private final File PROBLEMS_IN_FILE = getInputFile("problems");


	static private final String ATTEMPTS_TABLE_NAME = "ATTEMPTS";
	static private final String PEOPLE_TABLE_NAME = "PEOPLE";
	static private final String PROBLEMS_TABLE_NAME = "PROBLEMS";


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

	static private final String PROBLEM_ID_NAME = "ID";
	static private final String PROBLEM_OP_NAME = "OPERATOR";
	static private final String PROBLEM_ARG1_NAME = "ARG1";
	static private final String PROBLEM_ARG2_NAME = "ARG2";


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

	static private final String PROBLEMS_TABLE_CREATION_ARGS
			= PROBLEM_ID_NAME + " integer NOT NULL, "
			+ PROBLEM_ARG1_NAME + " integer NOT NULL, "
			+ PROBLEM_OP_NAME + " char(1), "
			+ PROBLEM_ARG2_NAME + " integer NOT NULL";


	private Database database;
	private CSVHandler csvHandler;

	private InputTable attemptsInputTable = new InputTable();
	private InputTable peopleInputTable = new InputTable();
	private InputTable problemsInputTable = new InputTable();


	private List<Problem> problems = new ArrayList<Problem>();

	private class Problem
	{
		private int id;
		private String op;
		private int arg1;
		private int arg2;
		private int answer;

		// General Java toString method
		public String toString() {

			return "Problem-" + id + " (" + arg1 + " " + op + " " + arg2 + ")";
		}

		// Construct Problem object from current state of object representing
		// results of "SELECT" query. This results object will correspond to a
		// particular row in the table. The constructed object is added to the
		// relevant array.
		Problem(ResultSet results) throws SQLException {

			id = results.getInt(PROBLEM_ID_NAME);
			op = results.getString(PROBLEM_OP_NAME);
			arg1 = results.getInt(PROBLEM_ARG1_NAME);
			arg2 = results.getInt(PROBLEM_ARG2_NAME);

			if (op.equals("+")) {
				answer = arg1 + arg2;
			} else if (op.equals("-")) {
				answer = arg1 - arg2;
			} else if (op.equals("*")) {
				answer = arg1 * arg2;
			} else if (op.equals("/")) {
				answer = arg1 / arg2;
			}

			problems.add(this);

		}

		// Render problem as a line in the output CSV file
		void print(CSVPrinter printer) throws IOException {

			printer.printRecord(id, op, arg1, arg2);
		}
	}

	private List<Attempt> attempts = new ArrayList<Attempt>();

	private class Attempt {
		private int personID;
		private int problemID;
		private int answer;

		Attempt(ResultSet results) throws SQLException
		{
			personID = results.getInt(ATTEMPTS_PERSONID_NAME);
			problemID = results.getInt(ATTEMPTS_PROBLEMID_NAME);
			answer = results.getInt(ATTEMPTS_ANSWER_NAME);

			attempts.add(this);
		}
	}

	private List<People> people = new ArrayList<People>();

	private class People
	{
		private int id;
		private int totalDone;
		private double donePerc;
		private int corrNum;
		private double doneCorrPerc;
		private double totalCorrPerc;
		private String lastName;
		private String firstName;
		private String postal;

		People(ResultSet results) throws SQLException
		{
			id = results.getInt("ID");
			lastName = results.getString("LASTNAME");
			firstName = results.getString("FIRSTNAME");
			postal = results.getString("POSTAL");

			people.add(this);
		}

		void print(CSVPrinter printer) throws IOException
		{
			if (totalDone > 0)
			{
				printer.printRecord(lastName, firstName, postal, totalDone, String.format("%.0f", donePerc),
						corrNum, String.format("%.0f", doneCorrPerc),
						String.format("%.0f",totalCorrPerc));
			}
		}

	}

	// Implementation of the "readInput" method as specified by the base-class.
	protected void readInput() throws IOException {

		attemptsInputTable.readFromFile(csvHandler, ATTEMPTS_IN_FILE);
		peopleInputTable.readFromFile(csvHandler, PEOPLE_IN_FILE);
		problemsInputTable.readFromFile(csvHandler, PROBLEMS_IN_FILE);

	}

	// Implementation of the "runCoreProcess" method as specified by the base-class.
	protected void runCoreProcess() throws SQLException {

		database.createTable(ATTEMPTS_TABLE_NAME, ATTEMPTS_TABLE_CREATION_ARGS);
		database.createTable(PEOPLE_TABLE_NAME, PEOPLE_TABLE_CREATION_ARGS);
		database.createTable(PROBLEMS_TABLE_NAME, PROBLEMS_TABLE_CREATION_ARGS);

		attemptsInputTable.writeToDatabase(database, ATTEMPTS_TABLE_NAME);
		peopleInputTable.writeToDatabase(database, PEOPLE_TABLE_NAME);
		problemsInputTable.writeToDatabase(database, PROBLEMS_TABLE_NAME);



		String SELECT_ALL_PROBLEM = "SELECT * FROM PROBLEMS";
		ResultSet results = database.executeQuery(SELECT_ALL_PROBLEM);

		while (results.next())
		{
			new Problem(results);
		}

		String SELECT_ALL_ATTEPMTS = "SELECT * FROM ATTEMPTS";
		results = database.executeQuery(SELECT_ALL_ATTEPMTS);

		while (results.next())
		{
			new Attempt(results);
		}

		String SELECT_ALL_PEOPLE = "SELECT * FROM PEOPLE";
		results = database.executeQuery(SELECT_ALL_PEOPLE);

		while (results.next())
		{
			new People(results);
		}



		for(int i =0; i < attempts.size(); i++)
		{
			int proID = attempts.get(i).problemID;
			int personID = attempts.get(i).personID - 1;

			people.get(personID).id = attempts.get(i).personID;
			if(attempts.get(i).answer == problems.get(proID-1).answer)
			{
				people.get(personID).totalDone ++;
				people.get(personID).corrNum ++;
			}
			else
			{
				people.get(personID).totalDone ++;
			}
			people.get(personID).donePerc = 100.0 * people.get(personID).totalDone / problems.size();
			people.get(personID).doneCorrPerc = 100.0 * people.get(personID).corrNum / people.get(personID).totalDone;
			people.get(personID).totalCorrPerc = 100.0 * people.get(personID).corrNum / problems.size();
		}


		//CREATE_SCORE_TABLE
		String SCORE_TABLE_NAME = "SCORE";
		String SCORE_TABLE_CREATION_ARGS
				= "ID INTEGER NOT NULL, LASTNAME  varchar(255), FIRSTNAME varchar(255), POSTAL varchar(255), "
				+ "TOTALDONE integer NOT NULL, DONEPERC FLOAT NOT NULL, CORRNUM integer NOT NULL, "
				+ "DONECORRPERC FLOAT NOT NULL, TOTALCORRPERC FLOAT NOT NULL";
		database.createTable(SCORE_TABLE_NAME, SCORE_TABLE_CREATION_ARGS);

		for(People people1 : people)
		{
			String add = people1.id + ", '" + people1.lastName + "', '" + people1.firstName + "', '" + people1.postal + "', "
					+ people1.totalDone + ", " + people1.donePerc + ", " + people1.corrNum + ", "
					+ people1.doneCorrPerc + ", " + people1.totalCorrPerc;
			database.addTableRow(SCORE_TABLE_NAME, add);
		}

//		ORDER BY POSTAL
		String POSTAL_ORDER = "SELECT * FROM SCORE WHERE TOTALDONE > 0 ORDER BY POSTAL, DONECORRPERC, TOTALCORRPERC";
		results = database.executeQuery(POSTAL_ORDER);
		int i = 0;
		while (results.next())
		{
			people.get(i).id = results.getInt("ID");
			people.get(i).lastName = results.getString("LASTNAME");
			people.get(i).firstName = results.getString("FIRSTNAME");
			people.get(i).postal = results.getString("POSTAL");
			people.get(i).totalDone = results.getInt("TOTALDONE");
			people.get(i).donePerc = results.getDouble("DONEPERC");
			people.get(i).corrNum = results.getInt("CORRNUM");
			people.get(i).doneCorrPerc = results.getDouble("DONECORRPERC");
			people.get(i).totalCorrPerc = results.getDouble("TOTALCORRPERC");
			i ++;
		}

////		ORDER BY DONECORRPERC
//		String DONECORRPERC_ORDER = "SELECT * FROM SCORE ORDER BY DONECORRPERC";
//		results = database.executeQuery(DONECORRPERC_ORDER);
//
//		while (results.next())
//		{
//			new People(results);
//			people.get(i).totalDone = results.getInt("TOTALDONE");
//			people.get(i).donePerc = results.getDouble("DONEPERC");
//			people.get(i).corrNum = results.getInt("CORRNUM");
//			people.get(i).doneCorrPerc = results.getDouble("DONECORRPERC");
//			people.get(i).totalCorrPerc = results.getDouble("TOTALCORRPERC");
//			i ++;
//		}
//
////		Order BY TOTALCORRPERC
//		String TOTALCORRPERC_ORDER = "SELECT * FROM SCORE ORDER BY TOTALCORRPERC";
//		results = database.executeQuery(TOTALCORRPERC_ORDER);
//
//		while (results.next())
//		{
//			new People(results);
//			people.get(i).totalDone = results.getInt("TOTALDONE");
//			people.get(i).donePerc = results.getDouble("DONEPERC");
//			people.get(i).corrNum = results.getInt("CORRNUM");
//			people.get(i).doneCorrPerc = results.getDouble("DONECORRPERC");
//			people.get(i).totalCorrPerc = results.getDouble("TOTALCORRPERC");
//			i ++;
//		}


	}

	// Implementation of the "writeOutput" method as specified by the base-class.
	protected void writeOutput() throws IOException {

		File outCSVFile = getOutputFile();

		CSVPrinter printer = csvHandler.createPrinter(outCSVFile);

		for (People people1 : people)
		{
			people1.print(printer);
		}

	}

	// Constructor.
	Q2Process(Database database, CSVHandler csvHandler) {

		this.database = database;
		this.csvHandler = csvHandler;
	}
}
