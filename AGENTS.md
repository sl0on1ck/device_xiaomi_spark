# Redmi Pad SE 8.7 (flare, MT6768/Helio G85) — OrangeFox/TWRP Recovery

## Device
- **Codename**: flare (WiFi), not spark (4G). Device tree uses `spark` for asserts — OK for boot but mismatch.
- **Firmware**: `flare_id_global_images_OS3.0.302.0.WHXIDXM_16.0` (Android 16, A16)
- **Board**: MediaTek Helio G85 (MT6768), ARM64
- **Storage**: UFS, dynamic partitions (super), Virtual A/B, vendor_boot
- **Boot**: vendor_boot (v4 header) with 3 ramdisks: vendor_ramdisk00 (platform), 01 (recovery), 02 (init_boot)

## Repos
- Device tree: `github.com/sl0on1ck/device_xiaomi_spark`
  - Branches: `main` (OrangeFox), `twrp` (TWRP)
- Builder: `github.com/sl0on1ck/OrangeFox-Recovery-Builder-2024`
  - Branch: `OrangeFox`
  - Workflow: `.github/workflows/OrangeFox-Recovery-Builder.yml` (both TWRP & OrangeFox)

## Approach
- Build `boot.img` with `BOARD_USES_RECOVERY_AS_BOOT := true` (recovery ramdisk packed into boot.img)
- `fastboot boot boot.img` for temporary testing (no flash)
- For permanent install: `inject.py` replaces recovery ramdisk in stock vendor_boot

## Build Config
- BoardConfig.mk: 131 lines — `TW_*` flags (TWRP), no `FOX_*` flags
- Key flags: `BOARD_INCLUDE_DTB_IN_BOOTIMG := true`, `TARGET_PREBUILT_DTB`, `BOARD_USES_RECOVERY_AS_BOOT := true`
- Boot header v4, kernel prebuilt (gzip, 14MB), dtb prebuilt (MTK 64-byte header + FDT, 155KB)
- Output file: `out/target/product/spark/boot.img` (128MB, padded to partition size)

## Build History
| # | Type | Status | Issue |
|---|------|--------|-------|
| 8 | OrangeFox | ✅ success | No DTB in image — kernel panic on boot |
| 9 | OrangeFox | ❌ failed | `BOARD_INCLUDE_DTB_IN_BOOTIMG` + broken copy rule in device.mk |
| 10 | TWRP | ❌ workflow fail | Build succeeded but workflow didn't find `boot.img` (looked only for `OrangeFox*.img`) |
| 11 | OrangeFox | ✅ success | Still no DTB (`BOARD_INCLUDE_DTB_IN_BOOTIMG` was removed) |
| **12** | **OrangeFox** | **running** | **DTB fix: `BOARD_INCLUDE_DTB_IN_BOOTIMG := true`, `--dtb` removed from MKBOOTIMG_ARGS** |
| **13** | **TWRP** | **running** | **Same DTB fix on `twrp` branch** |

## Symptom
`fastboot boot boot.img` → `Status read failed (No such device)` — kernel panics at early boot (USB disconnects). Root cause: missing DTB in boot image.

## Current Fix
- `BOARD_INCLUDE_DTB_IN_BOOTIMG := true` in BoardConfig.mk (line 50)
- `TARGET_PREBUILT_DTB := $(DEVICE_PATH)/prebuilt/dtb.img` (line 39)
- Build system handles DTB copy to `$(PRODUCT_OUT)/dtb.img` and passes `--dtb` to mkboootimg
- Manual `--dtb` removed from `BOARD_MKBOOTIMG_ARGS` to avoid duplication

## Builder Workflow
- Inputs: `MANIFEST_TYPE` (OrangeFox/TWRP), device tree params, `BUILD_TARGET` (boot/recovery/vendorboot)
- Sync: OrangeFox → `orangefox_sync.sh --branch 12.1`; TWRP → `repo init/sync twrp-12.1`
- Build: `lunch twrp_<device>-eng && mka bootimage`
- Release: auto-creates GitHub Release with boot.img

## To Test
```bash
# Temp boot (safe):
fastboot boot boot.img
# Permanent flash (after temp boot confirmed working):
python3 inject.py && fastboot flash vendor_boot modified_vendor_boot.img
```
