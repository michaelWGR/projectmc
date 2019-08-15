# -*- coding: utf-8 -*-
import qrcode
qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
content = '###      ###                                                    \n\n                             #'

qr.add_data(content)
qr.make(fit=True)

img = qr.make_image(fill_color="white", back_color="black")
print img
img.save('qrcode.jpeg')