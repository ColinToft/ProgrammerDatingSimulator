from ui import *
from objc_util import *
from ctypes_patch import make_callback_returnable

#try:
	#ProgressBar = ObjCClass('UIProgressBar')
#except:

def trackRectForBounds_(_self, _cmd, bounds):
	sliderClass = ObjCClass('UISlider')
	s = ObjCInstance(_self)
	
	sliderBounds = ObjCInstance(_self).bounds()
	
	slider = sliderClass.alloc().initWithFrame_(sliderBounds)
	
	newBounds = slider.trackRectForBounds_(bounds)
	newBounds.size.height = 40
	return newBounds

fancyCGRect = make_callback_returnable(CGRect)
trackRectForBounds_.restype = fancyCGRect
trackRectForBounds_.argtypes = [fancyCGRect]

methods = [trackRectForBounds_]
ProgressBar = create_objc_class('UIProgressBar', ObjCClass('UISlider'), methods=methods)


class MainView (View):
	def __init__(self, *args, **kwargs):
		super().__init__(self, *args, **kwargs)
		w = get_screen_size().w
		h = get_screen_size().h
		
		self.update_interval = 1 / 60
		self.shows_result = False
		self.bounds = (0, 0, 400, 400)
		self.background_color = 'white'
		
		self.optionButtons = []
		self.optionNames = ['Flirt', 'Chat', 'Items', 'Run']
		for i in range(4):
			b = Button(title=self.optionNames[i], background_color=(0.8, 0.8, 0.8))
			self.optionButtons.append(b)
			self.add_subview(b)
		
		SLIDER_PADDING = w * 0.03
		SLIDER_HEIGHT = h * 0.01
		SLIDER_Y = h * 0.03
		BUTTON_HEIGHT = h * 0.22
		BUTTON_WIDTH = w * 0.44
		BUTTON_TOP_Y = h * 0.42
		BUTTON_Y_PADDING = h * 0.02
		
		
		frame = CGRect(CGPoint(SLIDER_PADDING, SLIDER_Y), CGSize(w - SLIDER_PADDING * 2, SLIDER_HEIGHT))
		self.confidenceMeter = ProgressBar.alloc().initWithFrame_(frame)
		self.confidenceMeter.setThumbImage_forState_(0, ObjCClass('UIImage'))
		self.confidenceMeter.userInteractionEnabled = False
		
		#self.add_subview(self.confidenceMeterOld)
		self_objc = ObjCInstance(self)
		self_objc.addSubview_(self.confidenceMeter)
		
		buttonXPadding = (w - BUTTON_WIDTH * 2) / 3
		for i, ob in enumerate(self.optionButtons):
			ob.frame = Rect(buttonXPadding + (buttonXPadding + BUTTON_WIDTH) * (i % 2), BUTTON_TOP_Y + (BUTTON_HEIGHT + BUTTON_Y_PADDING) * (i // 2), BUTTON_WIDTH, BUTTON_HEIGHT)
			
		
	def update(self):
		v = self.confidenceMeter.value()
		self.confidenceMeter.value = 0.87
		
def main():
	v = MainView()
	v.present('sheet', hide_title_bar=True, hide_close_button=True)
	
if __name__ == '__main__':
	main()
