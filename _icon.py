from PIL import Image
src = r'C:\Users\VOS-User\.dsh\attachments\v1\objects\87\8791ab8551f242efe7543fef4cc7299db702311d078de4c2f92672d2671cdf46'
pub = r'C:\Users\VOS-User\Documents\deepseek-harness\default-workspace\bs-docs\site\docs\.vuepress\public'
im = Image.open(src).convert('RGBA')
print('src', im.size, im.mode)
# 判断有无透明像素
a = im.getchannel('A')
print('alpha min/max', a.getextrema())
def square(img, size, resample):
    w, h = img.size
    scale = size / max(w, h)
    nw, nh = max(1, round(w*scale)), max(1, round(h*scale))
    r = img.resize((nw, nh), resample)
    canvas = Image.new('RGBA', (size, size), (0,0,0,0))
    canvas.paste(r, ((size-nw)//2, (size-nh)//2), r)
    return canvas
im512 = square(im, 512, Image.NEAREST)
im512.save(pub + r'\logo.png')
square(im, 180, Image.LANCZOS).save(pub + r'\apple-touch-icon.png')
square(im, 32, Image.LANCZOS).save(pub + r'\favicon-32.png')
print('written logo/apple/favicon')
