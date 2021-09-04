# JLP 2021/09/04
# To a future self that ever revisits this code:
#
# This script takes a landscape PDF where there are actually 2 pages side-by-side within 1 PDF page.
# It splits the left & right side pages and writes it into a new PDF.
# The new pages are saved into a split/ folder in the working directory.
#
# In my PDF reader, the original PDF appeared as landscape, but the coordinate system was still based on portrait style.  This caused a bit of head scratching at first.  Perhaps the drawing below will help.
#
#   (0,792)                (612,792)
# (UpperLeft)            (UpperRight)
#      |----------------------|
#      |                      |
#      |       Original       |
#      |      Even Page       |
#      |  (also would appear  |
#      |   sideways in this   |
#      |         view)        |
#      |                      |
#      |   -   -   -   -   -  |
#      |                      |
#      |       Original       |
#      |       Odd Page       |
#      |     (Tilt head to    |
#      |   LEFT to view in    |
#      |  proper orientation) |
#      |                      |
#      |----------------------|
# (LowerLeft)            (LowerRight)
# (x,y) = (0,0)            (612,0)

from PyPDF2 import PdfFileWriter, PdfFileReader
import copy
import sys

def main():
    if len(sys.argv) < 2:
        print("Filename argument required!  Quitting.")
        quit()
    inputName = sys.argv[1]

    output = PdfFileWriter()
    input1 = PdfFileReader(open(inputName, "rb"))

    numPages = input1.getNumPages()
    for n in range(numPages):
        print("Separating page " + str(n))

#        # add the left page
        currPageLeft = copy.copy(input1.getPage(n))

#       Before crop
#        print(currPageLeft.mediaBox.upperLeft)
#        print(currPageLeft.mediaBox.upperRight)
#        print(currPageLeft.mediaBox.lowerLeft)
#        print(currPageLeft.mediaBox.lowerRight)

        currPageLeft.mediaBox.upperRight = (
                currPageLeft.mediaBox.getUpperRight_x() ,
                currPageLeft.mediaBox.getUpperRight_y() / 2)
        currPageLeft.mediaBox.lowerRight = (
                currPageLeft.mediaBox.getLowerRight_x() ,
                currPageLeft.mediaBox.getLowerRight_y() / 2)
        output.addPage(currPageLeft)

#       After crop
#        print(currPageLeft.mediaBox.upperLeft)
#        print(currPageLeft.mediaBox.upperRight)
#        print(currPageLeft.mediaBox.lowerLeft)
#        print(currPageLeft.mediaBox.lowerRight)

        currPageRight = input1.getPage(n)
        currPageRight.mediaBox.lowerLeft = (
                currPageRight.mediaBox.getUpperLeft_x() ,
                currPageRight.mediaBox.getUpperLeft_y() / 2)
        currPageRight.mediaBox.lowerRight = (
                currPageRight.mediaBox.getLowerRight_x() ,
                currPageRight.mediaBox.getUpperLeft_y() / 2)
        output.addPage(currPageRight)



#   JLP: Example code from the github page
#
#    # add page 1 from input1 to output document, unchanged
#    output.addPage(input1.getPage(0))
#    
#    # add page 2 from input1, but rotated clockwise 90 degrees
#    output.addPage(input1.getPage(1).rotateClockwise(90))
#    
#    # add page 3 from input1, rotated the other way:
#    output.addPage(input1.getPage(2).rotateCounterClockwise(90))
#    # alt: output.addPage(input1.getPage(2).rotateClockwise(270))
#    
#    ## add page 4 from input1, but first add a watermark from another pdf:
#    #page4 = input1.getPage(3)
#    #watermark = PdfFileReader(open("watermark.pdf", "rb"))
#    #page4.mergePage(watermark.getPage(0))
#    
#    # add page 5 from input1, but crop it to half size:
#    page5 = input1.getPage(4)
#    page5.mediaBox.upperRight = (
#        page5.mediaBox.getUpperRight_x() / 2,
#        page5.mediaBox.getUpperRight_y() / 2
#    )
#    output.addPage(page5)
#    
#    # print how many pages input1 has:
#    print("document1.pdf has %s pages." % input1.getNumPages())
    
    # finally, write "output" to PDF
    outputStream = open("split/" + inputName, "wb")
    output.write(outputStream)

if __name__ == "__main__":
    main()
