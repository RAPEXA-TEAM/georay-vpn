package com.example.cross_vpn

import android.content.Intent
import android.net.VpnService
import android.util.Log
import android.widget.Toast
import androidx.activity.viewModels
import com.example.cross_vpn.openconnect.VpnConstant
import com.example.cross_vpn.openconnect.VpnProfile
import com.example.cross_vpn.openconnect.api.GrantPermissionsActivity
import com.example.cross_vpn.openconnect.core.OpenConnectManagementThread
import com.example.cross_vpn.openconnect.core.OpenVpnService
import com.example.cross_vpn.openconnect.core.ProfileManager
import com.example.cross_vpn.openconnect.core.VPNConnector
import com.example.cross_vpn.v2ray.AppConfig
import com.example.cross_vpn.v2ray.AppConfig.ANG_PACKAGE
import com.example.cross_vpn.v2ray.dto.ServerConfig
import com.example.cross_vpn.v2ray.service.V2RayServiceManager
import com.example.cross_vpn.v2ray.service.V2RayServiceManager.serviceControl
import com.example.cross_vpn.v2ray.service.V2RayServiceManager.v2rayPoint
import com.example.cross_vpn.v2ray.util.*
import com.example.cross_vpn.v2ray.viewmodel.MainViewModel
import com.tencent.mmkv.MMKV
import io.flutter.embedding.android.FlutterFragmentActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.EventChannel
import io.flutter.plugin.common.EventChannel.EventSink
import io.flutter.plugin.common.EventChannel.StreamHandler
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugins.GeneratedPluginRegistrant
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch

class MainActivity : FlutterFragmentActivity() {

    var tag = "cross_vpn"
    private var mConnectionState = OpenConnectManagementThread.STATE_DISCONNECTED;
    private var mConn: VPNConnector? = null
    val mainViewModel: MainViewModel by viewModels()

    companion object {
        var globalEventSinkOpenConnect: EventSink? = null
        var globalEventSinkV2ray: EventSink? = null
        val settingsStorage by lazy {
            MMKV.mmkvWithID(
                MmkvManager.ID_SETTING,
                MMKV.MULTI_PROCESS_MODE
            )
        }
        val mainStorage by lazy { MMKV.mmkvWithID(MmkvManager.ID_MAIN, MMKV.MULTI_PROCESS_MODE) }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        GeneratedPluginRegistrant.registerWith(flutterEngine)
        mainViewModel.startListenBroadcast()
        MethodChannel(
            flutterEngine.dartExecutor,
            "cross_vpn/channeling"
        ).setMethodCallHandler { call, result ->
            when (call.method) {
                "vpnConnected" -> {
                    var connected = false
                    if (mainStorage.decodeBool(MmkvManager.VPN_CONNECTED, false)) {
                        connected = true
                    }
                    if (mConnectionState == OpenConnectManagementThread.STATE_CONNECTED) {
                        connected = true
                    }
                    result.success(connected)
                }
                "ping" -> {
                    GlobalScope.launch {
                        val argument: List<Any> = (call.arguments as List<Any>)
                        if(argument[1] == 0){
                            val config: ServerConfig? = AngConfigManager.getServerConfigFromStr(argument[0] as String)
                            config?.let {
                                config.getProxyOutbound()?.getServerAddress()?.let {
                                    result.success(SpeedtestUtil.ping(it))
                                } ?: result.success(0)
                            } ?: result.success(0)
                        }else{
                            result.success(SpeedtestUtil.ping(argument[0] as String))
                        }
                    }
                }
                "realPing" -> {
                    GlobalScope.launch {
                        while(true){
                            if (v2rayPoint.isRunning) {
                                try {
                                    result.success(v2rayPoint.measureDelay())
                                } catch (e: Exception) {
                                    result.success(-1)
                                }
                                break;
                            }
                        }
                    }
                }
                "toggleOpenConnect" -> {
                    if (mConnectionState == OpenConnectManagementThread.STATE_CONNECTED || mConnectionState == OpenConnectManagementThread.STATE_CONNECTING) {
                        mConn?.service?.stopVPN()
                        mConnectionState = OpenConnectManagementThread.STATE_DISCONNECTED
                        globalEventSinkOpenConnect?.success(mConnectionState);
                    } else {
                        val vpnProfiles: Collection<VpnProfile> = ProfileManager.getProfiles()
                        val argument: List<String> = (call.arguments as List<String>)
                        VpnConstant.serverAddress = argument[0]
                        VpnConstant.username = argument[1]
                        VpnConstant.password = argument[2]
                        var founded = false
                        lateinit var vpnProfile: VpnProfile
                        vpnProfiles.forEach {
                            if (it.mName == VpnConstant.serverAddress) {
                                founded = true
                                vpnProfile = it
                            }
                        }
                        if (founded) {
                            startVPN(vpnProfile)
                        } else {
                            startVPN(ProfileManager.createStr(VpnConstant.serverAddress))
                        }
                        result.success(null)
                    }
                }
                "toggleV2ray" -> {
                    if (mainViewModel.isRunning.value == true) {
                        Utils.stopVService(CrossVpnApp.globalAppContext)
                    } else if ((settingsStorage?.decodeString(AppConfig.PREF_MODE)
                            ?: "VPN") == "VPN"
                    ) {
                        MmkvManager.removeAllServer()
                        if (importBatchConfig((call.arguments as List<String>)[0])) {
                            val intent = VpnService.prepare(CrossVpnApp.globalAppContext)
                            if (intent == null) {
                                startV2raying()
                            } else {
                                startActivity(
                                    Intent(
                                        this,
                                        GrantPermissionActivityV2ray::class.java
                                    )
                                )
                            }
                        } else {
                            globalEventSinkV2ray?.success(AppConfig.MSG_MEASURE_CONFIG_CANCEL)
                        }
                    } else {
                        startV2raying()
                    }
                }
                else -> {
//                    if (call.method.equals("getPlatformVersion")) {
//                        result.success("Android " + android.os.Build.VERSION.RELEASE)
//                    } else if (call.method.equals("pingURL")) {
//                        val url_string: String? = call.argument("url")
//                        //      result.success(new PingTask(context).execute(url_string).get());
//                        try {
//                            result.success(ICMPPingTask().execute(url_string).get())
//                        } catch (e: ExecutionException) {
//                            result.success(e.toString())
//                        } catch (e: InterruptedException) {
//                            result.success(e.toString())
//                        }
//                    }
                }
            }
        }


        EventChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            "openconnect_events"
        ).setStreamHandler(
            object : StreamHandler {
                override fun onListen(listener: Any, eventSink: EventSink) {
                    globalEventSinkOpenConnect = eventSink;
                }

                override fun onCancel(listener: Any) {
                    globalEventSinkOpenConnect = null
                }
            })

        EventChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            "v2ray_events"
        ).setStreamHandler(
            object : StreamHandler {
                override fun onListen(listener: Any, eventSink: EventSink) {
                    globalEventSinkV2ray = eventSink;
                }

                override fun onCancel(listener: Any) {
                    globalEventSinkV2ray = null
                }
            })
    }

    override fun onResume() {
        super.onResume()
        mConn = object : VPNConnector(this, true) {
            override fun onUpdate(service: OpenVpnService?) {
                service?.let {
                    updateUI(it)
                }
            }
        }
    }

    override fun onPause() {
        mConn?.let {
            it.stopActiveDialog()
            it.unbind()
        }
        super.onPause()
    }

    override fun onDestroy() {
        super.onDestroy()
    }


    //OPEN CONNECT

    private fun updateUI(service: OpenVpnService) {
        val newState = service.connectionState
        service.startActiveDialog(this)
        mConnectionState = newState
        globalEventSinkOpenConnect?.success(newState)
    }


    private fun startVPN(profile: VpnProfile) {
        val intent = Intent(this, GrantPermissionsActivity::class.java)
        val pkg = this.packageName
        intent.putExtra(pkg + GrantPermissionsActivity.EXTRA_UUID, profile.uuid.toString())
        intent.action = Intent.ACTION_MAIN
        startActivity(intent)
    }

    //OPEN CONNECT


    //V2RAY


    private fun startV2raying() {
        if (mainStorage?.decodeString(MmkvManager.KEY_SELECTED_SERVER).isNullOrEmpty()) {
            return
        }
        V2RayServiceManager.startV2Ray(CrossVpnApp.globalAppContext)
    }

    fun importBatchConfig(server: String?, subid: String = ""): Boolean {
        val subid2 = if (subid.isNullOrEmpty()) {
            mainViewModel.subscriptionId
        } else {
            subid
        }
        val append = subid.isNullOrEmpty()

        var count = AngConfigManager.importBatchConfig(server, subid2, append)
        if (count <= 0) {
            count = AngConfigManager.importBatchConfig(Utils.decode(server!!), subid2, append)
        }
        if (count > 0) {
            mainViewModel.reloadServerList()
            return true;
        } else {
            return false;
        }
    }


//V2RAY

}
