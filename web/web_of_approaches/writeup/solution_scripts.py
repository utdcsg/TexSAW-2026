import png

alphanumeric_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
substitution_scheme = "hNWBuJSjIPc6YnOa0fdMlFU1HCkogisDGbKrT479VRE3Xt2wmAZQx85eqvyLzp"
base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def reverse_flag_image():
    reader = png.Reader('D4kG_XsG7s9t.png')
    width, height, pixels, metadata = reader.read()
    flag_segment = ""
    for y, row in enumerate(pixels):
        for x in range(1, width * 2, 2):
            flag_segment += chr(row[x])
    print(flag_segment)
    return flag_segment

def decode_substitution_cipher(s):
    decoded_string = ""
    for char in s:
        if char not in alphanumeric_chars:
            decoded_string += char
            continue
        index = substitution_scheme.index(char)
        decoded_string += alphanumeric_chars[index]
    return decoded_string

def retrive_hidden_bits(s):
    hidden_bits = ""
    current_index = 0
    while current_index < len(s):
        padding_start = s.find('=', current_index)
        if padding_start == -1:
            break
        num_bits = 2
        if padding_start + 1 < len(s) and s[padding_start + 1] == '=':
            num_bits = 4
        six_bit_char = s[padding_start - 1]
        six_bit_index = base64_chars.index(six_bit_char)
        char_bits = format(six_bit_index, '06b')
        hidden_bits += char_bits[-num_bits:]
        current_index = padding_start + num_bits // 2
    return hidden_bits


if __name__ == "__main__":
    reverse_flag_image()
    exit()
    retrieved_flags = [
        "M5v4Ij==o5HGgx==C1C4gT==HUmGgI==H1PxgQ==ISp7IB==iSb4Ij==C7AbCZ==IS4QIu==H5p2iJ==HU42CF==CWNQo/==oUFekB==C1P4Iu==kUvQk1==CSlGoZ==CKNxkB==k1YGgQ==ijPRo4==CZqGIa==IWhGIu==IWhGIn==IWhGIB==IWhGIu==IWhGIS==IWhGIO==",
        "FSzGC4==kUvTIP==HUAXIJ==iSb4Ia==gSJZiJ==gZNvoe==idNekM==oSmGoT==CUFTIJ==iSzGgv==CUJZHe==kWNekB==C1P4IJ==sUp8Ia==o7pZo1==HUAXsl==IS8RCQ==kj0Gom==i7FZoJ==o5p3Ia==IWhGIj==IWhGIB==IWhGIB==IWhGIh==IWhGIS==IWhGIY==",
        "FSb4g4==CdNbg7==CdNxkB==g7F4IB==gSJZiJ==gZNwCw==ISuGiQ==CUIGgu==HUi46J==IjfVCD==Ijnxg7==iUnxiM==g7lXIu==iSb4II==gefvoB==CdmGHl==o70GiS==kSlGgz==HePRgB==iWqGIN==IWhGIS==IWhGIO==IWhGIu==IWhGIj==IWhGIB==IWhGIB=="
    ]
    converted_flags = [decode_substitution_cipher(flag) for flag in retrieved_flags]
    flag_bits = ""
    print(converted_flags)
    for flag in converted_flags:
        flag_bits += retrive_hidden_bits(flag)
    
    flag_string = ""
    for i in range(0, len(flag_bits), 8):
        byte = flag_bits[i:i+8]
        flag_string += chr(int(byte, 2))

    print(f'Flag: texsaw{{{flag_string.strip()}}}')