package uk.ac.manchester.cs.msc.ssd.domcalc.impl;

import java.io.File;

import org.w3c.dom.Document;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import uk.ac.manchester.cs.msc.ssd.domcalc.SchemaValidator;

import javax.lang.model.element.Element;

/**
 * Author: Matthew Horridge<br>
 * The University of Manchester<br>
 * Bio-Health Informatics Group<br>
 * Date: 29-Sep-2011
 */
public class CalculatorImpl {

    /**
     * ZERO ARGUMENT CONSTRUCTOR - VERY IMPORTANT! DO NOT ALTER
     */
    public CalculatorImpl() {
    }

    /**
     * Computes the result to a calculation that is specified by an XML document
     *
     * @param schemaFile File containing RNC schema
     * @param testFile   File containing test XML document
     * @param testDoc    is the DOM representation of the test XML document
     * @return The result of the calculation.
     */

    private String[] Stack = new String[100];
    int Loc = -1;
    int count = 0;

    public int computeResult(File schemaFile, File testFile, Document testDoc) throws NumberFormatException, SAXException {


        // TODO: Implementation.

        // TODO: Validate test-file against schema using SchemaValidator class


        // TODO: Compute result

        // TODO: Return result or throw exception

        SchemaValidator schemaValidator = new SchemaValidator();
        boolean validatorResult = schemaValidator.validate(schemaFile, testFile);


        if (validatorResult == true) {
            Node rootNode = testDoc.getDocumentElement();
//            System.out.println(rootNode.getNodeName());
            Recur(rootNode);
//            for(int i = 0; i < 30; i++)
//                System.out.println(Stack[i]);
            return Integer.parseInt(Stack[0]);
        }
        else
            throw new SAXException();
    }

    private void Recur(Node node) throws SAXException {

        NodeList nodeList = node.getChildNodes();
        boolean okCal = true;
        String[] opr = new String[nodeList.getLength()];
        int num = 0;
        int count = 0;

        for (int i = 0; i < nodeList.getLength(); i++) {
            Node nodeC = nodeList.item(i);
            if (nodeC.getNodeType() == Node.ELEMENT_NODE) {
                if (nodeC.hasAttributes()) {

                    opr[num++] = nodeC.getAttributes().item(0).getNodeValue();
                } else {

                    okCal = false;
                    count ++;
                }
            }
        }

        if (count == 0 && node.getNodeName() == "expression")
        {
            Stack[0] = opr[0];
            return;
        }
        if (okCal) {
//            TODO: Calculate the result

            if (node.getNodeName() == "minus") {
                Stack[Loc] = String.valueOf(Integer.parseInt(opr[0]) - Integer.parseInt(opr[1]));
            } else if (node.getNodeName() == "plus") {
                int temp = 0;
                for (; num > 0; num--) {
                    temp += Integer.parseInt(opr[num -1]);
                }
                Stack[Loc] = String.valueOf(temp);
            } else if (node.getNodeName() == "times") {
                int temp = 1;
                for (; num > 0; num--) {
                    temp *= Integer.parseInt(opr[num - 1]);
                }
                Stack[Loc] = String.valueOf(temp);
            }

            return;
        }

        int n = 0;
        int[] args = new int[nodeList.getLength()];
        for (int i = 0; i < nodeList.getLength(); i++) {
            Node nodeC = nodeList.item(i);

            if (nodeC.getNodeType() == Node.ELEMENT_NODE) {

//                System.out.println(node.getNodeName() + "#");
                if (nodeC.hasAttributes())//args
                {
                    NamedNodeMap nodeMap = nodeC.getAttributes();

                    Stack[++Loc] = nodeMap.item(0).getNodeValue();

                } else//operator
                {
                    Stack[++Loc] = nodeC.getNodeName();
                    Recur(nodeC);
                }
                n ++;
            }
        }

        if (node.getNodeName() == "minus") {
            Stack[Loc - n] = String.valueOf(Integer.parseInt(Stack[Loc - (n - 1)]) - Integer.parseInt(Stack[Loc - (n - 2)]));
        } else if (node.getNodeName() == "plus") {
            int temp = 0;
            for (int i = 0; i < n;  i ++) {
                temp += Integer.parseInt(Stack[Loc - i]);
            }
            Stack[Loc - n] = String.valueOf(temp);
        } else if (node.getNodeName() == "times") {
            int temp = 1;
            for (int i = 0; i < n; i ++) {
                temp *= Integer.parseInt(Stack[Loc - i]);
            }
            Stack[Loc - n] = String.valueOf(temp);
        }
        Loc -= n;
    }
}
