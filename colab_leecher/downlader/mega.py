import asyncio
import logging
from datetime import datetime
from colab_leecher.utility.helper import status_bar, getTime, speedETA
from colab_leecher.utility.variables import BotTimes, Messages, Paths

async def megadl(link: str, num: int):
    BotTimes.task_start = datetime.now()
    cmd = ["megadl", link, "--path", Paths.down_path]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async for raw_line in process.stdout:
        try:
            line = raw_line.decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            await pro_for_mega(line)
        except Exception as e:
            logging.error(f"Error reading output: {e}")

    await process.wait()

import re

def to_bytes(value, unit):
    unit = unit.lower()
    if unit.startswith("pi"):
        return value * 1024**5
    elif unit.startswith("ti"):
        return value * 1024**4
    elif unit.startswith("gi"):
        return value * 1024**3
    elif unit.startswith("mi"):
        return value * 1024**2
    elif unit.startswith("ki"):
        return value * 1024
    else:
        return value

async def pro_for_mega(line: str):
    file_name = "N/A"
    percentage = 0.0
    downloaded_size = "N/A"
    total_size = "N/A"
    speed = "N/A"
    eta = "Unknown"

    try:
        pattern = re.compile(
            r"^(.*?):\s+([\d.]+)%\s+-\s+([\d.]+)\s+(\w+)\s+\([\d,]+\s+bytes\)\s+of\s+([\d.]+)\s+(\w+)\s+\(([\d.]+)\s+(\w+/s)\)$"
        )
        match = pattern.match(line)
        if match:
            file_name = match.group(1)
            percentage = float(match.group(2))

            # ukuran terunduh & total (untuk tampilan)
            downloaded_bytes = to_bytes(float(match.group(3)), match.group(4))
            total_bytes = to_bytes(float(match.group(5)), match.group(6))
            downloaded_size = sizeUnit(downloaded_bytes)
            total_size = sizeUnit(total_bytes)

            # kecepatan
            speed_value = float(match.group(7))
            speed_unit = match.group(8).replace("/s", "")
            speed_bps = to_bytes(speed_value, speed_unit)
            speed = f"{speed_value} {speed_unit}/s"

            # hitung ETA
            if speed_bps > 0:
                eta_seconds = int((total_bytes - downloaded_bytes) / speed_bps)
                eta = getTime(eta_seconds)

    except Exception as e:
        logging.error(f"Error parsing megadl line: {e}")

    Messages.download_name = file_name
    Messages.status_head = (
        f"<b>📥 DOWNLOADING FROM MEGA » </b>\n\n"
        f"<b>🏷️ Name » </b><code>{file_name}</code>\n"
    )

    await status_bar(
        Messages.status_head,
        speed,
        percentage,
        eta,
        downloaded_size,
        total_size,
        "MEGA",
    )

