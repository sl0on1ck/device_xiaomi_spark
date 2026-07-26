LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MODULE := libinit_spark
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := init_spark.cpp
LOCAL_STATIC_LIBRARIES := libbase
include $(BUILD_STATIC_LIBRARY)
