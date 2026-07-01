import asyncio
import os
import re
import tempfile

import pandas as pd
from adrf import serializers

# from rest_framework import status
from adrf.viewsets import ViewSet
from django.http import JsonResponse
from rest_framework import status

from catalog.models import ProductGalleryImageModel, ProductModel
from download.task_save_file import task_saving_data_oFfile

#
# class CatalogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductGalleryImageModel
#         fields = "__all__"


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductModel
#         fields = "__all__"


class CatalogViewSet(ViewSet):
    queryset = ProductGalleryImageModel.objects.all()

    async def create(self, request, *args, **kwargs):
        """
        TODO: Put a signal for alert about loads file.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        lock = asyncio.Lock()
        size_chunk = list(request.FILES.values())[0].DEFAULT_CHUNK_SIZE
        field_name = request.POST.get("file_name", "name_didnot_found")
        one_chunk = request.FILES.get("file")
        total_chunks = int(request.POST.get("total_chunks", "1"))
        chunk_index = int(request.POST.get("chunk_index", 0))
        # ---
        if not re.search(r"(\.xls|\.xlsx)$", field_name):
            return JsonResponse(
                {"error": "Check your file. It need xls or xlsx"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not size_chunk or not field_name or not one_chunk:
            return JsonResponse(
                {"error": "Missing file or filename"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # ---
        temp_dir = os.path.join(tempfile.gettempdir(), "chunked_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        chunk_path = os.path.join(temp_dir, f"{field_name}.part{chunk_index}")
        # ---
        async with lock:
            try:
                # ============================================
                # COLLECTING CHUNKS
                # ============================================
                if chunk_index < total_chunks:
                    with open(chunk_path, "wb") as f:
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
                    final_path = os.path.join(
                        temp_dir + "\\..\\..\\documents", field_name
                    )
                    with open(final_path, "wb") as f:
                        for i in range(total_chunks):
                            part_path = os.path.join(temp_dir, f"{field_name}.part{i}")
                            if not os.path.exists(part_path):
                                raise FileNotFoundError(
                                    f"Chunk {i} not found: {part_path}"
                                )
                            with open(part_path, "rb") as part_file:

                                f.write(part_file.read())
                            os.remove(part_path)
                        task_saving_data_oFfile(field_name)
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


# async def list(self, request):
#     data_dict = dict
#     queryset_items = await asyncio.to_thread(lambda : list(ProductGalleryImageModel.objects.all()))
#
#     serializer = await asyncio.to_thread(lambda : CatalogSerializer(queryset_items, many=True))
#     for item in list(serializer.data):
#         product_list = await asyncio.to_thread(lambda pk=item["product_id"]: list(ProductModel.objects.filter(pk = item["product"])), item["product_id"])
#         serializer_list = []
#         for product in product_list:
#             result_dict = await asyncio.to_thread(lambda : ProductSerializer(product))
#             serializer_list.append(result_dict)
#         item["product"] = serializer_list


# def create(self, request, *args, **kwargs):
#     serializer = CatalogSerializer(data=request.data)
#     return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
