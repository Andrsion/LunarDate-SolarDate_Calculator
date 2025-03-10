import flet as ft
from datetime import datetime
import re
import time
from lunardate import LunarDate

def main(page: ft.Page):
    page.title = "公农历重叠年份查找器"
    page.theme_mode = ft.ThemeMode.DARK

    welcome_message = ft.Text(
        "欢迎使用公农历重叠年份查找器！",
        color=ft.Colors.PINK,
        style=ft.TextThemeStyle.TITLE_MEDIUM,
        text_align=ft.TextAlign.CENTER,
    )

    page.add(
        ft.Container(
            content=welcome_message,
            alignment=ft.alignment.center,
            expand=True,
        )
    )

    time.sleep(2)
    page.remove(page.controls[0])
    page.add(create_main_content(page))

    page.update()

def create_main_content(page):
    background_container = ft.Container(
        bgcolor=ft.Colors.WHITE,
        padding=40,
        border_radius=10,
        expand=True,
    )

    def on_submit(e):
        input_fields = [lunar_input_field, solar_input_field, start_year_field]
        valid = True
        error_messages = []

        lunar_text = lunar_input_field.value
        valid_lunar, valid_lunar_data = validate_input(lunar_text, is_lunar=True)
        if not valid_lunar:
            error_messages.append(f"农历 {lunar_text}: {valid_lunar_data}")
            valid = False

        solar_text = solar_input_field.value
        valid_solar, valid_solar_data = validate_input(solar_text, is_lunar=False)
        if not valid_solar:
            error_messages.append(f"公历 {solar_text}: {valid_solar_data}")
            valid = False

        start_year = start_year_field.value
        if not start_year:
            start_year = 2000
        else:
            try:
                start_year = int(start_year)
                if start_year < 1900 or start_year >= 2100:
                    error_messages.append("错误：年份需在1900-2099之间")
                    valid = False
            except ValueError:
                error_messages.append("错误：请输入有效整数")
                valid = False

        if not valid:
            error_text.value = "\n".join(error_messages)
            error_text.color = ft.Colors.RED
            error_text.update()
        else:
            error_text.value = ""
            error_text.update()
            try:
                overlapping_years = find_overlapping_years(
                    valid_lunar_data, valid_solar_data, start_year
                )
                if overlapping_years:
                    result_listview.controls = [
                        ft.Text(year, size=20, color=ft.Colors.LIGHT_BLUE) for year in overlapping_years
                    ]
                    result_header.value = "以下年份中，农历和公历的日期重合："
                    result_header.color = ft.Colors.PINK
                else:
                    result_header.value = "未找到匹配的年份。"
                    result_header.color = ft.Colors.GREY
                result_header.update()
                result_listview.update()
            except ValueError as e:
                error_text.value = str(e)
                error_text.color = ft.Colors.RED
                error_text.update()

    lunar_input_field = ft.TextField(
        label="农历日期（如4月5日、4-5等）",
        hint_text="农历示例：4.5",
        width=200,
        error_style=ft.TextStyle(color=ft.Colors.RED),
        on_submit=on_submit,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500), 
    )

    solar_input_field = ft.TextField(
        label="公历日期（如4月5日、4-5等）",
        hint_text="公历示例：4.5",
        width=200,
        error_style=ft.TextStyle(color=ft.Colors.RED),
        on_submit=on_submit,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500), 
    )

    start_year_field = ft.TextField(
        label="开始年份（默认2000）",
        value="2000",
        width=150,
        error_style=ft.TextStyle(color=ft.Colors.RED),
        on_submit=on_submit,
        color=ft.Colors.BLACK, 
        hint_style=ft.TextStyle(color=ft.Colors.GREY_500), 
    )

    calculate_button = ft.ElevatedButton(
        text="计算", on_click=lambda e: on_submit(e), width=200, height=50, color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE
    )

    error_text = ft.Text(size=14, color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)

    result_header = ft.Text(size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    result_listview = ft.ListView(expand=True, spacing=4, padding=4)

    main_content = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        lunar_input_field,
                        solar_input_field,
                        start_year_field,
                        calculate_button,
                    ],
                    spacing=10,
                ),
                error_text,
                result_header,
                result_listview,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=40,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
    )

    background_container.content = ft.Column(
        [
            main_content,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return background_container

def validate_input(text, is_lunar=True):
    pattern = re.compile(r'^([^\d]*)(\d{1,2})([^\d]+)(\d{1,2})([^\d]*)$')
    match = pattern.match(text.strip())
    if not match:
        return False, "输入格式错误，示例：'4.5' 或 '4-5'"
    
    month = int(match.group(2))
    day = int(match.group(4))

    if month < 1 or month > 12:
        return False, "月份错误，应为1-12"
    
    if is_lunar:
        if day < 1 or day > 30:
            return False, "农历日期应为1-30"
    else:
        if month in [4, 6, 9, 11] and day > 30:
            return False, "公历月份最大30天"
        elif month == 2:
            if day > 29:
                return False, "公历2月最多29天"
        elif day > 31:
            return False, "公历日期无效"

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
        try:
            lunar_date = LunarDate(current_year, lunar_month, lunar_day)
            solar_date = lunar_date.toSolarDate()
            if (solar_date.month, solar_date.day) == (solar_month, solar_day):
                overlapping_years.append(current_year)
        except ValueError:
            pass
        current_year += 1

    return overlapping_years

ft.app(target=main)
