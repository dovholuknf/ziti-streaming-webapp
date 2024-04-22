# This file is part of ziti-streaming-webapp
# Copyright (c) 2024 Jacob Dybvald Ludvigsen (contributions@ingeniorskap.no)
# SPDX-License-Identifier: AGPL-3.0-or-later

import cv2 as cv
import base64
import queue
from queue import Full, Empty
import time
from multiprocessing import Queue, Pipe


def produce(q_img: Queue):
    stream = cv.VideoCapture(0)
    print(f"q_img in frame_producer: {q_img}")
    print(f"repr of q_img in frame_producer: {repr(q_img)}\n")

    while True:
        (ret, frame) = stream.read()

        # break if video is done
        if not ret:
            break

        _, image = cv.imencode(".webp", frame, params=[cv.IMWRITE_WEBP_QUALITY, 5])

        # encode jpeg to base64 string in utf-8 format
        base64_image = base64.b64encode(image).decode("utf-8")

        try:
            q_img.put(base64_image, timeout=1)
        except Full:
            print("q_img full")
        except Exception as e:
            print(f"frameproducer queue: {e}")

        time.sleep(1)

