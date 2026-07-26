LOCAL_PATH := $(call my-dir)

ifeq ($(TARGET_DEVICE),spark)
include $(call all-subdir-makefiles,$(LOCAL_PATH))
endif
