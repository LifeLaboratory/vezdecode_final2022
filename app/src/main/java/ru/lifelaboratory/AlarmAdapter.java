package ru.lifelaboratory;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Build;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;

public class AlarmAdapter extends ArrayAdapter<String> {

    private LayoutInflater inflater;
    private int layout;
    private ArrayList<String> alarmList;

    public AlarmAdapter(@NonNull Context context, int resource, @NonNull List<String> objects) {
        super(context, resource, objects);
        this.alarmList = (ArrayList<String>) objects;
        this.layout = resource;
        this.inflater = LayoutInflater.from(context);
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        final View viewHolder;
        if(convertView==null){
            convertView = inflater.inflate(this.layout, parent, false);
            viewHolder = convertView;
            convertView.setTag(viewHolder);
        } else{
            viewHolder = (View) convertView.getTag();
        }
        final String product = alarmList.get(position);

        ((TextView)viewHolder.findViewById(R.id.alarm_text)).setText(product);
        viewHolder.findViewById(R.id.alarm_btn).setOnClickListener(v -> {
            SharedPreferences sharedPreferences = this.getContext().getSharedPreferences("alarms", this.getContext().MODE_PRIVATE);
            HashSet<String> alarms = (HashSet<String>) sharedPreferences.getStringSet("time", new HashSet<>());
            HashSet<String> newAlarms = new HashSet<>();
            alarms.forEach(element -> {
                if (!product.equals(element))
                    newAlarms.add(element);
            });
            sharedPreferences.edit().putStringSet("time", newAlarms).apply();
        });

        return convertView;
    }
}
