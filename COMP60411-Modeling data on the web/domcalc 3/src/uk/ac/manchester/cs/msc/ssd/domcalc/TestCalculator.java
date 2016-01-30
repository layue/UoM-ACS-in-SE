package uk.ac.manchester.cs.msc.ssd.domcalc;

import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

/**
 * Author: Matthew Horridge<br>
 * The University of Manchester<br>
 * Bio-Health Informatics Group<br>
 * Date: 29-Sep-2011
 */
public class TestCalculator {

	public static final int SCHEMA_FILE_NAME_ARG = 0;
	public static final int TEST_FILE_NAME_ARG = 1;

	public static void main(String[] args) throws IOException, IllegalAccessException, InstantiationException, ClassNotFoundException {

		String answer = "";

		try {
			if(args.length != 2) {
				System.out.println("Invalid arguments");
				System.out.println("Expected: <schema-file> <test-file>");
				System.exit(1);
			}

			File schemaFile = new File(args[SCHEMA_FILE_NAME_ARG]);
			File testFile = new File(args[TEST_FILE_NAME_ARG]);

			answer = testFile.toString().substring(testFile.toString().lastIndexOf("_")+1,testFile.toString().lastIndexOf("."));

			Runner runner = new Runner();
			int result = runner.run(schemaFile, testFile);

			if(!answer.startsWith("err")) {
				int intAnswer = Integer.parseInt(answer);

				if(result == intAnswer) {
					System.out.println("RESULT: Correct! Expected: " + answer + ", and got: " + result);
				}
				else {
					System.out.println("RESULT: WRONG! Expected: " + answer + ", but got: " + result);
				}
			}
			else {
				if(answer.equals("errnan")) {
					System.out.println("RESULT: WRONG! Expected: " + answer + " (NumberFormatException), but got: " + result);
				}
				else if(answer.equals("errinvalid")) {
					System.out.println("RESULT: WRONG! Expected: " + answer + " (SAXException), but got: " + result);
				}
			}
		}
		catch (FileNotFoundException e) {
			System.out.println("Input file not found: " + e.getMessage());
		}
		catch (SAXException e) {
			if(answer.equals("errinvalid")) {
				System.out.println("RESULT: Correct Error!");
			}
			else {
				System.out.println("RESULT: WRONG! Expected: " + answer + ", but got errinvalid (SAXException)");
			}
		}
		catch (NumberFormatException e) {
			if(answer.equals("errnan")) {
				System.out.println("RESULT: Correct Error!");
			}
			else {
				System.out.println("RESULT: WRONG! Expected: " + answer + ", but got errnan (NumberFormatException)");
			}
		}
	}
}
