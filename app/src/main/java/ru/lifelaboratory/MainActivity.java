package ru.lifelaboratory;

import android.Manifest;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.util.Log;
import android.view.MotionEvent;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TimePicker;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.google.firebase.messaging.FirebaseMessaging;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashSet;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    SpeechRecognizer speechRecognizer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ListView productList = findViewById(R.id.alarm_list);
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
                HashSet<String> setWithTimes = (HashSet<String>) sharedPreferences.getStringSet("time", new HashSet<>());
                setWithTimes.add(time);
                editor.putStringSet("time", setWithTimes).apply();
                Toast.makeText(getApplicationContext(), "Будильник активирован на " + time, Toast.LENGTH_LONG).show();

                Intent myIntent = new Intent(getApplicationContext(), AlarmService.class);
                PendingIntent pendingIntent = PendingIntent.getBroadcast(getApplicationContext(), 0, myIntent, 0);

                AlarmManager alarmManager = (AlarmManager) getApplicationContext().getSystemService(Context.ALARM_SERVICE);
                Calendar calendar = Calendar.getInstance();
                calendar.setTimeInMillis(System.currentTimeMillis());
                calendar.add(Calendar.SECOND, 10);
                long frequency = 10 * 1000;
                alarmManager.setRepeating(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(), frequency, pendingIntent);

                AlarmAdapter adapter = new AlarmAdapter(this, R.layout.alarm_item, new ArrayList<>(sharedPreferences.getStringSet("time", new HashSet<>())));
                productList.setAdapter(adapter);
            });
        }

        AlarmAdapter adapter = new AlarmAdapter(this, R.layout.alarm_item, new ArrayList<>(sharedPreferences.getStringSet("time", new HashSet<>())));
        productList.setAdapter(adapter);

        if(ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED){
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, 42);
            }
        }

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);

        findViewById(R.id.btn_speech).setOnTouchListener((view, motionEvent) -> {
            if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                speechRecognizer.stopListening();
            }
            if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                Intent speechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
                speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.ENGLISH);
                speechRecognizer.startListening(speechRecognizerIntent);
            }
            return false;
        });

        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle bundle) {}

            @Override
            public void onBeginningOfSpeech() {}

            @Override
            public void onRmsChanged(float v) {}

            @Override
            public void onBufferReceived(byte[] bytes) {}

            @Override
            public void onEndOfSpeech() {}

            @Override
            public void onError(int i) {}

            @RequiresApi(api = Build.VERSION_CODES.N)
            @Override
            public void onResults(Bundle bundle) {
                ArrayList<String> data = bundle.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                data.forEach(element -> {
                    if (element.startsWith("Поставь будильник на")) {
                        String time = element.replace("Поставь будильник на ", "");
                        HashSet<String> setWithTimes = (HashSet<String>) sharedPreferences.getStringSet("time", new HashSet<>());
                        SharedPreferences.Editor editor = sharedPreferences.edit();
                        setWithTimes.add(time);
                        editor.putStringSet("time", setWithTimes).apply();
                        Toast.makeText(getApplicationContext(), "Будильник активирован на " + time, Toast.LENGTH_LONG).show();

                        AlarmAdapter adapter = new AlarmAdapter(getApplicationContext(), R.layout.alarm_item, new ArrayList<>(sharedPreferences.getStringSet("time", new HashSet<>())));
                        productList.setAdapter(adapter);
                    } else if (element.startsWith("стоп") || element.startsWith("Стоп")) {
                        AlarmService.mediaPlayer.stop();
                        AlarmService.mediaPlayer = null;
                        finish();
                        startActivity(getIntent());
                    }
                });
            }

            @Override
            public void onPartialResults(Bundle bundle) {}

            @Override
            public void onEvent(int i, Bundle bundle) {}
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 42 && grantResults.length > 0 ){
            if(grantResults[0] == PackageManager.PERMISSION_GRANTED)
                Toast.makeText(this,"Permission Granted",Toast.LENGTH_SHORT).show();
        }
    }

}