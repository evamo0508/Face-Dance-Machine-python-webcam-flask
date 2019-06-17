import cv2
import time
import dlib
import numpy as np
from imutils import face_utils

#=============================================
#----No.----|------facial expression------|
#    0          pessimistic

class Similarity():

    def __init__(self):
        # initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
        #print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("landmarks.dat")
        self.fa = face_utils.FaceAligner(self.predictor, desiredFaceWidth=256)

    def Frown(self, landmark):
        result=False
        similarity=0
        diff_l=landmark[37:40,1]-landmark[19:22,1]
        diff_r=landmark[42:45,1]-landmark[22:25,1]
        eye_dis=landmark[42,0]-landmark[39,0]
        eyebrow_dis=landmark[22,0]-landmark[21,0]

        if np.argmin(diff_l)==2 and np.argmin(diff_r)==0 and np.argmax(diff_l)==0 and np.argmax(diff_r)==2 :
            if np.argmax(landmark[19:22,1])==2 and np.argmax(landmark[22:25,1])==0:
                if eyebrow_dis/eye_dis<0.7:
                    result=True
                    similarity=(1-eyebrow_dis/eye_dis)*1.5

        #print("Frown:",similarity)
        return result,similarity

    def RightEyeWink(self, landmark):
        result=False
        similarity=0
        l=np.sum(landmark[40:42,1])-np.sum(landmark[37:39,1])
        r=np.sum(landmark[46:48,1])-np.sum(landmark[43:45,1])
        diff=np.sum(landmark[22:27,1])-np.sum(landmark[17:22,1])
        #slope_r=abs((landmark[24,1]-landmark[22,1])/(landmark[24,0]-landmark[22,0]))
        #slope_l=abs((landmark[19,1]-landmark[21,1])/(landmark[19,0]-landmark[21,0]))
        #print("r",r)
        #print("l",l)
        #print("diff",diff)
        if r<l or diff>0:
            result=True
            similarity=1
        #print("RightEyeWink:",similarity)
        return result,similarity

    def MouthOpen(self, landmark):
        result=False
        similarity=0
        upperlip=landmark[62,1]-landmark[51,1]
        height=landmark[66,1]-landmark[62,1]
        if height>upperlip:
            result=True
            similarity=1
        #print("MouthOpen:",similarity)
        return result,similarity

    def MouthClosed(self, landmark):
        close=np.sum(landmark[65:68,1])-np.sum(landmark[61:64,1])
        height=landmark[62,1]-landmark[51,1]
        result=False
        if close<=height:
            similarity=1
            result=True
        else:
            similarity=0
        ##print (close,height)
        #print("MouthClosed:",similarity)
        return result,similarity

    def MouthRight(self, landmark):
        middle_x=landmark[27,0]
        mouth_x=landmark[48:68,0]
        dis=mouth_x-middle_x
        result=False
        negative=[d for d in dis if d<0]
        if len(negative)<9:
            similarity=1-len(negative)/20*0.5
            result=True
        else:
            similarity=0
        #print("MouthRight:", similarity)
        return result,similarity

    def MouthLeft(self, landmark):
        middle_x=landmark[27,0]
        mouth_x=landmark[48:68,0]
        dis=mouth_x-middle_x
        result=False
        negative=[d for d in dis if d>0]
        if len(negative)<9:
            similarity=1-len(negative)/20*0.5
            result=True
        else:
            similarity=0
        #print("MouthLeft:", similarity)
        return result,similarity

    def Smile(self, landmark):
        result=False
        similarity=0
        h=(np.mean(landmark[60:65,1])+landmark[48,1]+landmark[54,1])/3
        mouth=np.amax(landmark[48:68,1])-np.amin(landmark[48:68,1])
        if landmark[48,1]<h and landmark[54,1]<h:
            similarity=0.8+0.2*(h-(landmark[48,1]+landmark[54,1])/2)/mouth
            result=True
        #print("Smile:",similarity)
        return result,similarity

    def PointDown(self, landmark):
        result=False
        similarity=0
        h=(np.mean(landmark[64:68,1])+landmark[60,1])/2
        mouth=np.amax(landmark[48:68,1])-np.amin(landmark[48:68,1])
        if landmark[48,1]>h and landmark[54,1]>h:
            result=True
            similarity=0.8+0.2*((landmark[48,1]+landmark[54,1])/2-h)/mouth
        #print("PointDown:",similarity)
        return result,similarity

    def MouthOval(self, landmark):
        result=False
        similarity=0
        height=landmark[57,1]-landmark[51,1]
        width=landmark[54,0]-landmark[48,0]
        if abs(height/width)>1:
            result=True
            similarity=1

        #print("MouthOval:",similarity)
        return result,similarity

    def MouthCircle(self, landmark):
        result=False
        similarity=0
        height=landmark[57,1]-landmark[51,1]
        width=landmark[54,0]-landmark[48,0]
        if abs(height/width-1)<0.5:
            result=True
            similarity=1-abs(height/width-1)*0.5

        #print("MouthCircle:",similarity)
        return result,similarity

    def MouthWide(self, landmark):
        result=False
        similarity=0
        height=landmark[57,1]-landmark[51,1]
        width=landmark[54,0]-landmark[48,0]
        if width/height>1:
            result=True
            similarity=0.8+0.2*width/height*0.3

        #print("WideMouth:",similarity)
        return result,similarity

    def FaceLeft(self, landmark):
        result=False
        similarity=0
        L_len=landmark[27,0]-landmark[0,0]
        R_len=landmark[16,0]-landmark[28,0]
        if R_len/L_len>1.5:
            result=True
            similarity=1

        #print("FaceLeft:",similarity)
        return result,similarity

    def FaceRight(self, landmark):
        result=False
        similarity=0
        L_len=landmark[27,0]-landmark[0,0]
        R_len=landmark[16,0]-landmark[28,0]
        if L_len/R_len>1.5:
            result=True
            similarity=1

        #print("FaceRight:",similarity)
        return result,similarity

    #compare ordered face
    def face_dance(self, target, face_mission):
        gray=cv2.cvtColor(np.array(target.convert('RGB')), cv2.COLOR_RGB2GRAY)
        start = time.time()
        rects = self.detector(gray, 0)
        #print("face_dance takes: ", 1000*(time.time()-start))
        try:
            shape = self.predictor(gray, rects[0])
            shape = face_utils.shape_to_np(shape)
        except:
            return -1,0
        result = -1
        similarity = 0
        for mission in face_mission:

            if mission==0:
                #print("==========pessimistic==========")
                #pessimistic
                mouth_left, left_score=self.MouthLeft(shape)
                mouth_closed, closed_score=self.MouthClosed(shape)
                smile, smile_score=self.Smile(shape)
                if mouth_left and mouth_closed and not smile:
                    similarity=(left_score*0.5+closed_score*0.5)
                    #print(similarity)
                    result = 0
                    break

            elif mission==1:
                #print("==========surprised==========")
                #surprised
                mouth_open, open_score=self.MouthOpen(shape)
                frown,frown_score=self.Frown(shape)
                mouth_O,O_score=self.MouthCircle(shape)
                mouth_oval,oval_score=self.MouthOval(shape)
                mouth_left, left_score=self.MouthLeft(shape)
                if mouth_open and not frown:
                    if mouth_O or mouth_oval:
                        similarity=open_score*0.3+(max(oval_score,O_score))*0.7
                        #print(similarity)
                        result = 1
                        break


            elif mission==2:
                #print("==========sadness==========")
                #sadness
                pointDown, pointDown_score=self.PointDown(shape)
                if pointDown :
                    similarity=pointDown_score
                    #print(similarity)
                    result = 3
                    break

            elif mission==3:
                #print("==========grin==========")
                #grin
                smile, smile_score=self.Smile(shape)
                mouth_open, open_score=self.MouthOpen(shape)
                if mouth_open and smile:
                    similarity=smile_score*0.7+mouth_open*0.3
                    #print(similarity)
                    result = 4
                    break


            elif mission==4:
                #LeftO
                #print("==========LeftO==========")
                frown,frown_score=self.Frown(shape)
                mouth_left, left_score=self.MouthLeft(shape)
                mouth_O,O_score=self.MouthCircle(shape)
                face_left, face_score=self.FaceLeft(shape)
                if not frown and mouth_left and mouth_O and face_left:
                    similarity=left_score*0.5+O_score*0.5
                    #print(similarity)
                    result = 6
                    break

            elif mission==5:
                #RightO
                #print("==========RightO==========")
                frown,frown_score=self.Frown(shape)
                mouth_Right, Right_score=self.MouthRight(shape)
                mouth_O,O_score=self.MouthCircle(shape)
                face_Right, face_score=self.FaceRight(shape)
                if not frown and mouth_Right and mouth_O and face_Right:
                    similarity=Right_score*0.5+O_score*0.5
                    #print(similarity)
                    result = 7
                    break


            elif mission==6:
                #print("==========calm==========")
                mouth_closed, closed_score=self.MouthClosed(shape)
                smile, smile_score=self.Smile(shape)
                pointDown, pointDown_score=self.PointDown(shape)
                frown,frown_score=self.Frown(shape)
                if mouth_closed and not smile and not pointDown and not frown:
                    similarity=1
                    #print(similarity)
                    result = 9
                    break

        return result
