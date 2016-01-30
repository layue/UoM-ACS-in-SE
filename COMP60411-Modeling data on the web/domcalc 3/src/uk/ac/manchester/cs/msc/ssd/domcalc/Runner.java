package uk.ac.manchester.cs.msc.ssd.domcalc;

import java.io.File;
import java.io.IOException;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import uk.ac.manchester.cs.msc.ssd.domcalc.impl.CalculatorImpl;

/**
 * Author: Matthew Horridge<br>
 * The University of Manchester<br>
 * Bio-Health Informatics Group<br>
 * Date: 29-Sep-2011
 */
public class Runner {

	public int run(File schemaFile, File testFile) throws IOException, SAXException, NumberFormatException {
		CalculatorImpl calculator = new CalculatorImpl();
		Document testDoc = readDOMDocument(testFile);
		return calculator.computeResult(schemaFile, testFile, testDoc);
	}

	private Document readDOMDocument(File file) throws IOException, SAXException {
		try {
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			factory.setNamespaceAware(true);
			return factory.newDocumentBuilder().parse(file);
		}
		catch (ParserConfigurationException e) {
			throw new Error("UNEXPECTED EXCEPTION!!!: " + e);
		}
	}
}
