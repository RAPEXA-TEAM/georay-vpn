package com.example.cross_vpn.pinging;

import android.app.Activity;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;

import java.net.InetAddress;
import java.net.MalformedURLException;
import java.net.Socket;
import java.net.URL;

class PingTask extends AsyncTask<String, Void, String> {
    private Activity context;
    private Exception exception;

    public PingTask(Activity con) {
        this.context = con;
    }

    protected String doInBackground(String... urls) {
        try {
            String url_string = urls[0];
            PingResult r = new PingResult();
            URL url = new URL(url_string);
            if (isNetworkConnected(context)) {
                r.net = getNetworkType(context);
                try {
                    String hostAddress;
                    long start = System.currentTimeMillis();
                    hostAddress = InetAddress.getByName(url.getHost()).getHostAddress();
                    long dnsResolved = System.currentTimeMillis();
                    Socket socket = new Socket(hostAddress, url.getPort());
                    socket.close();
                    long probeFinish = System.currentTimeMillis();
                    r.dns = (int) (dnsResolved - start);
                    r.cnt = (int) (probeFinish - dnsResolved);
                    r.host = url.getHost();
                    r.ip = hostAddress;
                    return r.toString();
                }
                catch (Exception ex) {
                    return ex.toString();
                }
            }
        } catch (Exception e) {
            this.exception = e;
            return e.toString();
        }

        return "FAILED";
    }

    protected void onPostExecute(String feed) {
        // TODO: check this.exception
        // TODO: do something with the feed
    }

    public static boolean isNetworkConnected(Context context) {
        ConnectivityManager cm =
                (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        return activeNetwork != null && activeNetwork.isConnectedOrConnecting();
    }

    public static String getNetworkType(Context context) {
        ConnectivityManager cm =
                (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetwork = cm.getActiveNetworkInfo();
        if (activeNetwork != null) {
            return activeNetwork.getTypeName();
        }
        return null;
    }
}
