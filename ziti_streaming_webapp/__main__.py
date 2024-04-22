# This file is part of ziti-streaming-webapp
# Copyright (c) 2024 Jacob Dybvald Ludvigsen (contributions@ingeniorskap.no)
# SPDX-License-Identifier: AGPL-3.0-or-later

import multiprocessing as mp
import time
import tomllib

from ziti_streaming_webapp.webapp import run_webapp
from ziti_streaming_webapp.frame_producer import produce


def main():
    # Load configuration file
    try:
        with open("./config.toml", "rb") as f:
            config_file = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        print(f"ERR: Config file couldn't load due to error: {e}")

    # forkserver is more memory-efficient and resilient
    mp.set_start_method("forkserver", force=True)
    print(mp.get_start_method())
    manager = mp.Manager()
    q_img = manager.Queue()

    # Pass ziti config as proxy object, because queues break otherwise
    ziti_dict = manager.dict()
    ziti_dict[f"{(config_file['webapp']['address'], int(config_file['webapp']['port']))}"]={
                      'ztx': f"{config_file['ziti']['identity']}",
                      'service': f"{config_file['ziti']['service']}"
                      }

    print(f"q_img in main: {q_img}")
    print(f"repr of q_img in main: {repr(q_img)}")
    video_process = mp.Process(
        target=produce,
        args=(q_img,
              ),
        daemon=True
        )
    video_process.start()

    time.sleep(2)

    webapp_process = mp.Process(
        target=run_webapp,
        args=(q_img,
              ziti_dict
              ),
        daemon=False
        )
    webapp_process.start()

    while True:
        time.sleep(1)
    webapp_process.join()
    video_process.join()


if __name__ == "__main__":
    main()
