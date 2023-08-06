import cv2
from keras.models import model_from_json
from license_recog.utils import *
import os
import statistics

class LP_Detector():
	def __init__(self,config):
		self.model_plate = None
		self.model_ocr = None
		
		self.ocr_classes = None
		self.config = config

		self.load_model_plate()
		self.load_model_ocr()


	def load_model_plate(self):

		model_path = self.config['model1']['path']

		with tf.device('/cpu:0'):
		    model_path = os.path.splitext(model_path)[0]
		    with open('%s.json' % model_path,'r') as json_file:
		    	model_json = json_file.read()
		    
		    self.model_plate = model_from_json(model_json, custom_objects={})
		    self.model_plate.load_weights('%s.h5' % model_path)

	def load_model_ocr(self):
		model_config = self.config['model2']['config']
		model_weight = self.config['model2']['weight']
		model_classes = self.config['model2']['classes']

		with open(model_classes, 'rt') as f:
		    self.ocr_classes = f.read().rstrip('\n').split('\n')

		self.model_ocr = cv2.dnn.readNetFromDarknet(model_config, model_weight)
		self.model_ocr.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		self.model_ocr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


	def get_plate(self,input,resized,origin):
		output = self.model_plate.predict(input)
		output 		= np.squeeze(output)

		Llp,LlpImgs,is_square_list = postprocess_plate(origin,resized,output)

		if len(LlpImgs):
			Ilp = LlpImgs[0]
			Ilp = cv2.cvtColor(Ilp, cv2.COLOR_BGR2GRAY)
			Ilp = cv2.cvtColor(Ilp, cv2.COLOR_GRAY2BGR)
			res_img = (Ilp*255.).astype(np.uint8)
			is_square = is_square_list[0]

			LlpImgs.pop(0)

			return res_img, is_square

		return None, None

	def get_number(self,image):

		H, W = image.shape[:2]

		# Create a 4D blob from a image.
		blob = cv2.dnn.blobFromImage(image, 1/255, (W, H), [0,0,0], 1, crop=False)

		# Sets the input to the network
		self.model_ocr.setInput(blob)

		# Runs the forward pass to get output of the output layers
		outs = self.model_ocr.forward(getOutputsNames(self.model_ocr))

		# Remove the bounding boxes with low confidence
		res = postprocess_ocr(image, outs,self.ocr_classes,0.2,0.1)

		if len(res) <= 0:
			return ""

		L = dknet_label_conversion(res, W, H)
		L = nms(L,.45)

		# Compute the average height
		heights = [l.wh()[1] for l in L]
		avg_H = statistics.mean(heights)

		# Sort letters by coordinate 'top'
		L.sort(key=lambda x: x.tl()[1])

		# Group the letters into rows
		groups = do_grouping(L,bias=avg_H/2)

		# For each row, we sort letters from left to right
		lp_str = ''
		for g in groups:
		    g.sort(key=lambda x: x.tl()[0])
		    temp_str = ''.join([chr(l.cl()) for l in g])
		    lp_str = lp_str + temp_str + ' '
		
		return lp_str


