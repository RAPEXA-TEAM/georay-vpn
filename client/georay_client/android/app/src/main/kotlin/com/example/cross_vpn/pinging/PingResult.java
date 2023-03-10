package com.example.cross_vpn.pinging;

public class PingResult {
    public String net = "NO_CONNECTION";
    public String host = "";
    public String ip = "";
    public int dns = Integer.MAX_VALUE;
    public int cnt = Integer.MAX_VALUE;

    @Override
    public String toString() {
        return "{\"cnt\":" + Integer.toString(cnt) + ",\"dns\":" + Integer.toString(dns) + ",\"host\":\""+ host + "\",\"ip\":\"" + ip + "\",\"net\":\"" + net + "\"}";
    }
}
