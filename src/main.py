from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
import ctypes
import math
from kivy.config import Config


Builder.load_file('calc.kv')
Window.size = (350, 500)

c = 'Chyba'


def dec2bin(number):
    i = 1
    bin_code = 0
    if '.' in number:
        dec_part_res = ''
        int_part_res = 0
        int_part, dec_part = int(number.split('.')[0]), float('0.' + number.split('.')[1])

        while int_part > 0:
            remainder = int_part % 2
            int_part_res = remainder * i + int_part_res
            int_part //= 2
            i = i * 10

        for x in range(1, 5):
            dec_part = 2 * dec_part
            if dec_part < 1:
                dec_part_res = dec_part_res + '0'
            elif dec_part > 1:
                dec_part_res = dec_part_res + '1'
                dec_part = float('0.' + str(dec_part).split('.')[1])
            else:
                dec_part_res = dec_part_res + '1'
                break

        bin_code = float(str(int_part_res) + '.' + dec_part_res)

    else:
        number = int(number.replace(" ", ""))
        while number > 0:
            remainder = number % 2
            bin_code = remainder * i + bin_code
            number //= 2
            i = i * 10

    return bin_code


def bin2dec(number):
    dec_code = 0
    i = 0
    if '.' in number:
        i = int(len(number.split('.')[0])) - 1
        for x in range(0, len(number)):
            if number[x].isdigit():
                dec_code = dec_code + int(number[x]) * pow(2, i)
                i -= 1
    else:
        number = int(number)
        while number != 0:
            dec = number % 10
            dec_code = dec_code + dec * pow(2, i)
            number //= 10
            i += 1

    dec_code = '{:,}'.format(int(dec_code)).replace(",", " ")
    return dec_code


def dec2hex(string):
    hex_characters = "0123456789ABCDEF"
    hex_code = ""
    if '.' in string:
        dec_part_res = ''
        int_part_res = ''
        int_part, dec_part = int(string.split('.')[0]), float('0.' + string.split('.')[1])

        while int_part > 0:
            remainder = int_part % 16
            int_part_res = hex_characters[remainder] + int_part_res
            int_part //= 16

        for x in range(1, 5):
            dec_part *= 16
            if 0 <= int(dec_part) <= 9:
                dec_part_res += str(int(dec_part))
            elif int(dec_part) == 10:
                dec_part_res += 'A'
            elif int(dec_part) == 11:
                dec_part_res += 'B'
            elif int(dec_part) == 12:
                dec_part_res += 'C'
            elif int(dec_part) == 13:
                dec_part_res += 'D'
            elif int(dec_part) == 14:
                dec_part_res += 'E'
            elif int(dec_part) == 15:
                dec_part_res += 'F'
            dec_part = float('0.' + str(dec_part).split('.')[1])

        hex_code = int_part_res + '.' + dec_part_res

    else:
        number = int(string.replace(" ", ""))
        while number > 0:
            remainder = number % 16
            hex_code = hex_characters[remainder] + hex_code
            number //= 16

    if hex_code == '':
        hex_code = '0'

    return hex_code


def hex2dec(string):
    dec_code = 0
    i = 0
    if '.' in string:
        help_string = []
        i = int(len(string.split('.')[0])) - 1
        for x in range(0, len(string)):
            if string[x] == '0':
                help_string.append(0)
            elif string[x] == '1':
                help_string.append(1)
            elif string[x] == '2':
                help_string.append(2)
            elif string[x] == '3':
                help_string.append(3)
            elif string[x] == '4':
                help_string.append(4)
            elif string[x] == '5':
                help_string.append(5)
            elif string[x] == '6':
                help_string.append(6)
            elif string[x] == '7':
                help_string.append(7)
            elif string[x] == '8':
                help_string.append(8)
            elif string[x] == '9':
                help_string.append(9)
            elif string[x] == 'A':
                help_string.append(10)
            elif string[x] == 'B':
                help_string.append(11)
            elif string[x] == 'C':
                help_string.append(12)
            elif string[x] == 'D':
                help_string.append(13)
            elif string[x] == 'E':
                help_string.append(14)
            elif string[x] == 'F':
                help_string.append(15)
            else:
                help_string.append('')

            if str(help_string[x]).isdigit():
                dec_code = dec_code + help_string[x] * pow(16, i)
                i -= 1
    else:
        while string != '':
            last_number = string[-1]
            match last_number:
                case 'A': last_number = 10
                case 'B': last_number = 11
                case 'C': last_number = 12
                case 'D': last_number = 13
                case 'E': last_number = 14
                case 'F': last_number = 15
            dec_code = dec_code + int(last_number) * pow(16, i)
            string = string[:-1]
            i += 1

    dec_code = '{:,}'.format(int(dec_code)).replace(",", " ")
    return dec_code


