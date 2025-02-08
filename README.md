# LunarDate-SolarDate_Calculator
 农历日期与公历日期重叠年份计算器

## Step 1. 安装 Python

1. 访问 Python 官方网站 [python.org](https://www.python.org/)。
2. 选择适合您操作系统的 Python 版本进行下载。
3. 运行安装程序，确保勾选了“Add Python to PATH”（将 Python 添加到 PATH）选项。
4. 完成安装后，打开命令行工具，输入 `python --version` 来验证 Python 是否安装成功。

## Step 2. 安装 Pip 工具

**通常情况下，Python 会自带 Pip！**
**但如果运行pip显示不存在，请先完成下面Step2的所有步骤。**

1. 打开命令行工具。
2. 在 Windows 上，输入以下命令：

   python -m ensurepip --upgrade

3. 在 macOS 或 Linux 上，输入以下命令：

   python -m ensurepip --upgrade

4. 验证 Pip 是否安装成功，输入 `pip --version`。

## Step 3. 安装 Poetry 包管理工具

1. 确保已经安装了 Python 和 Pip。
2. 打开命令行工具。
3. 安装 Poetry，输入以下命令：

   pip install poetry

4. 验证 Poetry 是否安装成功，输入 `poetry --version`。

## Step 4. 安装项目依赖

1. 克隆或下载项目代码到本地。
2. 打开命令行工具，导航到项目目录。
3. 使用 Poetry 创建并激活虚拟环境（可选，但推荐）：

   poetry install

4. 如果项目中存在 `pyproject.toml` 文件，Poetry 将自动安装所有依赖项。
5. 如果需要手动添加依赖项，可以使用以下命令：

   poetry add package_name

## Step 5. 运行它

1. 确保您在项目目录中，并且已经安装了所有依赖项。
2. 使用 Poetry 运行项目：

   poetry run python LunarDate-SolarDate_Calculator.py
