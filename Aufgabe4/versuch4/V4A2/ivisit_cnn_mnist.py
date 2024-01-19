# coding: utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# act_keras_new

# (i) define IVIST GUI elements

#@IVISIT:SIMULATION & simRL1

#@IVISIT:DICTSLIDER & Network-Parameters  & [200,20,-1,2,10] & par_Network & 0
#@IVISIT:DICTSLIDERITEM  & num_filters    & [1, 50, 2,1]     & num_filters  & int & 8
#@IVISIT:DICTSLIDERITEM  & filter_size    & [1, 15, 2,2]     & filter_size  & int & 3
#@IVISIT:DICTSLIDERITEM  & pool_size      & [1, 10, 2,1]     & pool_size    & int & 2

#@IVISIT:DICTSLIDER & Training-Parameters & [200,20,-1,2,10] & par_Training & 0
#@IVISIT:DICTSLIDERITEM  & batch_size     & [1,60000, 2,1]             & batch_size    & int & 500 
#@IVISIT:DICTSLIDERITEM  & epochs         & [1, 100, 2,1]              & epochs        & int & 5 
#@IVISIT:DICTSLIDERITEM  & learning_rate  & [0.000001, 10, 2,0.000001] & learning_rate & float & 0.001
#@IVISIT:DICTSLIDERITEM  & beta_1         & [0.000001, 1 , 2,0.000001] & beta_1        & float & 0.9
#@IVISIT:DICTSLIDERITEM  & beta_2         & [0.000001, 1 , 2,0.000001] & beta_2        & float & 0.999

#@IVISIT:DICTSLIDER & Drawing-Parameters  & [200,20,-1,2,10]    & par_Drawing & 0
#@IVISIT:DICTSLIDERITEM  & linewidth      & [1, 5, 2, 1]        & linewidth   & int   & 1
#@IVISIT:DICTSLIDERITEM  & linecolor      & [0, 255, 2,1]       & linecolor   & int   & 255
#@IVISIT:DICTSLIDERITEM  & shiftx         & [-15, 15, 2,1]      & shiftx      & int   & 0
#@IVISIT:DICTSLIDERITEM  & shifty         & [-15, 15, 2,1]      & shifty      & int   & 0
#@IVISIT:DICTSLIDERITEM  & scale          & [0.5, 2.0, 2,0.1]   & scale       & float & 1.0
#@IVISIT:DICTSLIDERITEM  & rotate         & [-180,180, 2,1]     & rotate      & float & 0
#@IVISIT:DICTSLIDERITEM  & p_noise        & [0  , 1  , 2,0.001] & p_noise     & float & 0
#@IVISIT:DICTSLIDERITEM  & sig_noise      & [0  , 100, 2,0.1]   & sig_noise   & float & 1

#@IVISIT:SLIDER  & idx_image        & [150,1] & [0,69999, 2,1] & idx_image        & -1 & int & 0 
#@IVISIT:SLIDER  & scale_image      & [150,1] & [1,20   , 2,1] & scale_image      & -1 & int & 0 
#@IVISIT:SLIDER  & filter_img_class & [150,1] & [-1,9   , 2,1] & filter_img_class & -1 & int & -1 

#@IVISIT:LISTSEL & Image Source & [20,5] & [ALL,TRAIN_DATA,TEST_DATA] & str_image_source & -1 & string & ALL

#IVISIT:CHECKBOX & select_image_from & [ALL,TRAIN,TEST,BBBBB,CCC,DDDDD] & dummystr & 0110

#@IVISIT:RADIOBUTTON & Input Source & [image,new_input] & str_input_source & image

#@IVISIT:BUTTON  & bt_build        & [<,BUILD NETWORK]   & bt_build
#@IVISIT:BUTTON  & bt_compile      & [<,COMPILE NETWORK] & bt_compile
#@IVISIT:BUTTON  & bt_train        & [<,TRAIN NETWORK]   & bt_train

