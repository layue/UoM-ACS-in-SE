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
class Q3Process extends DatabaseProcess {

    static private final File ATTEMPTS_IN_FILE = getInputFile("attempts");
    static private final File PROBLEMS_IN_FILE = getInputFile("problems");


    static private final String ATTEMPTS_TABLE_NAME = "ATTEMPTS";
    static private final String PROBLEMS_TABLE_NAME = "PROBLEMS";


    static private final String ATTEMPTS_PERSONID_NAME = "PERSONID";
    static private final String ATTEMPTS_PROBLEMID_NAME = "PROBLEMID";
    static private final String ATTEMPTS_ANSWER_NAME = "ANSWER";

    static private final String PROBLEM_ID_NAME = "ID";
    static private final String PROBLEM_OP_NAME = "OPERATOR";
    static private final String PROBLEM_ARG1_NAME = "ARG1";
    static private final String PROBLEM_ARG2_NAME = "ARG2";


    static private final String ATTEMPTS_TABLE_CREATION_ARGS
            = ATTEMPTS_PERSONID_NAME + " integer NOT NULL, "
            + ATTEMPTS_PROBLEMID_NAME + " integer NOT NULL, "
            + ATTEMPTS_ANSWER_NAME + " integer NOT NULL";

    static private final String PROBLEMS_TABLE_CREATION_ARGS
            = PROBLEM_ID_NAME + " integer NOT NULL, "
            + PROBLEM_ARG1_NAME + " integer NOT NULL, "
            + PROBLEM_OP_NAME + " char(1), "
            + PROBLEM_ARG2_NAME + " integer NOT NULL";


    private Database database;
	private CSVHandler csvHandler;


    private InputTable attemptsInputTable = new InputTable();
    private InputTable problemsInputTable = new InputTable();


    private List<Problem> problems = new ArrayList<Problem>();

    private class Problem
    {
        private int id;
        private String op;
        private int arg1;
        private int arg2;
        private int answer;
        private int donepeople;
        private int rightpeople;

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

            printer.printRecord(id, donepeople, donepeople == 0 ? 0 : String.format("%.0f", (double)100 * rightpeople / donepeople));
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

	// Implementation of the "readInput" method as specified by the base-class.
	protected void readInput() throws IOException {

        attemptsInputTable.readFromFile(csvHandler, ATTEMPTS_IN_FILE);
        problemsInputTable.readFromFile(csvHandler, PROBLEMS_IN_FILE);

	}

	// Implementation of the "runCoreProcess" method as specified by the base-class.
	protected void runCoreProcess() throws SQLException {

        database.createTable(ATTEMPTS_TABLE_NAME, ATTEMPTS_TABLE_CREATION_ARGS);
        database.createTable(PROBLEMS_TABLE_NAME, PROBLEMS_TABLE_CREATION_ARGS);


        attemptsInputTable.writeToDatabase(database, ATTEMPTS_TABLE_NAME);
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


        for(int i = 0; i < attempts.size(); i++)
        {
            int proID = attempts.get(i).problemID - 1;
            if (attempts.get(i).answer == problems.get(proID).answer)
            {
                problems.get(proID).rightpeople ++;
            }
            problems.get(proID).donepeople ++;
        }

	}

	// Implementation of the "writeOutput" method as specified by the base-class.
	protected void writeOutput() throws IOException {

        File outCSVFile = getOutputFile();

        CSVPrinter printer = csvHandler.createPrinter(outCSVFile);

        for (Problem problem : problems)
        {
            problem.print(printer);
        }
	}

	// Constructor.
	Q3Process(Database database, CSVHandler csvHandler) {

		this.database = database;
		this.csvHandler = csvHandler;
	}
}
