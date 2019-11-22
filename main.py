from CorrespondencesGetter import getCorrespondences

folderUrl = 'Images/The White Building/'
img1_name = 'image1.png'
img2_name = 'image2.png'

x,y = getCorrespondences(folderUrl+img1_name,folderUrl+img2_name,5)
print(x)
print(y)