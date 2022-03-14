import argparse
import os
from pytube import Playlist
from pytube import YouTube
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


class Parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def get_arguements(self):
        self.parser.add_argument("--pfile")
        self.parser.add_argument("--vfile")
        self.parser.add_argument("--v")
        self.parser.add_argument("-q")
        return self.parser.parse_args()


class Filter:

    def select_arguments(self, parse_args: dict):
        args = parse_args.__dict__
        for key, value in args.items():
            if value is not None:
                return key, value


class File:

    def get_path(self, name_file):
        return f"{os.path.dirname((os.path.abspath(__file__)))}/{name_file}"

    def open_file(self, path):
        with open(path, "r") as file:
            lines = file.read().splitlines()
        return lines


class VideoAction:

    def __init__(self, streams) -> None:
        self.streams = streams
        self.counter = 0

    def download_video(self):
        self.counter += 1
        for video in self.streams:
            for pvideos in video:
                pvideos.download(output_path=str(
                    f"download_videos_{self.counter}"))
                print(f"{pvideos.default_filename} is downloaded")


class VideoHelper:

    def __init__(self, url):
        self.video = YouTube(url)
    def get_actual_streams(self, q=None):
        vlist = []
        if q:
            vlist.append(self.video.streams.get_by_resolution(q))
        else:
            vlist.append(self.video.streams.get_highest_resolution())
        return vlist


class PlaylistHepler:

    def __init__(self, url):
        self.playlist = Playlist(url)

    def get_actual_streams(self, q=None):
        streams = []
        for video in self.playlist.videos:
            if q:
                streams.append(video.streams.get_by_resolution(q))
            else:
                streams.append(video.streams.get_highest_resolution())
        return streams


def main():
    streams = []
    parser_args = Parser().get_arguements()
    user_key, user_value = Filter().select_arguments(parser_args)
    if "file" in user_key:
        file = File()
        get_file = file.open_file(file.get_path(user_value))
        for url in get_file:
            if "playlist" in url:
                streams.append(PlaylistHepler(url).get_actual_streams())
            else:
                streams.append(VideoHelper(url).get_actual_streams())
    else:
        streams.append(VideoHelper(user_value).get_actual_streams())
    video_actions = VideoAction(streams)
    video_actions.download_video()


if __name__ == '__main__':
    main()