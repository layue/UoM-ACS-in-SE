/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package javaatm;

/**
 *
 * @author Cuong Tran
 */
public class Account {
    String no;          // four 4 number
    Integer balance;
    
    public Account ()
    {
        balance = 0;
        no = "";
    }
    
    public void setBalance (Integer val) throws Exception 
    {
           if (val >=0 )
               balance = val;
           else
               throw new Exception( "Invalid balance." );
    }
    
    public String getAccountNo () {
        return String.valueOf( this.no );
    }
    
    public void setAccountNo (String val) throws Exception
    {
        if (val.length() == 4 && val.matches("[0-9]+"))
            no = val;
        else
            throw new Exception ( "Invalid account number." );
    }
    
    public void withdraw (Integer val ) throws Exception
    {
        if ( val > 0 && val <= balance)
            balance -= val;
        else
            throw new Exception( "Invalid amount." );
    }
    
    public void deposit (Integer val) throws Exception
    {
        if (val > 0)
            balance += val;
        else
            throw new Exception ( "Invalid amount." );
    }
    
    public Integer balance () {
        return this.balance;
    }
}
