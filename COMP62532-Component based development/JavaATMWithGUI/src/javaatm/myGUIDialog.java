package javaatm;

import javax.swing.*;

public class myGUIDialog extends JDialog {
    public JPanel contentPane;
    public JButton balanceButton;
    public JLabel balanceLabel;
    public JTextField amount;
    public JButton withdrawButton;
    public JButton depositButton;
    public JLabel accno;


    public myGUIDialog() {
        this.setSize(500, 200);

        setContentPane(contentPane);

        setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);
    }
}
