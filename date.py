from lunardate import LunarDate
import re
from colorama import init, Fore, Style
import sys

# 初始化 colorama
init(autoreset=True)

def validate_input(text):
    # 正则表达式允许1到12月份，以及1到31日，分隔符可以是任意非数字字符
    pattern = re.compile(r'^(\d{1,2})([^0-9]+)(\d{1,2})$')
    match = pattern.match(text)
    if not match:
        return False, f"输入格式错误，应为月份+任意非数字分隔符+日期，如 '4月5日'、'4-5'、'4.5'、'4&5'、'4 5' 等。 错误来源： {text}"
    
    month = int(match.group(1))
    day = int(match.group(3))

    # 检查月份的有效性
    if month < 1 or month > 12:
        return False, f"月份错误，月份应在1到12之间。"
    
    # 检查日期的有效性
    if day < 1 or day > 31:
        return False, f"日期错误，日期应在1到31之间。"

    # 检查特殊月份的最大天数
    if month in [4, 6, 9, 11] and day > 30:
        return False, f"公历日期错误，该月份最大天数为30！"
    
    # 检查2月的日期
    if month == 2 and day > 29:
        return False, f"输入错误，2月最大天数为29！"

    # 检查农历月份的最大天数
    try:
        LunarDate(2023, month, day).toSolarDate()
    except ValueError:
        return False, f"农历日期错误，该月份不存在此日期！"

    return True, (month, day)

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def find_overlapping_years(lunar_input, solar_input, start_year=2000):
    lunar_month, lunar_day = lunar_input
    solar_month, solar_day = solar_input
    start_year = int(start_year) if start_year else 2000

    if start_year < 1900 or start_year >= 2100:
        raise ValueError("年份必须在1900年至2099年之间。")

    overlapping_years = []
    current_year = start_year
    while current_year < 2100:
        lunar_date = LunarDate(current_year, lunar_month, lunar_day)
        converted_solar_date = lunar_date.toSolarDate()
        if (converted_solar_date.month, converted_solar_date.day) == (solar_month, solar_day):
            if solar_month == 2 and solar_day == 29 and not is_leap_year(current_year):
                continue
            overlapping_years.append(current_year)
        current_year += 1

    return overlapping_years

def main():
    # 使用Fore.LIGHTMAGENTA_EX高亮显示提示信息
    intro_text = (
        "欢迎使用农历与公历重叠年份查找器！\n"
        "请按照提示输入相应的日期。\n"
        "支持的日期格式包括：4月5日、4-5、4.5、4&5、4 5 等。\n\n"
    )
    exit_instructions = (
        "在任意处按Ctrl+C或输入“q”、“quit”、“exit”（不区分大小写）退出程序。\n"
    )

    print(Fore.LIGHTMAGENTA_EX + intro_text)
    print(Fore.LIGHTBLUE_EX + exit_instructions)  # 使用Fore.LIGHTBLUE_EX高亮显示退出指令

    while True:
        lunar_input = input("请输入农历月份和日期（例如：4月5日、4-5、4.5、4&5、4 5等）: ")
        if lunar_input.lower() in ['q', 'quit', 'exit']:
            print("程序已中止···")
            break
        
        solar_input = input("请输入公历月份和日期（例如：4月5日、4-5、4.5、4&5、4 5等）: ")
        if solar_input.lower() in ['q', 'quit', 'exit']:
            print("程序已中止···")
            break
        
        start_year = input("请输入开始计算的年份（直接回车使用默认值2000年）: ")
        if start_year.lower() in ['q', 'quit', 'exit']:
            print("程序已中止···")
            break

        errors = []

        # 验证农历输入
        valid_lunar, valid_lunar_data = validate_input(lunar_input)
        if not valid_lunar:
            errors.append(f"农历 {lunar_input}: {valid_lunar_data}")

        # 验证公历输入
        valid_solar, valid_solar_data = validate_input(solar_input)
        if not valid_solar:
            errors.append(f"公历 {solar_input}: {valid_solar_data}")

        if errors:
            print("")
            print(Fore.LIGHTYELLOW_EX + "\n".join(errors))
            continue

        try:
            overlapping_years = find_overlapping_years(valid_lunar_data, valid_solar_data, start_year or None)
            if overlapping_years:
                print("")
                print("以下年份中，农历和公历的日期重合：")
                highlighted_years = ', '.join(Fore.LIGHTCYAN_EX + str(year) + Style.RESET_ALL for year in overlapping_years)
                print(highlighted_years)
            else:
                print("")
                print("未找到匹配的年份。")
        except ValueError as e:
            print("")
            print(Fore.LIGHTYELLOW_EX + str(e))

        input("按Enter键继续...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已中止···")