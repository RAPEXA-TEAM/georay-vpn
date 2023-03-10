package com.example.cross_vpn;
import android.content.Context;
import androidx.multidex.MultiDexApplication;
import com.example.cross_vpn.openconnect.core.FragCache;
import com.example.cross_vpn.openconnect.core.ProfileManager;
import com.tencent.mmkv.MMKV;

public class CrossVpnApp extends MultiDexApplication {

	public static Context globalAppContext;
	public void onCreate() {
		super.onCreate();
		MMKV.initialize(this);
		globalAppContext = getApplicationContext();
		System.loadLibrary("openconnect");
		System.loadLibrary("stoken");
		ProfileManager.init(getApplicationContext());
		FragCache.init();
	}
}
