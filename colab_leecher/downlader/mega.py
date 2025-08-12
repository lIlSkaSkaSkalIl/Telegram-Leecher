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

async def pro_for_mega(line: str):
    file_name = "N/A"
    percentage = 0
    downloaded_size = "N/A"
    total_size = "N/A"
    speed = "N/A"
    eta = "Unknown"

    try:
        if "%" in line and "[" in line and "]" in line:
            parts = line.split()
            file_name = parts[0]
            percentage = float(parts[1].strip("[]%"))
            downloaded_size = parts[2]
            total_size = parts[4]
            speed = parts[6]
            eta = parts[-1]

    except Exception:
        pass

    Messages.download_name = file_name
    Messages.status_head = f"<b>📥 DOWNLOADING FROM MEGA » </b>\n\n<b>🏷️ Name » </b><code>{file_name}</code>\n"

    await status_bar(
        Messages.status_head,
        speed,
        percentage,
        eta,
        downloaded_size,
        total_size,
        "MEGA",
    )
