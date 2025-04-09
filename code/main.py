import subprocess
import io
import json
import os
import re
import fitz
import time     
def auto_seg(path):
    pdf_path=path
    out_path="/home/sunhaoyou/sly2025/output_fis"

    try:
            start_time = time.time()
        # 执行命令并捕获输出
            result = subprocess.run(['magic-pdf', '-p', pdf_path,'-o',out_path,'-m','auto'])
        
        # 检查命令是否成功执行
            if result.returncode == 0:
            # 获取命令的标准输出（PDF的标题）
                end_time=time.time()
                print("用时：")
                print(end_time-start_time)
                return result.stdout.strip()
                
            else:
            # 如果命令执行失败，返回错误信息
                print("fail")
                return f"Error: {result.stderr.strip()}"
    except Exception as e:
            return f"Exception occurred: {str(e)}"
def deal(input_file_path):
     #input_file_path="D:\work\output\\29121863\\auto\\29121863_content_list.json"
     output_folder_path ="D:\work\output_fnl"
     output_file_path = os.path.join(output_folder_path, os.path.basename(input_file_path))
     with open(input_file_path, 'r', encoding='utf-8') as file:
         data = json.load(file)

# 修改第一个块的text_level为0
     

# 删除text为空的项
     data = [item for item in data if item.get('text', '').strip() != '' or item.get('type') == 'table']
     titles = []
     for item in data:
        if 'text_level' in item:
            
            item['type'] = 'title'
            titles.append(item.get('text', ''))
     first_title_index = None
     for index, item in enumerate(data):
         if item.get('type') == 'title':
             first_title_index = index
             break

     if first_title_index is not None:
         data = data[first_title_index:]
     if data and 'text_level' in data[0]:
         data[0]['text_level'] = 0

# 将结果写入新的文件
     with open(output_file_path, 'w', encoding='utf-8') as file:
         json.dump(data, file, ensure_ascii=False, indent=4)
     return titles
# def get_title_font_sizes(pdf_path, titles):
#     title_font_sizes = {}
#     # 打开PDF文件
#     doc = fitz.open(pdf_path)
    
#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)
#         blocks = page.get_text("blocks")  # 获取页面中的文本块
        
#         for block in blocks:
#             # 每个block是一个元组：(x0, y0, x1, y1, text, block_no, line_no, word_no)
#             text = block[4]
#             if text.strip() in titles:
#                 # 获取文本的字体大小
#                 font_size = block[5]
#                 title_font_sizes[text.strip()] = font_size
    
#     doc.close()
#     return title_font_sizes     
def txt_make():
    json_file_path = 'D:\work\output_fnl\\29121863_content_list.json'
    output_folder_path = 'D:\work\\txt'
    output_txt_path = os.path.join(output_folder_path, os.path.splitext(os.path.basename(json_file_path))[0] + '.txt')
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    # 遍历JSON数据
        for item in data:
            if item['type'] in ['title', 'text']:
            # 如果是标题，行前加#
                if item['type'] == 'title':
                    txt_file.write(f"#{item['text']}\n")
                else:
                    txt_file.write(item['text'] + '\n')

def first_txt(json_file_path):
    #json_file_path = 'D:\work\output_fnl\\29121863_content_list.json'
    output_folder_path = 'D:\work\\first_page'
    output_txt_path = os.path.join(output_folder_path, os.path.splitext(os.path.basename(json_file_path))[0] + '.txt')
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
    # 遍历JSON数据
        for item in data:
            if item['type'] in ['title', 'text'] and item['page_idx']==0:
            # 如果是标题，行前加#
                if item['type'] == 'title':
                    txt_file.write(f"#{item['text']}\n")
                else:
                    txt_file.write(item['text'] + '\n')


def main():
    # base_path = r'D:\work\output_fnl'  # 修正路径中的双反斜杠为单反斜杠

    # # 遍历 base_path 文件夹下的所有文件
    # for filename in os.listdir(base_path):
    #     # 构造完整的文件路径
    #     file_path = os.path.join(base_path, filename)
        
    #     # 检查是否为文件（排除文件夹）
    #     if os.path.isfile(file_path):
    #         # 调用 first_txt 函数处理每个文件
    #         first_txt(file_path)


    #处理
    # base_path = r"D:\work\output"
    # for folder_name in os.listdir(base_path):  # 遍历 base_path 下的所有文件夹
    #     folder_path = os.path.join(base_path, folder_name)
    #     if os.path.isdir(folder_path):  # 确保是文件夹
    #         target_file = os.path.join(folder_path, "auto", f"{folder_name}_content_list.json")
    #         if os.path.exists(target_file):  # 检查目标文件是否存在
    #             deal(target_file)  # 调用 deal 函数处理文件
    #         else:
    #             print(f"文件 {target_file} 不存在，跳过。")


    #划分
    base_path = r"/home/sunhaoyou/sly2025/fist_page"
    count = 0
    max_count = 1000
    for root, dirs, files in os.walk(base_path):
        for filename in files:
        # 检查文件扩展名是否为 .pdf，且文件名是否包含 "Article"
            if filename.lower().endswith(".pdf") and "Article" in filename:
                file_path = os.path.join(root, filename)  # 构造完整的文件路径
                try:
                    auto_seg(file_path)  # 调用 auto_seg 函数处理该文件
                    count += 1  # 每处理一个文件，计数器加1
                    if count >= max_count:  # 如果达到最大执行次数
                        print(f"Reached the maximum number of executions ({max_count}). Exiting.")
                        break  # 退出当前文件夹的遍历
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    #print(deal())
    #deal()
    #txt_make()
     #res=get_title_font_sizes("D:\\work\\paper\\29121863.pdf",deal())
     #print(res)

if __name__ == "__main__":
    main()