import os
import re
import time
import asyncio
from pathlib import Path
from typing import Optional, Union

from telethon import TelegramClient, events, Button
from telethon.events import CallbackQuery
from telethon.tl.custom.message import Message

# =========================
# Required env vars
# =========================
API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]

WATCH_CHAT = os.environ.get("WATCH_CHAT", "").strip()
if not WATCH_CHAT:
    raise SystemExit("WATCH_CHAT env var is required")

DOWNLOAD_DIR_ENV = os.environ.get("DOWNLOAD_DIR", "").strip()
if not DOWNLOAD_DIR_ENV:
    raise SystemExit("DOWNLOAD_DIR env var is required")

SESSION_PATH = os.environ.get("TG_SESSION_PATH", "/session/telethon.session")

# Optional tuning
PROGRESS_UPDATE_EVERY = float(os.environ.get("PROGRESS_UPDATE_EVERY", "2.0"))
DELETE_PARTIAL_ON_CANCEL = os.environ.get("DELETE_PARTIAL_ON_CANCEL", "1") not in ("0", "false", "False")

DOWNLOAD_DIR = Path(DOWNLOAD_DIR_ENV).expanduser()

# =========================
# Helpers
# =========================
def human_bytes(n: Optional[float]) -> str:
    if n is None:
        return "?"
    n = float(n)
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024
        i += 1
    return f"{n:.1f} {units[i]}" if i > 0 else f"{int(n)} {units[i]}"

def human_time(seconds: Optional[float]) -> str:
    if seconds is None or seconds == float("inf"):
        return "?"
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"

def parse_watch_chat(value: str) -> Union[int, str]:
    try:
        return int(value)
    except ValueError:
        return value

WATCH_CHAT_PARSED = parse_watch_chat(WATCH_CHAT)

# Ensure dirs exist
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
Path(SESSION_PATH).parent.mkdir(parents=True, exist_ok=True)

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

# msg_id -> asyncio.Task
ACTIVE_DOWNLOADS: dict[int, asyncio.Task] = {}

def cancel_button(msg_id: int):
    return [Button.inline("⛔ Cancel", data=f"cancel:{msg_id}".encode())]

def short_error(e: Exception) -> str:
    s = f"{type(e).__name__}: {e}"
    s = re.sub(r"\s+", " ", s)
    return s[:300]

@client.on(events.NewMessage(chats=WATCH_CHAT_PARSED))
async def on_new_message(event: events.NewMessage.Event):
    msg: Message = event.message
    if not msg or not msg.media:
        return

    status = await event.reply("⬇️ Starting download…", buttons=cancel_button(msg.id))

    async def run_download():
        start_t = time.monotonic()
        last_edit = 0.0
        last_bytes = 0
        last_bytes_t = start_t
        saved_path: Optional[str] = None

        async def progress_cb(downloaded: int, total: int):
            nonlocal last_edit, last_bytes, last_bytes_t

            now = time.monotonic()
            if now - last_edit < PROGRESS_UPDATE_EVERY and downloaded < total:
                return

            dt = max(now - last_bytes_t, 1e-6)
            speed = max(downloaded - last_bytes, 0) / dt
            elapsed = now - start_t
            pct = (downloaded / total * 100) if total else 0
            eta = (total - downloaded) / speed if speed > 0 and total else None

            text = (
                f"⬇️ Downloading… {pct:.1f}%\n"
                f"{human_bytes(downloaded)} / {human_bytes(total)}\n"
                f"Speed: {human_bytes(speed)}/s | ETA: {human_time(eta)}\n"
                f"Elapsed: {human_time(elapsed)}"
            )

            try:
                await status.edit(text, buttons=cancel_button(msg.id))
            except Exception:
                pass

            last_edit = now
            last_bytes = downloaded
            last_bytes_t = now

        try:
            saved_path = await client.download_media(
                msg,
                file=str(DOWNLOAD_DIR),
                progress_callback=progress_cb,
            )

            await status.edit(
                f"✅ Download complete\nSaved: {saved_path}",
                buttons=None
            )

        except asyncio.CancelledError:
            if DELETE_PARTIAL_ON_CANCEL and saved_path:
                try:
                    Path(saved_path).unlink(missing_ok=True)
                except Exception:
                    pass
            await status.edit("⛔ Download cancelled.", buttons=None)
            raise

        except Exception as e:
            if DELETE_PARTIAL_ON_CANCEL and saved_path:
                try:
                    Path(saved_path).unlink(missing_ok=True)
                except Exception:
                    pass
            await status.edit(f"❌ Download failed\n{short_error(e)}", buttons=None)

        finally:
            ACTIVE_DOWNLOADS.pop(msg.id, None)

    task = asyncio.create_task(run_download())
    ACTIVE_DOWNLOADS[msg.id] = task

@client.on(CallbackQuery)
async def on_callback(event: CallbackQuery.Event):
    data = event.data.decode(errors="ignore")
    if not data.startswith("cancel:"):
        return

    msg_id = int(data.split(":", 1)[1])
    task = ACTIVE_DOWNLOADS.get(msg_id)

    if not task:
        await event.answer("No active download.", alert=True)
        return

    task.cancel()
    await event.answer("Cancelling…")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Logged in as {me.id} | Watching {WATCH_CHAT} | Saving to {DOWNLOAD_DIR}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
