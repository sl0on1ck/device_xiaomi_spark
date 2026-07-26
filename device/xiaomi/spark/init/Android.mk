LOCAL_PATH := $(call my-dir)

ifneq ($(TARGET_NO_RECOVERY),true)
include $(CLEAR_VARS)
LOCAL_MODULE := libinit_spark
LOCAL_MODULE_TAGS := optional
LOCAL_FORCE_STATIC_EXECUTABLE := true
LOCAL_MODULE_PATH := $(TARGET_RECOVERY_ROOT_OUT)/system/bin
LOCAL_CFLAGS := -Wno-unused-parameter -Wno-unused-variable
LOCAL_SRC_FILES := init_spark.cpp
LOCAL_STATIC_LIBRARIES := libbase
include $(BUILD_EXECUTABLE)
endif
