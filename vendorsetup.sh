FDEVICE="spark"

fox_get_target_device() {
local chkdev=$(echo "$BASH_SOURCE" | grep -w \"$FDEVICE\")
   if [ -n "$chkdev" ]; then
      FOX_BUILD_DEVICE="$FDEVICE"
   else
      chkdev=$(set | grep BASH_ARGV | grep -w \"$FDEVICE\")
      [ -n "$chkdev" ] && FOX_BUILD_DEVICE="$FDEVICE"
   fi
}

if [ -z "$1" -a -z "$FOX_BUILD_DEVICE" ]; then
   fox_get_target_device
fi

if [ "$1" = "$FDEVICE" -o "$FOX_BUILD_DEVICE" = "$FDEVICE" ]; then
	export FOX_RECOVERY_INSTALL_PARTITION="/dev/block/by-name/recovery"
	export FOX_RECOVERY_VENDOR_PARTITION="/dev/block/mapper/vendor"
	export FOX_USE_BASH_SHELL=1
	export FOX_ASH_IS_BASH=1
	export FOX_USE_TAR_BINARY=1
	export FOX_USE_LZ4_BINARY=1
	export FOX_USE_XZ_UTILS=1
	export FOX_ENABLE_APP_MANAGER=1
	export FOX_DELETE_AROMAFM=1
	export OF_SCREEN_H=1340
	export OF_STATUS_H=80
	export OF_STATUS_INDENT_LEFT=48
	export OF_STATUS_INDENT_RIGHT=48
	export OF_CLOCK_POS=1
	export OF_HIDE_NOTCH=1
	export OF_DONT_PATCH_ENCRYPTED_DEVICE=1
	export OF_NO_TREBLE_COMPATIBILITY_CHECK=1
	export OF_QUICK_BACKUP_LIST="/boot;/data;"
	export OF_USE_LOCKSCREEN_BUTTON=1
	export OF_SKIP_FBE_DECRYPTION=1

	if [ "$FOX_VARIANT" = "FBEv2" ]; then
		export FOX_VANILLA_BUILD=1
	fi
fi