def round_dec_part(float_num, int_num):
    int_part = int(float_num)
    dec_part = float_num - int_part
    rounded_dec_part = round(dec_part, int_num)
    result = int_part + rounded_dec_part
    return result


class MyCalc(Widget):
    def __init__(self, **kwargs):
        super(MyCalc, self).__init__(**kwargs)
        self.result_clicked = False
        self.current_num_sys = 'dec'
        self.memory_value = '0'
        self.ids.dec_btn.background_color = (50 / 255, 145 / 255, 168 / 255, 1)

    def bin_keyboard(self):
        self.ids.dec_btn.background_color = (1, 1, 1, 1)
        self.ids.bin_btn.background_color = (50 / 255, 145 / 255, 168 / 255, 1)
        self.ids.hex_btn.background_color = (1, 1, 1, 1)

        self.ids.seven_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.eight_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.nine_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.four_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.five_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.six_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.three_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.two_btn.background_color = (133 / 255, 132 / 255, 130 / 255, 1)

        self.ids.pow_btn.text = "x²"
        self.ids.pow_btn.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.pow_btn.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.sqr_btn.text = "√x"
        self.ids.sqr_btn.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.sqr_btn.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.log_btn.text = "log"
        self.ids.log_btn.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.log_btn.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.one_over_x.text = "1/x"
        self.ids.one_over_x.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.one_over_x.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.percent_btn.text = "%"
        self.ids.percent_btn.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.percent_btn.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.pi_btn.text = "π"
        self.ids.pi_btn.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.pi_btn.color = (247 / 255, 242 / 255, 242 / 255)

    def hex_keyboard(self):
        self.ids.dec_btn.background_color = (1, 1, 1, 1)
        self.ids.bin_btn.background_color = (1, 1, 1, 1)
        self.ids.hex_btn.background_color = (50 / 255, 145 / 255, 168 / 255, 1)

        self.ids.seven_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.eight_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.nine_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.four_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.five_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.six_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.three_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.two_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.pow_btn.text = 'A'
        self.ids.pow_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)
        self.ids.pow_btn.color = (0, 0, 0, 1)

        self.ids.sqr_btn.text = 'B'
        self.ids.sqr_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)
        self.ids.sqr_btn.color = (0, 0, 0, 1)

        self.ids.log_btn.text = 'C'
        self.ids.log_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)
        self.ids.log_btn.color = (0, 0, 0, 1)

        self.ids.percent_btn.text = 'D'
        self.ids.percent_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)
        self.ids.percent_btn.color = (0, 0, 0, 1)

        self.ids.one_over_x.text = 'E'
        self.ids.one_over_x.background_color = (255 / 255, 255 / 255, 255 / 255, 1)
        self.ids.one_over_x.color = (0, 0, 0, 1)

        self.ids.pi_btn.text = 'F'
        self.ids.pi_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)
        self.ids.pi_btn.color = (0, 0, 0, 1)

    def dec_keyboard(self):
        self.ids.dec_btn.background_color = (50 / 255, 145 / 255, 168 / 255, 1)
        self.ids.bin_btn.background_color = (1, 1, 1, 1)
        self.ids.hex_btn.background_color = (1, 1, 1, 1)

        self.ids.seven_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.eight_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.nine_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.four_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.five_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.six_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.three_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.two_btn.background_color = (255 / 255, 255 / 255, 255 / 255, 1)

        self.ids.pow_btn.text = "x²"
        self.ids.pow_btn.background_color = (55/255, 55/255, 55/255)
        self.ids.pow_btn.color = (247/255, 242/255, 242/255)

        self.ids.sqr_btn.text = "√x"
        self.ids.sqr_btn.background_color = (55/255, 55/255, 55/255)
        self.ids.sqr_btn.color = (247/255, 242/255, 242/255)

        self.ids.log_btn.text = "log"
        self.ids.log_btn.background_color = (55/255, 55/255, 55/255)
        self.ids.log_btn.color = (247/255, 242/255, 242/255)

        self.ids.percent_btn.text = "%"
        self.ids.percent_btn.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.percent_btn.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.one_over_x.text = "1/x"
        self.ids.one_over_x.background_color = (55 / 255, 55 / 255, 55 / 255)
        self.ids.one_over_x.color = (247 / 255, 242 / 255, 242 / 255)

        self.ids.pi_btn.text = "π"
        self.ids.pi_btn.background_color = (55/255, 55/255, 55/255)
        self.ids.pi_btn.color = (247/255, 242/255, 242/255)

    def conversions(self, num_system):

        if self.ids.calc_input.text == c:
            return
        if '-' in self.ids.calc_input.text:
            return
        # code //
        if self.current_num_sys == 'hex':
            string = self.ids.calc_input.text.replace(" ", "")
            if num_system == '2dec':
                self.current_num_sys = 'dec'
                self.dec_keyboard()
                dec_code = hex2dec(string)
                self.ids.calc_input.text = str(dec_code)

            elif num_system == '2bin':
                self.current_num_sys = 'bin'
                self.bin_keyboard()
                dec_code = hex2dec(string)
                bin_code = dec2bin(str(dec_code))
                self.ids.calc_input.text = str(bin_code)
            return

        number = str(self.ids.calc_input.text.replace(" ", ""))
        if self.current_num_sys == 'dec':
            if num_system == '2bin':
                self.current_num_sys = 'bin'
                self.bin_keyboard()
                bin_code = dec2bin(number)
                self.ids.calc_input.text = str(bin_code)

            elif num_system == '2hex':
                self.current_num_sys = 'hex'
                self.hex_keyboard()
                hex_code = dec2hex(number)
                self.ids.calc_input.text = str(hex_code)

        elif self.current_num_sys == 'bin':
            if num_system == '2dec':
                self.current_num_sys = 'dec'
                self.dec_keyboard()
                dec_code = bin2dec(number)
                self.ids.calc_input.text = str(dec_code)

            elif num_system == '2hex':
                self.current_num_sys = 'hex'
                self.hex_keyboard()
                dec_code = bin2dec(number)
                hex_code = dec2hex(str(dec_code))
                self.ids.calc_input.text = str(hex_code)

    def keyboard_input(self, window, key, *args):
        str_key = ''
        ascii2char = {
            8: 'del', 256: '0', 257: "1", 258: "2", 259: "3", 260: "4", 261: "5", 262: "6", 263: "7", 264: "8", 265: "9", 266: ".", 267: "÷", 268: "×", 269: "-", 270: "+", 271: "=", 228: '(', 328: ')', 99: 'c'
        }

        for asciikeys, value in ascii2char.items():
            if asciikeys == key:
                str_key = value

        if str_key != '':
            if str_key in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.clicked(str_key)
            elif str_key in ['+', '-', '×', '÷']:
                self.operations(str_key)
            elif str_key == '=':
                self.result()
            elif str_key == 'del':
                self.special(str_key)
            elif str_key == '.':
                self.multidec()
            elif str_key == ')' or str_key == '(':
                self.brackets(str_key)
            elif str_key == 'c':
                self.all_clear()
        else:
            return

    def trigonometric(self, f):

        if f == "deg":
            if self.ids.deg_btn.text == "Deg(°)":
                self.ids.deg_btn.text = "Rad"
            else:
                self.ids.deg_btn.text = "Deg(°)"
            return

        if self.ids.calc_input.text == c:
            return
        if self.current_num_sys != 'dec':
            return
        # code //
        input_text = self.ids.calc_input.text.replace("π", str(math.pi)).replace(' ', '')
        if f == "sin":
            if self.ids.sin_btn.text == "sin":
                if self.ids.deg_btn.text == "Deg(°)":
                    deg2rad = math.radians(float(input_text))
                    result = math.sin(deg2rad)
                else:
                    result = math.sin(float(input_text))
                result = round_dec_part(result, 5)
                self.ids.calc_input.text = str(result)
            else:
                if float(self.ids.calc_input.text.replace(' ', '').replace('π', str(math.pi))) > 1 or float(self.ids.calc_input.text) < 0:
                    self.ids.calc_input.text = "Chyba"
                    return
                result = math.asin(float(self.ids.calc_input.text))
                if self.ids.deg_btn.text == "Deg(°)":
                    result = result * (180.0 / math.pi)
                result = round_dec_part(result, 5)
                self.ids.calc_input.text = str(result)

        elif f == "cos":
            if self.ids.cos_btn.text == "cos":
                if self.ids.deg_btn.text == "Deg(°)":
                    deg2rad = math.radians(float(input_text))
                    result = math.cos(deg2rad)
                else:
                    result = math.cos(float(input_text))
                result = round_dec_part(result, 5)
                self.ids.calc_input.text = str(result)
            else:
                if float(self.ids.calc_input.text.replace(' ', '').replace('π', str(math.pi))) > 1 or float(self.ids.calc_input.text) < 0:
                    self.ids.calc_input.text = "Chyba"
                    return
                result = math.acos(float(self.ids.calc_input.text))
                if self.ids.deg_btn.text == "Deg(°)":
                    result = result * (180.0 / math.pi)
                result = round_dec_part(result, 5)
                self.ids.calc_input.text = str(result)

        elif f == "tan":
            if self.ids.tan_btn.text == "tan":
                if float(input_text) % 180 == 90:
                    self.ids.calc_input.text = "Chyba"
                    return
                if self.ids.deg_btn.text == "Deg(°)":
                    deg2rad = math.radians(float(input_text))
                    result = math.tan(deg2rad)
                else:
                    result = math.tan(float(input_text))
                result = round_dec_part(result, 5)
                self.ids.calc_input.text = str(result)
            else:
                result = math.atan(float(input_text))
                if self.ids.deg_btn.text == "Deg(°)":
                    result = result * (180.0 / math.pi)
                if result < 89:
                    result = round_dec_part(result, 5)
                else:
                    integer_part, decimal_part = str(result).split(".")
                    result = integer_part + '.' + decimal_part[:5]
                self.ids.calc_input.text = str(result)

        dec_p = self.ids.calc_input.text.split('.')
        if dec_p[1] == '0':
            self.ids.calc_input.text = dec_p[0]

    def clicked(self, num):
        if self.result_clicked:
            if self.ids.calc_label.text != '(':
                self.ids.calc_label.text = ''
            self.ids.calc_input.text = f'{num}'
            self.result_clicked = False
            return
        if self.current_num_sys == 'bin' and int(num) > 1:
            return

        input_text = self.ids.calc_input.text
        if len(input_text) >= 14:
            return
        # code //
        if input_text == '0' or input_text == '-0':
            self.ids.calc_input.text = ''
            self.ids.calc_input.text = f'{num}'
        elif input_text == 'π':
            return
        elif self.ids.calc_input.text == "Chyba" or self.ids.calc_input.text == "Error":
            self.ids.calc_input.text = f'{num}'
        elif '.' not in input_text:
            if self.current_num_sys == 'dec':
                input_text = input_text.replace(" ", "")
                input_text = f'{input_text}{num}'
                formatted_text = '{:,}'.format(int(input_text)).replace(",", " ")
            else:
                input_text = input_text.replace(" ", "")
                formatted_text = f'{input_text}{num}'
            self.ids.calc_input.text = formatted_text
        else:
            self.ids.calc_input.text = f'{input_text}{num}'

    def operations(self, operation):
        if self.current_num_sys != 'dec':
            return
        if self.ids.calc_input.text == c:
            return

        label_text = self.ids.calc_label.text
        if self.result_clicked:
            self.result_clicked = False
            if len(label_text) > 0 and label_text[-1] != '(':
                self.ids.calc_label.text = self.ids.calc_label.text + operation
            else:
                self.ids.calc_label.text = self.ids.calc_label.text + self.ids.calc_input.text + operation
            self.ids.calc_input.text = '0'
            return

        # code //
        if len(label_text) == 0:
            self.ids.calc_label.text = self.ids.calc_label.text + self.ids.calc_input.text
        elif len(label_text) > 0 and label_text[-1] != ')':
            self.ids.calc_label.text = self.ids.calc_label.text + self.ids.calc_input.text

        self.ids.calc_input.text = ''

        operations = ['+', '-', '÷', '×', '%']
        if self.ids.calc_label.text[-1] not in operations:
            self.ids.calc_label.text = self.ids.calc_label.text + operation

        self.ids.calc_input.text = '0'

    def brackets(self, bracket):
        if self.current_num_sys != 'dec':
            return
        if self.ids.calc_input.text == c:
            return
        
        label_text = self.ids.calc_label.text

        right_brackets = 0
        left_brackets = 0

        for b in self.ids.calc_label.text:
            if b == ")":
                right_brackets = right_brackets+1
            elif b == "(":
                left_brackets = left_brackets+1

        if label_text != '':
            if bracket == '(':
                if label_text[-1] == ')':
                    self.ids.calc_label.text = self.ids.calc_label.text + '×('
                else:
                    self.ids.calc_label.text = self.ids.calc_label.text + '('
            elif bracket == ")":
                if left_brackets >= 1 and left_brackets > right_brackets:
                    self.ids.calc_label.text = self.ids.calc_label.text + self.ids.calc_input.text + ')'
                    self.ids.calc_input.text = '0'
        else:
            if bracket == '(':
                self.ids.calc_label.text = self.ids.calc_label.text + '('

    def all_clear(self):
        if self.ids.calc_input.text == '0':
            self.ids.calc_label.text = ''
        else: self.ids.calc_input.text = '0'

    def pos_neg(self):
        input_text = self.ids.calc_input.text

        if input_text == c:
            return
        if self.current_num_sys != 'dec':
            return

        elif '-' in input_text:
            self.ids.calc_input.text = f"{input_text.replace('-', '')}"
        else:
            self.ids.calc_input.text = f'-{input_text}'

    def multidec(self):
        if self.ids.calc_input.text == c:
            return

        if self.ids.calc_input.text[-1] != 'π' and self.ids.calc_input.text[-1] != 'e' and self.ids.calc_input.text[-1] != '.':
            self.ids.calc_input.text = self.ids.calc_input.text + "."
        else:
            return

    def special(self, op):

        if self.ids.calc_input.text == c:
            return
        if self.current_num_sys == 'bin':
            return

        if op == "alt":
            if self.current_num_sys != 'dec':
                return

            if self.ids.alt_btn.text == "2nd":
                self.ids.alt_btn.text = "1st"
                self.ids.sin_btn.text = "asin"
                self.ids.cos_btn.text = "acos"
                self.ids.tan_btn.text = "atan"
                self.ids.pow_btn.text = "xⁿ"
                self.ids.sqr_btn.text = "³√x"
                return
            else:
                self.ids.alt_btn.text = "2nd"
                self.ids.sin_btn.text = "sin"
                self.ids.cos_btn.text = "cos"
                self.ids.tan_btn.text = "tan"
                self.ids.pow_btn.text = "x²"
                self.ids.sqr_btn.text = "√x"
                return

        self.ids.calc_input.text = self.ids.calc_input.text.replace(" ", "")
        if op != 'del':
            self.ids.calc_input.text = self.ids.calc_input.text.replace("π", str(math.pi))

        if op == "pow":
            if self.ids.pow_btn.text == 'A':
                self.clicked('A')
                return

            elif self.ids.pow_btn.text == 'x²':
                if "." in self.ids.calc_input.text:
                    result = round_dec_part((float(self.ids.calc_input.text)**2), 2)
                else:
                    result = int(self.ids.calc_input.text) ** 2

                if len(str(result)) <= 15:
                    result = '{:,}'.format(result).replace(",", " ")
                    self.ids.calc_input.text = str(result)
                else:
                    self.ids.calc_input.text = '{:e}'.format(result)

            else:
                if self.result_clicked:
                    self.ids.calc_label.text = ''
                self.ids.calc_label.text = self.ids.calc_label.text + self.ids.calc_input.text + '^'
                self.ids.calc_input.text = '0'

        elif op == "sqr":
            if self.ids.sqr_btn.text == 'B':
                self.clicked('B')
                return
            elif self.ids.sqr_btn.text == '√x':
                if float(self.ids.calc_input.text) < 0:
                    self.ids.calc_input.text = 'Chyba'
                    return
                result = round_dec_part(math.sqrt(float(self.ids.calc_input.text)), 5)
                result = '{:,}'.format(result).replace(",", " ")
                self.ids.calc_input.text = str(result)
            else:
                if float(self.ids.calc_input.text) < 0:
                    self.ids.calc_input.text = 'Chyba'
                    return
                result = round_dec_part(pow(float(self.ids.calc_input.text), 1/3), 5)
                result = '{:,}'.format(result).replace(",", " ")
                self.ids.calc_input.text = str(result)

            dec_p = self.ids.calc_input.text.split('.')
            if dec_p[1] == '0':
                self.ids.calc_input.text = dec_p[0]

        elif op == "log":
            if self.ids.log_btn.text == 'C':
                self.clicked('C')
                return
            input_f = float(self.ids.calc_input.text.replace(" ", ""))
            if self.ids.log_btn.text == 'log':
                if input_f <= 0:
                    self.ids.calc_input.text = 'Chyba'
                    return
                self.ids.calc_input.text = str(round_dec_part(math.log10(input_f), 5))

            dec_p = self.ids.calc_input.text.split('.')
            if dec_p[1] == '0':
                self.ids.calc_input.text = dec_p[0]

        elif op == "%":
            if self.ids.percent_btn.text == 'D':
                self.clicked('D')
                return

            self.ids.calc_input.text = str(float(self.ids.calc_input.text)/100)

        elif op == "1/x":
            if self.ids.one_over_x.text == 'E':
                self.clicked('E')
                return

            input_text = self.ids.calc_input.text
            if input_text == '0':
                self.ids.calc_input.text = 'Chyba'
                return
            result = round_dec_part(1 / float(input_text), 3)
            self.ids.calc_input.text = str(result)

            dec_p = self.ids.calc_input.text.split('.')
            if dec_p[1] == '0':
                self.ids.calc_input.text = dec_p[0]

        elif op == 'pi':
            if self.ids.pi_btn.text == 'F':
                self.clicked('F')
                return

            if self.ids.calc_input.text != '0':
                self.ids.calc_input.text = str(round_dec_part(float(self.ids.calc_input.text) * math.pi, 5))
            else:
                self.ids.calc_input.text = 'π'

        elif op == "del":
            if "." not in self.ids.calc_input.text:
                if len(self.ids.calc_input.text.replace(" ", "")) > 1:
                    if self.current_num_sys == 'dec':
                        input_text = self.ids.calc_input.text[:-1]
                        self.ids.calc_input.text = '{:,}'.format(int(input_text)).replace(',', " ")
                    else:
                        self.ids.calc_input.text = self.ids.calc_input.text[:-1]
                else:
                    self.ids.calc_input.text = "0"
            else:
                self.ids.calc_input.text = self.ids.calc_input.text[:-1]

    def saved_value(self, memory):
        if self.current_num_sys != 'dec':
            return
        if self.ids.calc_input.text == c:
            return

        if memory == 'ms':
            self.memory_value = self.ids.calc_input.text
        elif memory == 'mr':
            self.ids.calc_input.text = self.memory_value

    def result(self):
        if self.current_num_sys != 'dec':
            return
        if self.result_clicked:
            return
        if len(self.ids.calc_label.text) < 1:
            return

        self.result_clicked = True

        if self.ids.calc_label.text[-1] != ')':
            self.ids.calc_label.text = self.ids.calc_label.text + self.ids.calc_input.text

        replace = {"^": "**", "÷": "/", "×": "*", "π": str(math.pi)}
        for old, new in replace.items():
            self.ids.calc_label.text = self.ids.calc_label.text.replace(old, new)

        operations = ['+', '-', '/', '*', '%']
        if self.ids.calc_label.text[-1] in operations:
            self.ids.calc_label.text = self.ids.calc_label.text[: -1]

        right_brackets = 0
        left_brackets = 0

        for b in self.ids.calc_label.text:
            if b == ")":
                right_brackets += 1
            elif b == "(":
                left_brackets += 1
        while left_brackets > right_brackets:
            self.ids.calc_label.text = self.ids.calc_label.text + ')'
            right_brackets += 1

        corrected_problem = self.ids.calc_label.text.replace(" ", "")

        try:
            result = round(eval(corrected_problem), 5)
            print(result)
            if len(str(result)) < 12:
                result = '{:,}'.format(result).replace(",", " ")
                if '.' in result:
                    dec_p = str(result).split('.')
                    if dec_p[1] == '0':
                        result = dec_p[0]
                self.ids.calc_input.text = str(result)
            else:
                self.ids.calc_input.text = '{:e}'.format(result)

            r_replace = {v: k for k, v in replace.items()}
            for old, new in r_replace.items():
                self.ids.calc_label.text = self.ids.calc_label.text.replace(old, new)

        except:
            self.ids.calc_input.text = 'Chyba'


class MyApp(App):

    def build(self):
        self.title = "kalkulačka"
        my_calc = MyCalc()
        Window.bind(on_keyboard=my_calc.keyboard_input)
        return my_calc


if ctypes.windll.kernel32.GetConsoleWindow() != 0:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.kernel32.CloseHandle(ctypes.windll.kernel32.GetConsoleWindow())

if __name__ == "__main__":
    MyApp().run()

