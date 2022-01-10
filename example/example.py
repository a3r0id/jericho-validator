from jericho_validator import Jericho

with open('example.png.b64') as f:
    data = f.read()
    
try:
    
    # Check the data URL (image)
    j = Jericho.jericho(data)

except Jericho.Exceptions.ImageTooLarge:
    print('Image is too large.')

except Jericho.Exceptions.EmptyFileName:
    print('File name is empty.')
    
except Jericho.Exceptions.UnsupportedImageType:
    print('Image type not supported.')

except Exception as e:
    print(e)
    
if j.isValid:
    print('Image is valid.')
    print('Image size in bytes: ' + str(j.sizeBytes))
    print('Image dimensions: ' + str(j.dimensions))
    print('Image filename: ' + j.filename)
    print('Image extension: ' + j.extension)
    print('Image format prefix: ' + j.formatPrefix)
    
else:
    print('Image is invalid.')





