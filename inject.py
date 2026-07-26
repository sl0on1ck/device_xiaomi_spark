import struct, sys, os, shutil

def align_to(val, align):
    return (val + align - 1) & ~(align - 1)

def inject_recovery(boot_img, stock_vendor_boot, output_img):
    with open(boot_img, 'rb') as f:
        boot_data = f.read()

    with open(stock_vendor_boot, 'rb') as f:
        vb_data = f.read()

    if boot_data[0:8] == b'ANDROID!':
        boot_hdr_size = struct.unpack_from('<I', boot_data, 12)[0]
        if boot_hdr_size == 0:
            boot_hdr_size = 1648
        ramdisk_offset = boot_hdr_size
        boot_ramdisk = boot_data[ramdisk_offset:]
    else:
        sys.exit("Not a valid boot.img")

    if vb_data[0:8] != b'VNDRBOOT':
        sys.exit("Not a valid vendor_boot.img")

    hdr_version = struct.unpack_from('<I', vb_data, 16)[0]
    if hdr_version != 4:
        sys.exit(f"Unsupported vendor_boot header version: {hdr_version}")

    page_size = struct.unpack_from('<I', vb_data, 8)[0]
    hdr_size = struct.unpack_from('<I', vb_data, 12)[0]

    dtb_offset = struct.unpack_from('<Q', vb_data, 92)[0]
    dtb_size = struct.unpack_from('<I', vb_data, 104)[0]

    vendor_ramdisk_table_size = struct.unpack_from('<I', vb_data, 120)[0]
    vendor_ramdisk_table_entry_size = struct.unpack_from('<I', vb_data, 124)[0]
    vendor_ramdisk_table_entry_num = struct.unpack_from('<I', vb_data, 128)[0]

    pos = align_to(hdr_size, page_size)

    table_offset = pos
    table_size = vendor_ramdisk_table_entry_num * vendor_ramdisk_table_entry_size
    table_end = align_to(table_offset + table_size, page_size)

    pos = table_end

    ramdisks = []
    for i in range(vendor_ramdisk_table_entry_num):
        entry_start = table_offset + i * vendor_ramdisk_table_entry_size
        rd_size = struct.unpack_from('<I', vb_data, entry_start + 8)[0]
        rd_offset_tab = struct.unpack_from('<I', vb_data, entry_start + 12)[0]
        rd_type = struct.unpack_from('<I', vb_data, entry_start + 16)[0]

        rd_offset = rd_offset_tab
        rd_data = vb_data[rd_offset:rd_offset + rd_size]
        ramdisks.append({'offset': rd_offset, 'size': rd_size, 'type': rd_type, 'data': rd_data})

    print(f"Stock vendor_boot: {vendor_ramdisk_table_entry_num} ramdisks")
    for i, rd in enumerate(ramdisks):
        t = "platform" if rd['type'] == 1 else ("recovery" if rd['type'] == 2 else f"type_{rd['type']}")
        print(f"  [{i}] {t}: {rd['size']} bytes")

    recovery_idx = None
    for i, rd in enumerate(ramdisks):
        if rd['type'] == 2:
            recovery_idx = i
            break

    if recovery_idx is None:
        sys.exit("No recovery ramdisk found in stock vendor_boot")

    print(f"Replacing recovery ramdisk [{recovery_idx}] ({ramdisks[recovery_idx]['size']} bytes) with OrangeFox ({len(boot_ramdisk)} bytes)")
    ramdisks[recovery_idx] = {
        'offset': 0,
        'size': len(boot_ramdisk),
        'type': 2,
        'data': boot_ramdisk
    }

    with open(output_img, 'wb') as f:
        f.write(vb_data[:pos])

        for i, rd in enumerate(ramdisks):
            f.write(rd['data'])
            padding = align_to(len(rd['data']), page_size) - len(rd['data'])
            f.write(b'\x00' * padding)
            new_offset = pos
            new_size = len(rd['data'])
            rd['offset'] = new_offset
            rd['size'] = new_size
            pos = f.tell()

        dtb_pos = f.tell()
        dtb_data = vb_data[dtb_offset:dtb_offset + dtb_size]
        f.write(dtb_data)
        dtb_padding = align_to(len(dtb_data), page_size) - len(dtb_data)
        f.write(b'\x00' * dtb_padding)
        f.seek(0)
        new_table_size = vendor_ramdisk_table_entry_num * vendor_ramdisk_table_entry_size

        for i, rd in enumerate(ramdisks):
            entry_start = table_offset + i * vendor_ramdisk_table_entry_size
            f.seek(entry_start + 8)
            f.write(struct.pack('<I', rd['size']))
            f.seek(entry_start + 12)
            f.write(struct.pack('<I', rd['offset']))
            f.seek(entry_start + 16)
            f.write(struct.pack('<I', rd['type']))

    out_size = os.path.getsize(output_img)
    print(f"Injected vendor_boot written: {output_img} ({out_size} bytes)")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: inject.py <boot.img> <stock-vendor_boot.img> <output.img>")
        sys.exit(1)
    inject_recovery(sys.argv[1], sys.argv[2], sys.argv[3])
