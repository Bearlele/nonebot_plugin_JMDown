import jmcomic
import hashlib
import PyPDF2
import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, Bot
from nonebot.internal.adapter import Event
from nonebot.params import CommandArg
import nonebot_plugin_localstore as store

# 获取插件缓存目录
cache_dir = store.get_plugin_cache_dir()
# 获取插件数据目录
data_dir = store.get_plugin_data_dir()
# 获取插件配置目录
config_dir = store.get_plugin_config_dir()

jm = on_command("jm", aliases={"JM"})

@jm.handle()
async def handle_function(event: Event, bot: Bot, args: Message = CommandArg()):
    location = args.extract_plain_text().strip()
    user_id = event.user_id
    if not location.isdigit():
        await jm.finish("请输入正确的本子 ID（数字）")

    await bot.send(event, "正在搜索", reply_message=True)
    result = download_and_convert_to_pdf(location)

    # 这里传入文件路径后上传并发送文件
    if result != "下载失败" and result != "下载错误":
        album_id = result.album_id
        filename = replace_special_characters(result.name)
        likes = result.likes
        views = result.views
        comment_count = result.comment_count

        # 处理列表类型的数据
        works = ','.join(result.works) if isinstance(result.works, list) else result.works
        actors = ','.join(result.actors) if isinstance(result.actors, list) else result.actors
        tags = ','.join(result.tags) if isinstance(result.tags, list) else result.tags
        authors = ','.join(result.authors) if isinstance(result.authors, list) else result.authors

        file_path = f'{cache_dir}/{filename}.pdf'

        # 加密 PDF
        encrypted_pdf_path = encrypt_pdf(file_path, location)

        print(f"{file_path} -> {encrypted_pdf_path}")

        info_list = [
            f"JM{album_id}",
            filename,
            f"点赞:: {likes}   浏览:: {views}   评论:: {comment_count}",
            f"所属作品:: {works}" if works else "",
            f"角色列表:: {actors}" if actors else "",
            f"标签:: {tags}" if tags else "",
            f"作者:: {authors}" if authors else ""
        ]

        final_str = "\n".join(filter(None, info_list))

        try:
            await bot.send(event, final_str)
            await bot.upload_group_file(group_id=event.group_id, file=encrypted_pdf_path, name=f"JM{location}-{filename}.pdf")
        except Exception as e:
            error_msg = str(e)
            
            # 判断是否是风控导致的失败
            if "rich media transfer failed" in error_msg:
                await jm.finish("上传文件时发生了错误，可能被风控")
            else:
                await jm.finish(f"上传文件时发生了错误: {error_msg}")

    else:
        await jm.finish(f"下载过程中发生了错误: {filename}")

def encrypt_pdf(input_pdf_path: str, password: str) -> str:
    # 计算原文件的 MD5
    hasher = hashlib.md5()
    with open(input_pdf_path, 'rb') as f:
        hasher.update(f.read())
    md5_hash = hasher.hexdigest()
    
    new_pdf_path = os.path.join(os.path.dirname(input_pdf_path), f"{md5_hash}.pdf")
    
    # 如果加密文件已存在，直接返回
    if os.path.exists(new_pdf_path):
        return new_pdf_path
    
    # 读取 PDF 并加密
    reader = PyPDF2.PdfReader(input_pdf_path)
    writer = PyPDF2.PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    writer.encrypt(password)
    
    # 保存加密后的 PDF
    with open(new_pdf_path, "wb") as f:
        writer.write(f)
    
    return new_pdf_path

def replace_special_characters(filename):
    """替换文件名中的特殊字符"""
    if not isinstance(filename, str):
        raise ValueError("传入的文件名无效")
    
    replacements = {
        "*": "_",
    }

    for old, new in replacements.items():
        filename = filename.replace(old, new)

    return filename

def download_and_convert_to_pdf(manga_id):
    """下载漫画并返回文件名"""
    config_file = str(config_dir) + "/option.yml"
    print(config_file)
    option = jmcomic.create_option_by_file(config_file)

    print(f"开始下载漫画 ID：{manga_id}...")

    try:
        album, downloader = jmcomic.download_album(manga_id, option)

        if album:
            return album
        else:
            return "下载失败"
    except Exception as e:
        return f"下载错误: {str(e)}"
