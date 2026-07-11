# cv + imageo version

import sys, os

import numpy as np
import imageio
import cv2

import tempfile, shutil


from PySide6.QtCore import Qt, QTimer, QByteArray
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,QLineEdit, QColorDialog, QFileDialog, QCheckBox, QSplitter, QScrollArea, QSizePolicy
from PySide6.QtGui import QColor, QPalette,QFontMetrics,QPainter, QPixmap, QImage,QCursor,  QIcon


CURSOR_BASE64 ="""
iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAYAAADEtGw7AAAACXBIWXMAAAsTAAALEwEAmpwYAABGBmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxMzggNzkuMTU5ODI0LCAyMDE2LzA5LzE0LTAxOjA5OjAxICAgICAgICAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgICAgICAgICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICAgICAgICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICAgICAgICAgIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIgogICAgICAgICAgICB4bWxuczpwaG90b3Nob3A9Imh0dHA6Ly9ucy5hZG9iZS5jb20vcGhvdG9zaG9wLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgICAgICAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+QWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKFdpbmRvd3MpPC94bXA6Q3JlYXRvclRvb2w+CiAgICAgICAgIDx4bXA6Q3JlYXRlRGF0ZT4yMDI1LTA4LTIyVDAwOjE1OjEwKzAzOjAwPC94bXA6Q3JlYXRlRGF0ZT4KICAgICAgICAgPHhtcDpNZXRhZGF0YURhdGU+MjAyNS0wOC0yNFQwNzozMTo0NiswMzowMDwveG1wOk1ldGFkYXRhRGF0ZT4KICAgICAgICAgPHhtcDpNb2RpZnlEYXRlPjIwMjUtMDgtMjRUMDc6MzE6NDYrMDM6MDA8L3htcDpNb2RpZnlEYXRlPgogICAgICAgICA8ZGM6Zm9ybWF0PmltYWdlL3BuZzwvZGM6Zm9ybWF0PgogICAgICAgICA8eG1wTU06SW5zdGFuY2VJRD54bXAuaWlkOjFkMGNkMDExLTFlZTEtNzI0ZC05YjZiLWRhZjEwZmQyZDNlYzwveG1wTU06SW5zdGFuY2VJRD4KICAgICAgICAgPHhtcE1NOkRvY3VtZW50SUQ+YWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjNlM2IwYTQ5LTgwYTMtMTFmMC1iOWRhLWZmMzA3NzcyMGFkZTwveG1wTU06RG9jdW1lbnRJRD4KICAgICAgICAgPHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD54bXAuZGlkOjM5NTFiODg5LWVlYjUtMjY0NC04MzU1LTlmNTk2ZTRkODA2MDwveG1wTU06T3JpZ2luYWxEb2N1bWVudElEPgogICAgICAgICA8eG1wTU06SGlzdG9yeT4KICAgICAgICAgICAgPHJkZjpTZXE+CiAgICAgICAgICAgICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6YWN0aW9uPmNyZWF0ZWQ8L3N0RXZ0OmFjdGlvbj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0Omluc3RhbmNlSUQ+eG1wLmlpZDozOTUxYjg4OS1lZWI1LTI2NDQtODM1NS05ZjU5NmU0ZDgwNjA8L3N0RXZ0Omluc3RhbmNlSUQ+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDp3aGVuPjIwMjUtMDgtMjJUMDA6MTU6MTArMDM6MDA8L3N0RXZ0OndoZW4+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpzb2Z0d2FyZUFnZW50PkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE3IChXaW5kb3dzKTwvc3RFdnQ6c29mdHdhcmVBZ2VudD4KICAgICAgICAgICAgICAgPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6YWN0aW9uPnNhdmVkPC9zdEV2dDphY3Rpb24+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDppbnN0YW5jZUlEPnhtcC5paWQ6ZTc0OGJjOTEtY2M5Ny0xYjRhLTk1MzgtODQ4M2I1N2E2ZWEyPC9zdEV2dDppbnN0YW5jZUlEPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6d2hlbj4yMDI1LTA4LTIyVDAwOjIwOjI2KzAzOjAwPC9zdEV2dDp3aGVuPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6c29mdHdhcmVBZ2VudD5BZG9iZSBQaG90b3Nob3AgQ0MgMjAxNyAoV2luZG93cyk8L3N0RXZ0OnNvZnR3YXJlQWdlbnQ+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpjaGFuZ2VkPi88L3N0RXZ0OmNoYW5nZWQ+CiAgICAgICAgICAgICAgIDwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmFjdGlvbj5zYXZlZDwvc3RFdnQ6YWN0aW9uPgogICAgICAgICAgICAgICAgICA8c3RFdnQ6aW5zdGFuY2VJRD54bXAuaWlkOjU3ZDI3NTBkLWZmYTUtZWQ0ZC1hYmZhLTE3Mzk4YTkxNzFjZTwvc3RFdnQ6aW5zdGFuY2VJRD4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OndoZW4+MjAyNS0wOC0yNFQwNzozMTo0NiswMzowMDwvc3RFdnQ6d2hlbj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OnNvZnR3YXJlQWdlbnQ+QWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKFdpbmRvd3MpPC9zdEV2dDpzb2Z0d2FyZUFnZW50PgogICAgICAgICAgICAgICAgICA8c3RFdnQ6Y2hhbmdlZD4vPC9zdEV2dDpjaGFuZ2VkPgogICAgICAgICAgICAgICA8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaSByZGY6cGFyc2VUeXBlPSJSZXNvdXJjZSI+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDphY3Rpb24+Y29udmVydGVkPC9zdEV2dDphY3Rpb24+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpwYXJhbWV0ZXJzPmZyb20gYXBwbGljYXRpb24vdm5kLmFkb2JlLnBob3Rvc2hvcCB0byBpbWFnZS9wbmc8L3N0RXZ0OnBhcmFtZXRlcnM+CiAgICAgICAgICAgICAgIDwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpIHJkZjpwYXJzZVR5cGU9IlJlc291cmNlIj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmFjdGlvbj5kZXJpdmVkPC9zdEV2dDphY3Rpb24+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpwYXJhbWV0ZXJzPmNvbnZlcnRlZCBmcm9tIGFwcGxpY2F0aW9uL3ZuZC5hZG9iZS5waG90b3Nob3AgdG8gaW1hZ2UvcG5nPC9zdEV2dDpwYXJhbWV0ZXJzPgogICAgICAgICAgICAgICA8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaSByZGY6cGFyc2VUeXBlPSJSZXNvdXJjZSI+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDphY3Rpb24+c2F2ZWQ8L3N0RXZ0OmFjdGlvbj4KICAgICAgICAgICAgICAgICAgPHN0RXZ0Omluc3RhbmNlSUQ+eG1wLmlpZDoxZDBjZDAxMS0xZWUxLTcyNGQtOWI2Yi1kYWYxMGZkMmQzZWM8L3N0RXZ0Omluc3RhbmNlSUQ+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDp3aGVuPjIwMjUtMDgtMjRUMDc6MzE6NDYrMDM6MDA8L3N0RXZ0OndoZW4+CiAgICAgICAgICAgICAgICAgIDxzdEV2dDpzb2Z0d2FyZUFnZW50PkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE3IChXaW5kb3dzKTwvc3RFdnQ6c29mdHdhcmVBZ2VudD4KICAgICAgICAgICAgICAgICAgPHN0RXZ0OmNoYW5nZWQ+Lzwvc3RFdnQ6Y2hhbmdlZD4KICAgICAgICAgICAgICAgPC9yZGY6bGk+CiAgICAgICAgICAgIDwvcmRmOlNlcT4KICAgICAgICAgPC94bXBNTTpIaXN0b3J5PgogICAgICAgICA8eG1wTU06RGVyaXZlZEZyb20gcmRmOnBhcnNlVHlwZT0iUmVzb3VyY2UiPgogICAgICAgICAgICA8c3RSZWY6aW5zdGFuY2VJRD54bXAuaWlkOjU3ZDI3NTBkLWZmYTUtZWQ0ZC1hYmZhLTE3Mzk4YTkxNzFjZTwvc3RSZWY6aW5zdGFuY2VJRD4KICAgICAgICAgICAgPHN0UmVmOmRvY3VtZW50SUQ+YWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOmRjNzNiNjM1LTdmOGEtMTFmMC05ZjZkLWFlNmE4MDBlNzEzNzwvc3RSZWY6ZG9jdW1lbnRJRD4KICAgICAgICAgICAgPHN0UmVmOm9yaWdpbmFsRG9jdW1lbnRJRD54bXAuZGlkOjM5NTFiODg5LWVlYjUtMjY0NC04MzU1LTlmNTk2ZTRkODA2MDwvc3RSZWY6b3JpZ2luYWxEb2N1bWVudElEPgogICAgICAgICA8L3htcE1NOkRlcml2ZWRGcm9tPgogICAgICAgICA8cGhvdG9zaG9wOkNvbG9yTW9kZT4zPC9waG90b3Nob3A6Q29sb3JNb2RlPgogICAgICAgICA8cGhvdG9zaG9wOkRvY3VtZW50QW5jZXN0b3JzPgogICAgICAgICAgICA8cmRmOkJhZz4KICAgICAgICAgICAgICAgPHJkZjpsaT5hZG9iZTpkb2NpZDpwaG90b3Nob3A6MDgxMTQ2NWItN2U3MS0xMWYwLTg0MjYtY2NkMDI1YTk3ZmMyPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGk+YWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjA5NGJlZTRjLTdlNWEtMTFmMC04NDI2LWNjZDAyNWE5N2ZjMjwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpPmFkb2JlOmRvY2lkOnBob3Rvc2hvcDoxMjM1NjAyZS03ZWJmLTExZjAtODQyNi1jY2QwMjVhOTdmYzI8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaT5hZG9iZTpkb2NpZDpwaG90b3Nob3A6M2UzMWU2NjItN2U3NS0xMWYwLTg0MjYtY2NkMDI1YTk3ZmMyPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGk+YWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOjgwMDZiY2E2LTdlNzMtMTFmMC04NDI2LWNjZDAyNWE5N2ZjMjwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpPmFkb2JlOmRvY2lkOnBob3Rvc2hvcDo5MGRkNGNkYy03ZTZhLTExZjAtODQyNi1jY2QwMjVhOTdmYzI8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaT5hZG9iZTpkb2NpZDpwaG90b3Nob3A6OTU4NzBhYjUtN2U2Yi0xMWYwLTg0MjYtY2NkMDI1YTk3ZmMyPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGk+YWRvYmU6ZG9jaWQ6cGhvdG9zaG9wOmI5NDMyNmFlLTdlNWYtMTFmMC04NDI2LWNjZDAyNWE5N2ZjMjwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpPmFkb2JlOmRvY2lkOnBob3Rvc2hvcDpjMDMzYWYzNS03ZTY4LTExZjAtODQyNi1jY2QwMjVhOTdmYzI8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaT5hZG9iZTpkb2NpZDpwaG90b3Nob3A6ZDhlN2FmNzYtN2U3NS0xMWYwLTg0MjYtY2NkMDI1YTk3ZmMyPC9yZGY6bGk+CiAgICAgICAgICAgICAgIDxyZGY6bGk+eG1wLmRpZDo5MmMxNzNlZC1jMzY3LWIxNGYtYTg3OC0yZjUxYmYyMzI5Y2U8L3JkZjpsaT4KICAgICAgICAgICAgICAgPHJkZjpsaT54bXAuZGlkOmUyOWM0ZGFkLTA3YWMtZjc0My1hZTQzLTM4OWU1M2UyZmE1YzwvcmRmOmxpPgogICAgICAgICAgICAgICA8cmRmOmxpPnhtcC5kaWQ6ZmE5ZTMwMzMtZWZiZS02ODQxLTg4MDktMTdiNzNhYjE5YjhlPC9yZGY6bGk+CiAgICAgICAgICAgIDwvcmRmOkJhZz4KICAgICAgICAgPC9waG90b3Nob3A6RG9jdW1lbnRBbmNlc3RvcnM+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjcyMDAwMC8xMDAwMDwvdGlmZjpYUmVzb2x1dGlvbj4KICAgICAgICAgPHRpZmY6WVJlc29sdXRpb24+NzIwMDAwLzEwMDAwPC90aWZmOllSZXNvbHV0aW9uPgogICAgICAgICA8dGlmZjpSZXNvbHV0aW9uVW5pdD4yPC90aWZmOlJlc29sdXRpb25Vbml0PgogICAgICAgICA8ZXhpZjpDb2xvclNwYWNlPjY1NTM1PC9leGlmOkNvbG9yU3BhY2U+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj4yMjwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWURpbWVuc2lvbj4yMjwvZXhpZjpQaXhlbFlEaW1lbnNpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+7aOt+gAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAAF2+SX8VGAAABX0lEQVR42rSVv2vCQBTHv2dNUklBi2gikZPWQpHQ2VlnFyeHTp38m9qlY93qYMGl7SB0sD+ggkTtdNQ1m6FCh9fJIEXjaeKDG254n3vv+34cIyLsw2LYk8WXL6Z5Rpr2CwBMxlkIIR/xafECAChyKZ6fOpHAV2ocBXxt8cLCA7siDHxju+0Kl+rjXeDSA9LttreCS4M1NY72fUsavtVIJ5NHaN3dysGJyD+GUSQZE+KbMtkcLfv+P/GgRz1vDl0/BABUqjUAwHD4Ea54njeHYZyg8/AIAGCM4WvyuVhQbOOiWiXFbPZDum4S55xsu+ynb9tlsqw8LCuPTDaHICli6yJNp1UAYLzA0ev1wXkevMD9oqnKQWDAbPkHqVRr9Np/96GLpBKJDEajNzjOGI3GVRPADQAMBi9yi36Nbmw6nZDjjFEqnUNRlEgnj9Xrl81U6hiuK65dV8B1hbwUUdrfABsm4y8fQOdUAAAAAElFTkSuQmCC
"""

