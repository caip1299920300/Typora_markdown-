# encoding:utf-8 
import shutil,os,requests,time

def get_time():
    # 获取当前时间
    str = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
    return str

def download_pic(url,path):
    '''
        下载图片函数
        url：图片的地址
        path: 图片保存在本地的目录
    '''
    try:
        headers = {'cookie': 'SINAGLOBAL=7755731542583.8125.1645778146660; _s_tentry=-; Apache=7132237945462.021.1645778388802; ULV=1645778388819:2:2:2:7132237945462.021.1645778388802:1645778146674; SUB=_2A25PHOZ1DeRhGeRM7FIS8i3LyD2IHXVsaFC9rDV8PUNbmtB-LVf5kW9NU8XyUlX9iNdrfCSpw9HLvxBA3GXLIcC0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5GCsvIfgqNxm9sIRXsBPfv5JpX5KzhUgL.FozES050eoeNe022dJLoIEqLxK-LBo5L12qLxK-LBo5L12qLxKnLB.BLB.zLxK-LBo5L1KykeBtt; ALF=1677314468; SSOLoginState=1645778469', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
        pic_name = f'image-{get_time()}.jpg'
        with open(path+pic_name,'wb') as f:
            img = requests.get(url,headers = headers).content
            f.write(img)
        return pic_name
    except:
        raise Exception(url+"-网络地址下载失败")

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
                # 图片移动或下载图片
                if "http://" in path_ or 'https://' in path_:
                    pic_name = download_pic(path_,md_dir+'/images/')
                    path_n   = './images/'+ pic_name
                else:
                    # 图片需要移动的地址
                    path_n = './images/'+md_text.split('](')[1].split(')')[0].split('\\')[-1]
                    # 移动图片
                    try:
                        shutil.move(path_,md_dir+path_n[1:])
                    except:
                        raise Exception("移动地址不存在")
                print("修改成功：",path_n)
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



        