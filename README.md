# OrangeFox Recovery для Redmi Pad SE 8.7 (spark)

Device tree для сборки OrangeFox Recovery.

## Подготовка

Извлеки kernel, dtb.img, dtbo.img из стоковой прошивки:

```bash
unpack_bootimg --boot_img=vendor_boot.img --out=vendor_boot_out
cp vendor_boot_out/kernel device/xiaomi/spark/prebuilt/kernel
cp vendor_boot_out/dtb.img device/xiaomi/spark/prebuilt/dtb.img
unpack_bootimg --boot_img=boot.img --out=boot_out
cp boot_out/dtbo.img device/xiaomi/spark/prebuilt/dtbo.img
```

## Сборка локально

```bash
repo init --depth=1 -u https://gitlab.com/OrangeFox/manifest.git -b fox_12.1
repo sync
cp -r device/xiaomi/spark ~/fox_12.1/device/xiaomi/spark
cd ~/fox_12.1
export ALLOW_MISSING_DEPENDENCIES=true
. build/envsetup.sh
lunch twrp_spark-eng
mka vendorbootimage
```

## Прошивка

```bash
fastboot flash vendor_boot out/target/product/spark/vendor_boot.img
fastboot reboot
```
