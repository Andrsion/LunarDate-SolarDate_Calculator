from kivy.metrics import dp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from lunardate import LunarDate
import os
import re

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)

class OverlappingYearsApp(App):
    def build(self):
        self.font_path = 'font/NotoSans.ttf'
        if not os.path.exists(self.font_path):
            raise FileNotFoundError("字体文件未找到，请确保 'font/NotoSans.ttf' 存在于项目目录中。")

        self.title = "农历与公历重叠年份查找器"
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.lunar_input = TextInput(hint_text="请输入农历月份和日期（例如：4月5日）", font_name=self.font_path)
        self.solar_input = TextInput(hint_text="请输入公历月份和日期（例如：4月5日）", font_name=self.font_path)
        self.start_year_input = TextInput(hint_text="请输入开始计算的年份", font_name=self.font_path, multiline=False)

        self.compute_button = RoundedButton(text="计算", font_name=self.font_path)
        self.result_label = Label(text="", font_name=self.font_path, size_hint_y=None, height=dp(50))

        self.compute_button.bind(on_release=self.find_overlapping_years)
        layout.add_widget(self.lunar_input)
        layout.add_widget(self.solar_input)
        layout.add_widget(self.start_year_input)
        layout.add_widget(self.compute_button)
        layout.add_widget(self.result_label)

        Window.size = (360, 480)
        return layout

    def validate_input(self, text):
        # 正则表达式允许1到12月份，以及1到31日，分隔符可以是任意非数字字符
        pattern = re.compile(r'^(1[0-2]|0?[1-9])([^\d]+)(3[01]|[12][0-9]|0?[1-9])$')
        match = pattern.match(text)
        if not match:
            raise ValueError("输入格式错误，应为月份+任意非数字分隔符+日期，如 '4-5'、'4.5'、'4&5'、'4 5' 等。")
        # 返回转换为整数的月份和日期
        return int(match.group(1)), int(match.group(3))

    def find_overlapping_years(self, instance):
        try:
            lunar_month, lunar_day = self.validate_input(self.lunar_input.text.strip())
            solar_month, solar_day = self.validate_input(self.solar_input.text.strip())
            start_year = int(self.start_year_input.text.strip())

            if start_year < 1900 or start_year >= 2100:
                raise ValueError("年份必须在1900年至2099年之间。")

            overlapping_years = []
            current_year = start_year
            lunar_date = LunarDate(current_year, lunar_month, lunar_day)  # 创建一次即可
            while current_year < 2100:
                converted_solar_date = lunar_date.toSolarDate()
                if (converted_solar_date.month, converted_solar_date.day) == (solar_month, solar_day):
                    overlapping_years.append(current_year)
                current_year += 1
                lunar_date = LunarDate(current_year, lunar_month, lunar_day)  # 移动到循环内部

            result_text = "以下年份中，农历和公历的日期重合：\n" + \
                ', '.join(map(str, overlapping_years)) if overlapping_years else "未找到匹配的年份。"
            self.show_popup(result_text)

        except ValueError as e:
            self.result_label.text = str(e)

    def show_popup(self, text):
        # 创建一个 Label 控件来显示文本
        popup_label = Label(
            text=text,
            font_name=self.font_path,
            text_size=(None, None),  # 允许 Label 宽度和高度根据内容自动调整
            halign='center',  # 水平居中
            valign='top',  # 垂直顶部对齐
        )

        # 创建关闭按钮，并绑定点击事件
        close_button = RoundedButton(
            text="关闭",
            font_name=self.font_path,
            size_hint_y=None,  # 确保按钮有固定的高度而不是依赖于size_hint
            height=dp(50)  # 根据dp调整按钮高度
        )
        close_button.bind(on_release=self.close_popup)  # 使用 on_release 事件

        # 创建一个 BoxLayout 来包含 Label 和关闭按钮
        button_layout = BoxLayout(orientation='vertical', spacing=10)
        button_layout.add_widget(popup_label)  # 将 Label 添加到布局中
        # 将关闭按钮添加到布局中，并确保它在底部
        button_layout.add_widget(close_button)

        # 创建弹窗，不显示标题，并将 BoxLayout 作为内容
        self.popup = Popup(  # 确保将popup引用存储在类属性中
            title='',
            content=button_layout,
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

        # 打开弹窗
        self.popup.open()

    def close_popup(self, instance):
        # 关闭 Popup 逻辑
        if self.popup:
            self.popup.dismiss()

# 程序入口点
if __name__ == '__main__':
    OverlappingYearsApp().run()