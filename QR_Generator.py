import cv2
import pandas as pd
import numpy as np
from pyzbar import pyzbar
import pyqrcode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

def QR_Generator(csv_file_path):
    pp = PdfPages('QR_Codes.pdf')

    df = pd.read_csv(csv_file_path, skipinitialspace=True)

    fig = plt.figure(figsize=(8.27, 11.69), dpi=640)

    i = 1
    for l in df.iterrows():
        l = l[1]
        code = l['Producer']
        code += ',' + l['Product Name']
        code += ',' + str(l['RF Number'])
        code += ',' + str(l['Mac Address'])
        code += ',' + str(l['RF Channel'])
        code += ',' + l['Production date']

        remarks = l['Remarks']
        if isinstance(remarks, float) and np.isnan(remarks):
            remarks = ''
        code += ',' + str(remarks)

        qrcode = pyqrcode.create('code')
        qrcode.png('img.png')

        plt.subplot(15, 12, i)
        img = mpimg.imread('img.png')
        plt.imshow(img, cmap='gray')
        plt.title(str(l['Mac Address']), y=0.8, fontsize=6)
        plt.axis('off')
        i = i + 1

    fig.tight_layout()

    pp.savefig(fig)
    pp.close()



if __name__=='__main__':
    QR_Generator("QR_Code_generator.csv")