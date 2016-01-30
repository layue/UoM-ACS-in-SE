package uk.ac.manchester.cs.msc.ssd.core;

import java.io.*;
import java.sql.*;

/*
 * Represents a process involving the setting up and accessing of
 * a database.
 */
public abstract class DatabaseProcess {

	static private final String IN_FILES_PATH = "files/in";
	static private final String OUT_FILES_PATH = "files/out";

	static private final String CSV_EXTENSION = ".csv";

	/**
	 * Provides a file located in the input-files directory.
	 *
	 * @param name Name of required file
	 * @return File in input-files directory with specified name
	 */
	static public File getInputFile(String name) {

		return getCSVFile(IN_FILES_PATH, name);
	}

	static private File getCSVFile(String path, String name) {

		return new File(path, name + CSV_EXTENSION);
	}

	/**
	 * Main method for running the relevant process. Invokes, in
	 * turn, the <code>readInput</code>, <code>runCoreProcess</code>
	 * and <code>writeOutput</code> methods.
	 *
	 * @throws IOException if any file-system access error occurs
	 * @throws SQLException if any database access error occurs
	 */
	public void run() throws IOException, SQLException {

		log("EXECUTING");

		readInput();
		runCoreProcess();
		writeOutput();

		log("FINISHED");
	}

	/**
	 * Abstract method whose implementations will read in any required
	 * CSV files.
	 *
	 * @throws IOException if any file-system access error occurs
	 */
	protected abstract void readInput() throws IOException;

	/**
	 * Abstract method whose implementations will execute the core
	 * process that will involve all required database acccess.
	 *
	 * @throws SQLException if any database access error occurs
	 */
	protected abstract void runCoreProcess() throws SQLException;

	/**
	 * Abstract method whose implementations will write out any
	 * resulting CSV files.
	 *
	 * @throws IOException if any file-system access error occurs
	 */
	protected abstract void writeOutput() throws IOException;

	/**
	 * Provides the single output file for this process. This file will
	 * be located in the output-files directory, with a name derived
	 * from the name of the relevant concrete extension of this class.
	 *
	 * @return File in output-files directory with name appropriate to
	 * this process
	 */
	protected File getOutputFile() {

		return getCSVFile(OUT_FILES_PATH, getProcessName());
	}

	private void log(String message) {

		System.out.println("\n" + message + ": " + getProcessName() + "\n");
	}

	private String getProcessName() {

		return getClass().getSimpleName();
	}
}
