package com.example.cross_vpn.openconnect;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import org.infradead.libopenconnect.LibOpenConnect;

import java.security.MessageDigest;

import com.example.cross_vpn.openconnect.core.UserDialog;

public class AuthFormHandler extends UserDialog {

    public static final String TAG = "OpenConnect";

    private LibOpenConnect.AuthForm mForm;
    private boolean isOK;

    private boolean noSave = false;
    private String formPfx;

    private int batchMode = BATCH_MODE_DISABLED;
    private boolean mAuthgroupSet;
    private boolean mAllFilled = true;


    private static final int BATCH_MODE_DISABLED = 0;
    private static final int BATCH_MODE_EMPTY_ONLY = 1;
    private static final int BATCH_MODE_ENABLED = 2;
    private static final int BATCH_MODE_ABORTED = 3;

    public AuthFormHandler(SharedPreferences prefs, LibOpenConnect.AuthForm form, boolean authgroupSet,
                           String lastFormDigest) {
        super(prefs);

        mForm = form;
        mAuthgroupSet = authgroupSet;
        formPfx = getFormPrefix(mForm);
        noSave = getBooleanPref("disable_username_caching");

        String s = getStringPref("batch_mode");
        if (s.equals("empty_only")) {
            batchMode = BATCH_MODE_EMPTY_ONLY;
        } else if (s.equals("enabled")) {
            batchMode = BATCH_MODE_ENABLED;
        }

        if (formPfx.equals(lastFormDigest)) {
            if (batchMode == BATCH_MODE_EMPTY_ONLY) {
                batchMode = BATCH_MODE_DISABLED;
            } else if (batchMode == BATCH_MODE_ENABLED) {
                batchMode = BATCH_MODE_ABORTED;
            }
        }
    }

    public String getFormDigest() {
        return formPfx;
    }


    private void saveAndStore() {
        for (LibOpenConnect.FormOpt opt : mForm.opts) {
            if ((opt.flags & LibOpenConnect.OC_FORM_OPT_IGNORE) != 0) {
                continue;
            }
            switch (opt.type) {
                case LibOpenConnect.OC_FORM_OPT_TEXT: {
                        setStringPref(formPfx + getOptDigest(opt), VpnConstant.username);
                    opt.value = VpnConstant.username;
                    break;
                }
                case LibOpenConnect.OC_FORM_OPT_PASSWORD: {
                        setStringPref(formPfx + getOptDigest(opt), VpnConstant.password);
                    opt.value = VpnConstant.password;
                    break;
                }
                case LibOpenConnect.OC_FORM_OPT_SELECT:
                    String s = (String)opt.userData;
                    if (!noSave) {
                        setStringPref(formPfx + getOptDigest(opt), s);
                        if ("group_list".equals(opt.name)) {
                            setStringPref("authgroup", s);
                        }
                    }
                    opt.value = s;
                    break;
            }
        }
    }

    private String digest(String s) {
        String out = "";
        if (s == null) {
            s = "";
        }
        try {
            MessageDigest digest = MessageDigest.getInstance("MD5");
            StringBuilder sb = new StringBuilder();
            byte d[] = digest.digest(s.getBytes("UTF-8"));
            for (byte dd : d) {
                sb.append(String.format("%02x", dd));
            }
            out = sb.toString();
        } catch (Exception e) {
            Log.e(TAG, "MessageDigest failed", e);
        }
        return out;
    }

    private String getOptDigest(LibOpenConnect.FormOpt opt) {
        StringBuilder in = new StringBuilder();

        switch (opt.type) {
            case LibOpenConnect.OC_FORM_OPT_SELECT:
                for (LibOpenConnect.FormChoice ch : opt.choices) {
                    in.append(digest(ch.name));
                    in.append(digest(ch.label));
                }
                /* falls through */
            case LibOpenConnect.OC_FORM_OPT_TEXT:
            case LibOpenConnect.OC_FORM_OPT_PASSWORD:
                in.append(":" + Integer.toString(opt.type) + ":");
                in.append(digest(opt.name));
                in.append(digest(opt.label));
        }
        return digest(in.toString());
    }

    private String getFormPrefix(LibOpenConnect.AuthForm form) {
        StringBuilder in = new StringBuilder();

        for (LibOpenConnect.FormOpt opt : form.opts) {
            in.append(getOptDigest(opt));
        }
        return "FORMDATA-" + digest(in.toString()) + "-";
    }

