package com.example.citywatch;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;

public class MainActivity extends AppCompatActivity {
    public static String e;
    private FirebaseAuth mAuth;
    private EditText mEmailField;
    private EditText mPasswordField;
    private Button login;
    ProgressDialog progressDialog;
    public static final String TAG = "t";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView tx = (TextView)findViewById(R.id.tx);

        Typeface custom_font = Typeface.createFromAsset(getAssets(),  "fonts/Oswald-VariableFont_wght.ttf");

        tx.setTypeface(custom_font);
        //initialze progress dialog
        progressDialog=new ProgressDialog(MainActivity.this);
        // Initialize Firebase Auth
        mAuth = FirebaseAuth.getInstance();
        mEmailField = findViewById(R.id.fieldEmail);
        mPasswordField = findViewById(R.id.fieldPassword);
        login=findViewById(R.id.button);
        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                signIn(mEmailField.getText().toString(), mPasswordField.getText().toString());
                // Sign in success, update UI with the signed-in user's information
                progressDialog.show();
                //set content view
                progressDialog.setContentView(R.layout.progress_dialog);
                //set transparent background
                progressDialog.getWindow().setBackgroundDrawableResource(
                        android.R.color.transparent);
            }

        });

    }
    private void  updateUI(FirebaseUser account){
        if(account != null){
            Toast.makeText(this,"Access Granted",Toast.LENGTH_LONG).show();
            startActivity(new Intent(this, DetailsActivity.class));

        }else if(account==null) {
            Toast.makeText(this,"Invalid Credentials",Toast.LENGTH_LONG).show();
        }
    }
    public boolean validateForm() {
        boolean valid = true;

         e = mEmailField.getText().toString();
        if (TextUtils.isEmpty(e)) {
            mEmailField.setError("Required.");
            progressDialog.hide();
            valid = false;
        } else {
            mEmailField.setError(null);
        }

        String p = mPasswordField.getText().toString();
        if (TextUtils.isEmpty(p)) {
            mPasswordField.setError("Required.");
            progressDialog.hide();
            valid = false;
        } else {
            mPasswordField.setError(null);
        }

        return valid;
    }
    private void signIn(String email, String password) {
        Log.d(TAG, "signIn:" + email);
        if (!validateForm()) {
            return;
        }

        mAuth.signInWithEmailAndPassword(email, password)
                .addOnCompleteListener(this, new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if (task.isSuccessful()) {
                            progressDialog.hide();
                            Log.d(TAG, "signInWithEmail:success");
                            final FirebaseUser user = mAuth.getCurrentUser();
                            updateUI(user);
                        } else {

                            Log.w(TAG, "signInWithEmail:failure", task.getException());
                            Toast.makeText(MainActivity.this, task.getException().getMessage(),
                                    Toast.LENGTH_SHORT).show();
                            progressDialog.hide();
                        }

                    }
                });
    }

}
