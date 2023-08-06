## dsa_reg

This package approximately computes the offsets needed to register DSA (Digital Slide Archive) item thumbnails.



## Installations
__Through pypi package__
``` Shell
$ pip install dsa-reg
```

__From Source__
``` Shell
$ git clone git@github.com:mmasoud1/dsa_reg.git

```

## Usage
After the package is installed, main operation can be performed as follows:

__Register by Thumbnails__
``` Python
from dsa_reg import rigidRegByThumb

#param refItemId (string): ref image Id 
#param targetItemId (string): target image Id
#param xBaseUrl (string): DSA Server URL e.g. https://styx.neurology.emory.edu/girder/api/v1
#param xAuthentication: boolean (0,1)  
#param xEnhancement: boolean (0,1)  
#return (Dict): homography metrix, psnr, x offset, y offset, horizontal scaleX, vertical  scaleY

rigidRegByThumb(refItemId, targetItemId, xBaseUrl)

# e.g. 
rigidRegByThumb(refItemId = "5e361da534679044bda81b16", 
	            targetItemId = "5e361-SOME-OTHER-ID", 
	            xBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1")



# if using a private DSA collection,  set xAuthentication = 1 to provide login credentials:

rigidRegByThumb(refItemId = "5e361da534679044bda81b16", 
	            targetItemId = "5e361-SOME-OTHER-ID", 
	            xBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1", 
	            xAuthentication = 1, 
	            xEnhancement = 0)

# If a preprocessing is needed such that the tile needs enhancement before registration, set xEnhancement boolean value to 1

```


__Register by Magnification__
``` Python
from dsa_reg import rigidRegByMagnification

rigidRegByMagnification(refItemId, targetItemId, xBaseUrl)

#e.g. 
rigidRegByMagnification(refItemId = "5e361da534679044bda81b16", 
			            targetItemId = "5e361-SOME-OTHER-ID", 
			            xBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1")

# magnification default value is 1



rigidRegByMagnification(refItemId, targetItemId, xBaseUrl, magnification,  xAuthentication)
# magnification can be smaller value < = 1 for fast processing and wise resources use

rigidRegByMagnification(refItemId, targetItemId, xBaseUrl, magnification,  xAuthentication, xEnhancement)

#e.g. 
rigidRegByMagnification(refItemId = "5e361da534679044bda81b16", 
			            targetItemId = "5e361-SOME-OTHER-ID", 
			            xBaseUrl = "https://styx.neurology.emory.edu/girder/api/v1",
			            magnification = 0.5,
			            xAuthentication = 1,
			            xEnhancement = 1)

```

## For contributing, issues and suggestions
Your contribution to enhance the registration technique is welcomed, please start by new issue or  pull a request.


### Next:
1. This is a demo of initial and approximated rigid registration results, the target is to extend the functionality to whole slide images registration in fast, accurate mode.