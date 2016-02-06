/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package javaatm;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Cuong Tran
 */
public class Bank {
    private ArrayList<Account> accounts= new ArrayList<Account>();
    public Bank () {
        try {
            // TODO: create two accounts (acc1, acc2) with account numbers 1111 and 2222
            // then set initial balance to them
            Account myacc = new Account();
            myacc.setBalance(100);
            myacc.setAccountNo("1111");
            accounts.add(myacc);
            Account myacc1 = new Account();
            myacc1.setBalance(123);
            myacc1.setAccountNo("2222");
            accounts.add(myacc1);
        } catch (Exception ex) {
            Logger.getLogger(Bank.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public void withdraw ( String accno, Integer amount ) throws Exception {
        // TODO: first retrieve the right account
        // then call the account to withdraw the specified amount
        Account myacc = retrieve(accno);
        myacc.withdraw(amount);
    }
    
    public void deposit ( String accno, Integer amount ) throws Exception {
        // TODO: first retrieve the right account
        // then call the account to deposit the specified amount
        Account myacc = retrieve(accno);
        myacc.deposit(amount);
    }
    
    public Integer balance ( String accno ) throws Exception {
        // TODO: first retrieve the right account
        // then call the account to check balance
        Account myacc = retrieve(accno);
        return myacc.balance();
    }
    
    /**
     * Retrieve the account associated to the provided account number
     * 
     * @param accno account number
     * @return Account
     * @throws Exception 
     */
    private Account retrieve ( String accno ) throws Exception
    {
        Iterator<Account> i = accounts.iterator();
        while ( i.hasNext() ) {
            Account acc = i .next();
            if ( acc.getAccountNo().equals( accno ) )
                return acc;
        }
//        for (Account acc : accounts) {
//            if ( acc.getAccountNo().equals( accno ) )
//                return acc;
//        }
        throw new Exception ( "Account not found." );
    }
}