#@IVISIT:BUTTON  & bt_newimg_erase & [<,ERASE_NEWIMAGE]  & bt_newimg_erase
#@IVISIT:BUTTON  & bt_newimg_copy  & [<,COPY_NEWIMAGE]   & bt_newimg_copy
#@IVISIT:BUTTON  & bt_newimg_add   & [<,ADD_NEWIMAGE]    & bt_newimg_add

#@IVISIT:IMAGE      & image               & 1.0     & [0,255]  & im_image         & int
#@IVISIT:IMAGE      & new input           & 1.0     & [0,255]  & im_input_new     & int
#@IVISIT:IMAGE      & network outputs     & 1.0     & [0,255]  & im_outputs       & int
#@IVISIT:TEXT_OUT   & Results             & [20,7] & just_left & txt_results 



import cv2
import numpy as np
import matplotlib
from copy import copy
import os
import threading   # for locks
import tkinter
import time

import tensorflow as tf
import datetime
import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.utils import to_categorical

import ivisit as iv
from ivisit.matplotlib import *
from supy.utilities import *
from supy.computervision import *

#from libRL_GridWorld import *

fontsz=16
matplotlib.rc('xtick', labelsize=fontsz)
matplotlib.rc('ytick', labelsize=fontsz)
matplotlib.rc('font', family='serif')
matplotlib.rc('text', usetex=True)

# (ii) define parameter variables to be controlled by IVISIT
class SimParameters(iv.IVisit_Parameters):
    idx_image    = 0                                                                                 # index of image to be displayed
    scale_image  = 5                                                                                 # scale factor for increasing size of image
    filter_img_class = -1                                                                            # filter for one particular class (-1 means all classes)
    par_Network  = {'num_filters':8, 'filter_size':3, 'pool_size':2}                                 # parameters for compiling CNN
    par_Training = {'batch_size':500, 'epochs':5, 'learning_rate':0.001,'beta_1':0.9,'beta_2':0.999} # parameters for training (ADAM + policy agent)
    par_Drawing  = {'linewidth':1, 'linecolor':255, 'shiftx':0,'shifty':0,'scale':1.0,'rotate':0.0,'p_noise':0,'sig_noise':1.} # parameters for drawing new image 
    bt_build    = '0'                                                                                # if '1' (button pressed) then build neural network using current Network Parameters
    bt_compile  = '0'                                                                                # if '1' (button pressed) then compile neural network using current Network Parameters
    bt_train    = '0'                                                                                # if '1' (button pressed) then train neural network 
    bt_evaluate = '0'                                                                                # if '1' (button pressed) then evaluate neural network using test data
    bt_newimg_erase = '0'                                                                            # if '1' then erase new image
    bt_newimg_copy  = '0'                                                                            # if '1' then copy image to new_image
    bt_newimg_add   = '0'                                                                            # if '1' then add image to new_image
    str_image_source='ALL'                                                                           # where select image from
    str_input_source='image'
    
# (iii) define simulation data to be displayed by IVISIT
class SimData(iv.IVisit_Data):
    txt_results  = ''                        # text output showing selected results
    im_image     = np.array([[0,0,0]])       # Input Image
    im_input_new = np.array([[0,0,0]])       # New Input Image
    im_outputs   = np.array([[0,0,0]])       # output distribution (class probabilitites) as image (with bars)

