package com.example.cross_vpn.v2ray.util

import android.net.VpnService
import android.os.Bundle
import android.os.PersistableBundle
import android.view.View
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.example.cross_vpn.CrossVpnApp
import com.example.cross_vpn.MainActivity.Companion.mainStorage
import com.example.cross_vpn.v2ray.service.V2RayServiceManager

class GrantPermissionActivityV2ray : AppCompatActivity(){
    private val requestVpnPermission = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) {
        if (it.resultCode == RESULT_OK) {
            if (mainStorage?.decodeString(MmkvManager.KEY_SELECTED_SERVER).isNullOrEmpty()) {
//                toast("no connection found for starting")
                return@registerForActivityResult
            }
            V2RayServiceManager.startV2Ray(this)
            finish()
        }
    }

    override fun onResume() {
        super.onResume()
        requestVpnPermission.launch(VpnService.prepare(this))
    }

    override fun onCreate(savedInstanceState: Bundle?, persistentState: PersistableBundle?) {
        super.onCreate(savedInstanceState, persistentState)
        setContentView(View(this))
    }
}