package ru.lifelaboratory;

import com.google.gson.JsonElement;
import com.vk.api.sdk.client.TransportClient;
import com.vk.api.sdk.client.VkApiClient;
import com.vk.api.sdk.client.actors.GroupActor;
import com.vk.api.sdk.client.actors.ServiceActor;
import com.vk.api.sdk.exceptions.ApiException;
import com.vk.api.sdk.exceptions.ClientException;
import com.vk.api.sdk.httpclient.HttpTransportClient;
import com.vk.api.sdk.objects.messages.Message;
import com.vk.api.sdk.queries.messages.MessagesGetLongPollHistoryQuery;

import java.util.List;
import java.util.Random;

class App {

    public static void main(String[] args) throws ApiException, ClientException, InterruptedException {
        System.out.println(System.getProperty("file.encoding"));
        TransportClient transportClient = new HttpTransportClient();
        VkApiClient vk = new VkApiClient(transportClient);

        GroupActor actor = new GroupActor(212881098, "6bec718902959df1c1db2a96f16d4e3d5ab46d798af5b02a60e4768c6011112ec55b9cc9f22eefbe58902");
        Integer ts = vk.messages().getLongPollServer(actor).execute().getTs();
        Random random = new Random();

        ServiceActor serviceActor = new ServiceActor(8147140, "lcRNF9VZvIXLo2hW6xMj", "d9441aced9441aced9441aceb9d9384a0add944d9441acebb211889bb22cd6337e1ec90");

        // G3eaMVHzxeYzGqBmIUlE
        // dda00070dda00070dda0007027dddd5838ddda0dda00070bf69508e964aa3717d9ff332

        while (true) {
            MessagesGetLongPollHistoryQuery historyQuery = vk.messages().getLongPollHistory(actor).ts(ts);
            List<Message> messageList = historyQuery.execute().getMessages().getItems();
            messageList.forEach(message -> {
                System.out.println(message.getText());
                if (message.getText().equals("Звонок") || message.getText().equals("Call")) {
                    try {
                        vk.messages()
                                .send(actor)
                                .userId(message.getFromId())
                                .randomId(random.nextInt(1000))
                                .message("Test")
                                .execute();
                        JsonElement response = vk.execute().code(serviceActor, "return API.messages.startCall();").execute();
                        System.out.println(response.toString());
                        vk.messages().
                    } catch (ApiException | ClientException e) {
                        throw new RuntimeException(e);
                    }
                }
            });
            ts = vk.messages().getLongPollServer(actor).execute().getTs();
            Thread.sleep(500);
        }


    }

}