# (iv) define IVISIT simulation 
class Sim(iv.IVisit_Simulation):
    def __init__(self,name_arg="ivisit_cnn_mnist.py"):
        iv.IVisit_Simulation.__init__(self,name_arg,SimParameters,SimData)
        self.nsteps=0                                  # step counter
        self.state,self.clicked_x, self.clicked_y='idle',-1,-1           # clicked coordinates of new input 
        self.im_new_input_canvas=None
        self.im_input_new=np.zeros((28,28),'uint8')    # new input image (for drawing over GUI)      
        self.lock = threading.Lock()
        self.init()

    def init(self):
        self.model = None           # neural network model
        self.flagCompiled=0         # if >0 then model is compiled
        self.flagTrained=0          # if >0 then model is trained
        self.acc=[]
        self.loss=[]
        self.val_acc=[]
        self.val_loss=[]
        
    def bind(self,parent=None,display=None):  # parent is typcially the ivisit object (having a display object where to bind to)
        if parent!=None: self.parent=parent
        if display==None: display=self.display
        if display==None and self.parent!=None: display=parent.display
        if display!=None:
            self.im_new_input_canvas=display.bind2Widget("new input","<Button-1>"       ,self.onPressedB1_newinput,"imgcanvas")
            self.im_new_input_canvas=display.bind2Widget("new input","<B1-Motion>"      ,self.onMotionB1_newinput ,"imgcanvas")
            self.im_new_input_canvas=display.bind2Widget("new input","<ButtonRelease-1>",self.onReleaseB1_newinput,"imgcanvas")
            self.display=display     # store reference to display for later manipulations etc.

    def onPressedB1_newinput(self,event):
        p=SimParameters
        self.lock.acquire()
        self.state,self.clicked_x, self.clicked_y = 'pressed', event.x, event.y
        self.lock.release()
        self.onMotionB1_newinput(event)

    def onMotionB1_newinput(self,event):
        p=SimParameters
        if self.state=='pressed':
            self.lock.acquire()
            x1,y1=round(self.clicked_x/p.scale_image),round(self.clicked_y/p.scale_image)
            self.clicked_x,self.clicked_y=event.x,event.y
            x2,y2=round(self.clicked_x/p.scale_image),round(self.clicked_y/p.scale_image)
            cv2.line(self.im_input_new,(x1,y1),(x2,y2),p.par_Drawing['linecolor'],int(p.par_Drawing['linewidth']))
            self.lock.release()

    def onReleaseB1_newinput(self,event):
        if self.state=='pressed':
            self.lock.acquire()
            self.state='idle'
            self.lock.release()
        
    def step(self):
        # (i) some preparations and extracting parameters
        self.nsteps=self.nsteps+1
        p = SimParameters     # short hand to simulation parameters
        d = SimData           # short hand to simulation data arrays

        # (ii) display selected image (and new input)
        s=p.str_image_source+'_'+str(p.filter_img_class)
        idx_list=dict_img_idx[p.str_image_source+'_'+str(p.filter_img_class)]      # get index list for images to select from
        idx_img = idx_list[p.idx_image%len(idx_list)]
        if idx_img>=60000:
            im=test_images[(idx_img-60000)%10000]     # get test image
            im_cls=test_labels[(idx_img-60000)%10000] # corresponding label
        else:
            im=train_images[idx_img%60000]            # get train image
            im_cls=train_labels[idx_img%60000]        # corresponding label
        d.im_image=getInt8Image(im.reshape((28,28)))
        newsize=(d.im_image.shape[1]*p.scale_image,d.im_image.shape[0]*p.scale_image) # scaled image size
        if p.scale_image>1:
            d.im_image=cv2.resize(d.im_image,newsize,interpolation=cv2.INTER_NEAREST)

        # (iii) draw new input image
        # (iii.1) check action buttons
        if p.bt_newimg_erase=='1': self.im_input_new[:,:]=0
        if p.bt_newimg_copy=='1': self.im_input_new[:,:]=getInt8Image(im.reshape((28,28)))
        if p.bt_newimg_add=='1': self.im_input_new[:,:]=np.minimum(self.im_input_new+getInt8Image(im.reshape((28,28))),255)
        im_inp_new=np.array(self.im_input_new)
        # (iii.1) do rotation
        if p.par_Drawing['rotate']!=0:
            im_inp_new=scipy.ndimage.rotate(im_inp_new,p.par_Drawing['rotate'], reshape=False, mode='constant', cval=0, prefilter=True)
        # (iii.2) do scaling
        if p.par_Drawing['scale']!=1.0:
            new_sz=(round(im_inp_new.shape[1]*p.par_Drawing['scale']),round(im_inp_new.shape[0]*p.par_Drawing['scale'])) # scaled image size
            im_inp_new=cv2.resize(self.im_input_new,new_sz,interpolation=cv2.INTER_NEAREST)
            if p.par_Drawing['scale']>1.0:
                pad=(new_sz[0]-28)//2
                im_inp_new=im_inp_new[pad:(pad+28),pad:(pad+28)]   # take central part of enlarger image
            else:
                pad=(28-new_sz[0])//2
                im_empty=np.zeros((28,28),'uint8')
                im_empty[pad:(pad+new_sz[1]),pad:(pad+new_sz[0])]=im_inp_new
                im_inp_new=im_empty
        # (iii.3) do shifting
        if p.par_Drawing['shiftx']!=0: im_inp_new=np.roll(im_inp_new,p.par_Drawing['shiftx'],1)
        if p.par_Drawing['shifty']!=0: im_inp_new=np.roll(im_inp_new,p.par_Drawing['shifty'],0)
        # (iii.4) add noise
        if p.par_Drawing['p_noise']>0:
            mask_noise=np.zeros((28,28),'uint8')                             # init with zeros
            mask_noise[np.random.rand(28,28)<p.par_Drawing['p_noise']]=1   # set random pixels
            rnd_val=np.random.normal(p.par_Drawing['linecolor'],p.par_Drawing['sig_noise'],(28,28))
            im_new=np.maximum(np.minimum(np.round(im_inp_new+np.multiply(mask_noise,rnd_val)),255),0)
            im_inp_new=np.array(im_new,'uint8')
            print("im_new=",im_inp_new)
        d.im_input_new=cv2.resize(im_inp_new,newsize,interpolation=cv2.INTER_NEAREST)   # scale to display size
        #d.im_input_new=cv2.resize(self.im_input_new,newsize,interpolation=cv2.INTER_NEAREST)   # scale to display size
        #print("self.im_input_new=",self.im_input_new)
        
        # (iii) (re-) build neural network?
        if p.bt_build=='1':
            print("building network")
            self.model = Sequential([
                Conv2D(p.par_Network['num_filters'], p.par_Network['filter_size'], input_shape=(28, 28, 1), name='layers_conv'),
                MaxPooling2D(pool_size=p.par_Network['pool_size'],name='layers_maxpool'),
                Flatten(name='layers_flatten'),
                Dense(10, activation='softmax',name='layers_dense'),
            ])
            self.flagCompile=0
            self.flagTrain=0

        # (iv) (re-) compile neural network
        if p.bt_compile=='1' and not self.model is None:
            print("compiling network")
            self.optimizer=tf.keras.optimizers.Adam(
                learning_rate=p.par_Training['learning_rate'],
                beta_1=p.par_Training['beta_1'],
                beta_2=p.par_Training['beta_2']
            )
            self.model.compile(
                optimizer=self.optimizer,
                loss='categorical_crossentropy',
                metrics=['accuracy'],
            )
            self.flagCompiled=1

        # (v) (re-) train neural network
        if p.bt_train=='1' and self.flagCompiled>0:
            print("training network")
            fun_scheduler = lambda epoch,lr: p.par_Training['learning_rate'] # scheduler function for updating learning rate (cannot directly be modified in optimizer)
            res=self.model.fit(
                train_images,
                to_categorical(train_labels),
                batch_size=p.par_Training['batch_size'],
                epochs=p.par_Training['epochs'],
                validation_data=(test_images, to_categorical(test_labels)),
                callbacks=[tf.keras.callbacks.LearningRateScheduler(fun_scheduler)]   # callbacks will be called at end of each epoch 
            )
            self.flagTrain=1
            print("res=",res.history.keys())
            self.acc     +=res.history['accuracy']
            self.loss    +=res.history['loss']
            self.val_acc +=res.history['val_accuracy']
            self.val_loss+=res.history['val_loss']

        # (vi) classify current image (or new input image)
        if p.str_input_source=='new_input': im=(im_inp_new/255) - 0.5 
        if self.flagCompiled>0:
            y = self.model.predict(im.reshape((1,28,28,1)))[0] # predict class probabilities of current image im
        else:
            y = np.zeros(10)
        y_hat=np.argmax(y)
        #print("y=",y,"predicted class y_hat=",y_hat,"actual class t=",im_cls)
        dx,pad,szy=10,10,50    # dx=width of bar; pad=spacing between bars; szy=height of image 
        szx=10*(dx+pad)+pad    # width of image
        d.im_outputs=255*np.ones((szy,szx,3),'uint8')  # allocate white RGB image (for displaying class distribution)
        if y_hat==im_cls: col=(0,255,0)      # color green if predicted class is correct
        else: col=(255,0,0)                  # color red if class is wrong
        for c in range(10): cv2.rectangle(d.im_outputs,(pad+c*(dx+pad),szy-pad),((c+1)*(dx+pad),pad+int((1-y[c])*(szy-2*pad))),col,3)  # draw bar for class c

        # (vii) text output
        if len(self.acc)>0: acc,loss,val_acc,val_loss=self.acc[-1],self.loss[-1],self.val_acc[-1],self.val_loss[-1]
        else: acc,loss,val_acc,val_loss=None,None,None,None
        d.txt_results='trained '+str(len(self.acc))+' epochs:\n'
        d.txt_results+='train       data: acc='+str(acc)+'; loss='+str(loss)+'\n'
        d.txt_results+='validation  data: acc='+str(val_acc)+'; loss='+str(val_loss)+'\n'
        d.txt_results+='current input:\n'
        d.txt_results+='idx_img='+str(idx_img)+'; predicted class y_hat='+str(y_hat)+'; target class t='+str(im_cls)+'\n'
            
        return
        
        # (ii) read in image
        #filename = 'fig19_GridWorld_RL.png'           # filename of image
        #d.im_gridworld = cv2.imread(filename, cv2.IMREAD_COLOR) # read in color image
        d.im_gridworld = np.array(im_gridworld) #cv2.imread(filename, cv2.IMREAD_UNCHANGED) # read in color image

        # (iii) do one step
        # (iii.1) get current state and handle reincarnation
        s=self.s                          # current state
        if p.bt_reincarnate=='1': s='s0'  # manual reincarnation: go to birth state
        if not s in [s_heaven,s_hell]:    # end state?
            self.flagEndState=0           # current state is not an end state
        else:                             # else current state is end state
            if self.flagEndState<=0:      # if last state was not an end state? 
                self.flagEndState=1       # then just entered heaven/hell --> set end state flag...
                self.countEndState=0      # ... and initialize counter
            else:
                self.countEndState+=1     # else last state was already an end state --> just increase counter
            if (p.str_reincarnation_mode=='auto_immediately' and self.countEndState>= 0) or \
               (p.str_reincarnation_mode=='auto_10steps'     and self.countEndState>=10):
                s='s0'                    # automatic reincaration
                self.flagEndState=0
                
        # (iii.1) select action a
        if p.str_agent=='RandomAgent':
            a=agentRandom.chooseAction(s)
        elif p.str_agent=='GoodAgent':
            a=goodAgent.chooseAction(s,p.par_PolicyAg['pRand'])
        elif p.str_agent=='EvilAgent':
            a=evilAgent.chooseAction(s,p.par_PolicyAg['pRand'])
        elif p.str_agent=='QLearningAgent':
            a=agentQ.chooseAction(s,p.par_QLearnAg['pRand'])
        else:
            assert 0,"unknown agent str_agent="+str(str_agent)
        # (iii.2) perform action a in GridWorld environment
        s_,r=gw.doAction(s,a)
        self.r_list[self.r_list_pos]=r                           # update reward list (to compute moving average)
        self.r_list_pos=(self.r_list_pos+1)%len(self.r_list)     # update position pointer
        # (iii.3) do learning
        if p.str_agent=='QLearningAgent':
            agentQ.learn(s,a,r,s_)
        str_lastmove="("+str(s)+","+str(a)+")-->"+str(s_)+" with r="+str(r)
        #print("t="+str(t)+": ("+str(s0)+","+str(a0)+")-->"+str(s)+" with r="+str(r))
        self.s=s_

        # (iv) do visualizations
        # (iv.1) draw state transitions as red rectangles
        x,y=gw.getPosition(s)
        x_,y_=gw.getPosition(s_)
        r,r_=int(fac_resize*35),int(fac_resize*50)
        d.im_gridworld=cv2.rectangle(d.im_gridworld, (int(x -r),int(y -r)), (int(x +r),int(y +r)), (255,50,50), 2)
        d.im_gridworld=cv2.rectangle(d.im_gridworld, (int(x_-r_),int(y_-r_)), (int(x_+r_),int(y_+r_)), (255,0,0), 3)
        d.im_gridworld=cv2.line(d.im_gridworld, (int(x),int(y)), (int(x_),int(y_)), (255,50,50), 2)
        # (iv.2) policy images
        d.im_pi_Random=getInt8Image(agentRandom.pi)
        d.im_pi_GoodPolicy=getInt8Image(goodAgent.pi)
        d.im_pi_EvilPolicy=getInt8Image(evilAgent.pi)
        d.im_Q_Values =getInt8Image(agentQ.Q)
        Q=agentQ.Q
        Qnorm=(Q.T-np.min(Q,axis=1)).T
        s=np.sum(Qnorm,axis=1)
        s=np.maximum(s,gw.eps)
        Qnorm=np.divide(Qnorm.T,s).T
        d.im_Q_Values_norm=getInt8Image(Qnorm)
        fac_upsample=8                                                                       # upsampling factor
        sizex_new,sizey_new=fac_upsample*d.im_pi_Random.shape[1],fac_upsample*d.im_pi_Random.shape[0]  # new image sizes
        d.im_pi_Random =cv2.resize(d.im_pi_Random,(sizex_new,sizey_new),interpolation=cv2.INTER_NEAREST)   # upsampling
        d.im_pi_GoodPolicy =cv2.resize(d.im_pi_GoodPolicy,(sizex_new,sizey_new),interpolation=cv2.INTER_NEAREST)   # upsampling
        d.im_pi_EvilPolicy =cv2.resize(d.im_pi_EvilPolicy,(sizex_new,sizey_new),interpolation=cv2.INTER_NEAREST)   # upsampling
        d.im_Q_Values  =cv2.resize(d.im_Q_Values,(sizex_new,sizey_new),interpolation=cv2.INTER_NEAREST)    # upsampling
        d.im_Q_Values_norm=cv2.resize(d.im_Q_Values_norm,(sizex_new,sizey_new),interpolation=cv2.INTER_NEAREST)    # upsampling
        # (iv.3) text outputs
        d.txt_results="Last move: "+str_lastmove+"\n"
        d.txt_results+="mean(r)="+str(np.mean(self.r_list))+" (averaged over last "+str(len(self.r_list))+" steps)\n"
        
        # (iv) delay
        if p.delay_ms>0: time.sleep(p.delay_ms/1000.)


