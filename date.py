from lunardate import LunarDate
import re
from colorama import init, Fore, Style
import sys

# 初始化 colorama
init(autoreset=True)

def validate_input(text, is_lunar=True):
    # 允许闰月前缀（如"闰4月5日"）
    pattern = re.compile(r'^(闰?)[^\d]*(\d{1,2})[^\d]+(\d{1,2})$')
    match = pattern.match(text.strip())
    if not match:
        return False, f"输入格式错误，示例：'闰4月5日' 或 '4-5'"
    
    is_leap = match.group(1) != ''
    month = int(match.group(2))
    day = int(match.group(3))

    # 通用月份检查
    if month < 1 or month > 12:
        return False, "月份错误，应为1-12"
    
    # 农历日期：允许1-30日（具体有效性由年份检查决定）
    if is_lunar:
        if day < 1 or day > 30:
            return False, "农历日期应为1-30"
    # 公历日期：严格检查
    else:
        if month in [4, 6, 9, 11] and day > 30:
            return False, "公历月份最大30天"
        elif month == 2:
            if day > 29:
                return False, "公历2月最多29天"
        elif day > 31:
            return False, "公历日期无效"

    return True, (month, day, is_leap) if is_lunar else (month, day)

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def find_overlapping_years(lunar_input, solar_input, start_year=2000):
    lunar_month, lunar_day, is_leap = lunar_input
    solar_month, solar_day = solar_input
    start_year = int(start_year) if start_year else 2000

    if start_year < 1900 or start_year >= 2100:
        raise ValueError("年份必须在1900年至2099年之间。 ")

    overlapping_years = []
    current_year = start_year
    while current_year < 2100:
        try:
            if is_leap:
                # 查找闰月
                leap_months = [i for i in range(1, 13) if LunarDate.fromSolarDate(current_year, 1, 1).isleapmonth(i)]
                if lunar_month not in leap_months:
                    continue
                lunar_date = LunarDate.fromSolarDate(current_year, 1, 1).nextLeapMonth()
                for _ in range(lunar_month - 1):
                    lunar_date = lunar_date.nextMonth(isLeapMonth=True)
            else:
                lunar_date = LunarDate(current_year, lunar_month, lunar_day)
            
            converted_solar_date = lunar_date.toSolarDate()
            if (converted_solar_date.month, converted_solar_date.day) == (solar_month, solar_day):
                if solar_month == 2 and solar_day == 29 and not is_leap_year(current_year):
                    continue
                overlapping_years.append(current_year)
        except ValueError:
            pass  # 跳过无效日期
        current_year += 1

    return overlapping_years

def main():
    intro_text = (
        "欢迎使用农历与公历重叠年份查找器！\n"
        "请按照提示输入相应的日期。\n"
        "支持的日期格式包括：4月5日、4-5、4.5、4&5、4 5 等。\n"
        "支持闰月输入，例如：'闰4月5日'、'闰4-5'\n\n"
    )
    exit_instructions = (
        "在任意处按Ctrl+C或输入“q”、“quit”、“exit”（不区分大小写）退出程序。\n"
    )

    print(Fore.LIGHTMAGENTA_EX + intro_text)
    print(Fore.LIGHTBLUE_EX + exit_instructions)

    while True:
        lunar_input = input("请输入农历月份和日期（例如：4月5日、4-5、4.5、4&5、4 5等）: ").strip().lower()
        if lunar_input in ['q', 'quit', 'exit']:
            print("程序已中止···")
            break

        solar_input = input("请输入公历月份和日期（例如：4月5日、4-5、4.5、4&5、4 5等）: ").strip().lower()
        if solar_input in ['q', 'quit', 'exit']:
            print("程序已中止···")
            break

        start_year_input = input("请输入开始计算的年份（默认2000）: ").strip()
        if start_year_input.lower() in ['q', 'quit', 'exit']:
            print("程序已中止···")
            break
        if not start_year_input:
            start_year = 2000
        else:
            try:
                start_year = int(start_year_input)
                if start_year < 1900 or start_year >= 2100:
                    print(Fore.RED + "错误：年份需在1900-2099之间")
                    continue
            except ValueError:
                print(Fore.RED + "错误：请输入有效整数")
                continue

        errors = []

        # 验证农历输入
        valid_lunar, valid_lunar_data = validate_input(lunar_input, is_lunar=True)
        if not valid_lunar:
            errors.append(f"{Fore.RED}农历 {lunar_input}: {valid_lunar_data}")

        # 验证公历输入
        valid_solar, valid_solar_data = validate_input(solar_input, is_lunar=False)
        if not valid_solar:
            errors.append(f"{Fore.RED}公历 {solar_input}: {valid_solar_data}")

        if errors:
            print("\n".join(errors))
            continue

        try:
            overlapping_years = find_overlapping_years(valid_lunar_data, valid_solar_data, start_year or None)
            if overlapping_years:
                highlighted_years = ', '.join(Fore.LIGHTCYAN_EX + str(year) + Style.RESET_ALL for year in overlapping_years)
                print(f"\n以下年份中，农历和公历的日期重合：{highlighted_years}")
            else:
                print("\n未找到匹配的年份。 ")
        except ValueError as e:
            print(Fore.YELLOW + str(e))

        input("按Enter键继续...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已中止···")



