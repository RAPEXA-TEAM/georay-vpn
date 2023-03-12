#!/usr/bin/env

# Response Trues

LOGOUT_CORRECTLY                      = {"code" : 200, "data" : "Device logout correctly!"}
CREATE_USER_CORRECTLY                 = {"code" : 200, "data" : "user created successfully"}
CREATE_USER_CORRECTLY_NOT_VERIFIED    = {"code" : 200, "data" : "user created successfully but not verified"}
PAYMENT_SUCCESSFULLY                  = {"code" : 200, "data" : "successful payment"}   
DEVICE_AND_OS_SET_CORRECTLY           = {"code" : 201, "data" : "Device and OS set correctly for this user"}

# Response Errors

ERROR_USER_OR_PASS_WRONG = {"code" : 401, "data" : "Error Forbidden"}
ERROR_REQUEST_NOT_VALID  = {"code" : 402, "data" : "Error Request not valid"}
ERROR_DATABASE           = {"code" : 403, "data" : "Error connecting to database"}
ERROR_USER_NOT_EXIST     = {"code" : 404, "data" : "Error"}
ERROR_PAYMENT_NOT_VALID  = {"code" : 405, "data" : "Error tx-id or payment-hash is not valid"}
ERROR_USER_NOT_VERIFIED  = {"code" : 406, "data" : "Error please verify your email address first"}
ERROR_DONE_EXPIRE_TIME   = {"code" : 407, "data" : "Error Contact to Seller or provider"}