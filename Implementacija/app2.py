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

def write_partition_mbr(disk_path, partition_index, hide):
    mbr = read_raw_data(disk_path, 0, 512)

    partition_table_start = 446
    partition_entry_size = 16

    partition_entry_start = partition_table_start + (partition_index * partition_entry_size)
    partition_entry = bytearray(mbr[partition_entry_start:partition_entry_start + partition_entry_size])

    print("MBR pre izmena:")
    display_hex(partition_entry)

    if hide is True:
        for i in range(0, 16):
            partition_entry[i] = 0x00
    else:
        print("Unesite vrednosti bajtova particije koju zelite da oporavite.")
        for i in range(0, 16):
            input_byte = input(f"Unesite bajt {i}: ")
            if "0x" not in input_byte:
                input_byte = "0x" + input_byte
            hex_input_byte = int(input_byte, 16)
            partition_entry[i] = hex_input_byte


    mbr = bytearray(mbr)
    mbr[partition_entry_start:partition_entry_start + partition_entry_size] = partition_entry
    write_raw_data(disk_path, 0, mbr)

    print("MBR posle izmena:")
    display_hex(partition_entry)

def main():
    disk_path = '/dev/sda'
    partition_index = int(input("Koju particiju zelite izmeniti na disku '/dev/sda' (1-4)? "))
    partition_index = partition_index - 1;
    if partition_index < 0 or partition_index > 3:
        print("Nevalidan redni broj particije.")
        exit(1)

    action = int(input("Koju akciju zelite preduzeti?\n1 - Sakrivanje particije\n2 - Otkrivanje particije\n"))
    # partition_id = "00"
    # if action == 2:
    #     partition_id = input("Unesite System ID particije pre sakrivanja: ")
    # if "0x" not in partition_id:
    #     partition_id = "0x" + partition_id

    # hex_partition_id = int(partition_id, 16)
    write_partition_mbr(disk_path, partition_index, action == 1)

    print("Kako biste videli izmene, molimo Vas restartujte racunar.")

if __name__ == '__main__':
    main()
