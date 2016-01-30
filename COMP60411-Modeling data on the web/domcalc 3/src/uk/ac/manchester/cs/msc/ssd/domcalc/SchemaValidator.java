package uk.ac.manchester.cs.msc.ssd.domcalc;

import java.io.File;
import java.io.IOException;

import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;

import org.xml.sax.SAXException;

import com.thaiopensource.relaxng.jaxp.CompactSyntaxSchemaFactory;

public class SchemaValidator {

    static public boolean validate(File schemaFile, File testFile) {

		try {

			createValidator(schemaFile).validate(new StreamSource(testFile));

			return true;
		}
		catch (SAXException e) {

			return false;
		}
		catch (IOException e) {

			throw new RuntimeException("Error reading test file: " + e);
		}
	}

    static private Validator createValidator(File schemaFile) {

		try {

			SchemaFactory schemaFactory = new CompactSyntaxSchemaFactory();
			Schema schema = schemaFactory.newSchema(schemaFile);

			return schema.newValidator();
		}
		catch (SAXException e) {

			throw new RuntimeException("Error reading schema file: " + e);
		}
	}
}