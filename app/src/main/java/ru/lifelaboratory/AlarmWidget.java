package ru.lifelaboratory;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.widget.RemoteViews;

import java.util.HashSet;

public class AlarmWidget extends AppWidgetProvider {

    private static CharSequence widgetText;

    static void updateAppWidget(Context context, AppWidgetManager appWidgetManager,
                                int appWidgetId) {

        SharedPreferences sharedPreferences = context.getSharedPreferences("alarms", context.MODE_PRIVATE);

        widgetText = "Нет активных будильников";
        HashSet<String> alarms = (HashSet<String>) sharedPreferences.getStringSet("time", new HashSet<>());
        if (alarms.size() > 0)
            for (String alarm : alarms) {
                widgetText = alarm;
                break;
            }

        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.alarm_widget);
        views.setOnClickPendingIntent(R.id.appwidget_text,
                PendingIntent.getActivity(context, 0, new Intent(context, MainActivity.class), 0));
        views.setTextViewText(R.id.appwidget_text, "Ближайший будильник: " + widgetText);
        appWidgetManager.updateAppWidget(appWidgetId, views);
    }

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        for (int appWidgetId : appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId);
        }
    }

    @Override
    public void onEnabled(Context context) {}

    @Override
    public void onDisabled(Context context) {}
}