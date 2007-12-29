package net.lulli.utils.db;

/**
 * Paolo Lulli 12 Aprile 2003
 * 
 * Classe per la connessione al db con JDBC
 */

import java.io.FileInputStream;
import java.io.IOException;
import java.sql.*;
import java.util.Properties;
import net.lulli.utils.*;


public class DBManager {

	private static String userName;
	private static String password;
	private static String connectionString;
	private static Properties properties;

	
	private static Logger l = new Logger();
	
	/**
	 * Costruttore senza parametri, li carica da file di properties
	 */

	public DBManager() {
		properties = new Properties();
		try {
			properties.load(new FileInputStream("myprops.properties"));
		} catch (IOException e) {
			System.out.print("Costruttore fallito: "
					+ this.getClass().getName());
		}
		userName = properties.getProperty("myprops.DB_USERNAME");
		password = properties.getProperty("myprops.DB_PASSWORD");
		connectionString = properties.getProperty("myprops.DB_CONNECTION_STRING");
	}
	
	
	/**
	 * Costruttore con i parametri per la connessione al db
	 */

	public DBManager(String DB_USERNAME, String DB_PASSWORD,
			String DB_CONNECTION_STRING) {
		userName = DB_USERNAME;
		password = DB_PASSWORD;
		connectionString = DB_CONNECTION_STRING;
	}

	/**
	 * Per default, imposta la validità del cambio per il giorno corrente
	 */

	public  boolean updateValuta(String currencyFrom, String currencyTo,
			String multiplyRate, String divideRate) {
		try {

			Class.forName("oracle.jdbc.driver.OracleDriver");

			String url = connectionString;
			Connection con = DriverManager.getConnection(connectionString,
					userName, password);

			Statement stmt = con.createStatement();
			String query = "select  2 + 2 from dual";
		
			ResultSet resultSet = null;


			stmt.executeUpdate(query);

			/*
			 * Nel caso in cui la query fosse una select ...
			 */
			if (null != resultSet) {
				while (resultSet.next()) {
					String risultato = resultSet.getString("RISULTATO_FIELD");
				}
			}
			stmt.close();
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

}