# ***********************************
# ***********************************
# main program
# ***********************************
# ***********************************

# load mnist data 
train_images = mnist.train_images()
train_labels = mnist.train_labels()
test_images = mnist.test_images()
test_labels = mnist.test_labels()

# Normalize the images.
train_images = (train_images / 255) - 0.5
test_images = (test_images / 255) - 0.5

# Reshape the images.
train_images = np.expand_dims(train_images, axis=3)
test_images = np.expand_dims(test_images, axis=3)

# create some indexes (for easy selection of images); indexes >=60000 are test images
dict_img_idx={}
dict_img_idx['ALL_-1'       ]=list(range(70000))
dict_img_idx['TRAIN_DATA_-1']=list(range(60000))
dict_img_idx['TEST_DATA_-1' ]=[i+60000 for i in range(10000)]
for c in range(10):
    idx_c_train = [i       for i in range(60000) if train_labels[i]==c]    # indexes of training images of class c
    idx_c_test  = [i+60000 for i in range(10000) if test_labels [i]==c]    # indexes of test images of class c 
    dict_img_idx['ALL_'  +str(c)]=idx_c_train+idx_c_test
    dict_img_idx['TRAIN_DATA_'+str(c)]=idx_c_train
    dict_img_idx['TEST_DATA_' +str(c)]=idx_c_test
    
sim=Sim()
sim.main_init()
#sim.init()
#sim.step()

iv.IVisit_main(sim=sim)
