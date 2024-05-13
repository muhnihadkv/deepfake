from django.shortcuts import render
import subprocess
from website.ImageForgeryDetection.FakeImageDetector import FID
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.

infoDict = {}
fileurl = ''
inputImageUrl = ''
result = {}
inputImage = ''

def index(request):
    return render(request, "index.html")


def image(request):
    return render(request, "image.html")


def contact(request):
    return render(request, "contact.html")


def getMetadata(path):
    global infoDict
    imgPath = path
    exeProcess = "hachoir-metadata"
    process = subprocess.Popen([exeProcess, imgPath],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               universal_newlines=True)
    
    for tag in process.stdout:
        line = tag.strip().split(':')
        infoDict[line[0].strip()] = line[-1].strip()
    for k, v in infoDict.items():
        print(k, ':', v)
    if "Metadata" in infoDict.keys():
        del infoDict["Metadata"]


def runAnalysis(request):
    global fileurl, inputImageUrl, result, infoDict,inputImage
    
    if request.POST.get('run'):
        inputImage=''
        if inputImageUrl=='' or 'input_image' in request.FILES:
            inputImg = request.FILES['input_image'] if 'input_image' in request.FILES else None
            if inputImg:
                fs = FileSystemStorage()
                file = fs.save(inputImg.name, inputImg)
                fileurl = os.getcwd() +fs.url(file)
                inputImageUrl = '../media/' + inputImg.name
        elif inputImageUrl!='':
            fileurl = os.getcwd() + '/media/' + os.path.basename(inputImageUrl)

        getMetadata(fileurl)
        print('fileurl---------------------------',fileurl)
        res = FID().predict_result(fileurl)

        if res[0] == 'Authentic':
            result = {'type': res[0], 'confidence': res[1]}
            inputImage=inputImageUrl
            inputImageUrl=''

            return render(request, "image.html",
                          {'result': result, 'input_image':inputImage, 'metadata': infoDict.items()})
        
        elif res[0] == 'Forged':
            result = {'type': res[0], 'confidence': res[1]}
            inputImage=inputImageUrl
            inputImageUrl=''
            return render(request, "image.html",
                            {'result': result, 'input_image': inputImage, 'metadata': infoDict.items()})


def getImages(request):
    global fileurl, inputImageUrl, result,inputImage
    outputImageUrl = "../media/tempresaved.jpg"
    
    if request.POST.get('ela'):
        FID().show_ela(fileurl)

        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})
    
    if request.POST.get('edge_map'):
        FID().detect_edges(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})
    
    if request.POST.get('na'):
        
        FID().apply_na(fileurl)
        return render(request, "image.html", {'url': outputImageUrl, 'input_image': inputImage, 'result': result,
                                              'metadata': infoDict.items()})