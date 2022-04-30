import pandas as pd
import numpy as np
import pyqrcode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import os
from PIL import Image
from zebra import Zebra

def QR_Generator_to_PDF(csv_file_path):
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


def QR_Generator_Zebra_Print(csv_file_path):



    df = pd.read_csv(csv_file_path, skipinitialspace=True)

    fig = plt.figure(figsize=(1.5, 1.5), dpi=640)

    q = 'ZDesigner GX430t'
    z = Zebra(q)
    z.reset_default()

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

    #    plt.subplot(10, 8, i)
        img = mpimg.imread('img.png')
        plt.imshow(img, cmap='gray')
        plt.title('Comexys', y=0.88, fontsize=11,fontweight="bold")
        rfn = str(l["RF Number"])
   #     plt.show()
        plt.axis('off')
        plt.text(-2, 38,f'RF - {rfn}', rotation=90, fontsize=11, fontweight="bold")
        i = i + 1
        fig.tight_layout()
        fn = os.path.join('img2.png')
        fig.savefig(fn)
        img = Image.open(fn)
        img=img.convert('1')
        fn_pcx = fn+'.pcx'
        img.save(fn_pcx)
        fig.clear()
#######################################################################
#        queues = z.getqueues()
#        print(queues)
#        z.print_config_label()

        z.setup(direct_thermal=True, label_height=(240, 24), label_width=504)
        img = Image.open(fn_pcx)
        img = img.crop((100, 90, 800, 804))
        w, h = img.size
        dst = Image.new('1', (w + w + 128, h), color=1)  # , color=(255,255,255))
        dst.paste(img, (0, 0))
        dst.paste(img, (w + 128, 0))
        img = dst
        img = img.resize((216 * 2 + 40, 216))
#        img.show()
        w, h = img.size
        data = img.tobytes()
        z.print_graphic(20, 0, w, h, data, 1)


if __name__=='__main__':
#    QR_Generator_to_PDF("QR_Code_generator.csv")

#   QR_Generator_test("QR_Code_generator.csv")
   QR_Generator_Zebra_Print("QR_Code_generator.csv")
