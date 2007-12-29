package org.openpursuit.opgame;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;


public class opgame extends Activity {
    public static final String KEY_TITLE = "title";
    public static final String KEY_BODY = "body";
//	private DBManager dbManager;

	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle icicle) {
        super.onCreate(icicle);
        setContentView(R.layout.main);
     //   dbManager = new DBManager(this);
    //    TextView tv = new TextView(this);
   //     tv.setText("Hello, Fusolab");
        //setContentView(R.layout.main); 
        final TextView txtHello = (TextView) findViewById(R.id.txtHello);
        final Button btnHello = (Button) findViewById(R.id.btnHello);

        //fillData();
        
    
    
    btnHello.setOnClickListener(new Button.OnClickListener() {
        public void onClick(View v) {
        txtHello.setText("hello World, IÕm Android!");
        DBManager dbManager = new DBManager();
        };
        
    });
    }
    }
   