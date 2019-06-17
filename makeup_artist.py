from PIL import Image
import random
from similarity import Similarity

ikon_categories={
0:'pessimistic',
1:'surprised',
2:'sad',
3:'grin',
4:'LeftO',
5:'RightO',
6:'calm',
7:'hang'
}


class Makeup_artist(object):
    def __init__(self):
        self.faces={}
        self.similarity=Similarity()
        self.bling=Image.open('images/'+'bling.png').resize((50,50))
        for i in ikon_categories.keys():
            self.faces[i]=Image.open('images/'+ikon_categories[i]+'.png').resize((60,60))
    def apply_makeup(self, img, ikon, volume):
        print("volume: {}".format(volume))
        width, height= img.size
        score=0
        img=img.transpose(Image.FLIP_LEFT_RIGHT)

        step=width//200
        if  len(ikon)==0:
            for c in range(1,4):
                ikon[c]=[0,0]
                current_step=0
        for c in ikon.keys(): #c:channel
            face, current_step=ikon[c]
            if current_step is 0:
                current_step+=1
                face=random.randint(0,7)
                ikon[c][0]=face
                img.paste(self.faces[face],(step*current_step,(c-1)*height//3),self.faces[face])
            elif current_step<200:
                if face==7:
                    if volume>80:
                        result=7
                    else:
                        result=-1
                else:
                    result=self.similarity.face_dance(img,[face])
                print(result,face)
                if result!=face:
                    current_step+=1
                    img.paste(self.faces[face],(step*current_step,(c-1)*height//3),self.faces[face])
                else:
                    img.paste(self.bling,(step*current_step,(c-1)*height//3),self.bling)
                    current_step=0
            else:
                if face==7:
                    if volume>80:
                        result=7
                    else:
                        result=-1
                else:
                    result=self.similarity.face_dance(img,[face])
                if result==face:
                    img.paste(self.bling,(step*current_step,(c-1)*height//3),self.bling)
                current_step=0
            ikon[c][1]=current_step
        return img, ikon

if __name__=='__main__':
    art=Makeup_artist()
    ikon={}
    img=Image.open('images/'+'sad.png').resize((500,200))
    img,ikon=art.apply_makeup(img,ikon)
    print(img)
