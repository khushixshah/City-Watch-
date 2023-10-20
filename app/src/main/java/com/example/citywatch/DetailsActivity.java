package com.example.citywatch;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.squareup.picasso.Picasso;

import java.util.Calendar;
import java.util.Date;

public class DetailsActivity extends AppCompatActivity {
    private Button button;
    private FirebaseAuth mAuth;
    Date currentTime = Calendar.getInstance().getTime();
    boolean doubleBackToExitPressedOnce = false;
    private FirebaseDatabase firebaseDatabase=FirebaseDatabase.getInstance();
    private DatabaseReference databaseReference=firebaseDatabase.getReference();
    private DatabaseReference first;
    public static DatabaseReference mDatabase;
    private DatabaseReference realdata;
    public static TextView name;
    public static TextView area;
    String currentuser = FirebaseAuth.getInstance().getCurrentUser().getUid();
    ProgressDialog progressDialog;
    public static ImageView imview;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_details);
        //fonts
        Typeface custom_font = Typeface.createFromAsset(getAssets(),  "fonts/Oswald-VariableFont_wght.ttf");


        //initialze progress dialog
        progressDialog=new ProgressDialog(DetailsActivity.this);
        progressDialog.show();
        //set content view
        progressDialog.setContentView(R.layout.progress_dialog);
        //set transparent background
        progressDialog.getWindow().setBackgroundDrawableResource(
                android.R.color.transparent);
        mAuth = FirebaseAuth.getInstance();
        button=(Button)findViewById(R.id.button2);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openCamera();
            }
        });
        TextView timetext = (TextView) findViewById(R.id.textView4);
        timetext.setTypeface(custom_font);
        name=(TextView)findViewById(R.id.textView2);
        name.setTypeface(custom_font);
        area=(TextView)findViewById(R.id.textView3);
        area.setTypeface(custom_font);
        timetext.setText(""+currentTime);
        imview = (ImageView) findViewById(R.id.imageView);
        mDatabase = FirebaseDatabase.getInstance().getReference().child(currentuser);
        mDatabase.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String link= dataSnapshot.child("image").getValue().toString();
                Picasso.get().load(dataSnapshot.child("image").getValue().toString()).into(imview);
                name.setText(dataSnapshot.child("name").getValue().toString());
                area.setText(dataSnapshot.child("area").getValue().toString());
                progressDialog.hide();
                Toast.makeText(DetailsActivity.this, "Welcome "+dataSnapshot.child("name").getValue().toString()+"!",
                        Toast.LENGTH_SHORT).show();

            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        //imview.setImageResource(0);
        //Drawable draw = getResources().getDrawable(R.drawable.);
        //draw = (draw);
        //imview.setImageDrawable(draw);

    }
    @Override
    protected void  onStart(){
        super.onStart();
        first = FirebaseDatabase.getInstance().getReference().child(currentuser);
        first.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String link= dataSnapshot.child("image").getValue(String.class);
                Picasso.get().load(link).into(imview);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

    }

    public void openCamera() {
        Intent intent = new Intent(this, CameraActivity.class);
        startActivity(intent);
    }

    @Override
    public void onBackPressed() {
        if (doubleBackToExitPressedOnce) {
            super.onBackPressed();
            mAuth.signOut();
            Intent intent= new Intent(this,MainActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(intent);
            return;
        }
        this.doubleBackToExitPressedOnce = true;
        Toast.makeText(this, "Press Back again to Logout", Toast.LENGTH_SHORT).show();

        new Handler().postDelayed(new Runnable() {

            @Override
            public void run() {
                doubleBackToExitPressedOnce=false;

            }
        }, 2000);
    }



}
