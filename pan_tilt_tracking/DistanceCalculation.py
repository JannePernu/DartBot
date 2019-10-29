import tyres as ty

def DistanceCalculation(w, dX):
  float sPos = kit.servo[1].angle
  
  while sPos > 0:
    ty.vasemmalle()
			
  while sPos < 0:
    ty.oikealle()
  
  while dX > w:
    ty.eteen()
   
  while dX < w:
    ty.taakse()
