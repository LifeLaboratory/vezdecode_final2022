package ru.lifelaboratory;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TimePicker;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.messaging.FirebaseMessaging;

import java.util.Calendar;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        SharedPreferences sharedPreferences = getSharedPreferences("alarms", MODE_PRIVATE);

        FirebaseMessaging.getInstance().setAutoInitEnabled(true);

        if (AlarmService.mediaPlayer != null && AlarmService.mediaPlayer.isPlaying()) {
            ((Button)findViewById(R.id.btn_main)).setText("Стоп");
            findViewById(R.id.btn_main).setOnClickListener(view -> {
                AlarmService.mediaPlayer.stop();
                AlarmService.mediaPlayer = null;
                finish();
                startActivity(getIntent());
            });
        } else {
            findViewById(R.id.btn_main).setOnClickListener(view -> {
                SharedPreferences.Editor editor = sharedPreferences.edit();
                TimePicker timePicker = findViewById(R.id.time);
                String time = "00:00";
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M)
                    time = timePicker.getHour() + ":" + timePicker.getMinute();
                editor.putString("time", time);
                editor.apply();
                Toast.makeText(getApplicationContext(), "Будильник активирован на " + time, Toast.LENGTH_LONG).show();

                Intent myIntent = new Intent(getApplicationContext(), AlarmService.class);
                PendingIntent pendingIntent = PendingIntent.getBroadcast(getApplicationContext(), 0, myIntent, 0);

                AlarmManager alarmManager = (AlarmManager) getApplicationContext().getSystemService(Context.ALARM_SERVICE);
                Calendar calendar = Calendar.getInstance();
                calendar.setTimeInMillis(System.currentTimeMillis());
                calendar.add(Calendar.SECOND, 10);
                long frequency = 10 * 1000;
                alarmManager.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(), frequency, pendingIntent);
            });
        }
    }



}