#Roshan Kalghatgi
#Quadratic Equation solver July 2020
#Inputs: ax^2 + bx + c, input a,b,c

import math

class quadsolver: 
    
    def __init__(self,a1,b1,c1):
    
        self.a = a1
        self.b = b1
        self.c = c1
    
    def solve(self): 
    
        #return both roots
        a = self.a
        b = self.b
        c = self.c
        
        #evaluate the determinent
        det = (b ** 2) - (4 * a * c)
    
        if det >= 0: 
            x1 = -b + math.sqrt(det)
    
            x1 = round(1.0 * x1 / (2 * a), 2)
    
            x2 = -b - math.sqrt(det)
    
            x2 = round(1.0 * x2 / (2 * a), 2)
    
        if det < 0: 
            #use complex
            #print ('det < 0')
            x1 = complex((-b/(2 * a)), round(-math.sqrt(-det)/ (2 * a),2))
            x2 = complex((-b/(2 * a)), round(math.sqrt(-det)/ (2 * a),2))
        
        self.x1 = x1
        self.x2 = x2

