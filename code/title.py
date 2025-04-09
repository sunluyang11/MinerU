import os
import json

def extract_first_text_level(json_data):
    """
    遍历JSON数据，返回第一个包含text_level属性的text内容。
    """
    for item in json_data:
        if 'text_level' in item and 'text' in item:
            return item['text']
    return None

def process_folder(folder_path):
    """
    遍历指定文件夹（包括子文件夹），处理所有包含'_content_list'的JSON文件，
    并将结果写入到txt文件中。
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('_content_list.json'):
                json_path = os.path.join(root, file)
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 提取第一个包含text_level的text内容
                first_text = extract_first_text_level(json_data)
                
                if first_text:
                    # 构建输出文件名
                    output_file_name = file.replace('_content_list.json', '.txt')
                    output_path = os.path.join(r"/home/sunhaoyou/sly2025/title", output_file_name)
                    
                    # 写入结果
                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(first_text)
                    print(f"Processed {json_path} and wrote result to {output_path}")

# 示例用法
folder_path = '/home/sunhaoyou/sly2025/output_fis'  # 替换为你的文件夹路径
process_folder(folder_path)