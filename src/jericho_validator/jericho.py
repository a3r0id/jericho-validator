import base64
from PIL import Image
from io import BytesIO
import string

class Jericho:
    
    class JerichoUtils:
        bytes10MB = 10485760
        
        extensionConversions = [
            ["PNG", "png"],
            ["JPG", "jpg"],
            ["JPEG", "jpeg"],
            ["GIF", "gif"],
            ["BMP", "bmp"],
            ["ICO", "ico"],
            ["TIFF", "tiff"],
            ["TIF", "tif"],
            ["WEBP", "webp"]]
        
        imageFormats = [
            ['data:image/jpeg;base64,', 'jpeg'],
            ['data:image/jpg;base64,', 'jpg'],
            ['data:image/png;base64,', 'png'],
            ['data:image/gif;base64,', 'gif'],
            ['data:image/bmp;base64,', 'bmp'],
            ['data:image/tiff;base64,', 'tiff'],
            ['data:image/webp;base64,', 'webp']]    
        
        def checkUrl(b64Url):
            thisFormat = None
            for format in Jericho.JerichoUtils.imageFormats:
                if b64Url.startswith(format[0]):
                    thisFormat = format
                    break
                
            if thisFormat is not None:
                b64 = None
                try:
                    b64 = b64Url.split(thisFormat[0])[1]
                except:
                    return None
                
                if len(b64) > 0:
                    return dict(
                        formatPrefix  = thisFormat[0],
                        extension     = thisFormat[1],
                        base64        = b64
                    )
                else:
                    return None
            
            raise Jericho.Exceptions.UnsupportedImageType("Image type not supported")
        
    class Exceptions:
        
        class ImageTooLarge(Exception):
            pass
        
        class EmptyFileName(Exception):
            pass
        
        class UnsupportedImageType(Exception):
            pass

    class ValidB64Image(object):
        """
        ## object
        
        - `self.b64` (str) - Base64 encoded image
        - `self.extension` (str) - Image extension
        - `self.formatPrefix` (str) - Image format prefix
        - `self.filename` (str) - Image filename
        - `self.bytes` (bytes) - Image bytes
        - `self.image` (PIL.Image) - Image object
        - `self.isValid` (bool) - Image is valid
        - `self.store` (str) - Image store
        - `self.sizeBytes` (int) - Image size in bytes
        - `self.dimensions` (list) - Image dimensions
        
        """
        def __init__(self, checked_url, filename):
            super().__init__()
            self.b64              = checked_url['base64'] 
            self.extension        = checked_url['extension']
            self.formatPrefix     = checked_url['formatPrefix']
            self.filename         = filename
            self.bytes            = None
            self.image            = None
            self.isValid          = False
            self.store            = None
            self.sizeBytes        = None    
            self.dimensions       = []
            
    class InvalidB64Url(Exception):
        def __init__(self):
            super().__init__()  
            self.isValid          = False      
                
    def jericho(b64Url, filename="image", maxSize=JerichoUtils.bytes10MB):
        """
        ### Checks if the given data URL is a valid image, returns ValidB64Image object if so else returns InvalidB64Url.
        --------------------------------------------------------------------------------------------------------------------
        ### Arguments:
        - `b64Url`: Base64 encoded image url. `(str)`
        - `filename`: Filename to save the image as, if not provided, file will be name "image.{valid extension}". `(str)`
        - `maxSize`: Max image size allowed, in bytes. Default: 10MB `(int)`
        --------------------------------------------------------------------------------------------------------------------
        ### Returns:
        `(ValidB64Image)` or `(InvalidB64Url)`
        --------------------------------------------------------------------------------------------------------------------
        ### Supported formats:
        - jpeg/jpg
        - png
        - gif
        - bmp
        - tiff
        - webp
        """
            
        # Check max size
        sizeBytes_ = (len(b64Url) * 3) / 4
        if maxSize is not None:
            if sizeBytes_ > maxSize:
                raise Jericho.Exceptions.ImageTooLarge("Encoded image exceeds max size")
        
        # Check integrity of filename
        if '.' in filename:
            filename = filename.split('.')[0]
            
        if len(filename) == 0:
            raise Jericho.Exceptions.EmptyFileName("Empty filename")
        
        # Validate filename characters
        filename = ''.join(x for x in filename if x in string.printable)
        
        # Initialize with an invalid imageObject
        vector     = Jericho.InvalidB64Url()
        
        # Check integrity of data URL
        checkedUrl = Jericho.JerichoUtils.checkUrl(b64Url)
        
        # if the data URL is valid, return a ValidB64Image object and populate it with the valid data
        if checkedUrl is not None:
            vector = Jericho.ValidB64Image(checkedUrl, filename)
            
            try:
                
                # Attempt to decode the base64 string into bytes then into a PIL image
                image_         = Image.open(BytesIO(base64.b64decode(vector.b64)))
                
                # Format detected by pillow
                actual_format_ = image_.format
                
                # Size detected by pillow
                actual_size_   = image_.size
                
                # Convert back to bytes buffer
                buffer_ = BytesIO()
                
                # Save the image to the buffer
                image_.save(buffer_, save_all=True, format=actual_format_)
                
                # Get the raw bytes of the valid pillow image
                bytes_ = buffer_.getvalue()
                
                # Ensure the image url's extension matches the image's format
                validExtension = False
                for conversion in Jericho.JerichoUtils.extensionConversions:
                    if conversion[0] == actual_format_:
                        if conversion[1] == vector.extension:
                            validExtension = True
                            break
                    
                if not validExtension:
                    return Jericho.InvalidB64Url()
                    
                
                ### Final Product/s ###
                
                # Valid pillow image bytes
                vector.bytes        = bytes_
                
                # Valid pillow image size
                vector.sizeBytes    = len(bytes_)
                
                # Valid pillow image dimensions
                vector.dimensions   = actual_size_
                
                # Valid pillow image object
                vector.image        = image_
                
                # Valid pillow image base64 string (for saving)
                vector.b64          = base64.b64encode(buffer_.getvalue()).decode('utf-8')
                
                # Validated filename (for saving)
                vector.filename     = filename + "." + vector.extension
                
                # A database-friendly object for saving to a database
                vector.store        = dict(
                b64                 = vector.formatPrefix + vector.b64,
                filename            = vector.filename,
                dimensions          = vector.dimensions
                )
                
                # Boolean indicating if the image is valid
                vector.isValid = True
                
            except Exception as e:
                print(e)
                # Invalid pillow image bytes, something went wrong or the image is invalid/corrupt
                vector.isValid = False
                
        return vector
            
            

            
            
            
        
        
        