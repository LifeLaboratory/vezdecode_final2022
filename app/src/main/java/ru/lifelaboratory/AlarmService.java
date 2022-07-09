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

import androidx.core.app.NotificationCompat;

import java.util.Calendar;
import java.util.Date;

public class AlarmService extends BroadcastReceiver {

    static MediaPlayer mediaPlayer;

    @Override
    public void onReceive(Context context, Intent intent) {

        SharedPreferences sharedPreferences = context.getSharedPreferences("alarms", context.MODE_PRIVATE);
        Log.e("Life", sharedPreferences.getString("time", "99:99"));

        Date currentTime = Calendar.getInstance().getTime();
        if ((currentTime.getHours() + ":" + currentTime.getMinutes()).equals(sharedPreferences.getString("time", "99:99"))) {
            showNotification(context, "Будильник", "Пора вставать, прям 100%");
            sharedPreferences.edit().clear().apply();
        }

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
