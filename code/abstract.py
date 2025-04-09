import os
import json

def extract_abstract_text(json_data):
    """
    遍历JSON数据，根据条件返回特定的text内容。
    - 如果某个包含text_level属性的text内容为'abstract'（忽略空格和大小写），则返回其下一个块中的text。
    - 如果某个不包含text_level属性的块的text以'abstract'开头，则返回其text内容。
    """
    abstract_found = False
    for i, item in enumerate(json_data):
        text = item.get('text', '').strip().lower()
        if 'text_level' in item and text == 'abstract':
            abstract_found = True
            # 返回下一个块中的text内容
            if i + 1 < len(json_data):
                return json_data[i + 1].get('text', '')
            break
        elif 'text_level' not in item and text.startswith('abstract'):
            return item.get('text', '')
    return None

def process_folder(input_folder, output_folder):
    """
    遍历指定文件夹（包括子文件夹），处理所有包含'_content_list'的JSON文件，
    并将结果写入到指定文件夹下的txt文件中。
    """
    total_files = 0
    not_found_count = 0

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('_content_list.json'):
                total_files += 1
                json_path = os.path.join(root, file)
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # 提取满足条件的text内容
                result_text = extract_abstract_text(json_data)
                
                if result_text:
                    # 构建输出文件名
                    output_file_name = file.replace('_content_list.json', '.txt')
                    output_path = os.path.join(output_folder, output_file_name)
                    
                    # 写入结果
                    with open(output_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(result_text)
                else:
                    not_found_count += 1

    # 统计未找到的比例
    not_found_ratio = (not_found_count / total_files) * 100 if total_files > 0 else 0
    print(f"Total files processed: {total_files}")
    print(f"Files without matching content: {not_found_count}")
    print(f"Percentage of files without matching content: {not_found_ratio:.2f}%")

# 示例用法
input_folder = '/home/sunhaoyou/sly2025/output_fis'  # 替换为你的输入文件夹路径
output_folder = '/home/sunhaoyou/sly2025/abstract'  # 替换为你的输出文件夹路径
process_folder(input_folder, output_folder)