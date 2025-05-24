import sys
import os

from PyQt6.QtWidgets import QApplication
from packaging.version import Version
import requests
from loguru import logger
import zipfile
from qfluentwidgets import ProgressBar

import conf


if sys.platform == 'win32':
    import win32api

REPO = 'xuanxuan1231/RandPicker'
UPDATER_REPO = 'xuanxuan1231/RandPicker-Updater'
APP_VERSION = Version('v1.5.1')

if sys.platform == 'win32':
    # 获取更新器的版本
    try:
        info = win32api.GetFileVersionInfo('./Updater.exe', '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        UPDATER_VERSION = Version(f'{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}')
    except Exception as e:
        logger.error(f'获取更新器版本时发生错误: {e}')
        UPDATER_VERSION = Version('0.0.0')


def get_channel_name(idx):
    # 0:M, 1:L, 2:T, 3:D, 4:E
    return ['main', 'lts', 'test', 'dev', 'exp'][idx] if 0 <= idx <= 4 else 'lts'


def check_update_app(origin: int = 0) -> dict:
    """
    检查更新并返回最新版本信息。
    :param origin: 更新源。
    :return: 包含最新版本号和是否是最新版本的字典
    """

    logger.info('开始检查更新。')
    result = {}
    # 获取通道
    try:
        import conf
        channel_idx = int(conf.ini.get('Update', 'channel', fallback='1'))
    except Exception:
        channel_idx = 1
    channel = get_channel_name(channel_idx)

    if origin == 1:
        # OSS源可根据实际情况扩展
        MANIFEST_URL = f'https://oss.may.pp.ua/RandPicker/{channel}/latest.json'
    else:
        # GitHub不同通道对应不同release/tag
        if channel == 'main':
            MANIFEST_URL = f'https://api.github.com/repos/{REPO}/releases/latest'
        else:
            # 其它通道用tag名区分
            MANIFEST_URL = f'https://api.github.com/repos/{REPO}/releases/tags/{channel}'

    logger.info(f'使用更新通道: {channel}，请求URL: {MANIFEST_URL}')

    try:
        response = requests.get(MANIFEST_URL, timeout=5)
        response.raise_for_status()
        latest_version = Version(response.json().get('tag_name'))

    except requests.RequestException as e:
        logger.error(f'检查更新时发生错误。{e}')
        return {'version': str(APP_VERSION),
                'url': '',
                'is_latest': True}

    if latest_version > APP_VERSION:
        is_latest = False
        logger.info(f'发现新版本 {latest_version}。')
    else:
        is_latest = True
        logger.info('当前版本是最新的。')

    result = {
        'version': str(latest_version),
        'is_latest': is_latest
        }

    return result


    
def check_update_updater(origin: int = 0) -> dict:
    """
    检查更新器的更新并返回最新版本信息。

    :return: 更新器的版本号
    """
    logger.info('开始检查更新器更新。')
    result = {}

    if origin == 1:
        MANIFEST_URL = 'https://oss.may.pp.ua/Updater/latest.json'
    else:
        MANIFEST_URL = f'https://api.github.com/repos/{UPDATER_REPO}/releases/latest'

    try:
        response = requests.get(MANIFEST_URL, timeout=5)
        response.raise_for_status()
        latest_version = Version(response.json().get('tag_name'))

    except requests.RequestException as e:
        logger.error(f'检查更新时发生错误。{e}')
        return {'version': str(UPDATER_VERSION),
                'is_latest': True}

    if latest_version > UPDATER_VERSION:
        is_latest = False
        logger.info(f'发现新版本 {latest_version}。')
    else:
        is_latest = True
        logger.info('当前版本是最新的。')

    if origin == 'oss':
        result = {
            'version': str(latest_version),
            'url': f'https://oss.may.pp.ua/Updater/{latest_version}/Updater.zip',
            'is_latest': is_latest
        }
    else:
        try:
            result = {
                'version': str(latest_version),
                'url': response.json().get('assets')[0].get('browser_download_url'),
                'is_latest': is_latest
            }
        except IndexError:
            logger.error('无法获取更新器的下载链接。')
            result = {
                'version': str(latest_version),
                'url': None,
                'is_latest': is_latest
            }

    return result


def download_asset_with_progress(url, save_path, parent=None):
    """下载release asset并显示进度条"""
    import requests
    from qfluentwidgets import ProgressBar, InfoBar, InfoBarPosition
    try:
        resp = requests.get(url, stream=True, timeout=10)
        resp.raise_for_status()
        total = int(resp.headers.get('content-length', 0))
        chunk_size = 8192
        downloaded = 0
        with open(save_path, 'wb') as f:
            pb = None
            if parent:
                pb = ProgressBar(parent)
                pb.setRange(0, 100)
                pb.setValue(0)
                parent.layout().addWidget(pb)
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if pb and total:
                        pb.setValue(int(downloaded / total * 100))
            if pb:
                pb.setValue(100)
        return True
    except Exception as e:
        logger.error(f'下载更新包失败: {e}')
        if parent:
            InfoBar.error(title='下载失败', content=str(e), parent=parent, position=InfoBarPosition.TOP)
        return False


def update_app(parent=None):
    """自动下载并提示安装新版应用（参考ClassIsland逻辑）"""
    logger.info('开始自动更新应用程序。')
    origin = conf.ini.get('Update', 'app')
    update_info = check_update_app(origin)
    url = update_info.get('url')
    if not url:
        logger.error('未找到可用的更新包下载链接。')
        from qfluentwidgets import InfoBar, InfoBarPosition
        if parent:
            InfoBar.error(title='下载失败', content='未找到可用的更新包下载链接。', parent=parent, position=InfoBarPosition.TOP)
        return
    filename = url.split('/')[-1]
    save_path = os.path.join(os.path.expanduser('~'), 'Downloads', filename)
    ok = download_asset_with_progress(url, save_path, parent)
    from qfluentwidgets import InfoBar, InfoBarPosition
    if ok:
        logger.info(f'更新包已下载到: {save_path}')
        InfoBar.success(title='下载完成', content=f'更新包已下载到: {save_path}', parent=parent, position=InfoBarPosition.TOP)
        # macOS: 打开Finder定位文件，Windows: 可自动运行
        import platform, subprocess
        if platform.system() == 'Darwin':
            subprocess.run(['open', '-R', save_path])
        elif platform.system() == 'Windows':
            os.startfile(save_path)
    else:
        logger.error('更新包下载失败。')


def update_updater(parent=None):
    """
    更新更新器。
    """
    logger.info('开始更新更新器。')
    progressBar = ProgressBar()
    progressBar.setParent(parent)
    parent.viewLayout.addWidget(progressBar)
    progressBar.setRange(0, 100)
    progressBar.setValue(0)

    URL = check_update_updater()['url']
    if URL:
        logger.info(f'更新器下载链接: {URL}')
    else:
        logger.warning('未找到更新器下载链接。')
        return
    progressBar.setValue(20)
    
    updater = requests.get(URL, timeout=5)
    with open('Updater.exe', 'wb') as f:
        f.write(updater.content)
    progressBar.setValue(75)
    logger.info('更新器下载完成。')

    progressBar.setValue(100)
    global UPDATER_VERSION
    if sys.platform == 'win32':
    # 获取更新器的版本
        try:
            info = win32api.GetFileVersionInfo('./Updater.exe', '\\')
            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            UPDATER_VERSION = Version(f'{win32api.HIWORD(ms)}.{win32api.LOWORD(ms)}.{win32api.HIWORD(ls)}.{win32api.LOWORD(ls)}')
        except Exception as e:
            logger.error(f'获取更新器版本时发生错误: {e}')
            UPDATER_VERSION = Version('0.0.0')
    return

    
'''if __name__ == '__main__':
    print(check_for_update('github'))'''