
def insertion_sort(my_list):
    for key_pos in range(1, len(my_list)):
        key_value = my_list[key_pos]
        scan_pos = key_pos - 1
        while (scan_pos >= 0) and (my_list[scan_pos] > key_value):
            my_list[scan_pos + 1] = my_list[scan_pos]
            scan_pos -= 1

        my_list[scan_pos + 1] = key_value

my_list = [15, 57, 14, 33, 72]
insertion_sort(my_list)
print(my_list)
