import io, math
from PIL import Image, ImageOps
from django.core.files.base import ContentFile


def compress_any_image(uploaded_file, max_bytes=1_000_000, min_quality=25):
    """
    Takes any uploaded image (PNG, JPG, HEIC, etc) and compresses to <= max_bytes (default 1 MB).
    Preserves transparency (converts to WebP), else saves as JPEG.
    Returns a ContentFile ready for ImageField.
    """
    uploaded_file.open("rb")
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)   # fix orientation

    # detect transparency
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

    target_fmt = "WEBP" if has_alpha else "JPEG"
    if target_fmt == "JPEG":
        img = img.convert("RGB")

    # binary search quality
    low, high = min_quality, 95
    best_bytes = None
    while low <= high:
        mid = (low + high) // 2
        buf = io.BytesIO()
        img.save(buf, format=target_fmt, optimize=True, quality=mid)
        size = buf.tell()

        if size <= max_bytes:
            best_bytes = buf.getvalue()
            low = mid + 1  # try better quality
        else:
            high = mid - 1

    # if still None, resize
    if not best_bytes:
        w, h = img.size
        scale = math.sqrt(max_bytes / buf.tell())  # approximate shrink
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        img = img.resize(new_size, Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format=target_fmt, optimize=True, quality=min_quality)
        best_bytes = buf.getvalue()

    # prepare file name
    base_name = getattr(uploaded_file, "name", "upload")
    ext = "webp" if target_fmt == "WEBP" else "jpg"
    if "." in base_name:
        base_name = base_name.rsplit(".", 1)[0]
    return ContentFile(best_bytes, name=f"{base_name}.{ext}")


# class UserProfile(models.Model):
#     avatar = models.ImageField(upload_to="avatars/")
#     name = models.CharField(max_length=120)
#
#     def save(self, *args, **kwargs):
#         if self.avatar and self.avatar.size > 1_000_000:  # > 1MB
#             self.avatar = compress_any_image(self.avatar, max_bytes=1_000_000)
#         super().save(*args, **kwargs)
