# This file is part of ziti-streaming-webapp
# Copyright (c) 2024 Jacob Dybvald Ludvigsen (contributions@ingeniorskap.no)
# SPDX-License-Identifier: AGPL-3.0-or-later

import multiprocessing as mp
import time

from ziti_streaming_webapp.webapp import run_webapp
from ziti_streaming_webapp.frame_producer import produce


def main():
    manager = mp.Manager()
    # q_img = manager.Queue(maxsize=5)
    q_img = mp.Queue()
    pipe_img_recv, pipe_img_send = mp.Pipe(duplex=False)

    video_process = mp.Process(
        target=produce,
        args=(q_img,
              pipe_img_send
              ),
        daemon=True
        )
    video_process.start()

    time.sleep(2)

    webapp_process = mp.Process(
        target=run_webapp,
        args=(q_img,
              pipe_img_recv
              ),
        daemon=True
        )
    webapp_process.start()

    while True:
        time.sleep(1)
    webapp_process.join()
    video_process.join()


if __name__ == "__main__":
    main()