# 环境部署与使用说明

本项目需要部署MinerU和Spacy，文档提供在线与离线两种部署方案。

## 在线部署

1. 强烈推荐python=3.10。

2. 安装magic-pdf,运行

```
pip install -U "magic-pdf[full]" --extra-index-url https://wheels.myhloli.com -i https://mirrors.aliyun.com/pypi/simple
```

3. 权重模型下载,推荐从modelscope下载模型

```
pip install modelscope

wget https://gcore.jsdelivr.net/gh/opendatalab/MinerU@master/scripts/download_models.py -O download_models.py
```

windows系统将wget改为curl即可。

4. 测试

```
magic-pdf -p 需要解析pdf路径 -o 输出路径
```

5. spacy安装，可以在清华源上下载

```
pip install spacy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

6. 使用pip list查看spacy版本，根据版本在https://github.com/explosion/spacy-models/releases选择对应模型文件下载，tar.gz和whl都要下载，执行
```
pip install tar.gz文件路径
```
模型选择时注意网站给出python和spacy版本要求。根据后续工作需求选择合适模型，以en_core_web_sm为例，en指英文(中文是zh)，core指具有标记、解析、词形还原和命名实体识别的通用模型；web 表示模型训练使用网络文本；sm指模型大小，另外有md和lg可以选择。

## 离线部署

考虑部分服务器不联网，给出如下离线部署方案。

1. 需要一个可联网的机器或虚拟机(下面简称主机)，操作系统必须与服务器完全相同，例如CentOS7不能与CentOS8或Ubuntu版本兼容。另外，CentOS7或其他早期Linux版本MinerU安装错误：尝试使用如下指令安装
```
pip install -U magic-pdf[full,old_linux] --extra-index-url https://wheels.myhloli.com -i https://mirrors.aliyun.com/pypi/simple
```
MinerU开发者反馈：由于CentOS7系统生命周期已经结束，后续更新不保证继续支持此系统。但目前最新版还可以兼容。

2. 根据上述在线部署方案在可联网的主机的anaconda虚拟环境中部署。

3. 下载conda pack
   ```
   pip install conda-pack
   ```
   将环境进行打包迁移

   ```
   conda pack -n 环境名称
   ```

4. 将压缩包上传至服务器如/home/用户名/anaconda/evns目录下，创建一个环境名的文件夹，运行
```
tar -xzvf 环境名.tar.gz -C /home/用户名/anaconda3/envs/环境名
```
5. 将主机中系统目录/home/.cache/modelscope 文件夹上传到服务器/home/用户名/.cache/ 目录下
6. 将主机中系统目录中magic-pdf.json文件上传至/home/用户名/ 中，修改文件中"models-dir"和"layoutreader-model-dir"两个地址，例如/home/用户名/.cache/modelscope/XXX 把.cache文件前面路径改成正确的，后面不需要修改。至此MinerU可以在服务器上运行。
7. spacy库已经在虚拟环境中，将spacy压缩包和whl文件上传到服务器
   ```
   pip install 压缩包路径
   ```  
   即可。


## 使用说明

所有脚本在code文件夹中，下面介绍主要脚本功能与目前完成情况。

### main.py

调用Mineru批量解析指定目录下所有pdf文件，将结果写入./output文件夹。

### author.py

根据解析结果判断文章哪一段是作者，返回该段bbox值，并根据bbox值从原pdf上将该段落截取下来。结果存放在./cut_pdf。目前由于极个别文章第一页是封面以及spacy库识别中文拼音人名和非英文人名可能出现分类错误，会出现截取失败或错误定位问题。

### convert.py

默认作者段格式为：作者名^注释。根据该结构解析作者名和对应的注释，结果写为json文件，存放在./author。由于截取作者段时出现错误，脚本输出结果暂时不理想。

### title.py

输出文章标题，基本无错误。结果放在./title中。

### abstract.py

输出文章摘要，在测试1000份样例中约27%无明确摘要段落标志，暂时没有什么好的想法。












