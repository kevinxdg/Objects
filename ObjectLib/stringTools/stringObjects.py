#coding=utf-8

class stringTool():
    def __init__(self, str_value='') -> None:
        self._string = str_value
        
    @property
    def string(self):
        return self._string
    
    @string.setter
    def string(self, value):
        self._string = value
        
    @property
    def length(self):
        return len(self._string)
        
    def find_decimal(self, s_start=0, s_end = -1):
        if s_end == -1:
            s_end = self.length
            
        if self.length==0:
            return [s_start, -1, 0]
        elif s_start >= self.length:
            return [s_start, -1, 0]
        elif s_start >= s_end:
            return [s_start, -1, 0]
        else:
            is_chars = True
            while(s_end > s_start and is_chars):
                tmp_str = self._string[s_start:s_end]
                if tmp_str.isdecimal():
                    is_chars = False
                else:
                    s_end = s_end - 1
            if is_chars:
                return [s_start, -1, 0]
            else:
                return [s_start, s_end, int(tmp_str)]
            
    def find_all_decimals(self, s_start=0, s_end = -1):        
        new_start = s_start
        if s_end == -1:
            s_end = self.length
        data = []
        while (new_start < s_end) :
            [s, e, d] = self.find_decimal(new_start)
            if e >= s:
                data.append([s, e, d])
                new_start = e + 1
            else:
                new_start = new_start + 1
        return data
    
    def find_float(self, s_start=0, s_end = -1):
        if s_end ==-1:
            s_end = self.length
        [s, e, d] = self.find_decimal(s_start=s_start, s_end=s_end)
        if e > s and e < s_end - 1:
            chr = self.string[e]
            new_start = e + 1
            if chr == '.':                    
                [s1, e1, d1] = self.find_decimal(new_start, s_end=s_end)
                if e1 > s1:                        
                    for i in range(e1-s1):
                        d1 = d1 / 10.0
                    new_data = d + d1                    
                    return([s, e1, new_data])
        return [s_start, -1, 0]
               
    def find_all_floats(self, s_start = 0, s_end = -1):
        if s_end ==-1:
            s_end = self.length
        new_start = s_start
        data = []
        while (new_start < s_end) :
            [s, e, d] = self.find_float(s_start=new_start, s_end=s_end)
            if e > s:
                data.append([s, e, d])
                new_start = e + 1
            else:
                new_start = new_start + 1
        return data
                    
    def find_all_numbers(self, s_start = 0, s_end = -1):
        if s_end ==-1:
            s_end = self.length
        new_start = s_start
        data = []
        while (new_start < s_end) :
            [s, e, d] = self.find_float(s_start=new_start, s_end=s_end)
            if e > s:
                data.append([s, e, d])
                new_start = e + 1            
            else:
                [s1, e1, d1] = self.find_decimal(s_start=new_start, s_end=s_end)
                if e1 > s1:
                    data.append([s1,e1,d1])
                    new_start =  e1 + 1
                else:
                    new_start = new_start + 1
        return data
                 
         
        
        
                

        
 
            