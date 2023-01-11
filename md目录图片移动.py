# encoding:utf-8 
import shutil,os

def md_picture_update(md_path):
    # md的目录地址
    md_dir = ""
    # 判断是否为md文件并提取md目录地址
    if '.md' in md_path.split('\\')[-1] and '/' not in md_path.split('\\')[-1]:
        md_dir = md_path[:-len(md_path.split('\\')[-1]) - 1]
    elif '.md' in md_path.split('/')[-1] and '\\' not in md_path.split('/')[-1]:
        md_dir = md_path[:-len(md_path.split('/')[-1]) - 1]
    else:
        print("输入的地址有误！")
        return
    if os.path.exists(md_path) and '.md' in md_path:
        # 读取md文件
        with open(md_path, "r", encoding='utf-8') as file:
            md_texts = file.readlines()
        # 判断是否存在images文件夹
        if os.path.exists(md_dir + '/images/') == False:
            os.mkdir(md_dir + '/images/')
        md_strs = ""  # 存储修改md的内容
        # 遍历md的每一行
        for md_text in md_texts:
            if '![' in md_text and ('](' in md_text and ')' in md_text):  # 匹配
                # 匹配到图片的地址
                path_ = md_text.split('](')[1].split(')')[0]
                # 如果图片已经在里面，则什么都不做
                if './images/' in path_ or '.\\images/' in path_ or './images\\' in path_ or '.\\images\\' in path_:
                    md_strs = md_strs + md_text
                    continue
                # 图片需要移动的地址
                path_n = './images/' + md_text.split('](')[1].split(')')[0].split('\\')[-1]
                # md地址内容替换
                md_text = md_text.replace(path_, path_n)
                # 图片移动
                shutil.move(path_, md_dir + path_n[1:])
                print("修改成功：", path_n)
            # 修改后的内容拼接
            md_strs = md_strs + md_text
        # 写入md文件
        with open(md_path, "w", encoding='utf-8') as file:
            file.write(md_strs)
        print("修改成功！")
    else:
        print("你输入的文件路径不对！")


while True:
    mds_path = input("输入需要提取图片的md大目录地址:")
    for md_path in os.listdir(mds_path):
        if '.md' in md_path:
            print(mds_path+'/'+md_path)
            md_picture_update(mds_path+'/'+md_path)



        