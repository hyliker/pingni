# Create your views here.

def get_check_code_image(request,image= MEDIA_ROOT + 'img/checkcode3.png', fontfile=MEDIA_ROOT + "thirdparty/LiHeiPro.ttf"):    
    from datetime import datetime
    import md5, cStringIO
    import Image, ImageDraw, ImageFont, random    
    im = Image.open(image)    
    draw = ImageDraw.Draw(im)    
    mp = md5.new()    
    mp_src = mp.update(str(datetime.now()))    
    mp_src = mp.hexdigest()    
    rand_str = mp_src[0:4]      
    draw.text((10,10), rand_str[0], font=ImageFont.truetype(fontfile, random.randrange(30,50)))    
    draw.text((48,10), rand_str[1], font=ImageFont.truetype(fontfile, random.randrange(30,50)))    
    draw.text((85,10), rand_str[2], font=ImageFont.truetype(fontfile, random.randrange(30,50)))    
    draw.text((120,10), rand_str[3], font=ImageFont.truetype(fontfile, random.randrange(30,50)))    
    del draw    
    request.session['checkcode'] = rand_str    
    buf = cStringIO.StringIO()    
    im.save(buf, 'gif')    
    return HttpResponse(buf.getvalue(),'image/gif') 
