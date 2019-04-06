------------------------------
Face Annotations
------------------------------
Updated July 15, 2015

Each of the 2,222 target face photos was manually annotated by two annotators for 77 different key landmark points, including the shape of the head, eyes, eyebrows, nose, and mouth. These can be used as ground-truth labels for active appearance models or other face recognition / manipulation applications.

**Cite these two papers if using these annotations:**

Bainbridge, W. A., Isola, P., & Oliva, A. (2013). The Intrinsic Memorability of Face Photographs. Journal of Experimental Psychology: General, 142(4), 1323 - 1334.

Khosla, A., Bainbridge, W.A., Torralba, A., & Oliva, A. (2013). Modifying the memorability of face photographs. Proceedings of the International Conference on Computer Vision (ICCV), Sydney, Australia.

------------------------------
Contents:

Images and Annotations
A folder containing JPEGs of the 2,222 target images (labeled by target ID #) and corresponding text files containing the pixel coordinates for the 77 landmarks. They are ordered as follows:
	Lines 1-8: Left eyebrow
	Lines 9-24: Face shape
	Lines 25-32: Right eyebrow
	Lines 33-45: Nose
	Lines 46-53: Left eye
	Lines 54-61: Right eye
	Lines 62-70: Upper lip
	Lines 71-77: Bottom lip

example-annotation.jpg
A JPEG image showing an example of where the 77 landmark points are located on a face.

checkAnnotation.m
A simple MATLAB script that will visualize the landmark points of an inputted image.

