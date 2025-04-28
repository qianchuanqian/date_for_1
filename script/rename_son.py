#以其中一个文件夹的images和labels的最后序号为其他文件夹的最开始的序号
import os


def rename_files_in_folder(start_number, folder_path):
    """按照原文件夹名字排序，并根据提供的起始数字重命名文件"""

    # 获取文件夹内所有文件的名称
    files = sorted(os.listdir(folder_path))

    # 避免重复文件夹路径和文件名扩展
    if not files:
        print("文件夹为空，请检查路径！")
        return

    # 设置起始数字
    number = start_number

    for file in files:
        file_path = os.path.join(folder_path, file)

        # 确保只处理文件，不处理子目录
        if os.path.isfile(file_path):
            # 获取文件的扩展名
            file_extension = os.path.splitext(file)[1]

            # 生成新的文件名，确保是6位数
            new_name = f"{str(number).zfill(7)}{file_extension}"

            # 构建新的文件路径
            new_file_path = os.path.join(folder_path, new_name)

            # 重命名文件
            os.rename(file_path, new_file_path)

            # 打印当前文件处理情况
            print(f"文件 {file} 重命名为 {new_name}")

            # 递增数字
            number += 1


if __name__ == "__main__":
    # 输入起始数字和文件夹路径
    start_number = 3791
    folder_path = "D:\\Dataset\\self-blind\\final_datasets\\bdd\\val\\labels"

    # 调用函数重命名文件
    rename_files_in_folder(start_number, folder_path)
