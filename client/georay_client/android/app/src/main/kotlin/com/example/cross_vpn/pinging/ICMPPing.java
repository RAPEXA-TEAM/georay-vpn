package com.example.cross_vpn.pinging;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.UnknownHostException;

public class ICMPPing {
    public String getLatency(String url_name){
        try {
            URL url = new URL(url_name);
            String hostAddress = InetAddress.getByName(url.getHost()).getHostAddress();
            String pingCommand = "/system/bin/ping " + hostAddress;
            String inputLine = "";
            try {
                // execute the command on the environment interface
                Process process = Runtime.getRuntime().exec(pingCommand);
                // gets the input stream to get the output of the executed command
                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));

                inputLine = bufferedReader.readLine();
                return inputLine;
            }
            catch (Exception e) {
                return e.toString();
            }
        } catch (UnknownHostException | MalformedURLException e) {
            return e.toString();
        }
    }
}