    private void spinnerSelect(LibOpenConnect.FormOpt opt, int index) {
        LibOpenConnect.FormChoice fc = opt.choices.get((int) index);
        String s = fc.name != null ? fc.name : "";

        if (opt.userData == null) {
            // first run
            opt.userData = s;
        } else if (!s.equals(opt.userData)) {
            opt.value = s;
            finish(LibOpenConnect.OC_FORM_RESULT_NEWGROUP);
        }
    }

    // If the user had saved a preferred authgroup, submit a NEWGROUP request before rendering the form
    public boolean setAuthgroup() {
        LibOpenConnect.FormOpt opt = mForm.authgroupOpt;
        if (opt == null) {
            return false;
        }

        String authgroup = getStringPref("authgroup");
        if (authgroup.equals("")) {
            return false;
        }

        LibOpenConnect.FormChoice selected = opt.choices.get(mForm.authgroupSelection);
        if (mAuthgroupSet || authgroup.equals(selected.name)) {
            // already good to go
            opt.value = authgroup;
            return false;
        }
        for (LibOpenConnect.FormChoice ch : opt.choices) {
            if (authgroup.equals(ch.name)) {
                opt.value = authgroup;
                return true;
            }
        }
        Log.w(TAG, "saved authgroup '" + authgroup + "' not present in " + opt.name + " dropdown");
        return false;
    }

    public Object earlyReturn() {
        if (setAuthgroup()) {
            return LibOpenConnect.OC_FORM_RESULT_NEWGROUP;
        }
        if (batchMode != BATCH_MODE_EMPTY_ONLY && batchMode != BATCH_MODE_ENABLED) {
            return null;
        }

        // do a quick pass through all prompts to see if we can fill in the
        // answers without bugging the user
        for (LibOpenConnect.FormOpt opt : mForm.opts) {
            if ((opt.flags & LibOpenConnect.OC_FORM_OPT_IGNORE) != 0) {
                continue;
            }
            switch (opt.type) {
                case LibOpenConnect.OC_FORM_OPT_PASSWORD:
                case LibOpenConnect.OC_FORM_OPT_TEXT:
                    String defval = noSave ? "" : getStringPref(formPfx + getOptDigest(opt));
                    if (defval.equals("")) {
                        return null;
                    }
                    opt.value = defval;
                    break;
                case LibOpenConnect.OC_FORM_OPT_SELECT:
                    if (opt.value == null) {
                        return null;
                    }
                    break;
            }
        }
        return LibOpenConnect.OC_FORM_RESULT_OK;
    }

    public void onStart(Context context) {
        super.onStart(context);

//        for (LibOpenConnect.FormOpt opt : mForm.opts) {
//            if ((opt.flags & LibOpenConnect.OC_FORM_OPT_IGNORE) != 0) {
//                continue;
//            }
//            switch (opt.type) {
//                case LibOpenConnect.OC_FORM_OPT_PASSWORD:
//                    hasPassword = true;
//                    /* falls through */
//                case LibOpenConnect.OC_FORM_OPT_TEXT:
//                    defval = noSave ? "" : getStringPref(formPfx + getOptDigest(opt));
//                    if (defval.equals("")) {
//                        if (opt.value != null && !opt.value.equals("")) {
//                            defval = opt.value;
//                        } else {
//                            /* note that this gets remembered across redraws */
//                            mAllFilled = false;
//                        }
//                    }
//                    hasUserOptions = true;
//                    break;
//                case LibOpenConnect.OC_FORM_OPT_SELECT:
//                    if (opt.choices.size() == 0) {
//                        break;
//                    }
//
//                    int selection = 0;
//                    if (opt == mForm.authgroupOpt) {
//                        selection = mForm.authgroupSelection;
//                    } else {
//                        // do any servers actually use non-authgroup downdowns?
//                        defval = noSave ? "" : getStringPref(formPfx + getOptDigest(opt));
//                        for (int i = 0; i < opt.choices.size(); i++) {
//                            if (opt.choices.get(i).name.equals(defval)) {
//                                selection = i;
//                            }
//                        }
//                    }
//                    hasUserOptions = true;
//                    break;
//            }
//        }

        if (batchMode == BATCH_MODE_ABORTED) {
            finish(LibOpenConnect.OC_FORM_RESULT_CANCELLED);
            return;
        }

//        if ((batchMode == BATCH_MODE_EMPTY_ONLY && mAllFilled) ||
//                batchMode == BATCH_MODE_ENABLED) {
        isOK = true;
        saveAndStore();
        finish(LibOpenConnect.OC_FORM_RESULT_OK);
//            return;
//        }
    }

    public void onStop(Context context) {
        super.onStop(context);
    }
}

