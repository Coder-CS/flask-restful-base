# flask-result-base

一个基于 Flask 的 Restful 基础模板

## 使用方法

### 从这个模板创建你自己的 github 存储库

点击 [项目主页](https://github.com/oOxianOo/flask-restful-base) 右上角的绿色按钮 "Use this template"，输入仓库名字并保存。

### 克隆仓库

```
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME
```

### 安装虚拟环境（可选）

```
python -m venv venv

# windows 启动虚拟环境
venv\Scripts\activate

# Unix/MacOS
. venv/bin/activate
```

### 安装依赖包

```shell script
pip install -r requirements.txt
```

### 设置

在根目录 (与app文件同级) 建立 setting.json 文件，所有的配置将优先从此文件读取，具体设置可查看 app 文件夹下的 config.py

*以下字段必须设置*



### 启动

```shell script
flask run
```

