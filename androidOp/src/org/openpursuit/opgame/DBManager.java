package org.openpursuit.opgame;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import com.mysql.jdbc.*;

import android.content.Context;
//import android.database.SQLException;

public class DBManager {
	DBManager() {
		 Connection con = null;
		    ResultSet rs = null;

		    try {
		      try {
		        Class.forName("com.mysql.jdbc.Driver").newInstance();
		        con =
		DriverManager.getConnection("jdbc:mysql://192.168.0.10:3306/openpursuit", "openpursuit", "opentrivial");
		      }
		      catch(ClassNotFoundException e) {
		        System.err.println("ClassNotFoundException: " + e.getMessage());
		      }
		      catch(InstantiationException e) {
		        System.err.println("InstantiationException: " + e.getMessage());
		      }
		      catch(IllegalAccessException e) {
		        System.err.println("IllegalAccessException: " + e.getMessage());
		      }

		      rs = con.createStatement().executeQuery("SELECT VERSION()");
		      rs.next();
		      System.out.println(rs.getString(1));

		    } catch(SQLException e) {
		      System.err.println("SQLException: " + e.getMessage());
		      System.err.println("SQLState: " + e.getSQLState());
		      System.err.println("VendorError: " + e.getErrorCode());
		    } finally {
		      try {
		        if(con != null)
		          con.close();
		      } catch(SQLException e) {}
		    }
		
	}
}
