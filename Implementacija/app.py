import os

def read_raw_data(disk_path, start, size):
    with open(disk_path, 'rb') as disk:
        disk.seek(start)
        data = disk.read(size)
        return data

def write_raw_data(disk_path, start, data):
    with open(disk_path, 'rb+') as disk:
        disk.seek(start)
        disk.write(data)

def display_hex(data):
    hex_data = ' '.join(f'{byte:02X}' for byte in data)
    print(hex_data)

def write_partition_mbr(disk_path, partition_index, hex_partition_id):
    mbr = read_raw_data(disk_path, 0, 512)

    partition_table_start = 446
    partition_entry_size = 16

    partition_entry_start = partition_table_start + (partition_index * partition_entry_size)
    partition_entry = bytearray(mbr[partition_entry_start:partition_entry_start + partition_entry_size])

    print("MBR pre izmena:")
    display_hex(partition_entry)

    previous_hex_partition_id = partition_entry[4]
    partition_entry[4] = hex_partition_id

    mbr = bytearray(mbr)
    mbr[partition_entry_start:partition_entry_start + partition_entry_size] = partition_entry
    write_raw_data(disk_path, 0, mbr)

    print("MBR posle izmena:")
    display_hex(partition_entry)

    return previous_hex_partition_id

def main():
    disk_path = '/dev/sda'
    partition_index = int(input("Koju particiju zelite izmeniti na disku '/dev/sda' (1-4)? "))
    partition_index = partition_index - 1;
    if partition_index < 0 or partition_index > 3:
        print("Nevalidan redni broj particije.")
        exit(1)

    action = int(input("Koju akciju zelite preduzeti?\n1 - Sakrivanje particije\n2 - Otkrivanje particije\n"))
    partition_id = "00"
    if action == 2:
        partition_id = input("Unesite System ID particije pre sakrivanja: ")
    if "0x" not in partition_id:
        partition_id = "0x" + partition_id

    hex_partition_id = int(partition_id, 16)
    previous_hex_partition_id = write_partition_mbr(disk_path, partition_index, hex_partition_id)
    if action == 1:
        print(f"System ID particije koja je sakrivena je {previous_hex_partition_id:02X}.")

    print("Kako biste videli izmene, molimo Vas restartujte racunar.")

if __name__ == '__main__':
    main()
