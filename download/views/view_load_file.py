# download/views/view_load_file.py:1
"""
Here is we only loading files. It is the one file *.xlsx that was sent from the:
  - JS's form (on the admin dashboard)
  - or API key POST: '/api/download/load/file/'
    .
"""
import asyncio
import logging
import os
import re
import tempfile
import zipfile
from io import BytesIO, StringIO
from pathlib import Path

import pandas as pd
from adrf.viewsets import ViewSet
from django.http import JsonResponse
from rest_framework import status

from catalog.models import ProductGalleryImageModel
from download.permissions.permission_drf import CanLoadFilePermission
from download.task_save_file import task_saving_data_oFfile
from project import BASE_DIR
from project.settings_conf import settings_first

log = logging.getLogger(__name__)


class CatalogViewSet(ViewSet):
    queryset = ProductGalleryImageModel.objects.all()
    PREFIX_LOG = "[CatalogViewSet]:"
    permission_classes = [CanLoadFilePermission]

    async def create(self, request, *args, **kwargs):
        """
        TODO: Put a signal for alert about loads file. xlsx - передача chunks - ломает файл.
            При этом старый файл передаётся без ошибок.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        log_t = "{}[{}]:".format(self.PREFIX_LOG[:-1], self.create.__name__)
        lock = asyncio.Lock()
        post_data = await asyncio.to_thread(lambda: request.POST)
        post_files = await asyncio.to_thread(lambda: request.FILES)

        field_name = post_data.get("file_name", "name_didnot_found")
        log.warning("{} DEBUG WARN FileName: {}".format(log_t, field_name))
        count_str = post_data.get("total_chunks", "1")
        total_chunks = (
            int(count_str)
            if "." in count_str and ".0" in count_str
            else int(float(count_str))
        )
        chunk_index = int(post_data.get("chunk_index", "0"))
        log.warning("{} DEBUG WARN CHUNK: {}".format(log_t, str(chunk_index)))
        chunk_size = post_data.get("chunk_size", "1")
        # ---
        if not post_files:
            post_files = post_data.get("files")
            if post_files is None:

                log.warning(f"{log_t} DEBUG WARN File: None")
                return await asyncio.to_thread(
                    lambda: JsonResponse(
                        {"error": "Missing file or filename"}, status=400
                    )
                )

        file_values = (
            list(post_files.values()) if not isinstance(post_files, str) else post_files
        )
        log.warning("{} DEBUG WARN CHUNK FILE: {}".format(log_t, str(file_values)))
        # size_chunk = file_values[0].DEFAULT_CHUNK_SIZE if not isinstance(post_files, str) and len(file_values) > 0 else 0
        one_chunk = post_files.get("file")
        log.warning("{} DEBUG WARN File: {}".format(log_t, str(one_chunk)))
        if not re.search(r"(\.xls|\.xlsx)$", field_name):
            return await asyncio.to_thread(
                lambda: JsonResponse(
                    {"error": "Check your file. It need xls or xlsx"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            )

        # field_name = (field_name.split("."))[0] + ".txt"
        if not chunk_size or not field_name or not one_chunk:
            return await asyncio.to_thread(
                lambda: JsonResponse(
                    {"error": "Missing file or filename"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            )
        # ---
        temp_dir = os.path.join(tempfile.gettempdir(), "chunked_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        chunk_path: str = os.path.join(str(temp_dir), f"{field_name}.part{chunk_index}")
        # ---
        async with lock:
            try:
                # ============================================
                # CHUNKS RECORDING TO THE FILE
                # ============================================
                if chunk_index < total_chunks:
                    # with open(str(chunk_path).replace("\\", "/"), "wb") as f:
                    # with Path(str(chunk_path).replace("\\", "/")).open(mode="wb") as f:
                    with open(str(chunk_path).replace("\\", "/"), "wb") as f:

                        # for chunk_part in chunk:
                        for chunk_part in one_chunk.chunks():
                            f.write(chunk_part)
            except Exception as e:
                return JsonResponse(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            # ---
            try:
                if chunk_index == total_chunks - 1:
                    # ============================================
                    # COLLECTING A WHOLE FILE
                    # ============================================
                    final_dir = str(settings_first.MEDIA_ROOT) + "/documents"
                    Path(final_dir).mkdir(parents=True, exist_ok=True)
                    final_path = str(final_dir + "/" + field_name).replace("\\", "/")
                    # with Path(final_path).open(mode="wb") as f:
                    with open(final_path, "wb") as f:
                        calculator = 0
                        for i in range(0, total_chunks):
                            part_path = os.path.join(temp_dir, f"{field_name}.part{i}")
                            while calculator < 3:
                                if calculator == 2 and not os.path.exists(part_path):
                                    raise FileNotFoundError(
                                        f"Chunk {i} not found: {part_path}"
                                    )
                                elif os.path.exists(part_path):
                                    calculator = 3
                                    break
                                await asyncio.sleep(0.3)
                                calculator += 1
                            # for chunk in pd.read_excel(str(part_path), sheet_name="Sheet1", chunk_size=10000):
                            #     df_full = pd.concat(chunk, ignore_index=True)
                            #     df_full.to_excel(part_path.replace("\\", "/"), index=False, sheet_name="Sheet1")

                            with open(part_path.replace("\\", "/"), "rb") as part_file:
                                # with Path(part_path.replace("\\", "/")).open(mode="rb") as part_file:
                                part_str = part_file.read()
                                f.write(part_str)
                            Path(part_path).unlink()
                        f.flush()
                        os.fsync(f.fileno())
                    await asyncio.sleep(0.1)
                    file_size = Path(final_path).stat().st_size
                    log.info("{} File size: {} bytes".format(log_t, file_size))
                    if file_size == 0:
                        log.error("{} File is empty after assembly".format(log_t))
                        return JsonResponse(
                            {"error": "File is empty after assembly"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                    # ============================================
                    # CHECK FILE ON VALIDATION
                    # ============================================
                    is_valid, error_msq = self.validate_file(final_path)
                    if not is_valid:
                        log.error(
                            "{} File validation failed: {}, error: {}".format(
                                log_t, final_path, error_msq
                            )
                        )
                        Path(final_path).unlink(missing_ok=True)
                        return JsonResponse(
                            {"error": "Invalid file format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    # ============================================
                    # RECORDING DATA IN DATABASE
                    # ============================================
                    task_saving_data_oFfile(field_name, request.user.id)
                    # ---
                    return JsonResponse(
                        {"success": True}, status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return JsonResponse(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return JsonResponse(
            {
                "status": "uploading",
                "chunk": chunk_index,
            },
            status=status.HTTP_200_OK,
        )

    def validate_file(self, file_path: str | Path, prefix_log="") -> bool:
        """CHeck that Excel file is correctly or not"""
        global df
        log_t = (
            "{}[{}]".format(prefix_log, self.validate_file.__name__)
            if len(prefix_log) > 0
            else ""
        )
        try:
            path = file_path if isinstance(file_path, Path) else Path(file_path)
            # ---
            # Checking the exists file or not.
            if not path.exists():
                return False, "File does not exist"
            file_size = path.stat().st_size
            # ---
            # Checking a min size for the Excel
            if file_size < 100:
                return False, "File to small size: {} bytes ".format(file_size)
            # ---
            # Check signature of file
            with open(path, "rb") as f:
                header = f.read(4)
                log.info("{} File header: {}".format(log_t, header.hex()))

            try:
                file_data = ""
                with open(path, "rb") as f:
                    file_data = f.read()
                zip_buffer = BytesIO(file_data)
                with zipfile.ZipFile(zip_buffer, "r") as zip_file:
                    is_xml = "[Content_Types].xml" in zip_file.namelist()
                    if not is_xml:
                        return (
                            False,
                            "Not valid Excel file & [Content_Types].xml: {}".format(
                                is_xml
                            ),
                        )

            except zipfile.BadZipFile as e:
                log.info(
                    "{} File BadZipFile => {}".format(
                        log_t, e.args[0] if len(e.args) else str(e)
                    )
                )

            except Exception as e:
                log.info(
                    "{} Error => {}".format(log_t, e.args[0] if len(e.args) else str(e))
                )
            # ---
            try:
                if path.name.split(".")[-1] == "xlsx":
                    df = pd.read_excel(path, engine="openpyxl")
                elif path.name.split(".")[-1] == "xls":
                    df = pd.read_excel(path)
                else:
                    return False, "Not valid Excel file."
                if df is not None:
                    log.info(
                        "{} File successfully read how Excel, shape: {}".format(
                            log_t, df.shape
                        )
                    )
                    return True, "Valid Excel file."
            except Exception as e:
                log.error(
                    "{} Invalid file: {}".format(
                        log_t, e.args[0] if len(e.args) else str(e)
                    )
                )
                return False, "Invalid Excel file."

            return False, "Not valid Excel file."
        except Exception as e:
            log.error(
                "{} Error =>  {}".format(log_t, e.args[0] if len(e.args) else str(e))
            )
            return False