# PACKAGE

MPS = "MPS" # распаковка и чтения из-MePass
EXE = "EXE" # распаковка рядом с EXE
CST = "CST"
UNF = "UNF" # новый режим: запуск без упаковки (unfrozen)
INS = "INS" # Insallator - processed


# Определяем начальный режим
CollectFlag = UNF if not getattr(sys, 'frozen', False) else CST

CustomTempName = "MouseStates_Temp"
_base_printed = False

def unpack_folder(folder_name: str, required_files: list[str] = None):
    if CollectFlag == UNF:
        return

    temp_dir = os.path.join(tempfile.gettempdir(), CustomTempName)
    os.makedirs(temp_dir, exist_ok=True) 

    source_dir = (
        os.path.join(sys._MEIPASS, folder_name)
        if getattr(sys, 'frozen', False)
        else os.path.join(os.path.dirname(__file__), folder_name)
    )

    if CollectFlag == MPS:
        return

    elif CollectFlag == EXE:
        target_dir = os.path.join(os.path.dirname(sys.executable), folder_name)

    elif CollectFlag == CST:

        target_dir = os.path.join(temp_dir, folder_name)

    else:
        raise ValueError(f"Unknown CollectFlag: {CollectFlag}")

    # Проверка, нужно ли пересоздавать папку
    need_repack = False
    if os.path.exists(target_dir):
        if required_files:
            for file_name in required_files:
                full_path = os.path.join(target_dir, file_name)
                if not os.path.isfile(full_path):
                    print(f"[WARN] Не найден обязательный файл: {full_path}")
                    need_repack = True
                    break
        else:
            print(f"Папка '{folder_name}' уже распакована в: {target_dir}")
            return

    if not os.path.exists(target_dir) or need_repack:
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            print(f"[INFO] Удалена старая папка: {target_dir}")
        shutil.copytree(source_dir, target_dir)
        print(f"Распаковано '{folder_name}' в: {target_dir}")
    else:
        print(f"Папка '{folder_name}' уже содержит все нужные файлы: {target_dir}")

