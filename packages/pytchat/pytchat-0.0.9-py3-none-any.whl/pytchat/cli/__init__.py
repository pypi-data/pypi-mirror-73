import argparse
from pathlib import Path
from .arguments import Arguments
from .. exceptions import InvalidVideoIdException, NoContents
from .. processors.html_archiver import HTMLArchiver
from .. tool.extract.extractor import Extractor
from .. tool.videoinfo import VideoInfo
from .. import __version__

'''
Most of CLI modules refer to
Petter Kraabøl's Twitch-Chat-Downloader
https://github.com/PetterKraabol/Twitch-Chat-Downloader
(MIT License)

'''


def main():
    # Arguments
    parser = argparse.ArgumentParser(description=f'pytchat v{__version__}')
    parser.add_argument('-v', f'--{Arguments.Name.VIDEO}', type=str,
                        help='Video IDs separated by commas without space.\n'
                        'If ID starts with a hyphen (-), enclose the ID in square brackets.')
    parser.add_argument('-o', f'--{Arguments.Name.OUTPUT}', type=str,
                        help='Output directory (end with "/"). default="./"', default='./')
    parser.add_argument(f'--{Arguments.Name.VERSION}', action='store_true',
                        help='Settings version')
    Arguments(parser.parse_args().__dict__)
    if Arguments().print_version:
        print(f'pytchat v{__version__}')
        return

    # Extractor
    if Arguments().video_ids:
        for video_id in Arguments().video_ids:
            if '[' in video_id:
                video_id = video_id.replace('[', '').replace(']', '')
            try:
                info = VideoInfo(video_id)
                print(f"Extracting...\n"
                      f" video_id: {video_id}\n"
                      f" channel:  {info.get_channel_name()}\n"
                      f" title:    {info.get_title()}")
                path = Path(Arguments().output + video_id + '.html')
                print(f"output path: {path.resolve()}")
                Extractor(video_id,
                          processor=HTMLArchiver(
                              Arguments().output + video_id + '.html'),
                          callback=_disp_progress
                          ).extract()
                print("\nExtraction end.\n")
            except (InvalidVideoIdException, NoContents) as e:
                print(e)
        return
    parser.print_help()


def _disp_progress(a, b):
    print('.', end="", flush=True)
