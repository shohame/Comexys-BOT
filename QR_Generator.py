import pandas as pd
import numpy as np
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
        code += ',' + str(l['Frequency MHz'])
        code += ',' + str(l['RF Channel'])
        code += ',' + str(l['RF Number'])
        code += ',' + str(l['Mac Address'])
        code += ',' + l['Production date']

        remarks = l['Remarks']
        if isinstance(remarks, float) and np.isnan(remarks):
            remarks = ''
        code += ',' + str(remarks)

        qrcode = pyqrcode.create(code)
        qrcode.png('img.png')

        plt.subplot(10, 8, i)
        img = mpimg.imread('img.png')
        plt.imshow(img, cmap='gray')
        plt.title('Comexys-'+str(l['RF Number']), y=0.9, fontsize=8)
        plt.axis('off')
        i = i + 1

    fig.tight_layout()

    pp.savefig(fig)
    pp.close()



if __name__=='__main__':
    QR_Generator("QR_Code_generator.csv")