import os
import json
import spacy
import fitz
import re
# 加载 spaCy 英语模型
nlp = spacy.load("en_core_web_sm")

import json
import spacy
def process_string(s):
    # 将$$及包括在内的内容替换为逗号
    s = re.sub(r'\$.*?\$', ',', s)
    # 删除所有非英文字母和非空格的字符
    s = re.sub(r'[^\s a-zA-Z]', '', s)
    return s
def find_min_word_paragraph_with_person(json_file_path):
    min_diff = float('inf')  # 初始化为无穷大，用于记录最小的（段落词数 - 人名数量）
    min_paragraph = None  # 初始化为空

    try:
        # 打开并读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"文件未找到：{json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"文件格式错误：{json_file_path}")
        return None

    # 遍历 JSON 数据中的所有项
    for item in json_data:
        if "text" in item:
            text = item["text"]
            text_p=process_string(text)
            # 使用 spaCy 处理文本
            doc = nlp(text_p)
            # 计算单词数量
            word_count = len([token for token in doc if token.is_alpha])
            # 统计人名数量
            person_count = sum(1 for ent in doc.ents if ent.label_ == "PERSON")
            print(text_p)
            print(person_count)
            # 确保人名数量不为0
            if person_count > 0:
                # 计算差值
                diff = word_count - person_count
                # 如果当前段落的差值更小，则更新结果
                if diff < min_diff:
                    min_diff = diff
                    min_paragraph = text

    return min_paragraph

def find_paragraph_bbox(json_file_path, target_paragraph):
   
    try:
        # 打开并读取 JSON 文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"文件未找到：{json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"文件格式错误：{json_file_path}")
        return None

    # 遍历 JSON 数据中的每个段落块
    for page in json_data.get("pdf_info", []):
        for block in page.get("preproc_blocks", []):
            if block["type"] == "text":
                lines = block.get("lines", [])
                # 检查每行的内容是否是目标段落的前缀（忽略空格）
                for line in lines:
                    line_content = ''.join(re.findall(r'[A-Za-z]', ''.join(span["content"] for span in line["spans"])))
    # 移除目标段落中的所有非字母部分并截取前缀
                    target_prefix = ''.join(re.findall(r'[A-Za-z]', target_paragraph))[:len(line_content)]
                    
                    if line_content == target_prefix:
                        return block["bbox"]
    return None

def process_files_in_directory(base_path):
    # 遍历基础路径下的所有文件
    input_pdf_basepath="/home/sunhaoyou/sly2025/fist_page"
    output_pdf_basepath="/home/sunhaoyou/sly2025/cut_pdf"
    sumi=0
    for root, dirs, files in os.walk(base_path):
        for file in files:
            # 检查文件名是否包含 "content_list" 且是 JSON 文件
            if "content_list" in file and file.endswith(".json"):
                content_list_file_path = os.path.join(root, file)
                #print(f"正在处理包含 'content_list' 的文件：{content_list_file_path}")
                # 获取包含人名且词语最少的段落
                min_paragraph = find_min_word_paragraph_with_person(content_list_file_path)
                if min_paragraph:
                    #print(f"找到目标段落：{min_paragraph}")
                    # 查找与该文件在同一文件夹内、文件名包含 "middle" 的 JSON 文件
                    middle_file_path = None
                    for other_file in files:
                        if "middle" in other_file and other_file.endswith(".json"):
                            middle_file_path = os.path.join(root, other_file)
                            break
                    if middle_file_path:
                        #print(f"正在处理包含 'middle' 的文件：{middle_file_path}")
                        # 获取该段落的 bbox
                        bbox = find_paragraph_bbox(middle_file_path, min_paragraph)
                        
                        if bbox:
                            #print(f"文件：{middle_file_path}")
                            #print(f"目标段落的 bbox：{bbox}")
                            #print("-" * 50)
                        
                            pdf_file_name = file.replace("_content_list.json", ".pdf")
                            input_pdf_path=os.path.join(input_pdf_basepath, pdf_file_name)
                            output_pdf_path=os.path.join(output_pdf_basepath, pdf_file_name)
                        
                            crop_pdf_page(input_pdf_path, output_pdf_path, bbox)
                    else:
                        print(f"未找到与 {content_list_file_path} 同一文件夹内包含 'middle' 的 JSON 文件")
                        sumi=sumi+1
                else:
                    print(f"未在文件 {content_list_file_path} 中找到符合条件的段落")
                    sumi=sumi+1
    print(f"总计失败 {sumi} ")
def crop_pdf_page(input_pdf_path, output_pdf_path, bbox):

    # 打开输入的 PDF 文件
    pdf_document = fitz.open(input_pdf_path)

    # 创建一个新的 PDF 文件
    new_pdf = fitz.open()

    # 遍历 PDF 的每一页
    
    page = pdf_document.load_page(0)  # 加载当前页面

        # 获取裁剪区域的矩形
    rect = fitz.Rect(bbox[0], bbox[1], bbox[2], bbox[3])

        # 裁剪页面
    cropped_page = page.set_cropbox(rect)

        # 将裁剪后的页面添加到新 PDF
    new_pdf.insert_pdf(pdf_document, from_page=0, to_page=0)

    # 保存裁剪后的 PDF 到输出路径
    new_pdf.save(output_pdf_path)
    new_pdf.close()
    pdf_document.close()

    #print(f"裁剪后的 PDF 已保存到 {output_pdf_path}")

#base_path = "/home/sunhaoyou/sly2025/output_fis"  # 替换为你的基础文件夹路径
#process_files_in_directory(base_path)
x=find_min_word_paragraph_with_person("/home/sunhaoyou/sly2025/sec_output/13068_2014_Article_138/auto/13068_2014_Article_138_content_list.json")
#y=find_paragraph_bbox("/home/sunhaoyou/sly2025/output_fis/5_2013_Article_254/auto/5_2013_Article_254_middle.json",x)
print(x)