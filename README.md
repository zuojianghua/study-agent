# study-agent
孩子的学习资料

## 抽取资料到markdown

安装minerU并下载模型
```
pip install -U "magic-pdf[full]" -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install modelscope -i https://pypi.tuna.tsinghua.edu.cn/simple
wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/scripts/download_models.py -O download_models.py
python download_models.py
```

更改配置文件 magic-pdf.json c:/Users/用户名
```
{
  "device-mode": "cuda"
}
```

抽取命令
```
magic-pdf -p .\yw_6_0.pdf -o yw_6_0 -m auto
```