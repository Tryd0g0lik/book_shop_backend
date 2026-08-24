# download/views/view_load_file.py:1
"""
Here is we only loading files. It is the one file *.xlsx that was sent from the:
  - JS's form (on the admin dashboard)
  - or API key POST: '/api/download/load/file/'
    .
"""
import asyncio
import json
import logging
import math
import os
import re
import zipfile
from io import BytesIO
from pathlib import Path

import pandas as pd
from adrf.viewsets import ViewSet
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from __tests__.tests_api.openapi_schema.users_schema import user_schema
from catalog.models import ProductGalleryImageModel
from download.permissions.permission_drf import CanLoadFilePermission
from download.task_save_file import task_saving_data_oFfile
from project.settings_conf import settings_first

log = logging.getLogger(__name__)


class DownloadOfCatalogViewSet(ViewSet):
    queryset = ProductGalleryImageModel.objects.all()
    permission_classes = [
        IsAdminUser,
    ]
    PREFIX_LOG = "[CatalogViewSet]:"

    @swagger_auto_schema(
        operation_description="""
        Method: POST.
        View: Form data.
        Pathname: '`/download/load/file/``'
        ============================================
        This is a method for use permissions. It is where the upload allows to be and not.
        The upload of file (xls) allows user to be:
        - user.groups == "admin"
        - user.groups == "moderators"
        - user.groups == "editors"
        - user.groups == "manager"

        Else infor to  the '`operation_summary`' from the class '`DownloadOfCatalogViewSet.create`'.
        ---
        Note: User token contain a two views. It is view a 'refresh' and 'access' view. For get all (a working ) token
        use '`utilities/middleware/functions_jwt_tokens.py`'
        """,
        operation_summary="""
        Note!! This method upload a file through chucks.
        Every thing a chunk single we get to tne '`/media/temp/chunked_uploads`' at view the '`< FILE_NAME>.xls.part<CHUNK_INDEX>'`.
        Example: It is '`media/temp/chunked_uploads/template_catalog.xls.part0`'
        ============================================
        If files of 'xls' upload and their we can using that the files of 'xlsx' need manual
        restart for recovery after upload.
        ============================================
        """,
        tags=[
            "download",
        ],
        manual_parameters=[
            openapi.Parameter(
                name="Content-Type",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="multipart/form-data",
                required=True,
            ),
            openapi.Parameter(
                name="Authorization",
                required=True,
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                example="Bearer <KEY>",
            ),
            openapi.Schema(
                name="user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_OBJECT,
                schema=user_schema,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["total_chunks", "chunk_size", "file_name", "chunk_index", "file"],
            properties={
                "total_chunks": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_BINARY,
                    description="Total number of chunks for an upload",
                    example="3",
                ),
                "chunk_size": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_FLOAT,
                    description="Size of current chunk in bytes",
                    example="18092",
                ),
                "file_name": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Original file name",
                    example="template_catalog.xls",
                ),
                "chunk_index": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Current chunk index. It ia the type str[int] ",
                    example="2",
                    format=openapi.FORMAT_INT64,
                ),
                "file": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="Excel file to upload (.xls or .xlsx). Note: Format .xlsx of file is uploading\
                                 not correctly!!\
                                 Note: This data can be to the form or body.",
                    example="\b'\x00\x00\xfd\x00\n\x00\t\x00\t\x00\x0f\x00,\x00'",
                    format=openapi.FORMAT_BINARY,
                ),
            },
            additional_properties=False,
        ),
        responses={
            200: openapi.Response(
                description="Got an intermediate chunk of file",
                examples={
                    "application/json": {"status": "uploading", "chunk_index": "2"}
                },
            ),
            201: openapi.Response(
                description="All chunks were sent and data were records in database.",
                examples={"application/json": {"success": "Ok"}},
            ),
            400: openapi.Response(
                description="Bad request. View a byte code.",
                examples={
                    "application/json": {"detail": "Missing < POSSIBLE LOCATION >"}
                },
            ),
            403: openapi.Response(
                description="Permission denied",
                examples={"application/json": {"detail": "Permission Denied"}},
            ),
            401: openapi.Response(description="Unauthorized"),
            500: openapi.Response(
                description="Server error",
                examples={"application/json": {"detail": "< TEXT_ERROR >"}},
            ),
        },
    )
    @action(
        detail=False,
        methods=["post"],
    )
    async def acreate(self, request, *args, **kwargs):
        """
        TODO: Put a signal for alert about loads file.
            xlsx - передача chunks - ломает файл.
            При этом старый файл передаётся без ошибок.
            Попробовать через кеш
        :param request:
        :param args: empty
        :param kwargs: empty
        :return:
        """
        log_t = "{}[{}]:".format(self.PREFIX_LOG[:-1], self.acreate.__name__)
        lock = asyncio.Lock()
        # ============================================
        # CHECKING PERMISSIONS
        # ============================================
        permission = CanLoadFilePermission()
        result_bool = await asyncio.to_thread(
            lambda: permission.has_permission(request, permission)
        )
        if request.method != "POST" or not result_bool:
            return JsonResponse(
                {"detail": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN
            )
        del result_bool
        # ============================================
        # GETTING DATA
        # ============================================
        post_data = (
            request.POST
            if (request.POST is not None and len(list(request.POST)) > 0)
            else request.data
        )
        post_files = request.FILES if request.FILES is not None else None
        file_name = post_data.get("file_name")
        count_str = post_data.get("total_chunks", "0")
        log.debug(
            "{} DEBUG count_str: {} Type: {}".format(
                log_t, str(count_str), type(count_str)
            )
        )
        total_chunks = int(
            math.floor(float(count_str))
            if "." in count_str and ".0" in count_str
            else math.ceil(float(count_str))
        )
        chunk_index = int(post_data.get("chunk_index", "0"))
        chunk_size = post_data.get("chunk_size", "1")
        # ============================================
        # BASIS CHECK OF THE RECEIVE FILE
        # ============================================

        log.debug(
            "{} DEBUG after post_data: {} ".format(
                log_t,
                str(post_data)[:50],
            )
        )
        log.debug(
            "{} DEBUG before post_files: {} & Mode bool: {}".format(
                log_t, post_files, bool(post_files)
            )
        )
        if not post_files:
            post_files = post_data.get("file")
        elif "file" in post_files:
            post_files = post_files.get("file")
        log.debug("{} DEBUG after post_files: {}".format(log_t, str(post_files)[:50]))
        post_files = (
            json.loads(post_files) if isinstance(post_files, str) else post_files
        )

        log.debug(
            "{} DEBUG after one_chunk: {} Type: {}".format(
                log_t,
                str(post_files)[:25] if post_files is not None else str(post_files),
                type(post_files),
            )
        )
        if post_files is None:
            return JsonResponse(
                {"detail": "Missing 'one_chunk'"}, status=status.HTTP_400_BAD_REQUEST
            )
        # --- Size & Name
        if not chunk_size or not file_name or not post_files:
            return await asyncio.to_thread(
                lambda: JsonResponse(
                    {
                        "detail": "Missing file: '{}' or filename: '{}', or size: '{}' of file".format(
                            post_files, file_name, chunk_index
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            )
        log.debug("{} DEBUG after they:  chunk_size: {}".format(log_t, chunk_size))
        # ============================================
        # REGEX TEMPLATE CHECKING
        # ============================================
        # --- Extension
        if not re.search(r"(\.xls|\.xlsx)$", file_name):
            return await asyncio.to_thread(
                lambda: JsonResponse(
                    {"detail": "Check your file. It need xls or xlsx"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            )
        log.debug("{} DEBUG after file_name: {}".format(log_t, file_name))

        # ============================================
        # COLLECTION OF TEMPS CHUNKS
        # Create files for the 'media/temp/chunked_uploads/<file_name.part<chunk_index>'
        # ============================================
        temp_dir = os.path.join(settings_first.MEDIA_ROOT, "temp", "chunked_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        chunk_path: str = os.path.join(str(temp_dir), f"{file_name}.part{chunk_index}")
        log.debug(
            "{} DEBUG after way to the temp chunks:  chunk_path: {}".format(
                log_t, chunk_path
            )
        )
        # ---
        async with lock:
            try:
                # ============================================
                # CHUNKS RECORDING TO THE FILE
                # ============================================
                log.debug(
                    "{} DEBUG before the chunks recording to the whole file under 'lock' mode. chunk_index: {}, total_chunks: {}".format(
                        log_t, chunk_index, total_chunks
                    )
                )
                if chunk_index < total_chunks:
                    log.debug(
                        "{} DEBUG before the record data in whole file. Index of chunk: {} \n \
                        chunk_path Type: {}, \n chunk_path: {} \n".format(
                            log_t,
                            chunk_index,
                            type(chunk_path),
                            str(chunk_path),
                        )
                    )
                    with open(str(chunk_path).replace("\\", "/"), "wb") as f:
                        log.debug(
                            "{} DEBUG type of 'chunk_part': {}".format(
                                log_t, type(post_files)
                            )
                        )
                        f.write(post_files)
                    log.debug(
                        "{} DEBUG after the record of while file. Chunk index: {} successfully!".format(
                            log_t, chunk_index
                        )
                    )
                else:
                    log.debug(
                        "{} Check of the chunks number! File did not was recorded in the whole file! Not success!"
                    )
                    return JsonResponse(
                        {
                            "detail": "Check of the chunks number. \
                    Count - chunk_index: {} & total_chunks: {}".format(
                                chunk_index, total_chunks
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except TypeError:
                try:
                    with open(str(chunk_path).replace("\\", "/"), "wb") as f:
                        for chunk_part in post_files.chunks():  # one_chunk.chunks()
                            log.debug(
                                "{} DEBUG type from chunks 'chunk_part': {}".format(
                                    log_t, type(chunk_part)
                                )
                            )
                            f.write(chunk_part)
                    log.debug(
                        "{} DEBUG after the record of while file. Chunk index: {} successfully!".format(
                            log_t, chunk_index
                        )
                    )
                except Exception as e:
                    return JsonResponse(
                        {"detail": list(e.args)[0] if e.args else str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            except Exception as e:
                return JsonResponse(
                    {"detail": list(e.args)[0] if e.args else str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            # ---
            try:
                if chunk_index == total_chunks - 1:
                    final_path: str = await self.record_to_whole_file(
                        temp_dir, total_chunks, file_name
                    )
                    await asyncio.sleep(0.7)
                    # ============================================
                    # CHECK FILE ON VALIDATION
                    # ============================================
                    is_valid, error_msq = self.validate_file(final_path)
                    log.debug(
                        "{} DEBUG is_valid: {}, error_msq: {}".format(
                            log_t, is_valid, error_msq
                        )
                    )
                    if not is_valid:
                        log.error(
                            "{} File validation failed: {}, error: {}".format(
                                log_t, final_path, error_msq
                            )
                        )
                        # Path(final_path).unlink(missing_ok=True)
                        return JsonResponse(
                            {"detail": "Invalid file format. {}".format(error_msq)},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    # ============================================
                    # RECORDING DATA IN DATABASE
                    # ============================================
                    log.debug(
                        "{} DEBUG RECORDING DATA IN DATABASE".format(
                            log_t,
                        )
                    )
                    task_saving_data_oFfile(file_name, request.user.id)
                    log.debug(
                        "{} DEBUG AFTER RECORDING DATA IN DATABASE".format(
                            log_t,
                        )
                    )
                    # ---
                    return JsonResponse(
                        {"success": "Ok"}, status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                return JsonResponse(
                    {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return JsonResponse(
            {
                "status": "uploading",
                "chunk_index": chunk_index,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    async def record_to_whole_file(
        path_dir: str, total_chunks: int, field_name: str
    ) -> str:
        """
        Static method for records the chunks to the whole file.
        :param str path_dir: Path name to the directory of the final one file.
        :param itn total_chunks: Count/number of chunks (total).
        :param str field_name: File name of the final file.
        :return: str path of the finale one file. It is a path where app will be to take the file for records data in database.
        """
        # ============================================
        # COLLECTING AT WHOLE FILE
        # ============================================
        final_dir = str(settings_first.MEDIA_ROOT) + "/documents"
        Path(final_dir).mkdir(parents=True, exist_ok=True)
        final_path = str(final_dir + "/" + field_name).replace("\\", "/")
        with open(final_path, "wb") as f:
            # That we take the chunks
            for i in range(0, total_chunks):
                part_path = os.path.join(path_dir, f"{field_name}.part{i}")
                try:
                    if not os.path.exists(part_path):
                        raise FileNotFoundError(f"Chunk {i} not found: {part_path}")

                    # That is we recording to the whole file.
                    with open(part_path.replace("\\", "/"), "rb") as part_file:
                        part_str = part_file.read()
                        f.write(part_str)
                    await asyncio.sleep(0.5)
                    Path(part_path).unlink()
                except Exception as e:
                    error_t = "{} File '{}'".format(
                        f"{field_name}.part{i}", list(e.args)[0] if e.args else str(e)
                    )
                    log.error(error_t)
                    raise FileNotFoundError(error_t) from e
            f.flush()
            os.fsync(f.fileno())
        return final_path

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
            file_size = Path(path).stat().st_size
            log.info("{} File size: {} bytes".format(log_t, file_size))
            if file_size == 0:
                return False, "File is empty after assembly"
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
                        log_t, list(e.args)[0] if len(e.args) else str(e)
                    )
                )

            except Exception as e:
                log.info(
                    "{} Error => {}".format(
                        log_t, list(e.args)[0] if len(e.args) else str(e)
                    )
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
                        log_t, list(e.args)[0] if len(e.args) else str(e)
                    )
                )
                return False, "Invalid Excel file."

            return False, "Not valid Excel file."
        except Exception as e:
            log.error(
                "{} Error =>  {}".format(
                    log_t, list(e.args)[0] if len(e.args) else str(e)
                )
            )
            return False
