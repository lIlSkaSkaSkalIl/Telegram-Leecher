import asyncio
import logging
from datetime import datetime
from colab_leecher.utility.helper import status_bar, getTime
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

async def pro_for_mega(line: str):
    file_name = "N/A"
    percentage = 0.0
    downloaded_size = "N/A"
    total_size = "N/A"
    speed = "N/A"
    eta = "Unknown"

    try:
        # Regex data megadl
        pattern = re.compile(
            r"^(.*?):\s+([\d.]+)%\s+-\s+([\d.]+)\s+(\w+)\s+\(([\d,]+)\s+bytes\)\s+of\s+([\d.]+)\s+(\w+)\s+\(([\d.]+)\s+(\w+/s)\)$"
        )
        match = pattern.match(line)

        if match:
            file_name = match.group(1)
            percentage = float(match.group(2))

            downloaded_value, downloaded_unit = float(match.group(3)), match.group(4)
            downloaded_size = f"{downloaded_value} {downloaded_unit}"
            downloaded_bytes = int(match.group(5).replace(",", ""))

            total_value, total_unit = float(match.group(6)), match.group(7)
            total_size = f"{total_value} {total_unit}"
            total_bytes = convert_to_bytes(total_value, total_unit)

            # Hitung speed & ETA pakai speedETA
            speed, eta_seconds, percentage = speedETA(BotTimes.task_start, downloaded_bytes, total_bytes)
            eta = getTime(int(eta_seconds)) if eta_seconds > 0 else "Unknown"

    except Exception as e:
        logging.error(f"Error parsing line: {e}")

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


def convert_to_bytes(value, unit):
    """Konversi ukuran file ke bytes berdasarkan unit."""
    unit = unit.lower()
    if unit.startswith("kb"):
        return int(value * 1024)
    elif unit.startswith("mb"):
        return int(value * 1024**2)
    elif unit.startswith("gb"):
        return int(value * 1024**3)
    elif unit.startswith("tb"):
        return int(value * 1024**4)
    return int(value)

