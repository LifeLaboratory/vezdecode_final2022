package ru.lifelaboratory;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.MediaPlayer;
import android.os.Build;
import android.util.Log;

import androidx.annotation.RequiresApi;
import androidx.core.app.NotificationCompat;

import java.util.Calendar;
import java.util.Date;
import java.util.HashSet;

public class AlarmService extends BroadcastReceiver {

    static MediaPlayer mediaPlayer;

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    public void onReceive(Context context, Intent intent) {

        SharedPreferences sharedPreferences = context.getSharedPreferences("alarms", context.MODE_PRIVATE);
        Log.e("Life", String.valueOf(sharedPreferences.getStringSet("time", new HashSet<>())));

        Date currentTime = Calendar.getInstance().getTime();
        HashSet<String> alarms = (HashSet<String>) sharedPreferences.getStringSet("time", new HashSet<>());
        HashSet<String> newAlarms = new HashSet<>();
        alarms.forEach(element -> {
            String currentTimeStr = currentTime.getHours() + ":" + currentTime.getMinutes();
            if (currentTimeStr.equals(element))
                showNotification(context, "Будильник", "Пора вставать, прям 100%");
            else
                newAlarms.add(element);
        });
        sharedPreferences.edit().putStringSet("time", newAlarms).apply();

    }

    public void showNotification(Context context,
                                 String title,
                                 String message) {
        Intent intent = new Intent(context, MainActivity.class);
        String channel_id = "notification_channel";
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_ONE_SHOT);

        NotificationCompat.Builder builder = new NotificationCompat
                .Builder(context, channel_id)
                .setAutoCancel(true)
                .setSmallIcon(R.drawable.ic_launcher_foreground)
                .setVibrate(new long[]{1000, 1000, 1000, 1000, 1000})
                .setOnlyAlertOnce(true)
                .setContentIntent(pendingIntent);

        builder = builder.setContentTitle(title).setContentText(message);
        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel notificationChannel = new NotificationChannel(
                    channel_id,
                    "web_app",
                    NotificationManager.IMPORTANCE_HIGH);
            notificationManager.createNotificationChannel(notificationChannel);
        }

        notificationManager.notify(0, builder.build());

        mediaPlayer = MediaPlayer.create(context, R.raw.alarm);
        mediaPlayer.start();
    }
}
