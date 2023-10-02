:: 安装环境
start "" cmd /k "conda create -y -n chanlun python=3.10&&activate chanlun&&conda install -y pandas requests numpy redis matplotlib pymysql&&conda install -y -c conda-forge ta-lib  ipywidgets&&pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/&&pip3 install -r requirements.txt&&pip3 install wheel&&pip3 install package/pytdx-1.72r2-py3-none-any.whl"
