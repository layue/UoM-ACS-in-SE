/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package javaatm;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

/**
 *
 * @author Cuong Tran
 */
public class JavaATM {

    private myGUIDialog atmDialog;
    private Bank bank;
    private String accno;


    private class CardReader {

        /**
         * Simulate card reading operation.
         *
         * @return an account number
         */
        public String readAccountNo () {
            String[] accno = { "1111", "2222" };

            Random r = new Random ();

            return accno[ r.nextInt(2) ];

        }
    }

    public JavaATM(myGUIDialog atmDialogid, Bank bankid) {

        this.bank = bankid;
        this.atmDialog = atmDialogid;

        CardReader reader = this.new CardReader();
        this.accno = reader.readAccountNo();

        atmDialogid.accno.setText("Account Number: " + accno);

        atmDialog.balanceButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    int balance = bank.balance(accno);
                    atmDialog.balanceLabel.setText(String.valueOf(balance));
                } catch (Exception e1) {
                    e1.printStackTrace();
                }
            }
        });

        atmDialog.withdrawButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    int withdraw = Integer.parseInt(atmDialog.amount.getText());
                    bank.withdraw(accno, withdraw);

                    int balance = bank.balance(accno);
                    atmDialog.balanceLabel.setText(String.valueOf(balance));
                } catch (Exception e1) {
                    e1.printStackTrace();
                }
            }
        });

        atmDialog.depositButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    int deposit = Integer.parseInt(atmDialog.amount.getText());
                    bank.deposit(accno,deposit);

                    int balance = bank.balance(accno);
                    atmDialog.balanceLabel.setText(String.valueOf(balance));
                } catch (Exception e1) {
                    e1.printStackTrace();
                }
            }
        });

        atmDialog.setVisible(true);
    }
}
