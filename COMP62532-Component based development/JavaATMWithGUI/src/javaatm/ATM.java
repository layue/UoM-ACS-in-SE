package javaatm;

/**
 * Created by X on 03/02/16.
 */
public class ATM {
    public static void main(String[] args) {
        myGUIDialog ATMDialog = new myGUIDialog();
        Bank bank = new Bank();

        new JavaATM (ATMDialog, bank);
    }
}