def resource_path(relative_path: str) -> str:
    global _base_printed

    if CollectFlag == UNF:
        base = os.path.dirname(os.path.abspath(__file__))
    elif CollectFlag == MPS:
        base = sys._MEIPASS
    elif CollectFlag == EXE:
        base = os.path.dirname(sys.executable)
    elif CollectFlag == CST:
        base = os.path.join(tempfile.gettempdir(), CustomTempName)
    else:
        raise ValueError(f"Unknown CollectFlag: {CollectFlag}")

    if not _base_printed:
        print(f"Грузится из папки: {base}")
        _base_printed = True

    return os.path.join(base, relative_path)


class FileItemWidget(QWidget):
    """Виджет для отображения одного файла с возможностью управления."""
    def __init__(self, file_path, parent_list_widget):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.parent_list_widget = parent_list_widget
        self.file_path = file_path
        self.is_active = False

        self.base_style = "FileItemWidget { background-color: none; border: 1px solid #555; border-radius: 4px; padding: 5px; }"
        self.act_style = "FileItemWidget { background-color: #326b96; border: 1px solid #555; border-radius: 4px; padding: 5px; }"

        self.setStyleSheet(self.base_style)
        self.set_active(False) # Задаем начальный (неактивный) цвет

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)

        file_name = os.path.basename(file_path)

        self.label_index = QLabel("0.")
        self.label_index.setStyleSheet("background-color: transparent;  color: white; font-size: 16px;")
        self.label_index.setFixedWidth(30)

        self.original_file_name = file_name # Сохраняем имя для пересчета
        self.label_name = QLabel(self.original_file_name)
        self.label_name.setStyleSheet("background-color: transparent; color: white; font-size: 16px;")
        
        self.label_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.label_name.setMinimumWidth(40)

        self.label_index.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.label_name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        main_layout.addWidget(self.label_index)
        main_layout.addWidget(self.label_name)
        
       # КНОПКА КАСТОМИЗАЦИИ КУРСОРA СТЕЙТА
        self.cursor_pixmap = self.parent_list_widget.app_cursor_pixmap
        self.btn_set_cursor = QPushButton() 

        # Мгновенно генерируем иконку из основного курсора программы
        if self.cursor_pixmap and not self.cursor_pixmap.isNull():
            # Масштабируем до аккуратных 16x16 пикселей с сохранением пропорций и сглаживанием
            thumb = self.cursor_pixmap.scaled(
                16, 16, Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.btn_set_cursor.setIcon(QIcon(thumb))


        self.btn_up = QPushButton("↑")
        self.btn_down = QPushButton("↓")
        self.btn_replace = QPushButton("R")
        self.btn_remove = QPushButton("X")

        btn_style = "background-color: transparent; color: white; font-size: 16px;  border: 1px solid #666;"
        for btn in (self.btn_up, self.btn_down, self.btn_replace, self.btn_remove, self.btn_set_cursor):
            btn.setStyleSheet(btn_style)
            btn.setFixedSize(30,30)
        

        main_layout.addWidget(self.btn_set_cursor)
        main_layout.addWidget(self.btn_up)
        main_layout.addWidget(self.btn_down)
        main_layout.addWidget(self.btn_replace)
        main_layout.addWidget(self.btn_remove)


        # Сигналы
        self.btn_set_cursor.clicked.connect(self.set_cursor)
        self.btn_up.clicked.connect(self.move_up)
        self.btn_down.clicked.connect(self.move_down)
        self.btn_remove.clicked.connect(self.remove_self)
        self.btn_replace.clicked.connect(self.replace_file)

            

    def set_active(self, active: bool):
        self.is_active = active
        if active:
            self.setStyleSheet(self.act_style)
        else:
            self.setStyleSheet(self.base_style)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_list_widget.set_active_widget(self)
        super().mousePressEvent(event)
        
    def replace_file(self):
        file_filter = "Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mkv *.mov)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите медиафайл", os.path.dirname(self.file_path), file_filter
        )
        if file_path:
            self.update_path(file_path)
            self.parent_list_widget.set_active_widget(self)

    def update_path(self, new_path):
        self.file_path = new_path
        self.original_file_name = os.path.basename(new_path) # Обновляем оригинал
        self.label_name.setText(self.original_file_name)
        self.parent_list_widget.sync_data_array()


    def set_cursor(self):
        """Открывает диалог для выбора индивидуального курсора этой сцены."""
        file_filter = "Cursor Files (*.png *.jpg *.jpeg)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение курсора", "", file_filter
        )
        
        if file_path:
            self.cursor_pixmap = QPixmap(file_path)
            thumb_pixmap = self.cursor_pixmap.scaled(
                16, 16, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.btn_set_cursor.setIcon(QIcon(thumb_pixmap))
            
            # 4. Если этот стейт сейчас активен на экране — мгновенно применяем курсор
            if self.parent_list_widget.active_widget == self:
                self.parent_list_widget.apply_state_cursor(self)


    def move_up(self):
        self.parent_list_widget.move_widget(self, -1)
        self.parent_list_widget.set_active_widget(self)

    def move_down(self):
        self.parent_list_widget.move_widget(self, 1)
        self.parent_list_widget.set_active_widget(self)

    def remove_self(self):
        self.parent_list_widget.remove_widget(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        metrics = QFontMetrics(self.label_name.font())
        
        available_width = self.label_name.width()

        elided_text = metrics.elidedText(
            self.original_file_name, 
            Qt.TextElideMode.ElideRight, 
            available_width
        )
        self.label_name.setText(elided_text)



class CaptureAreaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        

        self.parent_app = parent  # Ссылка на RecorderApp
        self._pixmap_cache = {}
        self.current_image_path = None
        self.user_color = "green"
        self.current_video_frame = None  # Сюда пишем QPixmap кадра видео

        # Переменные для кастомного курсора
        self.cursor_pixmap = None
        self.current_mouse_pos = None

        # ВАЖНО: включаем отслеживание мыши, даже если кнопки не зажаты
        self.setMouseTracking(True)


    def set_custom_cursor(self, pixmap):
        """Принимает уже готовый QPixmap курсора из памяти."""
        self.cursor_pixmap = pixmap
        self.update()

    def mouseMoveEvent(self, event):
        """Запоминаем координаты мыши при движении и обновляем экран."""
        self.current_mouse_pos = event.position().toPoint()
        self.update()  # Вызывает paintEvent для перерисовки курсора на новом месте
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        """Перенаправляем клик по экрану в логику контроллера RecorderApp."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.parent_app:
                self.parent_app.handle_capture_area_click()
        super().mousePressEvent(event)

    def set_image(self, file_path):
        """Переключение на статичное изображение."""
        self.current_video_frame = None  # Сбрасываем видео-кадр
        if not file_path:
            self.current_image_path = None
            self.update()
            return

        self.current_image_path = file_path
        if file_path not in self._pixmap_cache:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self._pixmap_cache[file_path] = pixmap
        self.update()

    def set_video_frame(self, pixmap):
        """Установка текущего кадра видео для отрисовки."""
        self.current_video_frame = pixmap
        self.update()

    def enterEvent(self, event):
        """Срабатывает, когда мышка заходит на территорию области захвата."""
        # Если запись НЕ идет, обновляем системный курсор под текущий стейт
        if self.parent_app and not self.parent_app.is_recording:
            active_widget = self.parent_app.active_widget
            if active_widget and not active_widget.cursor_pixmap.isNull():
                custom_sys_cursor = QCursor(active_widget.cursor_pixmap, 0, 0)
                self.setCursor(custom_sys_cursor)
                
        super().enterEvent(event)

    def clear_cache(self):
        self._pixmap_cache.clear()
        self.current_video_frame = None
        self.update()



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.fillRect(self.rect(), QColor(self.user_color))

        pixmap = None
        if self.current_video_frame:
            pixmap = self.current_video_frame
        elif self.current_image_path and self.current_image_path in self._pixmap_cache:
            pixmap = self._pixmap_cache[self.current_image_path]

        if pixmap:
            img_w, img_h = pixmap.width(), pixmap.height()
            win_w, win_h = self.width(), self.height()
            scale = max(win_w / img_w, win_h / img_h)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            x = (win_w - new_w) // 2
            y = (win_h - new_h) // 2
            painter.drawPixmap(x, y, new_w, new_h, pixmap)


class RecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Mouse App States Recorder")
        self.resize(1050, 660) 

        # Курсор
        byte_array = QByteArray.fromBase64(CURSOR_BASE64.encode())
        self.app_cursor_pixmap  = QPixmap()
        self.app_cursor_pixmap.loadFromData(byte_array)
        icon = QIcon(self.app_cursor_pixmap)
        self.setWindowIcon(icon) 

        self.active_widget = None
        self.file_paths_array = []
        self.q_param = 6
        self.user_hex_color = "green"

        self.timer_record = QTimer()
        self.timer_record.timeout.connect(self.capture_frame)
        
        self.timer_video = QTimer()
        self.timer_video.timeout.connect(self.play_video_step)
        
        self.is_recording = False
        self.video_writer = None

        # Переменные видеоплеера
        self.cap = None  # Объект cv2.VideoCapture
        self.video_fps = 30
        self.video_playing = False
        self.is_first_rec_click = True
        self.frame_jitter = False
        
        self.mouse_only_buffer = None 
        self.alpha_qt = False 
        

        #self.img_to_byde()
        self.init_ui()
        

        if not self.app_cursor_pixmap.isNull():
            self.app_cursor = QCursor(self.app_cursor_pixmap, 0, 0)
            self.setCursor(self.app_cursor)

            self.capture_area.set_custom_cursor(None) 
            self.capture_area.setCursor(self.app_cursor)


    def img_to_byde(self):
        import base64
        with open("./assets/arrow.png", "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode('utf-8')
            print(base64_string) 


    def init_ui(self):

        app_layout = QHBoxLayout()
        app_layout.setContentsMargins(0, 0, 0, 0)
        app_layout.setSpacing(0)


        # MAIN PANEL

        self.main_area = QWidget()
        self.main_area.setStyleSheet("background-color: #111d26;") 
        
        main_layout = QVBoxLayout(self.main_area) 
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.toolbar = QWidget()
        self.toolbar.setStyleSheet("background-color: #2c3e50;")
        
        toolbar_layout = QHBoxLayout(self.toolbar)
        self.btn_record = QPushButton("REC")
        self.btn_record.setFixedSize(150, 40)
        self.btn_record.clicked.connect(self.toggle_recording)
        self.btn_record.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        self.status_label = QLabel("current state: pause")
        self.status_label.setStyleSheet("color: grey; font-size: 18px;")
        
        toolbar_layout.addWidget(self.btn_record)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.status_label)
        
        self.capture_area = CaptureAreaWidget(self)
        self.capture_area.setFixedSize(800, 600)

        zone_layout = QVBoxLayout(self.capture_area)

        self.info_text = QLabel("capture area", self.capture_area)

        self.info_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_text.setStyleSheet("background-color: transparent; color: #ecf0f1; font-size: 18px; font-weight: bold;")
        self.info_text.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        zone_layout.addWidget(self.info_text)

        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.capture_area)
        main_layout.addStretch()


        # SETTING PANEL

        self.settings_area = QWidget()
        self.settings_area.setStyleSheet("background-color: #1a252f;") 
        self.settings_area.setMinimumWidth(330)
        
        setting_layout = QVBoxLayout(self.settings_area) 
        setting_layout.setContentsMargins(10, 20, 10, 10)
        
        self.setting_label = QLabel("SETTINGS")
        self.setting_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

        self.area_size = QLabel("Area Size:")
        self.area_size.setStyleSheet("color: white; font-size: 18px; ")

        # SIZES

        size_inputs_widget = QWidget()
        size_inputs_layout = QHBoxLayout(size_inputs_widget)
        size_inputs_layout.setContentsMargins(0, 0, 0, 0)
        size_inputs_layout.setSpacing(5)

        self.width_input = QLineEdit()
        self.width_input.setText("800")
        self.width_input.setPlaceholderText("W")
        self.width_input.setFixedHeight(30)
        self.width_input.setStyleSheet("background-color: #2c3e50; color: white; font-size: 16px; border: 1px solid #34495e; padding-left: 5px;")
        self.width_input.editingFinished.connect(self.update_capture_area_size) 

        x_label = QLabel("x")
        x_label.setStyleSheet("color: white; font-size: 16px;")
        x_label.setFixedWidth(10)

        self.height_input = QLineEdit()
        self.height_input.setText("600")
        self.height_input.setPlaceholderText("H")
        self.height_input.setFixedHeight(30)
        self.height_input.setStyleSheet("background-color: #2c3e50; color: white; font-size: 16px; border: 1px solid #34495e; padding-left: 5px;")
        self.height_input.editingFinished.connect(self.update_capture_area_size)
        
        size_inputs_layout.addWidget(self.width_input)
        size_inputs_layout.addWidget(x_label)
        size_inputs_layout.addWidget(self.height_input)

        self.base_param_label = QLabel("Params:")
        self.base_param_label.setStyleSheet("color: white; font-size: 18px; ")

        self.mouse_checkbox = QCheckBox("MOUSE ONLY", self)
        self.mouse_checkbox.setChecked(False) 
        self.mouse_checkbox.setStyleSheet("color: white;  font-size: 18px;")
        

        self.color_btn = QPushButton("C-KEY")
        self.color_btn.setFixedHeight(30)
        self.color_btn.setStyleSheet("color: white;  background-color: grey; font-size: 18px;")
        self.color_btn.clicked.connect(self.choose_area_color) # Привязываем функцию

        self.color_btn.setEnabled(False)


        self.alpha_checkbox = QCheckBox("A.MOV ", self)
        self.alpha_checkbox.setChecked(False) 
        self.alpha_checkbox.setStyleSheet("color: grey;  font-size: 18px;")
        self.alpha_checkbox.setEnabled(False)

        

        self.mouse_checkbox.toggled.connect(self.color_btn.setEnabled)
        self.mouse_checkbox.toggled.connect(self.alpha_checkbox.setEnabled)

        self.alpha_checkbox.toggled.connect(self.on_alpha_toggled)
        self.mouse_checkbox.toggled.connect(self.on_checkbox_toggled)

        mouse_grab_w = QWidget()
        mouse_grab_layout = QHBoxLayout(mouse_grab_w)
        mouse_grab_layout.setContentsMargins(0, 0, 0, 0)
        mouse_grab_layout.setSpacing(5)

        mouse_grab_layout.addWidget(self.mouse_checkbox)
        mouse_grab_layout.addWidget(self.alpha_checkbox)
        mouse_grab_layout.addWidget(self.color_btn)


        self.quality_label = QLabel("Record Quality:")
        self.quality_label.setStyleSheet("color: white; font-size: 18px; ")


        self.quality_input = QLineEdit()
        self.quality_input.setText("6")
        self.quality_input.setPlaceholderText("W")
        self.quality_input.setFixedHeight(30)
        self.quality_input.setStyleSheet("background-color: #2c3e50; color: white; font-size: 16px; border: 1px solid #34495e; padding-left: 5px;")
        self.quality_input.editingFinished.connect(self.update_quality) 


        codec_w = QWidget()
        codec_layout = QHBoxLayout(codec_w)
        codec_layout.setContentsMargins(0, 0, 0, 0)
        codec_layout.setSpacing(5)


        codec_layout.addWidget(self.quality_input)
 

        self.state_label = QLabel("States:")
        self.state_label.setStyleSheet("color: white; font-size: 18px; ")

        self.plus_state = QPushButton(" ADD STATES ")
        self.plus_state.setFixedHeight(40) 
        self.plus_state.setStyleSheet("background-color: #2c3e50; color: white; font-size: 16px; border: 1px solid #34495e; padding-left: 5px;")
        self.plus_state.clicked.connect(self.open_file_dialog)

        # LIST OBJECTS
        self.container_widget = QWidget()
        self.list_layout = QVBoxLayout(self.container_widget)
        self.list_layout.setAlignment(Qt.AlignmentFlag.AlignTop) 
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container_widget)

        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)



        # SETTING COMBINE
        setting_layout.addWidget(self.setting_label)
        setting_layout.addSpacing(10)
        
        setting_layout.addWidget(self.area_size)
        setting_layout.addWidget(size_inputs_widget)

        setting_layout.addSpacing(8)

        setting_layout.addWidget(self.base_param_label)
        setting_layout.addWidget(mouse_grab_w)

        #setting_layout.addWidget(self.quality_label)
        #setting_layout.addWidget(codec_w)
        setting_layout.addSpacing(8)

        setting_layout.addWidget(self.state_label)
        setting_layout.addWidget(scroll)
        setting_layout.addWidget(self.plus_state)


       # COMBINE_INTERFACE

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.main_area)
        self.splitter.addWidget(self.settings_area)
        self.splitter.setSizes([800, 250])
        self.splitter.setHandleWidth(1)

        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: black;
            }
        """)

        
        self.setCentralWidget(self.splitter)
        

    # USER INTERFACE METHODS 
    
    def on_checkbox_toggled(self, is_checked: bool):
        if is_checked:
            self.color_btn.setStyleSheet(f"color: white; background-color: {self.user_hex_color}; font-size: 18px;")
            self.alpha_checkbox.setStyleSheet("color: white;  font-size: 18px;")
        else:
            self.color_btn.setStyleSheet("color: black; background-color: grey; font-size: 18px;")
            self.alpha_checkbox.setStyleSheet("color: grey;  font-size: 18px;")


    def on_alpha_toggled(self, is_checked: bool):
        if is_checked:
            self.color_btn.setStyleSheet(f"color: white; background-color: grey; font-size: 18px;")
            self.color_btn.setEnabled(False)
            self.alpha_qt = True
        else:
            self.color_btn.setStyleSheet(f"color: white; background-color: {self.user_hex_color}; font-size: 18px;")
            self.color_btn.setEnabled(True)
            self.alpha_qt = False


    def sync_data_array(self):
        """Проходит по всем виджетам в лейауте, обновляет их индексы на экране и собирает пути."""
        self.file_paths_array.clear()
        
        current_index = 0
        for i in range(self.list_layout.count()):
            item = self.list_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.label_index.setText(f"{current_index}.") 
                    self.file_paths_array.append(widget.file_path)
                    current_index += 1



    def move_widget(self, widget, direction):
        """Перемещает виджет вверх (-1) или вниз (+1) в лейауте."""
        index = self.list_layout.indexOf(widget)
        new_index = index + direction

        if 0 <= new_index < self.list_layout.count():
            self.list_layout.takeAt(index)
            self.list_layout.insertWidget(new_index, widget)
            self.sync_data_array()

    def remove_widget(self, widget):
        if self.active_widget == widget:
            self.active_widget = None
            
        self.list_layout.removeWidget(widget)
        widget.setParent(None) 
        widget.deleteLater()
        
        self.sync_data_array()
        
        if len(self.file_paths_array) == 0:
            self.close_video()
            self.capture_area.clear_cache()
            self.capture_area.set_image(None)
            self.info_text.show()


    # OPTIONS METHODS 

    def choose_area_color(self):
        color = QColorDialog.getColor(initial=QColor("green"), parent=self)

        if color.isValid():
            self.user_hex_color = color.name()

            self.capture_area.user_color = self.user_hex_color
            self.color_btn.setStyleSheet(f"color: white; background-color: {self.user_hex_color}; font-size: 18px;")

    def update_capture_area_size(self):
        try:
            w = int(self.width_input.text())
            h = int(self.height_input.text())        
            self.capture_area.setFixedSize(w, h)
        except ValueError:
            pass


    def update_quality(self):
        try:
            q = int(self.quality_input.text()) 
            self.q_param = q
        except ValueError:
            pass

    # MEDIA STRUCTURE


    def open_file_dialog(self):
        """Открывает диалог выбора файлов с фильтром на фото и видео."""
        file_filter = "Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mkv *.mov)"
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Выберите изображения или видео", 
            "", 
            file_filter
        )
        
        if files:
            for file_path in files:
                self.add_file_item(file_path)

    def add_file_item(self, file_path):
        """Создает виджет, добавляет его в интерфейс и обновляет массив."""
        item_widget = FileItemWidget(file_path, self)
        self.list_layout.addWidget(item_widget)
    
        self.sync_data_array()
        
        if self.info_text.isVisible():
            self.info_text.hide()


    def get_current_active_index(self):
        """Возвращает числовой индекс текущего выделенного виджета."""
        if self.active_widget:
            for i in range(self.list_layout.count()):
                if self.list_layout.itemAt(i).widget() == self.active_widget:
                    return i
        return 0

    def handle_capture_area_click(self):
        """Логика кликов по capture region """
        print("клик!")

        if not self.file_paths_array:
            return

        current_idx = self.get_current_active_index()
        file_path = self.file_paths_array[current_idx]
        ext = os.path.splitext(file_path)[1].lower()
        is_video = ext in ['.mp4', '.avi', '.mkv', '.mov']

        # === ЛОГИКА В РЕЖИМЕ ЗАПИСИ (REC) ===
        if self.is_recording:
            # ОБРАБОТКА ПЕРВОГО КЛИКА ПОСЛЕ СТАРТА REC
            if self.is_first_rec_click:
                self.is_first_rec_click = False
                if is_video:
                    # Снимаем первый кадр с паузы и запускаем
                    self.video_playing = True
                    self.timer_video.start(1000 // self.video_fps)
                    self.status_label.setText("current state: recording process (video playing)")
                    return

            # ОБРАБОТКА ВСЕХ ПОСЛЕДУЮЩИХ КЛИКОВ (Переключение дальше без зацикливания)
            next_idx = current_idx + 1
            if next_idx < len(self.file_paths_array):
                self.activate_widget_by_index(next_idx)

        # === ЛОГИКА В ОБЫЧНОМ РЕЖИМЕ (БЕЗ ЗАПИСИ) ===
        else:
            next_idx = current_idx + 1
            # Зацикливаем список элементов, если дошли до конца
            if next_idx >= len(self.file_paths_array):
                next_idx = 0

            self.activate_widget_by_index(next_idx)

    def set_active_widget(self, widget):
        """Переключение фокуса на выбранный виджет-стейт."""
        if self.active_widget:
            self.active_widget.set_active(False)

        self.active_widget = widget
        
        if self.active_widget:
            self.active_widget.set_active(True)
            
            self.apply_state_cursor(self.active_widget)
            
            play_now = not self.is_recording
            self.load_media(widget.file_path, play_immediately=play_now)
        else:
            self.close_video()
            self.capture_area.set_image(None)
            self.capture_area.set_custom_cursor(None)


    def activate_widget_by_index(self, index):
        """Вспомогательный метод для переключения активного элемента и медиа."""
        next_widget = self.list_layout.itemAt(index).widget()
        if next_widget:
            # Делаем активным в UI списке (красим в синий)
            if self.active_widget:
                self.active_widget.set_active(False)
            self.active_widget = next_widget
            self.active_widget.set_active(True)

            # Загружаем медиафайл на экран
            next_file = self.file_paths_array[index]
            next_ext = os.path.splitext(next_file)[1].lower()
            is_next_video = next_ext in ['.mp4', '.avi', '.mkv', '.mov']

            self.load_media(next_file, play_immediately=is_next_video)
            self.apply_state_cursor(self.active_widget)


    def apply_state_cursor_old(self, widget):
        if not widget or widget.cursor_pixmap.isNull():
            return

        custom_sys_cursor = QCursor(widget.cursor_pixmap, 0, 0)

        # 1. РЕЖИМ ЗАПИСИ (REC)
        if self.is_recording:
            # Во время записи глобальный блок ОПРАВДАН, чтобы курсор случайно 
            # не сменился на стрелку при наведении мыши на кнопки тулбара
            if not QApplication.overrideCursor():
                QApplication.setOverrideCursor(custom_sys_cursor)
            elif QApplication.overrideCursor().pixmap().cacheKey() != widget.cursor_pixmap.cacheKey():
                QApplication.changeOverrideCursor(custom_sys_cursor)

            self.capture_area.set_custom_cursor(widget.cursor_pixmap)
            self.capture_area.setCursor(Qt.CursorShape.BlankCursor)

        # 2. ОБЫЧНЫЙ РЕЖИМ (ПРЕВЬЮ) — БЕЗОПАСНЫЙ ДЛЯ РЕСАЙЗА
        else:
            # Если запись остановлена — полностью убираем тотальный блок курсоров
            if QApplication.overrideCursor():
                QApplication.restoreOverrideCursor()

            self.capture_area.set_custom_cursor(None)
            
            # Меняем локальный курсор для фона главного окна
            self.setCursor(self.app_cursor)
            self.capture_area.setCursor(custom_sys_cursor)
           

    def apply_state_cursor(self, widget):
        if not widget or widget.cursor_pixmap.isNull():
            return

        custom_sys_cursor = QCursor(widget.cursor_pixmap, 0, 0)

        # 1. РЕЖИМ ЗАПИСИ (REC)
        if self.is_recording:
            if not QApplication.overrideCursor():
                QApplication.setOverrideCursor(custom_sys_cursor)
            elif QApplication.overrideCursor().pixmap().cacheKey() != widget.cursor_pixmap.cacheKey():
                QApplication.changeOverrideCursor(custom_sys_cursor)

            self.capture_area.set_custom_cursor(widget.cursor_pixmap)
            self.capture_area.setCursor(custom_sys_cursor)

        # 2. ОБЫЧНЫЙ РЕЖИМ (ПРЕВЬЮ)
        else:
            if QApplication.overrideCursor():
                QApplication.restoreOverrideCursor()

            self.capture_area.set_custom_cursor(None)
            self.capture_area.setCursor(custom_sys_cursor)
            self.setCursor(self.app_cursor)


    def load_media(self, file_path, play_immediately=True):
        """Загрузка медиафайла. Определяет видео/картинку."""
        self.close_video()  # Закрываем предыдущее видео, если оно было
        
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()
        is_video = ext in ['.mp4', '.avi', '.mkv', '.mov']

        if not self.is_recording:
            self.status_label.setText(f"preview {'video' if is_video else 'image'}")

        if is_video:
            self.cap = cv2.VideoCapture(file_path)
            if self.cap.isOpened():
                # Получаем родной FPS видеофайла
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.video_fps = int(fps) if fps > 0 else 30
                
                # Читаем самый первый кадр, чтобы показать превью
                self.show_next_video_frame()
                
                if play_immediately:
                    self.video_playing = True
                    self.timer_video.start(1000 // self.video_fps)
                else:
                    self.video_playing = False
                    self.timer_video.stop()
        else:
            # Статичное изображение
            self.video_playing = False
            self.timer_video.stop()
            self.capture_area.set_image(file_path)


    def show_next_video_frame(self):
        """Читает один кадр из cv2 и отправляет его в область захвата."""
        if not self.cap or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        
        if not ret:
            self.video_playing = False
            self.timer_video.stop()
            if not self.is_recording:
                self.status_label.setText("preview video (ended)")
            return

        if ret:
            # Конвертируем BGR (OpenCV) -> RGB -> QPixmap
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.capture_area.set_video_frame(pixmap)

    def play_video_step(self):
        """Срабатывает по таймеру видеоплеера."""
        if self.video_playing:
            self.show_next_video_frame()

    def close_video(self):
        """Освобождение ресурсов видеоплеера."""
        self.timer_video.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_playing = False


    # RECORDING

    def toggle_recording(self):
        if self.info_text.isVisible():
            self.info_text.hide()

        if not self.is_recording:
            if not self.file_paths_array:
                return  


            if self.alpha_qt:

                self.video_writer = imageio.get_writer(
                    'mouse_alpha.mov',
                    fps=30, 
                    codec='qtrle',
                    pixelformat='argb' 
                )
            else:
                self.video_writer = imageio.get_writer(
                    'mouse_record.mp4', 
                    fps=30, 
                    codec='libx264', 
                    # quality=self.q_param, больше не нужен, так как crf=0 принудительно включает 100% качество
                    pixelformat='yuv444p',
                    output_params=['-crf', '0', '-preset', 'ultrafast']
                )

            self.is_recording = True
            
            # Ставим первый стейт активным
            first_widget = self.list_layout.itemAt(0).widget()
            if first_widget:
                if self.active_widget:
                    self.active_widget.set_active(False)
                self.active_widget = first_widget
                self.active_widget.set_active(True)

            # === АКТИВИРУЕМ КУРСОР ДЛЯ РЕЖИМА ЗАПИСИ ===
            if self.active_widget:
                self.apply_state_cursor(self.active_widget)

            self.is_first_rec_click = True
            self.load_media(self.file_paths_array[0], play_immediately=False)

            self.timer_record.start(1000 // 30)  
            self.status_label.setText("current state: recording process")
            self.btn_record.setText("STOP")
            
        else:
            self.is_recording = False
            self.timer_record.stop()
            self.close_video()
            
            if self.video_writer is not None:
                self.video_writer.close()
                self.video_writer = None
            
            if self.alpha_qt:
                self.status_label.setText("current state: save mouse_alpha.mov")
            else:
                self.status_label.setText("current state: save mouse_record.mp4")

            self.btn_record.setText("REC")

            # === ВОЗВРАЩАЕМ КУРСОР В ОБЫЧНЫЙ РЕЖИМ (ЭКОНОМИЯ CPU) ===
            # Глобальный override убираем, возвращаем управление локальным виджетам
            QApplication.setOverrideCursor(self.app_cursor)
            
            if self.active_widget:
                self.apply_state_cursor(self.active_widget)
                self.load_media(self.active_widget.file_path, play_immediately=True)


    def capture_frame(self):
        if not self.is_recording or self.video_writer is None:
            return
            
        w = self.capture_area.width()
        h = self.capture_area.height()
        
        # Получаем актуальный курсор стейта
        cursor_pixmap = self.capture_area.cursor_pixmap
        if (cursor_pixmap is None or cursor_pixmap.isNull()) and self.active_widget:
            cursor_pixmap = self.active_widget.cursor_pixmap
            
        global_mouse_pos = QCursor.pos()
        mouse_pos = self.capture_area.mapFromGlobal(global_mouse_pos)
        is_mouse_inside = self.capture_area.rect().contains(mouse_pos)

        if self.mouse_checkbox.isChecked():
            # === РЕЖИМ 1: MOUSE ONLY ===
            if self.alpha_qt:
                if self.mouse_only_buffer is None or self.mouse_only_buffer.format() != QImage.Format.Format_ARGB32:
                    self.mouse_only_buffer = QImage(w, h, QImage.Format.Format_ARGB32)
            else:
                if self.mouse_only_buffer is None or self.mouse_only_buffer.format() != QImage.Format.Format_RGB888:
                    self.mouse_only_buffer = QImage(w, h, QImage.Format.Format_RGB888)
                
            painter = QPainter(self.mouse_only_buffer)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            if self.alpha_qt:
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
                painter.fillRect(self.mouse_only_buffer.rect(), Qt.GlobalColor.transparent)
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            else:
                painter.fillRect(self.mouse_only_buffer.rect(), QColor(self.user_hex_color))
            
            # Впекаем курсор в буфер памяти скрытно от глаз пользователя
            if is_mouse_inside and cursor_pixmap:
                painter.drawPixmap(mouse_pos.x(), mouse_pos.y(), cursor_pixmap)
                
            # Рисуем однопиксельный маяк для After Effects 2020
            self.frame_jitter = not self.frame_jitter
            color = QColor(255, 0, 0, 1) if self.alpha_qt else (Qt.GlobalColor.red if self.frame_jitter else Qt.GlobalColor.green)
            if self.alpha_qt and not is_mouse_inside:
                color = QColor(255, 0, 0, 1)
            painter.setPen(color)
            painter.drawPoint(w - 1, h - 1)
            
            painter.end()
            image = self.mouse_only_buffer
            
        else:
            # === РЕЖИМ 2: СТАНДАРТНЫЙ ЗАХВАТ (МЕДИА + КУРСОР) ===
            pixmap = self.capture_area.grab() 
            fmt = QImage.Format.Format_ARGB32 if self.alpha_qt else QImage.Format.Format_RGB888
            image = pixmap.toImage().convertToFormat(fmt)
            
            if is_mouse_inside and cursor_pixmap:
                painter = QPainter(image)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                painter.drawPixmap(mouse_pos.x(), mouse_pos.y(), cursor_pixmap)
                
                # Добавляем пиксель-маяк для AE 2020 и в стандартный режим
                self.frame_jitter = not self.frame_jitter
                color = Qt.GlobalColor.red if self.frame_jitter else Qt.GlobalColor.green
                painter.setPen(color)
                painter.drawPoint(w - 1, h - 1)
                
                painter.end()

        width = image.width()
        height = image.height()
        ptr = image.bits() 
        
        channels = 4 if self.alpha_qt else 3
        frame = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, channels))
        self.video_writer.append_data(frame)


   


if __name__ == "__main__":
    app = QApplication(sys.argv)

    unpack_folder("assets")

    window = RecorderApp()
    window.show()
    sys.exit(app.exec())